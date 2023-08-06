# Wirecard
A Python wrapper for the [Wirecard REST API](https://document-center.wirecard.com/display/PTD/REST+API). Only supports credit card payments with 3D secure enrolment.

[![CircleCI](https://circleci.com/gh/Flickswitch/wirecard.svg?style=svg)](https://circleci.com/gh/Flickswitch/wirecard)


All examples below use Wirecard test data. You can find them in the links below:
- [API Credentials](https://document-center.wirecard.com/display/PTD/Credit+Card#CreditCard-TestCredentials)
- [3D Credit Card](https://document-center.wirecard.com/display/PTD/Appendix+K%3A+Test+Access+Data+and+Credentials)

## Setting up environment variables
```bash
export WIRECARD_USERNAME='70000-APILUHN-CARD'
export WIRECARD_PASSWORD='8mhwavKVb91T'
export WIRECARD_MERCHANT_ACCOUNT_ID='33f6d473-3036-4ca5-acb5-8c64dac862d1'
export WIRECARD_API_URL='https://api-test.wirecard.com/engine/rest/payments'
export WIRECARD_ORIGIN_IP='127.0.0.1'
```

## Using it
```python
from wirecard import AccountHolder, Card, RequestedAmount, Wirecard


card = Card(
    account_number='4012000300001003',
    expiration_month='01',
    expiration_year='2023',
    security_code='003',
    _type='visa',
)
account_holder = AccountHolder(
    first_name='John',
    last_name='Doe',
)
requested_amount = RequestedAmount(
    amount='10.99',
    currency='ZAR',
)

w = Wirecard()

result = w.check_3d_enrollment(card, account_holder, requested_amount)

# If everything is fine, you should redirect the user to the ACS page
# https://document-center.wirecard.com/display/PTD/Payment+Features#PaymentFeatures-ACSHTTPSRedirect

# Here's a Django View Example
transaction_id = result.get('payment').get('transaction-id')
acs_url = result.get('payment').get('three-d').get('acs-url')
pareq = result.get('payment').get('three-d').get('pareq')

context = {
    'acs_url': acs_url,
    'pareq': pareq,
    'term_url': 'https://your_callback_url',
    'md': f'{"transaction_id": {transaction_id}, "cvv": {card.security_code}}',
}

return render(
    request,
    'acs_template.html',
    context,
)

# The bank successfully calls your callback
# Here's a Django View Example
pares = request.POST.get('PaRes')
md = json.loads(request.POST.get('MD', 'null'))

parent_transaction_id = md['transaction_id']
cvv = md['cvv']

w = Wirecard()
result = w.authorize_and_capture_payment(pares, parent_transaction_id, cvv)
```

Instead of using environment variables, you can initialize the `Wirecard` with the necessary information:
```python
w = Wirecard(
    username='70000-APILUHN-CARD',
    password='8mhwavKVb91T',
    merchant_account_id='33f6d473-3036-4ca5-acb5-8c64dac862d1',
    url='https://api-test.wirecard.com/engine/rest/payments',
    origin_ip='127.0.0.1',
)
```

## Exceptions
- `WirecardFailedInit`: raised when the initialization of `Wirecard` fails
- `WirecardInvalidCard`: raised when an invalid card is given to `Card`
- `WirecardInvalidRequestedAmount`: raised when an invalid card is given to `RequestedAmount`
- `WirecardFailedTransaction`: raised when any communication with the Wirecard platform fails
- `WirecardInvalidResponse`: Raised when Wirecard fails to return JSON

## Testing
Install [poetry](https://github.com/sdispater/poetry).

```bash
$ poetry install
$ poetry run pytest
```

## License
[MIT](https://github.com/flickswitch/wirecard/blob/master/LICENSE).
