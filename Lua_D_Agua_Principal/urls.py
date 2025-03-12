"""
URL configuration for Lua_D_Agua_Principal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path
import admin.views as admin_views
import principal.views as principal_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  #    path('admin/', admin.site.urls),

                  # ADMIN
                  path('admin/', admin_views.index, name='admin_index'),
                  path('admin/dashboard/', admin_views.dashboard, name='dashboard'),
                  path('admin/edit/<int:product_id>', admin_views.product_edit, name='edit'),
                  path('admin/register/', admin_views.FileFieldFormView.as_view(), name='register'),
                  path('admin/products/delete/<int:product_id>/', admin_views.delete_product, name='delete_product'),

                  # PRINCIPAL
                  path('', principal_views.index, name='home_index'),
                  path('services/', principal_views.services, name='services'),
                  path('product/', principal_views.product, name='product'),
                  path('product/<int:product_id>', principal_views.product_id, name='product_id'),
                  path('product/<str:product_category>/', principal_views.product_by_category, name='product_category'),

                  # path("create/admin/", admin_views.create_admin, name="create_admin"),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
