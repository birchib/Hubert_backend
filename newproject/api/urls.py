from django.urls import path
from .views import get_dbset, PersonListView
# from .views import get_dbset, create_dbset, dbset_detail, PersonListView

urlpatterns = [
    path('persons/', PersonListView.as_view(), name='person-list'),
] 