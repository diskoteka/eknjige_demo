import datetime
import locale
import xlwt

from django.urls import reverse, reverse_lazy

from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404

from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.http import HttpResponseRedirect, JsonResponse, HttpResponse, HttpResponseForbidden

from django.contrib.auth import get_user_model

from rest_framework.views import APIView
from rest_framework.response import Response

from tablib import Dataset

from .models import Omm, Racun, Instanca, Tarifa, Partner, Svjetiljka, Korisnik, OJR
from .resources import SvjetiljkaResource, OmmResource, RacunResource, InstancaResource, OJRResource
from .forms import RenewRacunForm, ImageUploadForm

from django.core.mail import send_mail
from django.conf import settings

from twilio.rest import Client
from sendsms import api


# views variables
User = get_user_model()
locale.setlocale(locale.LC_ALL, '')


# send email - sms
def email(request):
    subject = 'Dojava alarma'
    message = 'Server #1 preopterećen; Server #2 preopterećen;'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['mario.juricic@rocketmail.com', ]

    send_mail(subject, message, email_from, recipient_list)

    return render(request, 'email.html')


def sms(request):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    message = client.messages.create(to='+385919799455', from_='+385951008218', body='Dojava alarma: Server #1 preopterećen; Server #2 preopterećen;')

    print(message.sid)

    return render(request, 'sms.html')


