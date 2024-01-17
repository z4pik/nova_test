from django.urls import path
from .views import CreateDocumentView

urlpatterns = [
    path('create/', CreateDocumentView.as_view(), name='create-document'),
]