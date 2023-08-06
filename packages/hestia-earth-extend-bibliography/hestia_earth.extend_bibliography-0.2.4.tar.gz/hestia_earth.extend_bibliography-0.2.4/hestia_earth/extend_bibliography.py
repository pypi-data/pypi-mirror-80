from functools import reduce
from hestia_earth.schema import SchemaType, Bibliography

from .bibliography_apis.utils import has_key, is_enabled, unique_values
from .bibliography_apis.crossref import extend_crossref
from .bibliography_apis.mendeley import extend_mendeley
from .bibliography_apis.wos import extend_wos


def is_node_of(node_type: SchemaType): return lambda node: node.get('type') == node_type.value


def update_source(source: dict, bibliographies: list):
    def update_key(key: str):
        value = source.get(key)
        biblio = next((x for x in bibliographies if value and value.get('title') == x.get('originalTitle')), None)
        if biblio and biblio.get('name'):
            if key == 'bibliography':
                source['name'] = biblio.get('name')
            source[key] = {**source[key], **biblio}
            del source[key]['originalTitle']

    update_key('bibliography')
    update_key('metaAnalysisBibliography')
    return source


def need_update_source(node: dict):
    def has_title(key: str): return key in node and 'title' in node.get(key)

    return is_node_of(SchemaType.SOURCE)(node) and (has_title('bibliography') or has_title('metaAnalysisBibliography'))


def update_node(bibliographies: list):
    def update_single_node(node):
        if isinstance(node, list):
            return list(reduce(lambda p, x: p + [update_single_node(x)], node, []))
        elif isinstance(node, dict):
            node = update_source(node, bibliographies) if need_update_source(node) else node
            list(map(update_single_node, node.values()))
        return node
    return update_single_node


def get_node_citation(node: dict):
    required = Bibliography().required
    required_values = list(filter(lambda x: node.get(x) is not None, required))
    title = node.get('title', '')
    title = title if len(title) > 0 else None
    return None if len(required_values) == len(required) else title


def get_titles_from_node(node: dict):
    title = get_node_citation(node) if is_node_of(SchemaType.BIBLIOGRAPHY)(node) else None
    return list(set(reduce(lambda x, y: x + get_citations(y), node.values(), [] if title is None else [title])))


def get_citations(nodes):
    if isinstance(nodes, list):
        return list(set(reduce(lambda p, x: p + get_citations(x), nodes, [])))
    elif isinstance(nodes, dict):
        return get_titles_from_node(nodes)
    else:
        return []


def extend(content, **kwargs):
    nodes = content.get('nodes') if 'nodes' in content else []

    actors = []

    if has_key('mendeley_username', **kwargs):
        (authors, bibliographies) = extend_mendeley(sorted(get_citations(nodes)), **kwargs)
        actors.extend([] if authors is None else authors)
        nodes = list(map(update_node(bibliographies), nodes))

    if has_key('wos_api_key', **kwargs) or (has_key('wos_api_user', **kwargs) and has_key('wos_api_pwd', **kwargs)):
        (authors, bibliographies) = extend_wos(sorted(get_citations(nodes)), **kwargs)
        actors.extend([] if authors is None else authors)
        nodes = list(map(update_node(bibliographies), nodes))

    if is_enabled('enable_crossref', **kwargs):
        (authors, bibliographies) = extend_crossref(sorted(get_citations(nodes)), **kwargs)
        actors.extend([] if authors is None else authors)
        nodes = list(map(update_node(bibliographies), nodes))

    return {'nodes': unique_values(actors) + nodes}
