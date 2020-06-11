import hashlib
import random
import string

from functools import wraps
from urllib.parse import parse_qs

from django.conf import settings

from requests import Request


class PayboxAPI:
    """
    100 'Некорректная подпись запроса *'
    101 'Неверный номер магазина''
    110 'Отсутствует или не действует контракт с магазином'
    120 'Запрошенное действие отключено в настройках магазина''
    200 'Не хватает или некорректный параметр запроса'
    340 'Транзакция не найдена'
    350 'Транзакция заблокирована'
    360 'Транзакция просрочена'
    365 'Срок жизни рекуррентного профиля истек'
    400 'Платеж отменен покупателем или платежной системой'
    420 'Платеж отменен по причине превышения лимита'
    465 'Ошибка связи с платежной системой'
    466 'Истек SSL сертификат'
    470 'Ошибка на стороне платежной системы'
    475 'Общий сбой платежной системы'
    490 'Отмена платежа невозможна'
    600 'Общая ошибка'
    700 'Ошибка в данных введенных покупателем'
    701 'Некорректный номер телефона'
    711 'Номер телефона неприемлем для выбранной ПС'
    850 'Ни одна из платежных систем не готова принять запрос'
    1000 'Внутренняя ошибка сервиса (может не повториться при повторном обращении)'
    """
    def __init__(self, *args, **kwargs):
        self.PG_URL = kwargs.pop('pg_url', None) or getattr(settings, 'PG_URL', '')
        self.PG_SECRET = kwargs.pop('pg_secret', None) or getattr(settings, 'PG_SECRET', '')
        self.PG_MERCHANT_ID = kwargs.pop('pg_merchant_id', None) or getattr(settings, 'PG_MERCHANT_ID', '')
        self.PG_TESTING_MODE = kwargs.pop('pg_testing', None) or getattr(settings, 'PG_TESTING_MODE', '')
        self.PG_RESULT_URL = kwargs.pop('pg_result_url', None) or getattr(settings, 'PG_RESULT_URL', '')
        self.PG_SUCCESS_URL = kwargs.pop('pg_success_url', None) or getattr(settings, 'PG_SUCCESS_URL', '')
        self.PG_CHECK_URL = kwargs.pop('pg_check_url', None) or getattr(settings, 'PG_CHECK_URL', '')
        self.PG_REFUND_URL = kwargs.pop('pg_refund_url', None) or getattr(settings, 'PG_REFUND_URL', '')
        self.PG_CAPTURE_URL = kwargs.pop('pg_capture_url', None) or getattr(settings, 'PG_CAPTURE_URL', '')
        self.PG_FAILURE_URL = kwargs.pop('pg_failure_url', None) or getattr(settings, 'PG_FAILURE_URL', '')

    @staticmethod
    def parse_body(body):
        body = body.decode('utf-8')
        body = parse_qs(body)
        for k, v in body.items():
            body[k] = v[0]
        return body

    def get_sig(self, mydict, url='payment.php'):
        new_list = list()
        for key in sorted(mydict.keys()):
            new_list.append(str(mydict[key]))
        res = url + ';' + ';'.join(new_list) + ';' + self.PG_SECRET
        hashed = hashlib.md5(res.encode('utf-8')).hexdigest()
        return hashed

    @staticmethod
    def verify_sig(request, url=''):
        if request.method == 'GET':
            sig = request.GET.get('pg_sig')
            my_dict = request.GET.dict()
        else:
            my_dict = PayboxAPI.parse_body(request.body)
            sig = my_dict.pop('pg_sig', None)
        if sig != PayboxAPI().get_sig(my_dict, url=url):
            return False
        return True

    @staticmethod
    def verify_paybox():
        def decorator(func):
            @wraps(func)
            def inner(request, *args, **kwargs):
                if not PayboxAPI.verify_sig(request):
                    raise Exception(detail='Неправильная подпись')
                response = func(request, *args, **kwargs)
                return response
            return inner
        return decorator

    @staticmethod
    def generate_salt(length=8):
        chars = string.ascii_letters + string.digits
        rnd = random.SystemRandom()
        return ''.join(rnd.choice(chars) for _ in range(length))

    def get_url(self, order_id, amount, description, salt, email=None, phone=None):
        params = {
            'pg_order_id': order_id,
            'pg_merchant_id': self.PG_MERCHANT_ID,
            'pg_amount': amount,
            'pg_currency': 'KZT',
            'pg_description': description,
            'pg_salt': salt,
            'pg_testing_mode': self.PG_TESTING_MODE,
            'pg_request_method': 'POST',
            'pg_success_url_method': 'POST',
            'pg_failure_url_method': 'POST',
            'pg_result_url': self.PG_RESULT_URL,
            'pg_success_url': self.PG_SUCCESS_URL,
            'pg_check_url': self.PG_CHECK_URL,
            'pg_refund_url': self.PG_REFUND_URL,
            'pg_capture_url': self.PG_CAPTURE_URL,
            'pg_failure_url': self.PG_FAILURE_URL,
        }

        if email:
            params['pg_user_contact_email'] = email

        if phone:
            params['pg_user_phone'] = phone

        params['pg_sig'] = self.get_sig(params)

        return Request('GET', self.PG_URL, params=params).prepare().url
