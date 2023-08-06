from setuptools import find_packages, setup


with open('README.md', 'r') as fh:
    long_description = fh.read()


setup(
    name='hestia_earth.extend_bibliography',
    version='0.2.4',
    description='Hestia library to extend Bibliography Nodes with different APIs',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Guillaume Royer',
    author_email='guillaumeroyer.mail@gmail.com',
    license='GPL-3.0-or-later',
    url='https://gitlab.com/hestia-earth/hestia-data-validation',
    keywords=['hestia', 'mendeley'],
    packages=find_packages(exclude=('tests', 'scripts')),
    python_requires='>=3',
    classifiers=[],
    install_requires=[
        'hestia-earth.schema>=0.0.27',
        'python-Levenshtein',
        'mendeley',
        'habanero',
        'wos',
        'xmltodict',
    ],
    dependency_links=[
        'git+git://github.com/jsabuco/mendeley-python-sdk.git#egg=mendeley'
    ]
)
