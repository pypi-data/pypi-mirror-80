import setuptools
import numpy

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="DMT_core",
    version="0.0.3",
    author="M.Mueller, M.Krattenmacher",
    author_email="markus.mueller3@tu-dresden.de, mario.krattenmacher@web.de",
    description="Device Modeling Toolkit",
    #long_description=long_description,
    #long_description_content_type="text/markdown",
    url="https://gitlab.com/dmt-development/dmt",
    #packages=setuptools.find_packages(),
    packages=setuptools.find_namespace_packages(include=['DMT.*']),
    license="GNU GPLv3+",
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Operating System :: OS Independent",
    ],
    include_dirs=[numpy.get_include()],
    package_data={'': ['*.yaml']},
    include_package_data=True,
    install_requires=[
        'scipy',
        'numpy',
        'scikit-rf',
        'reprint',
        'pandas',
        'numba',
        'h5py',
        'tables',
        'cython',
        'pyqtgraph',
        'matplotlib',
        'PySide2',
        'pylint',
        'pytest',
        'pylatex',
        'pylatexenc',
        'pint',
        'pyyaml',
        'pypandoc',
        'more_itertools',
    ],
)
