from django.conf.urls import patterns, url


urlpatterns = patterns('regme.views',
    url('register/', 'register', {}, 'register'),
    url('registered/', 'registered', {}, 'registered'),
)
