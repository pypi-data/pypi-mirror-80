"""W-Data format
https://github.com/mforbes/wdata-format
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / 'README.md').read_text(encoding='utf-8')

# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.

setup(
    name='wdata',
    version='0.1.0',
    description='W-Data format for superfluid dynamics',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/mforbes/wdata-format',
    author='Michael McNeil Forbes',
    author_email='michael.forbes+python@gmail.com',
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Visualization',
        'Topic :: Scientific/Engineering :: Physics',

        # Pick your license as you wish
        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
    ],

    keywords='VisIT',

    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    python_requires='>=3.5, <4',

    install_requires=[
        'numpy',
        'tzlocal',
        'pytz',
        'zope.interface'
    ],
    extras_require={
        'test': ['nox', 'pytest-cov'],
    },

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # `pip` to create the appropriate form of executable for the target
    # platform.
    #
    # For example, the following would provide a command called `sample` which
    # executes the function `main` from this package when invoked:
    #entry_points={
    #    'console_scripts': [
    #        'sample=sample:main',
    #    ],
    #},

    project_urls={  # Optional
        'Bug Reports': 'https://github.com/mforbes/wdata-format/issues',
        #'Funding': 'https://donate.pypi.org',
        #'Say Thanks!': 'http://saythanks.io/to/example',
        'Source': 'https://github.com/mforbes/wdata-format/issues',
    },
)
