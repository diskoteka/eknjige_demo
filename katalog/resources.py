from import_export import resources
from .models import Svjetiljka, Omm, Racun, Instanca


class SvjetiljkaResource(resources.ModelResource):
    class Meta:
        model = Svjetiljka


class OmmResource(resources.ModelResource):
    class Meta:
        model = Omm


class RacunResource(resources.ModelResource):
    class Meta:
        model = Racun


class InstancaResource(resources.ModelResource):
    class Meta:
        model = Instanca
