import logging

from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.urls import reverse

from rest_framework import (
    viewsets,
    serializers,
)
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from paybox_api import PayboxAPI


logger = logging.getLogger(__name__)


class PayboxViewSet(viewsets.ViewSet):
    permission_classes = (AllowAny,)

    @action(methods=['post'], detail=False)
    @method_decorator(PayboxAPI.verify_paybox())
    def check(self, request):
        # Do smth here
        return Response()

    @action(methods=['post'], detail=False)
    @method_decorator(PayboxAPI.verify_paybox())
    def result(self, request):
        body = PayboxAPI.parse_body(request.body)

        if body['pg_result'] == '1':
            # Handle success result
        else:
            # Handle failure result
        return Response()

    @action(methods=['post'], detail=False)
    @method_decorator(PayboxAPI.verify_paybox())
    def refund(self, request):
        # Do smth here
        return Response({'refund': 'refund'})

    @action(methods=['post'], detail=False)
    @method_decorator(PayboxAPI.verify_paybox())
    def capture(self, request):
        # Do smth here
        return Response({'capture': 'capture'})

    @action(methods=['post'], detail=False)
    @method_decorator(PayboxAPI.verify_paybox())
    def success(self, request):
        # Do smth here
        return HttpResponseRedirect('google.com')

    @action(methods=['post'], detail=False)
    @method_decorator(PayboxAPI.verify_paybox())
    def failure(self, request):
        # Do smth here
        return HttpResponseRedirect('google.com')
