try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
    
config =[
    'description': 'My Project',
    'author': 'Sreenidhin C C',
    'url': 'URL to get it at.'
    'download_url':'where to download it',
    'author_email': 'ccsreenidhin@gmail.com'
    'version':'0.1',
    'install_requires':['nose'],
    'packages':['NAME'],
    'Scripts': [],
    'name': 'projectname'
]

setup(**config)
    
    
