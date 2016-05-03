from django.conf.urls import patterns, include, url
from django.contrib import admin
from siteshow import views
from django.conf import settings 
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'DectectSite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$',views.index),
    url(r'^contact/$',views.contact),
    url(r'^phish/$',views.phish),
    url(r'^zeus/$',views.zeus),
    url(r'^faq/$',views.faq),
    url(r'^malware/$',views.malware),
    url(r'^search_phish/$',views.search_phish),
    url(r'^search_zeus/$',views.search_zeus),
    url(r'^search_malware/$',views.search_malware),
    url(r'^download_cvs/$',views.download_cvs),
    url(r'^download_cvs_phish/$',views.download_cvs_phish),
    url(r'^download_cvs_zeus/$',views.download_cvs_zeus),
    url(r'^download_cvs_malware/$',views.download_cvs_malware),
    url(r'^download_txt/$',views.download_txt),
    url(r'^download_txt_phish/$',views.download_txt_phish),
    url(r'^download_txt_zeus/$',views.download_txt_zeus),
    url(r'^download_txt_malware/$',views.download_txt_malware),
    url(r'^download_json/$',views.download_json),
    url(r'^download_json_phish/$',views.download_json_phish),
    url(r'^download_json_zeus/$',views.download_json_zeus),
    url(r'^download_json_malware/$',views.download_json_malware),
    url(r'^emailToServer/$',views.emailToServer),
    url(r'^whois/$',views.whois),
    url(r'^virustotal/$',views.virustotal),
    url(r'^safebrowsing/$',views.safebrowsing),
    url(r'^detectOnline/$',views.detectOnline),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.STATICFILES_ROOT }),

)
