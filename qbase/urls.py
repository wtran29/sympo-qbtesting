from django.urls import path
from qbase.views import qbase_request

urlpatterns = [
    path('', view=qbase_request, ),
]