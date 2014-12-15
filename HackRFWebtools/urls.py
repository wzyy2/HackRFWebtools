from django.conf.urls import patterns, include, url
from views import *

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'HackRFWebtools.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$',index),
    url(r'^do$',do),
    # url(r'^admin/', include(admin.site.urls)),
)
