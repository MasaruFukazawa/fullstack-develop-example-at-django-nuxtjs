# -*- coding:utf-8 -*-

from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Hello


# Create your views here.
class Db(APIView):

    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        entry = Hello.objects.get(pk=1)
        return Response({"message": entry.world})
