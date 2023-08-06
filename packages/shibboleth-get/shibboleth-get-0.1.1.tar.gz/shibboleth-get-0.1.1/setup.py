from setuptools import setup

setup(
    name='shibboleth-get',
    version='0.1.1',
    description='Get the content of pages shielded by Shibboleth',
    url='https://github.com/MatthewScholefield/shibboleth-get',
    author='Matthew D. Scholefield',
    author_email='matthew331199@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='shibboleth get',
    py_modules=['shibboleth_get'],
    install_requires=[
        'selenium',
        'prettyparse'
    ],
    entry_points={
        'console_scripts': [
            'shibboleth-get=shibboleth_get:main'
        ],
    }
)
