from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('flik.app.views',
    url(r'^admin/', include(admin.site.urls)),
    # Examples:
    # url(r'^$', 'flik.views.home', name='home'),
    url(r'^$', 'login_view', name='login'),
    url(r'^logout$', 'logout_view', name='logout'),
    url(r'^signup$', 'signup', name='signup'),
    url(r'^dashboard$', 'dashboard', name='dashboard'),
    url(r'^dashboard/fingerprints$', 'dashboard_fingerprints', name='dashboard-fingerprints'),
    url(r'^dashboard/offers$', 'dashboard_offers', name='dashboard-offers'),

    url(r'^dashboard/fingerprints/create$', 'dashboard_fingerprints_create',\
        name='dashboard-fingerprints-create'),
    url(r'^dashboard/offers/create$', 'dashboard_offers_create',\
        name='dashboard-offers-create'),
    url(r'^dashboard/campaigns/create$', 'dashboard_campaigns_create',\
        name='dashboard-campaigns-create'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
)
