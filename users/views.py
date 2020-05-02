import csv

from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.core.paginator import Paginator

from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import User
from users.serializers import UserSerializer, UserDeserializer


class UserLoginView(APIView):
    def post(self, request):
        try:
            user = authenticate(email=request.data['email'], password=request.data['password'])
            if user:
                return Response({"token": user.token})
        except Exception as e:
            return Response({"token": "None"})


class UserRegistrationView(APIView):
    def post(self, request):
        try:
            deserializer = UserDeserializer(data=request.data)
            deserializer.is_valid(raise_exception=True)
            deserializer.save()
            return HttpResponse("True")
        except Exception as e:
            print(e)
            return HttpResponse("False")


class UserDetailView(APIView):

    def get(self, request):
        page = request.query_params.get('page')
        users = User.objects.all()
        field_names = ['id', 'email', "first_name", "last_name"]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="export.csv"'

        writer = csv.writer(response)
        writer.writerow(field_names)
        if page:
            size = 2
            paginator = Paginator(users, size)
            resources = paginator.page(page)
            serializer = UserSerializer(resources, many=True)


        else:
            for obj in User.objects.all():
                writer.writerow([getattr(obj, field) for field in field_names])

        return response
