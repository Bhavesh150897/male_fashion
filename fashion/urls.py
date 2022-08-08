from django.urls import path
from fashion import views
from django.conf import settings
from django.urls import include, re_path
from django.conf.urls.static import static
from .views import RegisterView
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from .forms import MyPasswordResetForm, MySetPasswordForm, MyPasswordChangeForm

urlpatterns = [
    re_path(r'^$',views.ProductView.as_view(), name='home'),
    re_path(r'^about/$', views.about, name='about'),
    re_path(r'^shop/$', views.shop, name='shop'),
    re_path(r'^contact-us/$', views.contact, name='contact'),
    re_path(r'^cart/$', views.cart, name='cart'),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('pluscart/', views.plus_cart,name='pluscart'),
    path('minuscart/', views.minus_cart,name='minuscart'),
    path('removecart/', views.remove_cart,name='removecart'),
    path('product/<int:id>/favourites', views.Favorites, name='Favorites'),
    path('favourites', views.favoritesPage, name='favoritesPage'),
    re_path(r'^checkout/$', views.checkout, name='checkout'),
    re_path(r'^signup/$', RegisterView.as_view(), name='signup'),
    re_path(r'^login/$', views.login, name='login'),
    path('product-details/<int:pk>/', views.productDetails.as_view(), name='productDetails'),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("profile/", views.CustomerView.as_view(), name="userProfile"),
    path("address/", views.address, name="address"),
    # path('product/checkout/<id>/', views.create_checkout_session, name='product_checkout'),

    path('passwordchange/', auth_views.PasswordChangeView.as_view(template_name='fashion/passwordchange.html', form_class=MyPasswordChangeForm, success_url='/passwordchangedone/'), name='passwordchange'),
    path('passwordchangedone/', auth_views.PasswordChangeDoneView.as_view(template_name='fashion/passwordchangedone.html'), name='passwordchangedone'),

    path("password-reset/", auth_views.PasswordResetView.as_view(template_name='fashion/password_reset.html', form_class=MyPasswordResetForm), name="password_reset"),
    path("password-reset/done/", auth_views.PasswordResetDoneView.as_view(template_name='fashion/password_reset_done.html'), name="password_reset_done"),
    path("password-reset-confirm/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name='fashion/password_reset_confirm.html', form_class=MySetPasswordForm), name="password_reset_confirm"),
    path("password-reset-complete/", auth_views.PasswordResetCompleteView.as_view(template_name='fashion/password_reset_complete.html'), name="password_reset_complete"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
