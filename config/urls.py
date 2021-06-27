from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from jd.views import index

urlpatterns = [
    path('', index, name='index'),
    path('admin/', admin.site.urls),
    path('jd/', include('jd.urls')),
    path('account/', include('account.urls'))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
