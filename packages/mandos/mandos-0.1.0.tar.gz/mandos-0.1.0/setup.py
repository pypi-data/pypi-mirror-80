# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mandos', 'mandos.model', 'mandos.search']

package_data = \
{'': ['*'], 'mandos': ['resources/*']}

install_requires = \
['chembl-webresource-client>=0.10,<0.11',
 'pandas>=1.1,<2.0',
 'pocketutils>=0.3.2,<0.4',
 'requests>=2.24,<3.0',
 'tomlkit>=0.7,<1.0',
 'tqdm>=4.48,<5.0',
 'typer[colorama]>=0.3,<1.0']

entry_points = \
{'console_scripts': ['mandos = mandos.cli:cli']}

setup_kwargs = {
    'name': 'mandos',
    'version': '0.1.0',
    'description': 'Get the biological targets of compounds.',
    'long_description': '# Mandos\n\n[![Version status](https://img.shields.io/pypi/status/mandos)](https://pypi.org/project/mandos/)\n[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/mandos)](https://pypi.org/project/mandos/)\n[![Docker](https://img.shields.io/docker/v/dmyersturnbull/mandos?color=green&label=DockerHub)](https://hub.docker.com/repository/docker/dmyersturnbull/mandos)\n[![GitHub release (latest SemVer including pre-releases)](https://img.shields.io/github/v/release/dmyersturnbull/mandos?include_prereleases&label=GitHub)](https://github.com/dmyersturnbull/mandos/releases)\n[![Latest version on PyPi](https://badge.fury.io/py/mandos.svg)](https://pypi.org/project/mandos/)\n[![Documentation status](https://readthedocs.org/projects/mandos-chem/badge/?version=latest&style=flat-square)](https://mandos-chem.readthedocs.io/en/stable/)\n[![Build & test](https://github.com/dmyersturnbull/mandos/workflows/Build%20&%20test/badge.svg)](https://github.com/dmyersturnbull/mandos/actions)\n[![Maintainability](https://api.codeclimate.com/v1/badges/aa7c12d45ad794e45e55/maintainability)](https://codeclimate.com/github/dmyersturnbull/mandos/maintainability)\n[![Coverage](https://coveralls.io/repos/github/dmyersturnbull/mandos/badge.svg?branch=master&service=github)](https://coveralls.io/github/dmyersturnbull/mandos?branch=master)\n\nA pragmatic tool for cheminformatics and drug discovery.\n\nExample:\n\n```bash\ncat "VREFGVBLTWBCJP-UHFFFAOYSA-N" > compounds.txt\nmandos search mechanism,activity,atc,trial,predicted compounds.txt\n```\n\nIt will output a CSV file containing extended data and a simple text file of compound–predicate–object triples:\n\n```\nCHEMBL661 (alprazolam)  positive allosteric modulator  CHEMBL2093872 (GABA-A receptor; anion channel)\nCHEMBL661 (alprazolam)  activity at                    CHEMBL2093872 (GABA-A receptor; anion channel)\nCHEMBL661 (alprazolam)  activity at                    CHEMBL2096986 (Cholecystokinin receptor)\nCHEMBL661 (alprazolam)  activity at                    CHEMBL4106143 (BRD4/HDAC1)\nCHEMBL661 (alprazolam)  predicted at                   CHEMBL2094116 (Serotonin 3 (5-HT3) receptor)\nCHEMBL661 (alprazolam)  predicted at                   CHEMBL4430    (Cytochrome P450 17A1)\nCHEMBL661 (alprazolam)  phase-3 trial for              D012559       (Schizophrenia)\nCHEMBL661 (alprazolam)  phase-4 trial for              D016584       (Panic Disorder)\nCHEMBL661 (alprazolam)  phase-4 trial for              D016584       (Anxiety Disorders)\nCHEMBL661 (alprazolam)  has ATC L3 code                N05B          (ANXIOLYTICS)\nCHEMBL661 (alprazolam)  has ATC L4 code                N05BA         (Benzodiazepine derivatives)\n```\n\n**[See the docs](https://mandos-chem.readthedocs.io/en/latest/)** for more info.\n\n\n[New issues](https://github.com/dmyersturnbull/mandos/issues) and pull requests are welcome.\nPlease refer to the [contributing guide](https://github.com/dmyersturnbull/mandos/blob/master/CONTRIBUTING.md).\nGenerated with [Tyrannosaurus](https://github.com/dmyersturnbull/tyrannosaurus).\n',
    'author': 'Douglas Myers-Turnbull',
    'author_email': None,
    'maintainer': 'Douglas Myers-Turnbull',
    'maintainer_email': None,
    'url': 'https://github.com/dmyersturnbull/mandos',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4',
}


setup(**setup_kwargs)
