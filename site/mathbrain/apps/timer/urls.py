from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template


urlpatterns = patterns("",
    url(r"^$", direct_to_template, {"template": "timer/2u.html"}, name="2utimer"),
    url(r"^2u/$", direct_to_template, {"template": "timer/2u.html"}, name="2utimer"),
    url(r"^3u/$", direct_to_template, {"template": "timer/3u.html"}, name="3utimer"),
)
