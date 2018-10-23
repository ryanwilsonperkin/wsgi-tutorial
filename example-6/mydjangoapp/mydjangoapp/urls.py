from django.urls import path
from .views import view

urlpatterns = [
    path('', view),
    path('<path:path>', view),
]
