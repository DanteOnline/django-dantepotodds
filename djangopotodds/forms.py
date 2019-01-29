from django import forms


class PotOddsInputForm(forms.Form):
    pot = forms.IntegerField(label='pot', error_messages={'required': 'This field is required.',
                                                          'invalid': 'Поле должно быть целым числом'})
    bet = forms.IntegerField(label='bet')


class PotOddsQuizInputForm(forms.Form):
    pot_odds = forms.IntegerField(label='Шансы банка')
