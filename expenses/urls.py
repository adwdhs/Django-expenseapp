from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='expenses'),
    path('add-expense', views.add_expense, name='add-expense'),
    path('edit-expense/<str:pk>', views.editExpense, name='edit-expense'),
    path('delete-expense/<str:pk>', views.deleteExpense, name='delete-expense'),
    path('summary', views.categorySummary, name='summary'),
    path('stats', views.statsView, name='stats'),
]