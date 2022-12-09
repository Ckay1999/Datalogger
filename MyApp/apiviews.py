from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from rest_framework.parsers import FileUploadParser
from rest_framework import status
from bson import ObjectId
from django.http import Http404
from .models import UserOperator
from .serializers import UserOperatorSerializer

class UserOperatorDetail(APIView):
    parser_class = (FileUploadParser,)

    def get_object(self, pk):
        try:
            pk = ObjectId(pk)
            return UserOperator.objects.get(pk=pk)
        except UserOperator.DoesNotExist:
            raise Http404

    def get(self, request, pk=None):
        if pk:
            pk = ObjectId(pk)
            useroperator = self.get_object(pk)
            serializer = UserOperatorSerializer(useroperator)
        else:
            useroperator = UserOperator.objects.all()
            serializer = UserOperatorSerializer(useroperator, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk=None):
        serializer = UserOperatorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        pk = ObjectId(pk)
        useroperator = self.get_object(pk)
        serializer = UserOperatorSerializer(useroperator, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk="5ed3f42ebb2cf5272ee5361b"):
        pk = ObjectId(pk)
        useroperator = self.get_object(pk)
        useroperator.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

