from django.shortcuts import render
from rest_framework.views import APIView 
from rest_framework.response import Response
from .models import user    
from rest_framework import status
from .serializers import GetAllUserSerializer
# Create your views here.
def home(request):
    return render(request, 'app1/home.html')

def base(request):
    return render(request, 'app1/base.html')

class GetAllUserAPIView(APIView):
    def get(self,request):
        users = user.objects.all()
        serializer = GetAllUserSerializer(users, many=True)
        return Response(data = serializer.data, status=status.HTTP_200_OK)    


