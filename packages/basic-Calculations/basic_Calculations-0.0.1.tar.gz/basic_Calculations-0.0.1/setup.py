from setuptools  import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable', 
    'Intended Audience :: Education', 
    'Operating System :: Microsoft :: Windows :: Windows 10', 
    'License :: OSI Approved :: MIT License', 
    'Programming Language :: Python :: 3'
]

setup(
    name = 'basic_Calculations', 
    version = '0.0.1', 
    description = 'This module helps you to do calculations between 2 numbers easily.',
    Long_description = open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url = '',
    author = 'Shreyansh Kushwaha',
    author_email = 'shreyansh.halk@gmail.com',
    License = 'MIT',
    classifiers = classifiers,
    keywords = 'Calculations',
    packages = find_packages(), 
    install_requires = ['']
)