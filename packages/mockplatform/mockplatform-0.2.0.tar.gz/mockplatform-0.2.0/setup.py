from os.path import abspath, dirname, join

from setuptools import setup, find_packages

packages = find_packages()
root_directory = abspath(dirname(__file__))


def get_long_description():
    with open(join(root_directory, 'README.md'), encoding='utf-8') as f:
        return f.read()


setup_kwargs = {
    'name': 'mockplatform',
    'description': 'Sometimes things go wrong',
    'long_description': get_long_description(),
    'long_description_content_type': 'text/markdown',
    'version': '0.2.0',
    'url': 'https://github.com/jakewan/mockplatform',
    'author': 'Jacob Wan',
    'author_email': 'jacobwan840@gmail.com',
    'packages': packages,
    'install_requires': [
        'sanic'
    ],
    'extras_require': {
        'dev': [
            'pycodestyle',
            'autopep8',
            'pytest'
        ]
    },
    'entry_points': {
        'console_scripts': [
            'mockplatform = mockplatform.app:run'
        ]
    },
    'include_package_data': True,
    'python_requires': '>=3.7.3',
}

setup(**setup_kwargs)
