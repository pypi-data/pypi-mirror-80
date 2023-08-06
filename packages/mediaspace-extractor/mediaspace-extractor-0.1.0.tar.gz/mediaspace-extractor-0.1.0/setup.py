from setuptools import setup

setup(
    name='mediaspace-extractor',
    version='0.1.0',
    description='Extract video download links from Mediaspace',
    url='https://github.com/MatthewScholefield/mediaspace-extractor',
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
    keywords='mediaspace extractor',
    py_modules=['mediaspace_extractor'],
    install_requires=[
        'selenium',
        'prettyparse',
        'shibboleth-get'
    ],
    entry_points={
        'console_scripts': [
            'mediaspace-extractor=mediaspace_extractor:main'
        ],
    }
)
