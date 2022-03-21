from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('wiki/<str:entryTitle>', views.entry, name='wiki'),
    path('search', views.search, name='search'),
    path('add', views.addEntry, name="addEntry"),
    path('edit/<str:entryTitle>', views.editEntry, name='editEntry'),
    path('random', views.randomEntry, name='randomEntry')
]
