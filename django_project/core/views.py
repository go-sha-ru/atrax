from django.shortcuts import render
from django.views.generic import FormView

from core.forms import PhoneInfoForm
from core.models import NumberingRegister


class PhoneView(FormView):
    template_name = "core/form.html"
    form_class = PhoneInfoForm
    phone_info = None

    def form_valid(self, form):
        phone_number = form.cleaned_data['phone_number']
        code = phone_number[1: 4]
        phone = phone_number[4:]
        if info := NumberingRegister.objects.filter(code=code, start__lte=phone, end__lte=phone).first():
            self.phone_info = {"phone": phone_number, "operator": info.operator, "region": info.region}

        return render(self.request, "core/form.html", {"phone_info": self.phone_info, "form": form})
