from setuptools import setup

setup(
    name = 'BadgeGenerator',
    version = '1.0.0',
    author = 'Hugo Emmanuel de Castro',
    author_email = 'hugocastrohc@outlook.com',
    packages = ['BadgeGenerator'],
    description = 'A Python Badger Generator to use and automatize your projects',
    long_description = '''A Python Badger Generator to use and automatize your projects

    Just use like:

        from BadgeGenerator import Badge

        Badge()
    
    -Ex:
        from BadgeGenerator import Badge

        Badge(color="red",logo="python",subject="Python") 
        ''',

    url = 'https://github.com/HugoCastroBR/BadgeGenerator',
    project_urls = {
        'Código fonte': 'https://github.com/HugoCastroBR/BadgeGenerator',
        'Download': 'https://github.com/HugoCastroBR/BadgeGenerator/archive/1.0.0.zip'
    },

    license = 'MIT',
    keywords = 'Badge BadgeGen BadgeGenerator Generator Brasil Brazil shield Shields '
)
setup(

    
)