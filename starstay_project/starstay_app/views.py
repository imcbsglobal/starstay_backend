from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .models import Visitor, Showcase
from .serializers import VisitorSerializer, UserSerializer, ShowcaseSerializer, DemonstrationSerializer


import requests
from django.conf import settings

def send_whatsapp_message(phone, message):
    url = "https://app.dxing.in/api/send/whatsapp"

    params = {
        "secret": "7b8ae820ecb39f8d173d57b51e1fce4c023e359e",
        "account": "1761365422812b4ba287f5ee0bc9d43bbf5bbe87fb68fc4daea92d8",
        "recipient": phone,
        "type": "text",
        "message": message,
        "priority": 1,
    }

    try:
        response = requests.get(url, params=params)
        return response.json()
    except Exception as e:
        print("WhatsApp Error:", e)
        return None

# --------------------- VISITOR API ---------------------
@csrf_exempt
@api_view(["POST", "GET"])
def visitor_list(request):

    if request.method == "GET":
        visitors = Visitor.objects.all().order_by("-id")
        serializer = VisitorSerializer(visitors, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = VisitorSerializer(data=request.data)
        if serializer.is_valid():
            visitor = serializer.save()

            # Send WhatsApp to Admin
            admin_number = "919072791379" 
            
            message = (
                f"🔔 New Visitor Registered - Starstay 🩷!\n\n"
                f"👤 Name: {visitor.name}\n"
                f"📱 Phone: {visitor.phone}\n"
                f"📧 Email: {visitor.email}\n\n"
                f"✅ Registration Time: {visitor.created_at.strftime('%Y-%m-%d %H:%M:%S') if hasattr(visitor, 'created_at') else 'N/A'}"
            )

            # Send WhatsApp notification
            whatsapp_response = send_whatsapp_message(admin_number, message)
            
            # Optional: Log the response for debugging
            if whatsapp_response:
                print("✅ WhatsApp sent successfully:", whatsapp_response)
            else:
                print("❌ WhatsApp sending failed")

            return Response({"message": "Visitor registered successfully!"}, status=201)

        return Response(serializer.errors, status=400)


# --------------------- USER REGISTER API ---------------------
@csrf_exempt
@api_view(["POST"])
def user_register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "User registered successfully!"}, status=201)
    return Response(serializer.errors, status=400)


# --------------------- ADMIN LOGIN ---------------------
@csrf_exempt
@api_view(["POST"])
def admin_login(request):
    username = request.data.get("username")
    password = request.data.get("password")

    ADMIN_USER = "imcbs"
    ADMIN_PASS = "1234"

    if username == ADMIN_USER and password == ADMIN_PASS:
        return Response({"message": "Admin login successful!", "token": "admin123token"})

    return Response({"error": "Invalid admin credentials"}, status=401)


# --------------------- SHOWCASE LIST API ---------------------
@csrf_exempt
@api_view(["GET", "POST"])
def showcase_list(request):
    if request.method == "GET":
        showcase_items = Showcase.objects.all()
        serializer = ShowcaseSerializer(showcase_items, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = ShowcaseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


# --------------------- SHOWCASE DETAIL API ---------------------
@csrf_exempt
@api_view(["GET", "PUT", "PATCH", "DELETE"])
def showcase_detail(request, pk):
    try:
        item = Showcase.objects.get(pk=pk)
    except Showcase.DoesNotExist:
        return Response({"error": "Item not found"}, status=404)

    if request.method == "GET":
        serializer = ShowcaseSerializer(item)
        return Response(serializer.data)

    elif request.method in ["PUT", "PATCH"]:
        serializer = ShowcaseSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == "DELETE":
        item.delete()
        return Response({"message": "Deleted successfully"}, status=204)


# --------------------- DASHBOARD COUNTS ---------------------
@api_view(["GET"])
def dashboard_data(request):
    visitors = Visitor.objects.count()
    showcase = Showcase.objects.count()

    return Response({
        "visitors": visitors,
        "showcase_items": showcase,
    })

@csrf_exempt
@api_view(["GET", "POST"])
def demonstration_list(request):
    if request.method == "GET":
        demonstrations = Demonstration.objects.all()
        serializer = DemonstrationSerializer(demonstrations, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = DemonstrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


# --------------------- DEMONSTRATION DETAIL API ---------------------
@csrf_exempt
@api_view(["GET", "PUT", "PATCH", "DELETE"])
def demonstration_detail(request, pk):
    try:
        item = Demonstration.objects.get(pk=pk)
    except Demonstration.DoesNotExist:
        return Response({"error": "Item not found"}, status=404)

    if request.method == "GET":
        serializer = DemonstrationSerializer(item)
        return Response(serializer.data)

    elif request.method in ["PUT", "PATCH"]:
        serializer = DemonstrationSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == "DELETE":
        item.delete()
        return Response({"message": "Deleted successfully"}, status=204)