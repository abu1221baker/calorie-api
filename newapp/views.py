from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from .serializer import *
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

# Create your views here.
@permission_classes([IsAuthenticated])
@api_view(['GET','POST'])
def calorie_view(request):
    if request.method == 'GET':
        food_items = FoodItem.objects.all()
        serializer = FoodItemSerializer(food_items, many=True)
        data = {
            "message": "Calorie Data Retrieved Successfully",
            "data": serializer.data
        }
        return Response(data)
    if request.method == 'POST':
        serializer = FoodItemSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            data = {
                "message": "Food Item Created Successfully",
                "data": serializer.data
            }
            return Response(data, status=201)
        return Response(serializer.errors, status=400)

@permission_classes([IsAuthenticated])
@api_view(['GET'])
def per_item(request,name):
    try:
        item = FoodItem.objects.filter(name__iexact=name)
        serializer = FoodItemSerializer(item,many=True)
        data = {
            "message": "Food Item Retrieved Successfully",
            "data": serializer.data
        }
        return Response(data)
    except FoodItem.DoesNotExist:
        data = {
            "message": "Food Item Not Found"
        }
        return Response(data, status=404)


@csrf_exempt
@api_view(['POST']) 
def create_profile(request):


    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    data = json.loads(request.body)

    if User.objects.filter(username=data["username"]).exists():
        return JsonResponse({"error": "Username already exists"}, status=400)

    # 1️⃣ Create User
    user = User.objects.create_user(
        username=data["username"],
        email=data.get("email"),
        password=data["password"]
    )

    # 2️⃣ Create Profile
    Profile.objects.create(
        user=user,
        age=data.get("age"),
        weight=data.get("weight"),
        height=data.get("height")
    )

    return JsonResponse({"message": "User registered successfully"}, status=201)


@permission_classes([IsAuthenticated])
@api_view(['GET',])
def view_profile(request):
    if request.method == 'GET':
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles, many=True)
        data = {
            "message": "Profiles Retrieved Successfully",
            "data": serializer.data
        }
        return Response(data)
