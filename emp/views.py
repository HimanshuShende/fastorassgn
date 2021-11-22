from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.http import JsonResponse

from rest_framework import serializers, status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

from .serializer import EnquirySerializer, UserSerializer
from .models import Enquiry, User
# Create your views here.


"""
    All API endpoints are checked for authentication and only authenticated 
    users will be allowed.
"""

@api_view(['GET', 'POST'])
@parser_classes([JSONParser])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def enquiryOperations(request, format=None):
    """
        GET : Returns all public enquiries.
        POST : Creates an enquiry and returns it.
    """
    if request.method == 'GET':
        enqueries = Enquiry.objects.getAllPublicEnquiries()
        serializer = EnquirySerializer(enqueries, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = EnquirySerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET', 'POST'])
@parser_classes([JSONParser])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def employeeOperations(request, format=None):
    """
        GET : Returns all users detail.
        POST : Creates a user but with no password and no access to admin panel
               and returns the created user.
    """
    if request.method == 'GET':
        enqueries = User.objects.all()
        serializer = UserSerializer(enqueries, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        data = request.data
        serializer = UserSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def claimEnquiry(request, pk):
    """
        GET : User can claim an enquiry.
    """
    try:
        obj = Enquiry.objects.get(id = pk)

        if obj.claimed_by != None and obj.claimed_by != request.user:
            return Response("Enquiry has already been claimed.")
        obj.claimed_by = request.user
        obj.public = False
        obj.save()
        serializer = EnquirySerializer(obj)
        return Response(serializer.data)
    except ObjectDoesNotExist:
        return Response(
            f"Enquiry with id {pk} does not exists.",
            status.HTTP_404_NOT_FOUND
        )


@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def myClaimedEnquiry(request):
    """
        GET : Returns a user's claimed enquiries.
    """
    objs = Enquiry.objects.filter(claimed_by=request.user)
    serializer = EnquirySerializer(objs, many=True)
    return Response(serializer.data)
