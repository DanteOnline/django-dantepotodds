from django.test import TestCase
from django.test import Client
from django.urls import reverse


class BaseTextCases:
    class TestView(TestCase):
        request_url_name = ''

        @property
        def request_url(self):
            return reverse(self.request_url_name)

        def setUp(self):
            self.client = Client()
            self.STATUS_OK = 200

        def test_get_ok_status(self):
            def send_request(request):
                response = request(reverse(self.request_url_name))
                self.assertEquals(response.status_code, self.STATUS_OK)

            send_request(self.client.get)
            send_request(self.client.post)
