# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wirecard']

package_data = \
{'': ['*']}

install_requires = \
['glom>=20.8.0,<21.0.0', 'requests>=2.24,<3.0']

setup_kwargs = {
    'name': 'wirecard',
    'version': '0.3.0',
    'description': 'A Python wrapper for the Wirecard REST API.',
    'long_description': '# Wirecard\nA Python wrapper for the [Wirecard REST API](https://document-center.wirecard.com/display/PTD/REST+API). Only supports credit card payments with 3D secure enrolment.\n\n[![CircleCI](https://circleci.com/gh/Flickswitch/wirecard.svg?style=svg)](https://circleci.com/gh/Flickswitch/wirecard)\n\n\nAll examples below use Wirecard test data. You can find them in the links below:\n- [API Credentials](https://document-center.wirecard.com/display/PTD/Credit+Card#CreditCard-TestCredentials)\n- [3D Credit Card](https://document-center.wirecard.com/display/PTD/Appendix+K%3A+Test+Access+Data+and+Credentials)\n\n## Setting up environment variables\n```bash\nexport WIRECARD_USERNAME=\'70000-APILUHN-CARD\'\nexport WIRECARD_PASSWORD=\'8mhwavKVb91T\'\nexport WIRECARD_MERCHANT_ACCOUNT_ID=\'33f6d473-3036-4ca5-acb5-8c64dac862d1\'\nexport WIRECARD_API_URL=\'https://api-test.wirecard.com/engine/rest/payments\'\nexport WIRECARD_ORIGIN_IP=\'127.0.0.1\'\n```\n\n## Using it\n```python\nfrom wirecard import AccountHolder, Card, RequestedAmount, Wirecard\n\n\ncard = Card(\n    account_number=\'4012000300001003\',\n    expiration_month=\'01\',\n    expiration_year=\'2023\',\n    security_code=\'003\',\n    _type=\'visa\',\n)\naccount_holder = AccountHolder(\n    first_name=\'John\',\n    last_name=\'Doe\',\n)\nrequested_amount = RequestedAmount(\n    amount=\'10.99\',\n    currency=\'ZAR\',\n)\n\nw = Wirecard()\n\nresult = w.check_3d_enrollment(card, account_holder, requested_amount)\n\n# If everything is fine, you should redirect the user to the ACS page\n# https://document-center.wirecard.com/display/PTD/Payment+Features#PaymentFeatures-ACSHTTPSRedirect\n\n# Here\'s a Django View Example\ntransaction_id = result.get(\'payment\').get(\'transaction-id\')\nacs_url = result.get(\'payment\').get(\'three-d\').get(\'acs-url\')\npareq = result.get(\'payment\').get(\'three-d\').get(\'pareq\')\n\ncontext = {\n    \'acs_url\': acs_url,\n    \'pareq\': pareq,\n    \'term_url\': \'https://your_callback_url\',\n    \'md\': f\'{"transaction_id": {transaction_id}, "cvv": {card.security_code}}\',\n}\n\nreturn render(\n    request,\n    \'acs_template.html\',\n    context,\n)\n\n# The bank successfully calls your callback\n# Here\'s a Django View Example\npares = request.POST.get(\'PaRes\')\nmd = json.loads(request.POST.get(\'MD\', \'null\'))\n\nparent_transaction_id = md[\'transaction_id\']\ncvv = md[\'cvv\']\n\nw = Wirecard()\nresult = w.authorize_and_capture_payment(pares, parent_transaction_id, cvv)\n```\n\nInstead of using environment variables, you can initialize the `Wirecard` with the necessary information:\n```python\nw = Wirecard(\n    username=\'70000-APILUHN-CARD\',\n    password=\'8mhwavKVb91T\',\n    merchant_account_id=\'33f6d473-3036-4ca5-acb5-8c64dac862d1\',\n    url=\'https://api-test.wirecard.com/engine/rest/payments\',\n    origin_ip=\'127.0.0.1\',\n)\n```\n\n## Exceptions\n- `WirecardFailedInit`: raised when the initialization of `Wirecard` fails\n- `WirecardInvalidCard`: raised when an invalid card is given to `Card`\n- `WirecardInvalidRequestedAmount`: raised when an invalid card is given to `RequestedAmount`\n- `WirecardFailedTransaction`: raised when any communication with the Wirecard platform fails\n- `WirecardInvalidResponse`: Raised when Wirecard fails to return JSON\n\n## Testing\nInstall [poetry](https://github.com/sdispater/poetry).\n\n```bash\n$ poetry install\n$ poetry run pytest\n```\n\n## License\n[MIT](https://github.com/flickswitch/wirecard/blob/master/LICENSE).\n',
    'author': 'Jonatas Baldin',
    'author_email': 'jonatas.baldin@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Flickswitch/wirecard',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
