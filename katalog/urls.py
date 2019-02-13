from django.urls import path
from katalog import views


# single views
urlpatterns = [
    path('', views.index, name='index'),
    path('omm/scada/', views.scada, name='scada'),
    path('svjetiljke/gmap/', views.gmap, name='gmap'),
]

# email - sms
urlpatterns += [
    path('send/mail/', views.email, name='send-mail'),
    path('send/sms/', views.sms, name='send-sms'),
]

# chart views
urlpatterns += [
    path('tarife/charts/', views.TarifeChartHome.as_view(), name='tarife-charts'),
    path('tarife/api/chart/data/', views.TarifeChartData.as_view()),
    path('instance/charts/', views.InstanceChartHome.as_view(), name='instance-charts'),
    path('instance/api/chart/data/', views.InstanceChartData.as_view()),
    path('racuni/charts/', views.RacuniChartHome.as_view(), name="racuni-charts"),
    path('racuni/api/chart/data/', views.RacuniChartData.as_view()),
]

# renew form managers
urlpatterns += [
    path('racun/<int:pk>/renew/', views.renew_racun_manager, name='racun-renew-manager'),
]

# export - import - delete
urlpatterns += [
    path('racuni/exp/', views.racun_export, name='racun_exp'),
    path('racuni/imp/', views.racun_import, name='racun_imp'),
    path('racuni/del/', views.racun_del, name='racun_del'),
    path('racuni/delall/', views.racun_del_all, name='racun_del_all'),
    path('instance/exp/', views.instanca_export, name='instanca_exp'),
    path('instance/imp/', views.instanca_import, name='instanca_imp'),
    path('instance/del/', views.instanca_del, name='instanca_del'),
    path('instance/delall/', views.instanca_del_all, name='instanca_del_all'),
    path('omma/exp/', views.omm_export, name='omm_exp'),
    path('omma/imp/', views.omm_import, name='omm_imp'),
    path('omma/del/', views.omm_del, name='omm_del'),
    path('omma/delall/', views.omm_del_all, name='omm_del_all'),
    path('svjetiljke/exp/', views.svjetiljka_export, name='svj_exp'),
    path('svjetiljke/imp/', views.svjetiljka_import, name='svj_imp'),
    path('svjetiljke/del/', views.svj_del, name='svj_del'),
    path('svjetiljke/delall/', views.svj_del_all, name='svj_del_all'),
]

# predlosci
urlpatterns += [
    path('predlosci/racuni/', views.template_racuni, name='predlosci_racuni'),
    path('predlosci/instance/', views.template_instance, name='predlosci_instance'),
    path('predlosci/omm/', views.template_omm, name='predlosci_omm'),
]

# class based views
urlpatterns += [
    path('racuni/', views.RacunListView.as_view(), name='racuni'),
    path('racun/<int:pk>', views.RacunDetailView.as_view(), name='racun-detalji'),
    path('instance/', views.InstancaListView.as_view(), name='instance'),
    path('instanca/<int:pk>', views.InstancaDetailView.as_view(), name='instanca-detalji'),
    path('tarife/', views.TarifaListView.as_view(), name='tarife'),
    path('tarifa/<int:pk>', views.TarifaDetailView.as_view(), name='tarifa-detalji'),
    path('omma/', views.OmmListView.as_view(), name='omma'),
    path('omm/<int:pk>', views.OmmDetailView.as_view(), name='omm-detalji'),
    path('partneri/', views.PartnerListView.as_view(), name='partneri'),
    path('partner/<int:pk>', views.PartnerDetailView.as_view(), name='partner-detalji'),
    path('svjetiljke/', views.SvjetiljkaListView.as_view(), name='svjetiljke'),
    path('svjetiljka/<int:pk>', views.SvjetiljkaDetailView.as_view(), name='svjetiljka-detalji'),
]

# crud forms
urlpatterns += [
    path('racun/create/', views.RacunCreate.as_view(), name='racun_create'),
    path('racun/<int:pk>/update/', views.RacunUpdate.as_view(), name='racun_update'),
    path('racun/<int:pk>/delete/', views.RacunDelete.as_view(), name='racun_delete'),
    path('instanca/create/', views.InstancaCreate.as_view(), name='instanca_create'),
    path('instanca/<int:pk>/update/', views.InstancaUpdate.as_view(), name='instanca_update'),
    path('instanca/<int:pk>/delete/', views.InstancaDelete.as_view(), name='instanca_delete'),
    path('tarifa/create/', views.TarifaCreate.as_view(), name='tarifa_create'),
    path('tarifa/<int:pk>/update/', views.TarifaUpdate.as_view(), name='tarifa_update'),
    path('tarifa/<int:pk>/delete/', views.TarifaDelete.as_view(), name='tarifa_delete'),
    path('omm/create/', views.OmmCreate.as_view(), name='omm_create'),
    path('omm/<int:pk>/update/', views.OmmUpdate.as_view(), name='omm_update'),
    path('omm/<int:pk>/delete/', views.OmmDelete.as_view(), name='omm_delete'),
    path('partner/create/', views.PartnerCreate.as_view(), name='partner_create'),
    path('partner/<int:pk>/update/', views.PartnerUpdate.as_view(), name='partner_update'),
    path('partner/<int:pk>/delete/', views.PartnerDelete.as_view(), name='partner_delete'),
    path('svjetiljka/create/', views.SvjetiljkaCreate.as_view(), name='svjetiljka_create'),
    path('svjetiljka/<int:pk>/update/', views.SvjetiljkaUpdate.as_view(), name='svjetiljka_update'),
    path('svjetiljka/<int:pk>/delete/', views.SvjetiljkaDelete.as_view(), name='svjetiljka_delete'),
]

# pic upload
urlpatterns += [
    path('svjetiljka/<int:pk>/upload_pic/', views.upload_pic, name='upload_pic'),
]
