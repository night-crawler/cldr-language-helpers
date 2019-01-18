from setuptools import setup
from cldr_language_helpers import __version__

try:
    import pypandoc

    long_description = pypandoc.convert('README.md', 'rst')
except (IOError, ImportError):
    long_description = ''


setup(
    name='cldr-language-helpers',
    version=__version__,
    packages=['cldr_language_helpers'],
    package_data={'cldr_language_helpers': ['data/*.json']},
    url='https://github.com/night-crawler/cldr-language-helpers',
    license='MIT',
    author='night-crawler',
    author_email='lilo.panic@gmail.com',
    description='Some helpful unicode string processing tools in native Python',
    long_description=long_description,
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.6',
    install_requires=['funcy']
)
