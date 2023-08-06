# Always prefer setuptools over distutils
from setuptools import setup, find_packages
import pathlib


# Read setup data from files
here = pathlib.Path(__file__).parent.resolve()
long_description = (here / 'README.md').read_text(encoding='utf-8')
version_string = (here / 'src' / 'timeclock' / '__version__').read_text(encoding='utf-8').strip()


setup(
    name='cskytimeclock',
    version=version_string,
    description='Employees Only Command Line Interface and python API for saving Concentric Sky time entries to timeclock',
    long_description=long_description,  # Optional
    long_description_content_type='text/markdown',
    author='Concentric Sky',
    author_email='notto@concentricsky.com',

    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',

        # Pick your license as you wish
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate you support Python 3. These classifiers are *not*
        # checked by 'pip install'. See instead 'python_requires' below.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
    ],

    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    package_data={
        'timeclock': ['__version__'],
    },

    python_requires='>=3.6, <4',
    install_requires=[
        'click~=7.1',
        'requests~=2.24',
        'six~=1.15',
    ],
    extras_require={  # Optional
        'dev': [
            'pytest~=6.0',
            'responses~=0.12',
        ],
    },

    entry_points={  # Optional
        'console_scripts': [
            'timeclock=timeclock:cli',
        ],
    },

    project_urls={  # Optional
        'Concentric Sky Careers': 'https://www.concentricsky.com/team/careers',
    },
)
