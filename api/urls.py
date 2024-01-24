from django.urls import path
from .views import *

urlpatterns = [
     path("view-loan/<int:loan_id>/" , viewLoan),
    path("register/" , register),
    path("eligible/" , is_eligible),
    path("create-loan/" , createLoan),
    path("view-loans/<int:cust_id>/",viewLoans)
   
]