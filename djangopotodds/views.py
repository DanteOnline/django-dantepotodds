from django.shortcuts import render
from potodds import PotOdds
from .forms import PotOddsInputForm


def calculate_view(request):
    template_name = 'calculation.html'
    form_name = 'form'
    if request.method == 'GET':
        return render(request, template_name, {form_name: PotOddsInputForm()})
    else:
        form = PotOddsInputForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            pot = data['pot']
            bet = data['bet']
            pot_odds = PotOdds(pot, bet)
            result = pot_odds.get_odds()
            return render(request, template_name, {form_name: PotOddsInputForm(), 'result': result})
        else:
            return render(request, template_name, {form_name: form})

# class CalculationView(FormView):
#     form_class = PotOddsInputForm
#     template_name = 'calculation.html'
#     success_url = reverse_lazy('potodds:calculation')
def quiz_view(request):
    return render(request, 'quiz.html')