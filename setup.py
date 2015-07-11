from setuptools import setup, find_packages
import codecs
import os
import sys
import ohmystars


install_requires = [
    'github3.py==0.9.3',
    'tinydb>=2.2.0',
    'colorama>=0.2.4',
]

### Conditional dependencies:

# sdist
if not 'bdist_wheel' in sys.argv:
    try:
        #noinspection PyUnresolvedReferences
        import argparse
    except ImportError:
        install_requires.append('argparse>=1.2.1')

    if 'win32' in str(sys.platform).lower():
        # Terminal colors for Windows
        install_requires.append('pyreadline')


# bdist_wheel
extras_require = {
    # http://wheel.readthedocs.org/en/latest/#defining-conditional-dependencies
    ':python_version == "2.6"'
    ' or python_version == "3.0"'
    ' or python_version == "3.1" ': ['argparse>=1.2.1'],
    ':sys_platform == "win32"': ['pyreadline'],
}

def long_description():
    with codecs.open('README.md', encoding='utf8') as f:
        return f.read()

setup(name='oh-my-stars',
    version=ohmystars.__version__,
    description="a CLI tool to search your GitHub stars.",
    long_description=long_description(),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Operating System :: OS Independent",
        'Environment :: Console',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Terminals',
        'Topic :: Utilities',
    ],
    platforms = 'any',
    keywords='github command tools',
    author=ohmystars.__author__,
    author_email='wolfg1969@gmail.com',
    url='https://github.com/wolfg1969/oh-my-stars',
    license=ohmystars.__license__,
    zip_safe=False,
    entry_points = {
        'console_scripts': [
            'mystars = ohmystars.__main__:main',
        ],
    },
    packages=find_packages(),
    extras_require=extras_require,
    install_requires=install_requires,
    data_files=[('.', ['Oh My Stars.alfredworkflow', ]),]
)
