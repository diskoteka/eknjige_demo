from django.db import models
from django.urls import reverse


# Create your models here. - dodat poveznicu svjetiljki i OMM
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
    # dodati (tip_stupa, duljina_kraka/konzole, tip_izvora_svjetlosti, )

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
    # dodati naziv i cjenik distributera

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


class Korisnik(models.Model):
    naziv = models.CharField(max_length=25, null=True)
    email = models.EmailField()
    adresa = models.CharField(max_length=25, null=True)

    def __str__(self):
        return self.email

    def get_absolute_url(self):
        return reverse('korisnik-detalji', args=[str(self.id)])
    
    def _mail(self):
        return self.email


class OJR(models.Model):
    ID_elementa = models.IntegerField(primary_key=True)
    OIB_OJR = models.CharField(max_length=50)
    Kupac = models.CharField(max_length=50)
    GRUPA = models.CharField(max_length=2)
    Adresa_OMM = models.CharField(max_length=50)
    Broj_trafostanice = models.CharField(max_length=50)
    Šifra_OMM = models.CharField(max_length=50)
    Vlasnik_OMM = models.CharField(max_length=50)
    Naziv_distribucijskog_podrucja = models.CharField(max_length=50)
    Naziv_pogona = models.CharField(max_length=50)
    Zakupljena_snaga = models.CharField(max_length=50)
    Potrošnja_2013 = models.CharField(max_length=25)
    Potrošnja_2014 = models.CharField(max_length=25)
    Potrošnja_2015 = models.CharField(max_length=25)
    Potrošnja_2016 = models.CharField(max_length=25, null=True)
    Potrošnja_2017 = models.CharField(max_length=25, null=True)
    Potrošnja_2018 = models.CharField(max_length=25, null=True)
    Vrsta_sustava_upravljanja = models.CharField(max_length=50)
    Strujni_krugovi_u_upotrebi = models.CharField(max_length=50)
    Max_broj_strujnih_krugova = models.CharField(max_length=50)
    Tip_kablova = models.CharField(max_length=25)
    Tip_NN_mreze = models.CharField(max_length=25)
    Uzemljenje = models.CharField(max_length=25)
    Prenaponska_zaštita = models.CharField(max_length=25)
    OMM_u_trafostanici = models.CharField(max_length=25)
    Uklopni_uređaj_funkcionalan = models.CharField(max_length=25)
    Grupna_regulacija = models.CharField(max_length=25)
    Faktor_regulacije_K_OMMa = models.CharField(max_length=25)
    Faktor_regulacije_K_svjetiljki = models.CharField(max_length=25)
    Provedeno_kontrolno_mjerenje = models.CharField(max_length=25)
    Napomena = models.CharField(max_length=25)
    x_koordinata = models.CharField(max_length=25)
    y_koordinata = models.CharField(max_length=25)
    ID_elementa_EP = models.CharField(max_length=25)
    
    def __str__(self):
        return self.ID_elementa

    def get_absolute_url(self):
        return reverse('OJR-detalji', args=[str(self.ID_elementa)])
