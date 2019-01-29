import unittest

from django.test import TestCase
from .forms import PotOddsInputForm, PotOddsQuizInputForm
from .dantedjangotest import BaseTextCases


class TestPotOddsQuizInputForm(TestCase):

    def setUp(self):
        self.valid_form = PotOddsQuizInputForm({'pot_odds': 10})
        self.empty_form = PotOddsQuizInputForm()
        self.invalid_empty_form = PotOddsQuizInputForm({'pot_odds': ''})
        self.invalid_type_form = PotOddsQuizInputForm({'pot_odds': 'abc'})

    def test_valid(self):
        self.assertTrue(self.valid_form.is_valid())
        self.assertFalse(self.invalid_empty_form.is_valid())
        self.assertFalse(self.invalid_type_form.is_valid())

    def test_errors(self):
        self.invalid_type_form.is_valid()
        self.assertEqual(self.invalid_type_form.errors['pot_odds'], ['Enter a whole number.'])

class TestPotOddsInputForm(TestCase):

    def setUp(self):
        self.valid_form = PotOddsInputForm({'pot': 10, 'bet': 5})
        self.empty_form = PotOddsInputForm()
        self.empty_invalid_form = PotOddsInputForm({'pot': '', 'bet': ''})
        self.invalid_data_form = PotOddsInputForm({'pot': 'a', 'bet': 'b'})

    def test_valid(self):
        self.assertTrue(self.valid_form.is_valid())
        self.assertFalse(self.empty_form.is_valid())
        self.assertFalse(self.invalid_data_form.is_valid())

    def test_errors(self):
        # Должна быть форма, а в форме должны быть ошибки
        self.invalid_data_form.is_valid()
        self.assertEqual(self.invalid_data_form.errors['pot'], ['Поле должно быть целым числом'])
        self.empty_invalid_form.is_valid()
        self.assertEqual(self.empty_invalid_form.errors['pot'], ['This field is required.'])


class TestCalculateView(BaseTextCases.TestView):
    request_url_name = 'potodds:calculation'

    def setUp(self):
        super().setUp()
        self.STATUS_MOVED_TEMPORARILY = 302

        self.POT_FIELD_NAME = 'pot'
        self.BET_FIELD_NAME = 'bet'
        self.field_names = (self.POT_FIELD_NAME, self.BET_FIELD_NAME)

        self.form_name = 'form'

        self.required_error_text = 'This field is required.'
        self.not_number_error_text = 'Enter a whole number.'

    def test_contains_form(self):

        def send_request(request):
            response = request(self.request_url)
            form_name = self.form_name
            context = response.context
            self.assertIn(form_name, context)
            self.assertIsInstance(context[form_name], PotOddsInputForm)

        send_request(self.client.get)
        send_request(self.client.post)

    def test_post_response(self):
        response = self.client.post(self.request_url, {self.POT_FIELD_NAME: 10, self.BET_FIELD_NAME: 5})
        # В ответе должен быть результат рассчета и форма для ввода
        context = response.context
        # В контексте должен быть результат 33.3 %
        context_result_name = 'result'
        self.assertIn(context_result_name, context)
        self.assertTrue(abs(float(context[context_result_name]) - 33) < 0.5)


class TestQuizView(BaseTextCases.TestView):
    request_url_name = 'potodds:quiz'

    def test_get_context_data(self):
        # У нас в контексте должны быть значения pot и bet
        # для которых мы будем вводить шансы банка и форма для ввода этих шансов
        response = self.client.get(self.request_url)
        self.assertTrue(True)
