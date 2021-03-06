from django.conf.urls import patterns, include, url
from django.conf import settings
from django.views.generic import TemplateView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
import views
import kupra.views

import kupra.urls

urlpatterns = patterns('',
    # Examples:
    url(r"^$", views.home, name="home"),
    url(r"^account/signup/$", views.SignupView.as_view(), name="account_signup"),
    url(r"^account/private/$", kupra.views.KupraUserUpdateView.as_view(), name="account_private"),
    # url(r'^openshift/', include('openshift.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^kupra/', include(kupra.urls)),
    url(r"^account/", include("account.urls")),
)
if settings.DEBUG:
    urlpatterns += patterns('', (r'^media\/(?P<path>.*)$',
                                 'django.views.static.serve',
                                 {'document_root': settings.MEDIA_ROOT}),
                           )
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()
    import debug_toolbar
    urlpatterns += patterns('',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )
