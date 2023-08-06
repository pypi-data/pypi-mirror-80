# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pycgtool', 'pycgtool.parsers']

package_data = \
{'': ['*']}

install_requires = \
['cython>=0.29.21,<0.30.0',
 'mdtraj>=1.9.4,<2.0.0',
 'numpy>=1.19.1,<2.0.0',
 'tqdm>=4.49.0,<5.0.0',
 'wheel>=0.35.1,<0.36.0']

extras_require = \
{'docs': ['sphinx-autoapi>=1.5.0,<2.0.0',
          'sphinx-rtd-theme>=0.5.0,<0.6.0',
          'sphinx>=3.2.1,<4.0.0']}

entry_points = \
{'console_scripts': ['pycgtool = pycgtool.__main__:main']}

setup_kwargs = {
    'name': 'pycgtool',
    'version': '2.0.0a5',
    'description': 'Generate coarse-grained molecular dynamics models from atomistic trajectories.',
    'long_description': "# PyCGTOOL\n\n[![License](https://img.shields.io/github/license/jag1g13/pycgtool.svg)](LICENSE)\n[![Build Status](https://img.shields.io/github/workflow/status/jag1g13/pycgtool/Python%20package)](https://github.com/jag1g13/pycgtool/actions)\n[![Documentation](https://readthedocs.org/projects/pycgtool/badge/?version=master)](http://pycgtool.readthedocs.io/en/master/?badge=master)\n[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.598143.svg)](https://doi.org/10.5281/zenodo.598143)\n\nGenerate coarse-grained molecular dynamics models from atomistic trajectories.\n\nThe aim of this project is to provide a tool to aid in parametrising coarse-grained (CG) molecular mechanics models.\nPyCGTOOL generates coarse-grained models from atomistic simulation trajectories using a user-provided mapping. \nEquilibrium values and force constants of bonded terms are calculated by Boltzmann Inversion of bond distributions collected from the input trajectory.\n\nAlternatively map-only mode (behaving similarly to MARTINIZE) may be used to generate initial coordinates to use with existing CG topologies such as the MARTINI lipid models.\nFor instance, a pre-equilibrated atomistic membrane may be used to create starting coordinates for a MARTINI membrane simulation.\n\nPyCGTOOL makes it easy to test multiple variations in mapping and bond topology by making simple changes to the config files.\n\nThis version has several advantages over the original C++ implementation CGTOOL:\n* PyCGTOOL is able to run anywhere the necessary library dependencies are available (all available from pip)\n* Does not require that residues are present in contiguous sorted blocks\n* May map multiple residues with a single pass\n* Support for polymers such as DNA or proteins making use of GROMACS' pdb2gmx\n* Much more automated testing ensures that regressions will be identified quickly\n\nIf you find this useful, please cite as:\n```\nGraham, J. (2017). PyCGTOOL, https://doi.org/10.5281/zenodo.598143\n```\n\n## Install\n\nPyCGTOOL requires Python 3.6 or higher and may be installed using pip:\n```\npip install pycgtool\n```\n\n## Usage\n\nInput to PyCGTOOL is GROMACS GRO and XTC files, along with two custom files: MAP and BND.  These files provide the atomistic-to-CG mapping and bonded topology respectively.  Example files are present in the [test/data](https://github.com/jag1g13/pycgtool/tree/master/test/data) directory.  The format of these files is described in the [full documentation](https://pycgtool.readthedocs.io/en/master/index.html).\n\nFor more information, see [the tutorial](https://pycgtool.readthedocs.io/en/master/tutorial.html).\nIt is important to perform validation of any new parameter set; a brief example is present at the end of the tutorial.\n\nFor a full list of options, see the [documentation](https://pycgtool.readthedocs.io/en/master/index.html) or use:\n```\npycgtool -h\n```\n\n### Generate a Model\n\nTo generate a CG model from an atomistic simulation:\n```\npycgtool -g <GRO file> -x <XTC file> -m <MAP file> -b <BND file>\n```\n\n### Map Only\n\nTo use PyCGTOOL to convert a set of atomistic simulation coordinates to CG coordinates:\n```\npycgtool -g <GRO file> -m <MAP file>\n```\n\nOr to convert a complete simulation trajectory:\n```\npycgtool -g <GRO file> -x <XTC file> -m <MAP file>\n```\n\n## Maintainers\n\nJames Graham ([@jag1g13](https://github.com/jag1g13))\n\n## Contributing\n\nIf you experience problems using PyCGTOOL or wish to see a new feature added please [open an issue](https://github.com/jag1g13/pycgtool/issues/new) or submit a PR.\n\nTo help develop PyCGTOOL, you can create a fork of this repository, clone your fork and install PyCGTOOL using:\n```\npoetry install\n```\n\nThis will install PyCGTOOL in editable mode (similar to `pip install -e .`) along with all the necessary runtime and development dependencies.\nThe Makefile at the root of the repository contains targets for running unit and integration tests (`make test`) and linting (`make lint`).\n\n## License\n\n[GPL-3.0](LICENSE) © James Graham, University of Southampton\n",
    'author': 'James Graham',
    'author_email': 'j.graham@soton.ac.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jag1g13/pycgtool',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
