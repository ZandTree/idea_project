from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    url('auth/', include('djoser.social.urls')),
    path('api/v1/', include('api.urls'))
]
urlpatterns += [re_path(r'^.*', TemplateView.as_view(template_name="index.html"))]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()
    # urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
