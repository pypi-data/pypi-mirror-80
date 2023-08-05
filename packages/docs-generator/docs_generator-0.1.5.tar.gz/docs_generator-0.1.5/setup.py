from setuptools import setup, find_packages

setup(
    name='docs_generator',
    version_format='{tag}.dev{commitcount}+{gitsha}',
    install_requires=[
        'nbconvert',
        'mkdocs',
        'pyyaml',
        'mkdocs-material',
        'pytest'
    ],
    setup_requires=['setuptools-git-version'],
    packages=['docs_generator'],
    url='https://github.com/sirily11/algorithms',
    license='',
    author='sirily11',
    author_email='sirily1997@gmail.com',
    description='A program which convert jupyter notebook to mkdocs'
)
