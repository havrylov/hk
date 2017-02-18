from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = [url(r'', include('budget.urls', namespace="budget")),
               url(r'^captcha/', include('captcha.urls')),
               url(r'^test_data/', include('test_data.urls', namespace="test_data"))]
    # Examples:
    # url(r'^$', 'hk.views.home', name='home'),
    # url(r'^hk/', include('hk.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
