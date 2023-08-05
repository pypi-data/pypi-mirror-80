from setuptools import setup, find_packages

setup(
    name='docs_generator',
    version='0.1.2',
    install_requires=[
        'jupyter',
        'mkdocs',
        'pyyaml',
        'mkdocs-material',
        'pytest'
    ],
    packages=['docs_generator'],
    url='https://github.com/sirily11/algorithms',
    license='',
    author='sirily11',
    author_email='sirily1997@gmail.com',
    description='A program which convert jupyter notebook to mkdocs'
)
