from django.conf.urls import patterns, include, url
from django.conf import settings 
import siteshow.urls
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'DectectSite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^siteshow/',include(siteshow.urls)),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.STATICFILES_ROOT }),

)
