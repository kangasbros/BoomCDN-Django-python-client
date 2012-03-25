from django.conf.urls.defaults import patterns, include, url

from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'files.views.add_file', name='add_file'),sign_key_profile
    url(r'^files/add_file/?$', 'files.views.add_file', name='add_file'),
    url(r'^files/alias/?$', 'files.views.alias', name='alias'),
    url(r'^files/delete/?$', 'files.views.delete', name='delete'),
    # url(r'^bombcdn_client/', include('bombcdn_client.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()

