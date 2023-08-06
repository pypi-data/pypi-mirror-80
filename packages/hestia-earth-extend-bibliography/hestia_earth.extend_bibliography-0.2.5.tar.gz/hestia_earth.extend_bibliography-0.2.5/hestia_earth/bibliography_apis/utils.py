from random import randint
import Levenshtein
import time
from hestia_earth.schema import Actor


MAXIMUM_DISTANCE = 10


def current_time(): return int(round(time.time() * 1000))


def has_key(key: str, **kwargs): return kwargs.get(key, None) is not None


def is_enabled(key: str, **kwargs): return kwargs.get(key, False) is True


def join_list_string(values): return ' '.join(list(filter(None, values))).strip()


def non_empty_value(value): return value != '' and value is not None and value != []


def remove_empty_values(values): return list(map(lambda x: {k: v for k, v in x.items() if non_empty_value(v)}, values))


def unique_values(values: list, key='id'): return list({v[key]: v for v in values}.values())


def actor_id(author):
    return author.get('scopusID') if 'scopusID' in author and author.get('scopusID') \
        else f"H-{str(randint(10**9, 10**10-1))}"


def biblio_name(authors, year):
    author_suffix = ''

    if len(authors) == 2:
        author_suffix = f"& {authors[1].get('lastName')}"
    elif len(authors) >= 3:
        author_suffix = 'et al'

    return f"{authors[0].get('lastName')} {author_suffix} ({year})"


def create_actors(actors):
    def create_actor(author):
        actor = Actor()
        actor.fields = {**actor.fields, **author}
        actor.fields['id'] = actor_id(author)
        initials = actor.fields.get('firstName')[0] if actor.fields.get('firstName') is not None else None
        actor.fields['name'] = join_list_string([
            initials, actor.fields.get('lastName'), actor.fields.get('primaryInstitution')
        ])
        actors.append(actor.to_dict())

        author = Actor()
        author.fields['id'] = actor.fields.get('id')
        return remove_empty_values([author.to_dict()])[0]
    return create_actor


def extend_bibliography(authors=[], year=None):
    biblio = {}
    actors = []
    biblio['authors'] = list(map(create_actors(actors), authors))
    biblio['name'] = biblio_name(authors, str(year)) if len(authors) > 0 and year is not None else ''
    return (biblio, actors)


def get_distance(str1: str, str2: str):
    return Levenshtein.distance(str1.rstrip().lower(), str2.rstrip().lower())


def find_closest_result(title: str, fetch_items):
    items = fetch_items(title)
    distances = list(map(lambda i: get_distance(title, i['title']), items))
    distance = min(distances) if len(distances) else 1000
    closest_title = items[distances.index(distance)]['item'] if len(distances) else None
    return [closest_title, distance]
