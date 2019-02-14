import datetime

from django import forms
from django.core.exceptions import ValidationError

from .models import Racun, Svjetiljka


class RenewRacunForm(forms.ModelForm):
    sum_kolicina = 0

    for racun in Racun.objects.all():
        sum_kolicina += racun.kolicina

    # pripazit na dijeljenje s nulom!!!
    prosjek = sum_kolicina / Racun.objects.count()

    def clean_kolicina(self):
        data = self.cleaned_data['kolicina']

        if data < self.prosjek - 5000:
            raise ValidationError('preveliko negativno odstupanje')

        if data > self.prosjek + 5000:
            raise ValidationError('preveliko pozitivno odstupanje')

        return data

    class Meta:
        model = Racun
        fields = ['kolicina', ]
        labels = {'kolicina': 'Količina', }
        help_texts = {'kolicina': 'unesi novu količinu', }


class ImageUploadForm(forms.Form):
    image = forms.ImageField()
