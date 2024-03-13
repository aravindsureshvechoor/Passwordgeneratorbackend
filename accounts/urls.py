from django.urls import path
from .views import RegisterView, RetrieveUserView, SavePassword, ViewSavedPassword, DeleteSavedPassword
urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('me/', RetrieveUserView.as_view()),
    path('save-password/', SavePassword.as_view()),
    path('view-passwords/', ViewSavedPassword.as_view()),
    path('delete-password/<int:id>/', DeleteSavedPassword.as_view()),
]
