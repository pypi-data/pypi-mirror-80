import os, sys
import codecs
from setuptools import setup, find_packages, Command
from setuptools.extension import Extension


here = os.path.abspath(os.path.dirname(__file__))

with open("README.rst", "r") as fh:
    long_description = fh.read()

def read(rel_path):
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()

def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")

try:
    from sphinx.setup_command import BuildDoc
    cmdclass = {'build_sphinx': BuildDoc}
except ModuleNotFoundError:
    cmdclass = {'empty': None}

#['setup.py', '-b', 'html', './doc/source', './doc/_build/html'])

setup(
    name="aidapy",
    version=get_version(os.path.join('aidapy', '__init__.py')),
    author="AIDA Consortium",
    author_email="coordinator.aida@kuleuven.be",
    description="AI package for heliophysics",
    long_description=long_description,
    url="https://gitlab.com/aidaspace/aidapy",
    license='MIT',
    python_requires='>=3.5',
    install_requires=[
         'numpy',
         'matplotlib',
         'xarray',
         'astropy',
         'heliopy>=0.12.0',
         'heliopy-multid',
         'sunpy',
         'cdflib',
         'requests',
         'more_itertools',
         'extension',
         'bottleneck'
    ],
    tests_require=[
        'pytest',
        'pylint',
        'pytest-cov',
        'coverage'
    ],
    extras_require={
        'doc': ['sphinx_rtd_theme', 'sphinx>=1.4', 'ipython', 'ipykernel', 'nbsphinx', 'sphinxcontrib-apidoc'],
        'ml': ['torch>=1.3', 'skorch', 'h5py', 'joblib'], #'sklearn', 'mpi4py',
        'vdf_cub': ['tricubic']
    },
    cmdclass=cmdclass,
    classifier=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Education',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Scientific/Engineering :: Astronomy',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Scientific/Engineering :: Physics'
    ],
    packages=find_packages(exclude=['doc*', 'example*',
                                    'test*', '*egg-info*']),
    data_files=None,
    zip_safe=False,
    include_package_data=True,
    setup_requires=['pytest-runner'],
    test_suite = 'tests',
    command_options={
        'build_sphinx': {
            'source_dir': ('setup.py', 'doc/source'),
            'build_dir': ('setup.py',  './doc/_build'),
            'builder': ('setup.py', 'html')
        }
    }
    ## Uncommend to wrap C/C++/Fortran codes
    #ext_modules=cythonize(extensions),
)
