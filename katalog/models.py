from django.db import models
from django.urls import reverse


# Create your models here.
class Svjetiljka(models.Model):
    oib = models.CharField(max_length=50)
    stup = models.CharField(max_length=5)
    tip_svjetiljke = models.CharField(max_length=25)
    tip_svjetlosti = models.CharField(max_length=25)
    snaga = models.IntegerField()
    klasa_povrsine = models.CharField(max_length=10)
    x_koordinata = models.CharField(max_length=15)
    y_koordinata = models.CharField(max_length=15)
    slika = models.ImageField(default='default.jpg', blank=True)

    def __str__(self):
        return f'[{self.oib}]: {self.tip_svjetiljke} ({self.snaga})'

    def get_absolute_url(self):
        return reverse('svjetiljka-detalji', args=[str(self.id)])


class Omm(models.Model):
    sifra = models.IntegerField(null=True)
    adresa = models.CharField(max_length=50)
    trafo = models.CharField(max_length=25, null=True)
    brojilo = models.CharField(max_length=100)

    def __str__(self):
        return f'[{self.id}]: {self.adresa} ({self.sifra})'

    def get_absolute_url(self):
        return reverse('omm-detalji', args=[str(self.id)])


class Racun(models.Model):
    datum = models.DateField()
    broj = models.CharField(max_length=25, null=True)
    kolicina = models.IntegerField()
    # foreign key; tarifa
    tarifa = models.ForeignKey('Tarifa', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'[{self.id}]: {self.datum} ({self.tarifa.naziv})'

    def get_absolute_url(self):
        return reverse('racun-detalji', args=[str(self.id)])

    def suma_opskrbe(self):
        return self.tarifa.rjt_rvt * self.kolicina + self.tarifa.oie * self.kolicina + self.tarifa.trnp *\
               self.kolicina

    def prikaz_tarife(self):
        return f'{self.tarifa.naziv} ({self.tarifa.mjesec})'
    prikaz_tarife.short_description = 'Tarifa'


class Instanca(models.Model):
    # foreign key; racun
    racun = models.ForeignKey('Racun', on_delete=models.SET_NULL, null=True)
    datum_od = models.DateField()
    datum_do = models.DateField()
    konstanta = models.IntegerField(default=1)
    potrosak = models.IntegerField()
    # foreign key; omm
    omm = models.ForeignKey('Omm', on_delete=models.SET_NULL, null=True)
    stanje_od = models.CharField(max_length=25, null=True)
    stanje_do = models.CharField(max_length=25, null=True)
    mrezarina = models.DecimalField(max_digits=4, decimal_places=2)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f'[{self.id}]: {self.datum_od} --> {self.datum_do}'

    def get_absolute_url(self):
        return reverse('instanca-detalji', args=[str(self.id)])

    def suma_opskrbe(self):
        return self.racun.tarifa.rjt_rvt * self.potrosak + self.racun.tarifa.oie * self.potrosak + \
               self.racun.tarifa.trnp * self.potrosak

    def suma_mrezarine(self):
        return self.racun.tarifa.rvt_r1 * self.potrosak + self.racun.tarifa.naknada * self.mrezarina

    def prikaz_tarife(self):
        return f'{self.racun.tarifa.naziv} ({self.racun.tarifa.mjesec})'

    def prikaz_omm(self):
        return f'{self.omm.adresa}'
    prikaz_omm.short_description = 'Omm'


class Tarifa(models.Model):
    naziv = models.CharField(max_length=25)
    mjesec = models.DateField()
    rjt_rvt = models.DecimalField(max_digits=5, decimal_places=4)
    oie = models.DecimalField(max_digits=5, decimal_places=4)
    trnp = models.DecimalField(max_digits=6, decimal_places=5)
    rvt_r1 = models.DecimalField(max_digits=3, decimal_places=2)
    naknada = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return f'{self.naziv} ({self.mjesec})'

    def get_absolute_url(self):
        return reverse('tarifa-detalji', args=[str(self.id)])


class Partner(models.Model):
    naziv = models.CharField(max_length=25, null=True)
    oib = models.IntegerField()
    tvrtka = models.CharField(max_length=25, null=True)
    adresa = models.CharField(max_length=25, null=True)
    email = models.EmailField()

    def __str__(self):
        return f'[{self.id}]: {self.tvrtka} ({self.oib})'

    def get_absolute_url(self):
        return reverse('partner-detalji', args=[str(self.id)])
