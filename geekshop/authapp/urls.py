from django.urls import path
import authapp.views as authapp


app_name = 'authapp'

urlpatterns = [
    path('login/', authapp.Login.as_view(), name='login'),
    path('logout/', authapp.Logout.as_view(), name='logout'),
    path('register/', authapp.register, name='register'),
    path('profile/', authapp.edit, name='edit'),

    # path('profile/<int:pk>/', authapp.Edit.as_view(template_name='authapp/edit.html'), name='edit'),
    path('verify/<email>/<key>/', authapp.verify, name='verify'),

]