# templates
def template_racuni(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="racuni.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Računi')

    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['datum', 'broj', 'kolicina', 'tarifa', 'id',]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    wb.save(response)
    return response


def template_instance(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="instance.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Instance')

    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['sifra', 'adresa', 'trafo', 'brojilo', 'id',]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    wb.save(response)
    return response


def template_omm(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="omm.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Omm')

    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['sifra', 'adresa', 'trafo', 'brojilo', 'id',]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    wb.save(response)
    return response


# upload pics views
def upload_pic(request, pk):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)

        if form.is_valid():
            m = Svjetiljka.objects.get(pk=pk)
            m.slika = form.cleaned_data['image']
            m.save()
            return HttpResponseRedirect(reverse('svjetiljke'))

    return HttpResponseForbidden('Niste odabrali sliku svjetiljke!')


# renew views
def renew_racun_manager(request, pk):
    racun = get_object_or_404(Racun, pk=pk)

    if request.method == 'POST':
        form = RenewRacunForm(request.POST)

        if form.is_valid():
            racun.kolicina = form.cleaned_data['kolicina']
            racun.save()

            return HttpResponseRedirect(reverse('racuni'))

    else:
        predlozena_kolicina = racun.kolicina
        form = RenewRacunForm(initial={'kolicina': predlozena_kolicina, })

    return render(request, 'katalog/racun_renew_manager.html', {'form': form, 'racun': racun})


# chart views
class TarifeChartHome(generic.View):
    def get(self, request, *args, **kwargs):
        return render(request, 'katalog/tarifa_charts.html')


class TarifeChartData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        tarife = []

        for tarifa in Tarifa.objects.filter(mjesec__year=2017):
            tarife += [tarifa.naknada, ]

        labels = ["Sij", "Velj", "Ožu", "Tra", "Svi", "Lip", "Srp", "Kol", "Ruj", "Lis", "Stu", "Pro"]
        default_items = tarife
        data = {
            'labels': labels,
            'default': default_items,
        }
        return Response(data)


class RacuniChartHome(generic.View):
    def get(self, request, *args, **kwargs):
        return render(request, 'katalog/racun_charts.html')


class RacuniChartData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        racuni = []

        for racun in Racun.objects.filter(datum__year=2017):
            racuni += [racun.kolicina, ]

        labels = ["Sij", "Velj", "Ožu", "Tra", "Svi", "Lip", "Srp", "Kol", "Ruj", "Lis", "Stu", "Pro"]
        default_items = racuni
        data = {
            'labels': labels,
            'default': default_items,
        }
        return Response(data)


class InstanceChartHome(generic.View):
    def get(self, request, *args, **kwargs):
        return render(request, 'katalog/instanca_charts.html')


class InstanceChartData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        instance = []

        for instanca in Instanca.objects.filter(datum_od__year=2017):
            instance += [instanca.potrosak, ]
            if len(instance) > 11:
                break

        labels = ["Sij", "Velj", "Ožu", "Tra", "Svi", "Lip", "Srp", "Kol", "Ruj", "Lis", "Stu", "Pro"]
        default_items = instance
        data = {
            'labels': labels,
            'default': default_items,
        }
        return Response(data)


# import - export - delete views
def ojr_import(request):
    if request.method == 'POST':
        OJR_resource = OJRResource()
        dataset = Dataset()
        nova_OJR = request.FILES['myfile']

        imported_data = dataset.load(nova_OJR.read())
        result = OJR_resource.import_data(dataset, dry_run=True)

        if not result.has_errors():
            OJR_resource.import_data(dataset, dry_run=False)

    return render(request, 'katalog/OJR_import.html')


def instanca_import(request):
    if request.method == 'POST':
        instanca_resource = InstancaResource()
        dataset = Dataset()
        nove_instance = request.FILES['myfile']

        imported_data = dataset.load(nove_instance.read())
        result = instanca_resource.import_data(dataset, dry_run=True)

        if not result.has_errors():
            instanca_resource.import_data(dataset, dry_run=False)

    return render(request, 'katalog/instanca_import.html')


def instanca_export(request):
    instanca_resource = InstancaResource()
    dataset = instanca_resource.export()
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="instanca.csv"'
    return response


def instanca_del(request):
    return render(request, 'katalog/instanca_confirm_delete_all.html')


def instanca_del_all(request):
    instance = Instanca.objects.all()

    if instance.exists():
        instance.delete()

    return render(request, 'katalog/instanca_list.html')


def racun_import(request):
    if request.method == 'POST':
        racun_resource = RacunResource()
        dataset = Dataset()
        novi_racuni = request.FILES['myfile']

        imported_data = dataset.load(novi_racuni.read())
        result = racun_resource.import_data(dataset, dry_run=True)

        if not result.has_errors():
            racun_resource.import_data(dataset, dry_run=False)

    return render(request, 'katalog/racun_import.html')


def racun_export(request):
    racun_resource = RacunResource()
    dataset = racun_resource.export()
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="racun.csv"'
    return response


def racun_del(request):
    return render(request, 'katalog/racun_confirm_delete_all.html')


def racun_del_all(request):
    racuni = Racun.objects.all()

    if racuni.exists():
        racuni.delete()

    return render(request, 'katalog/racun_list.html')


def omm_import(request):
    if request.method == 'POST':
        omm_resource = OmmResource()
        dataset = Dataset()
        nova_omm = request.FILES['myfile']

        imported_data = dataset.load(nova_omm.read())
        result = omm_resource.import_data(dataset, dry_run=True)

        if not result.has_errors():
            omm_resource.import_data(dataset, dry_run=False)

    return render(request, 'katalog/omm_import.html')


def omm_export(request):
    omm_resource = OmmResource()
    dataset = omm_resource.export()
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="omm.csv"'
    return response


def omm_del(request):
    return render(request, 'katalog/omm_confirm_delete_all.html')


def omm_del_all(request):
    omma = Omm.objects.all()

    if omma.exists():
        omma.delete()

    return render(request, 'katalog/omm_list.html')


def svjetiljka_import(request):
    if request.method == 'POST':
        svjetiljka_resource = SvjetiljkaResource()
        dataset = Dataset()
        nove_svjetiljke = request.FILES['myfile']

        # imported_data = dataset.load(nove_svjetiljke.read().decode('utf-8'),format='csv')
        imported_data = dataset.load(nove_svjetiljke.read())
        result = svjetiljka_resource.import_data(dataset, dry_run=True)

        if not result.has_errors():
            svjetiljka_resource.import_data(dataset, dry_run=False)

    return render(request, 'katalog/svjetiljka_import.html')


def svjetiljka_export(request):
    svjetiljka_resource = SvjetiljkaResource()
    dataset = svjetiljka_resource.export()
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="svjetiljke.csv"'
    return response


def svj_del(request):
    return render(request, 'katalog/svjetiljka_confirm_delete_all.html')


def svj_del_all(request):
    svjetiljke = Svjetiljka.objects.all()

    if svjetiljke.exists():
        svjetiljke.delete()

    return render(request, 'katalog/svjetiljka_list.html')


# single views
def index(request):
    br_racuna = Racun.objects.count()
    br_instanci = Instanca.objects.count()
    br_omma = Omm.objects.count()
    br_tarifa = Tarifa.objects.count()
    br_partnera = Partner.objects.count()
    br_svjetiljki = Svjetiljka.objects.count()
    br_korisnika = User.objects.count()

    sum_r = 0
    sum_i = 0

    for racun in Racun.objects.all():
        sum_r += racun.suma_opskrbe()

    for instanca in Instanca.objects.all():
        sum_i += instanca.suma_opskrbe() + instanca.suma_mrezarine()

    sum_r_local = locale.currency(sum_r, grouping=True)
    sum_i_local = locale.currency(sum_i, grouping=True)

    suma_svih = br_racuna + br_instanci + br_omma + br_tarifa + br_partnera + br_svjetiljki + br_korisnika

    context = {
        'br_racuna': br_racuna,
        'br_instanci': br_instanci,
        'br_omma': br_omma,
        'br_tarifa': br_tarifa,
        'br_partnera': br_partnera,
        'br_svjetiljki': br_svjetiljki,
        'br_korisnika': br_korisnika,
        'suma_svih': suma_svih,
        'sum_r': sum_r_local,
        'sum_i': sum_i_local
    }

    return render(request, 'index.html', context=context)


def gmap(request):
    return render(request, 'gmap.html')


def scada(request):
    return render(request, 'scada.html')


# generic view models
class OjrListView(generic.ListView):
    model = OJR


class OjrDetailView(generic.DetailView):
    model = OJR


class RacunListView(generic.ListView):
    model = Racun


class RacunDetailView(generic.DetailView):
    model = Racun


class InstancaListView(generic.ListView):
    model = Instanca


class InstancaDetailView(generic.DetailView):
    model = Instanca


class TarifaListView(generic.ListView):
    model = Tarifa


class TarifaDetailView(generic.DetailView):
    model = Tarifa


class OmmListView(generic.ListView):
    model = Omm


class OmmDetailView(generic.DetailView):
    model = Omm


class PartnerListView(generic.ListView):
    model = Partner


class PartnerDetailView(generic.DetailView):
    model = Partner


class SvjetiljkaListView(generic.ListView):
    model = Svjetiljka


class SvjetiljkaDetailView(generic.DetailView):
    model = Svjetiljka


# crud view models
class OjrCreate(CreateView):
    model = OJR
    fields = '__all__'


class OjrUpdate(UpdateView):
    model = OJR
    fields = '__all__'


class OjrDelete(DeleteView):
    model = OJR
    fields = '__all__'


class RacunCreate(CreateView):
    model = Racun
    fields = '__all__'


class RacunUpdate(UpdateView):
    model = Racun
    fields = '__all__'


class RacunDelete(DeleteView):
    model = Racun
    success_url = reverse_lazy('racuni')


class InstancaCreate(CreateView):
    model = Instanca
    fields = '__all__'


class InstancaUpdate(UpdateView):
    model = Instanca
    fields = '__all__'


class InstancaDelete(DeleteView):
    model = Instanca
    success_url = reverse_lazy('instance')


class TarifaCreate(CreateView):
    model = Tarifa
    fields = '__all__'


class TarifaUpdate(UpdateView):
    model = Tarifa
    fields = '__all__'


class TarifaDelete(DeleteView):
    model = Tarifa
    success_url = reverse_lazy('tarife')


class OmmCreate(CreateView):
    model = Omm
    fields = '__all__'


class OmmUpdate(UpdateView):
    model = Omm
    fields = '__all__'


class OmmDelete(DeleteView):
    model = Omm
    success_url = reverse_lazy('omma')


class PartnerCreate(CreateView):
    model = Partner
    fields = '__all__'


class PartnerUpdate(UpdateView):
    model = Partner
    fields = '__all__'


class PartnerDelete(DeleteView):
    model = Partner
    success_url = reverse_lazy('partneri')


class SvjetiljkaCreate(CreateView):
    model = Svjetiljka
    fields = '__all__'


class SvjetiljkaUpdate(UpdateView):
    model = Svjetiljka
    # fields = '__all__'
    fields = ['oib', 'stup', 'tip_svjetiljke', 'tip_svjetlosti', 'snaga', 'klasa_povrsine']


class SvjetiljkaDelete(DeleteView):
    model = Svjetiljka
    success_url = reverse_lazy('svjetiljke')
