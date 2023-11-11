from django.urls import path
from django.views.decorators.cache import cache_page

from home.apps import HomeConfig
from home.views import IndexView, CategoryListView, ClientListView, ClientCreateView, ClientUpdateView, ClientDeleteView

app_name = HomeConfig.name

urlpatterns = [
    path('', cache_page(60)(IndexView.as_view()), name='index'),
    path('categorys/', CategoryListView.as_view(), name='category_list'),
    path('<int:pk>clients/', ClientListView.as_view(), name='clients_list'),
    path('clients/create/', ClientCreateView.as_view(), name='clients_create'),
    path('update/<int:pk>', ClientUpdateView.as_view(), name='clients_update'),
    path('delete/<int:pk>', ClientDeleteView.as_view(), name='clients_delete'),

]