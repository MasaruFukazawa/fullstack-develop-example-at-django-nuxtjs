# -*- coding:utf-8 -*-

from django.urls import path

from . import views

urlpatterns = [path("backend/", views.Db.as_view())]
