from setuptools import setup

with open('README.md', 'r') as fh:
	long_description = fh.read()

setup(
    name = 'azurestapi',
    version = '0.0.1',
    author = 'akashjeez',
    author_email = 'akashit63@gmail.com',
    url = 'https://github.com/akashjeez/azurestapi',
    description = 'A Python Package to List Azure Resources for Different Azure Services!',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    classifiers = [
        'Programming Language :: Python :: 3', 
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires = '>=3.8',
    install_requires = ['requests', 'pandas', 'xlsxwriter'],
    py_modules = ['azurestapi'],
    package_dir = {'': 'src'}
)
