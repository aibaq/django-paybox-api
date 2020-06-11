
from django.test import (
    RequestFactory,
    TestCase,
)

from test_app.utils import get_pagetype


class GetPagetypeTest(TestCase):

    def test_get_pagetype_home_no(self):
        request = RequestFactory().get('/')
        self.assertEqual(get_pagetype(request), 'Home')

    def test_get_pagetype_home_yes(self):
        request = RequestFactory().get('/abc/')
        self.assertEqual(get_pagetype(request), 'Not-Home')
