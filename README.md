# Installation

```
pip install git+ssh://git@github.com/aibaq/django-paybox-api.git@0.0.1
```

# Settings

```
INSTALLED_APPS += ['paybox_api']

PG_URL = 'https://api.paybox.money/payment.php'
PG_REVOKE_URL = 'https://api.paybox.money/revoke.php'
PG_SECRET = os.getenv('PG_SECRET')
PG_SECRET_TICKET = os.getenv('PG_SECRET_TICKET')
PG_MERCHANT_ID = os.getenv('PG_MERCHANT_ID')
PG_TESTING_MODE = '1'
PG_RESULT_URL = 'http://yourdomain/payments/paybox/result/'
PG_SUCCESS_URL = 'http://yourdomain/payments/paybox/success/'
PG_CHECK_URL = 'http://yourdomain/payments/paybox/check/'
PG_REFUND_URL = 'http://yourdomain/payments/paybox/refund/'
PG_CAPTURE_URL = 'http://yourdomain/payments/paybox/capture/'
PG_FAILURE_URL = 'http://yourdomain/payments/paybox/failure/'
```

# Usage

```
from app.payments.paybox import PayboxAPI

PayboxAPI().get_url(
    order_id=1,
    amount=1000,
    description='Iphone11',
    salt=PayboxAPI.generate_salt(),
    email='testemail@gmail.com',
    phone='+77777777777',
)
```
Open generated url in browser

handle callbacks at views.py : see test_app
