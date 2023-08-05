# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['plenty_taxhub_generator', 'plenty_taxhub_generator.packages']

package_data = \
{'': ['*']}

install_requires = \
['plenty_api>=0.2,<0.3',
 'pylint>=2.6.0,<3.0.0',
 'requests>=2.24.0,<3.0.0',
 'typing>=3.7.4,<4.0.0']

setup_kwargs = {
    'name': 'plenty-taxhub-generator',
    'version': '0.0.1',
    'description': 'Generate the required data sheet for the DutyPay(dutypay.eu) TaxHub platform from Plentymarkets.',
    'long_description': 'plenty_taxhub_generator\n_________________\n\n## Description\n\nCreate a Tax Hub Report with sales order and refunds from PlentyMarkets.\nTax Hub is a report used by [DutyPay](https://www.dutypay.eu/de/).\n\n## Installation\n\n`poetry install plenty_taxhub_generator`\n\nor\n\n`python3 -m pip install plenty_taxhub_generator --user --upgrade`\n\n## Usage\n\nPrepare a configuration file with the following format:\n\n```\n[General]\nbase_url=https://{your-plenty-cloud}.plentymarkets-cloud01.com\n\n[Mappings]\nreferrer_id={IDs of the order origins}\ncountry_id=AT=2,CZ=6,ES=8,FR=10,GB=12,IT=15,PL=23 # list of countries where VAT is charged\n\n[fixed_values]\nsource_zone=DE\nmarket_zone_currency=EUR\n```\n\nAnd place the config at:\n- `/home/user/.plenty_taxhub_generator_config.ini` for Linux systems\n- `C:\\\\Users\\user\\.plenty_taxhub_generator_config.ini` for Windows systems\n\nCreate a API user on PlentyMarkets:\nSetup-> Settings-> User-> Accounts-> New-> Access: REST-API\n\nThen just run the program:\n`python3 -m plenty_taxhub_generator --from 2020-09-01 --to 2020-09-30`\n\nPlease provide the date in one of the following formats:\n* YYYY-MM-DDTHH:MM:SS+UTC-OFFSET\n* YYYY-MM-DDTHH:MM\n* YYYY-MM-DD\n\nYou will be asked to provide your API credentials from Plentymarkets. Afterwards these will be saved into your Keyring (system intern password storage) for a certain amount of time.\n\nThe report will be placed by default at your current working directory. But you can provide a different location with the `-o/--out` option.  \nYou can view the mappings in your config with the `-m/--mappings` option.\nAnd you can change the base URL of your PlentyMarkets system with `-c/--url/--change_url`.\n',
    'author': 'Sebastian Fricke',
    'author_email': 'sebastian.fricke.linux@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
