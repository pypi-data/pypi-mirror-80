from setuptools import setup, find_packages

setup(
    name='rastasteady',
    version='0.2.13',
    description='',
    long_description='',
    install_requires=[
        'click',
        'flask'
    ],
    entry_points='''
        [console_scripts]
        rastasteady=rastasteady.cli:cli
        rastasteady-cli=rastasteady.cli:cli
        rastasteady-web=rastasteady.web.web:web
    ''',
    packages=find_packages(),
    zip_safe=False,
)
