from .models import *
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
import datetime as dt
import json
from django.utils import timezone
from .serializers import *
from django.db.models import Avg
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework.permissions import AllowAny, IsAuthenticated
from asyncio.log import logger
import applogger
from rest_framework import viewsets
from rest_framework.test import APITestCase

class UserLogin(APIView):
    def post(self,request):
        try:
            username=request.data.get("username")
            password=request.data.get("password")
            if username == "" or password == "": #blank data validating
                logger.info("Please enter Username and password!")
                return Response({"status":True,"msg":"Please enter Username and password!"})
            # Authenticates the user using the provided username and password
            user = authenticate(username=username, password=password)
            if user is None:
                logger.info("invalid credential!")
                return Response({"status":True,"msg":"invalid Credential!"})
            else:
                # Generates access and refresh tokens for the authenticated user
                refresh = RefreshToken.for_user(user)
                refresh_token = str(refresh)
                access_token = str(refresh.access_token)

                token_lifetime = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']
                now = dt.datetime.now()
                login_date=str(now.strftime("%y-%m-%d %H:%M:%S"))                
                new_time = now + token_lifetime
                expires_in = str(new_time.strftime("%y-%m-%d %H:%M:%S"))
            logger.info(f"{username} logged in successfully!")
            return Response ({
                    'status': True,
                    'token':access_token ,
                    'login time':login_date,
                    'expires_in': expires_in,
                    'msg': 'User logged in successfully',
                    })
        except : # Handles exceptions and provides an appropriate response in case of errors
            #Error handelling
            logger.exception(f"{request} Something Went wrong!") #log history 
            return Response({"status": False, "msg": "Something went wrong!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class VendorView(APIView):
    permission_classes = (IsAuthenticated,)
    #createing Vendors
    def post(self,request):
        try:
            user=request.user
            if not user.is_superuser: # Checks if the user is a superuser for authorization
                logger.info(" unauthorized access!")
                return Response({"status": False, "msg": "unauthorized access!"}, status=status.HTTP_403_FORBIDDEN)
           
            serializer = VendorCreateSerializer(data=request.data)
            
            
            if serializer.is_valid():
                vender_code = serializer.validated_data['vender_code']
                if Vendors.objects.filter(vender_code=vender_code).exists():
                    logger.info(f"{user} -{vender_code} this vendor already exists!")
                    return Response(
                        {"status": False, "msg": f"{vender_code} this vendor already exists!"},
                        status=status.HTTP_409_CONFLICT
                    )

                serializer.save()
                logger.info(f"{user} - vendor {serializer.data['name']} created Successfully!")
                return Response(
                    {"status": True, "msg": f"vendor {serializer.data['name']} created Successfully!"},
                    status.HTTP_201_CREATED
                )
            else:
                logger.info(f"{user} - all required fields!")
                return Response(
                    {"status": False, "msg": "Please fill all required fields!", "errors": serializer.errors},
                    status.HTTP_400_BAD_REQUEST
                )

        except : # Handles exceptions and provides an appropriate response in case of errors
            logger.exception(f"{request} Something Went wrong!") #log history  
            return Response({"status": False, "msg": "Something went wrong!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  
    
    #get all Vendor's informations
    def get(self, request):
        try:
            user = request.user
            if not user.is_superuser:
                logger.info(f"{user} unauthorized access!")
                return Response({"status": False, "msg": "unauthorized access!"}, status=status.HTTP_403_FORBIDDEN)

            vendor_data = Vendors.objects.all() #geting all vendor datas
            serializer = VendorSerializer(vendor_data, many=True)
            logger.info(f"{user} vendors data accessed!")
            return Response({"status": True, "data": serializer.data})
        except Exception as e:
            logger.exception(f"{request} Something went wrong!")
            return Response({"status": False, "msg": "Something went wrong!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class VendorOperations(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self,request,vendor_id):
        try:
            user=request.user
            if not user.is_superuser: # Checks if the user is a superuser for authorization
                logger.info(f"{user} unauthorized access!")
                return Response({"status": False, "msg": "unauthorized access!"}, status=status.HTTP_403_FORBIDDEN)
            if Vendors.objects.filter(id=vendor_id).exists(): # Validates the input data, ensuring the existence of the specified vendor ID
                vendorInfo=Vendors.objects.get(id=vendor_id) # Retrieves information about a vendor based on the provided vendor ID
                serializer = VendorSerializer(vendorInfo)
                logger.info(f"{user}- {vendor_id} vendor details accessed!")
                return Response({"status":True,"data":serializer.data})
            else:
                logger.info(f"{user}- {vendorInfo.name}requested ID have no vendor!")
                return Response({"status":False,"msg":"Vendor Unavailable!"})
        except : # Handles exceptions and provides an appropriate response in case of errors # Handles exceptions and provides an appropriate response in case of errors

            logger.exception(f"{request} Something Went wrong!") #log history  
            return Response({"status": False, "msg": "Something went wrong!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self,request,vendor_id):
        try:
            user=request.user
            if not user.is_superuser: # Checks if the user is a superuser for authorization
                logger.info(f"{user} unauthorized access!")
                return Response({"status": False, "msg": "unauthorized access!"}, status=status.HTTP_403_FORBIDDEN)
            if Vendors.objects.filter(id=vendor_id).exists():
                vendorInfo=Vendors.objects.get(id=vendor_id) # Retrieves information about a vendor based on the provided vendor ID
                serializer = VendorUpdateSerializer(vendorInfo, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()

                logger.info(f"{user}- {vendor_id} Vendor Updated Successfully!")
                return Response({"status":True,"msg":"Vendor Updated Successfully!"})
            else:
                logger.info(f"{user}- {vendor_id} requested ID have no vendor!")
                return Response({"status":False,"msg":"Vendor Unavailable!"})
        except : # Handles exceptions and provides an appropriate response in case of errors
            logger.exception(f"{request} Something Went wrong!") #log history  
            return Response({"status": False, "msg": "Something went wrong!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self,request,vendor_id):
        try:
            user=request.user
            if not user.is_superuser:  # Checks if the user is a superuser for authorization
                logger.info(f" {user} unauthorized access!")
                return Response({"status": False, "msg": "unauthorized access!"}, status=status.HTTP_403_FORBIDDEN)
            if Vendors.objects.filter(id=vendor_id).exists(): #vendor exists check
                vendorInfo=Vendors.objects.get(id=vendor_id) # Retrieves information about a vendor based on the provided vendor ID
                vendorInfo.delete() #vendor removing
                
                logger.info(f"{user}-{vendor_id} Vendor removed Successfully!")
                return Response({"status":True,"msg":"Vendor removed Successfully!"})
            else:
                logger.info(f"{user}- {vendor_id}requested ID have no vendor!")
                return Response({"status":False,"msg":"Vendor Unavailable!"})  
        except : # Handles exceptions and provides an appropriate response in case of errors
            logger.exception(f"{request} Something Went wrong!") #log history  
            return Response({"status": False, "msg": "Something went wrong!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class Purchase_Order(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self,request):
        try:
            user=request.user
            if not user.is_superuser: # Checks if the user is a superuser for authorization
                logger.info(f" {user} unauthorized access!")
                return Response({"status": False, "msg": "unauthorized access!"}, status=status.HTTP_403_FORBIDDEN)
            
            # Creates a new purchase order entry in the database with the provided information
            serializer = POCreationSerializer(data=request.data)
            if serializer.is_valid():
                po_number = serializer.validated_data['po_number']
                # Check if the PO with the given po_number already exists
                if PO.objects.filter(po_number=po_number).exists():
                    logger.info(f"{user} -{po_number} this vendor already exists!")
                    return Response(
                        {"status": False, "msg": f"{po_number} this vendor already exists!"},
                        status=status.HTTP_409_CONFLICT
                    )
                serializer.save() #saving data in PO table
                logger.info(f"{user} -PO {serializer.data['po_number']} created Successfully!")
                return Response(
                    {"status": True, "msg": f"PO {serializer.data['po_number']} created Successfully!"},
                    status.HTTP_201_CREATED)
            else:
                logger.info(f"{user} - all required fields!")
                return Response(
                    {"status": False, "msg": "Please fill all required fields!", "errors": serializer.errors},
                    status.HTTP_400_BAD_REQUEST
                )
       
        except : # Handles exceptions and provides an appropriate response in case of errors
            logger.exception(f"{request} Something Went wrong!") #log history  
            return Response({"status": False, "msg": "Something went wrong!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request):
        try:
            user=request.user
            if not user.is_superuser: # Checks if the user is a superuser for authorization
                logger.info(f" {user} unauthorized access!")
                return Response({"status": False, "msg": "unauthorized access!"}, status=status.HTTP_403_FORBIDDEN)

            vendor=request.data.get("vendor") #filtering po by vendors
            if vendor:
                POInfo = PO.objects.filter(vendor_id=vendor)
            else:
                POInfo = PO.objects.all() #fetching data from database
            serializer = POSerializer(POInfo, many=True)

            logger.info(f"{user} all PO data accessed!")
            return Response({"status": True, "data": serializer.data})
        except : # Handles exceptions and provides an appropriate response in case of errors
            logger.exception(f"{request} Something Went wrong!") #log history  
            return Response({"status": False, "msg": "Something went wrong!"}, status.HTTP_404_NOT_FOUND)

class PO_operations(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self,request,po_id):
        try:
            user=request.user
            if not user.is_superuser: # Checks if the user is a superuser for authorization
                logger.info(f" {user} unauthorized access!")
                return Response({"status": False, "msg": "unauthorized access!"}, status=status.HTTP_403_FORBIDDEN)
            
            if PO.objects.filter(id=po_id).exists():#PO existing checking
                POInfo=PO.objects.get(id=po_id) #querry for po information
                serializer = POSerializer(POInfo)
                logger.info(f"{user} PO details accessed!")
                return Response({"status":True,"data":serializer.data})
            else:
                logger.info(f"{user}- requested ID have no PO!")
                return Response({"status":False,"msg":"PO Unavailable!"})
        except : # Handles exceptions and provides an appropriate response in case of errors
            logger.exception(f"{request} Something Went wrong!") #log history  
            return Response({"status": False, "msg": "Something went wrong!"}, status.HTTP_404_NOT_FOUND)
        
    def delete(self,request,po_id):
        try:
            user=request.user
            if not user.is_superuser: # Checks if the user is a superuser for authorization
                logger.info(f" {user} unauthorized access!")
                return Response({"status": False, "msg": "unauthorized access!"}, status=status.HTTP_403_FORBIDDEN)
            if PO.objects.filter(id=po_id).exists():
                POInfo=PO.objects.get(id=po_id)
                POInfo.delete() #removing po through id
                
                logger.info(f"{user}- {po_id} PO deleted Successfully!")
                return Response({"status":True,"msg":"PO deleted Successfully!"})
            else:
                logger.info(f"{user}- requested ID have no PO!")
                return Response({"status":False,"msg":"Vendor Unavailable!"})
        except : # Handles exceptions and provides an appropriate response in case of errors
            logger.exception(f"{request} Something Went wrong!") #log history  
            return Response({"status": False, "msg": "Something went wrong!"}, status.HTTP_404_NOT_FOUND)
        
    def put(self,request,po_id):
        try:
            user=request.user
            if not user.is_superuser: # Checks if the user is a superuser for authorization
                logger.info(f" {user} unauthorized access!")
                return Response({"status": False, "msg": "unauthorized access!"}, status=status.HTTP_403_FORBIDDEN)
            
            if PO.objects.filter(id=po_id).exists(): #checking po existance
                POInfo=PO.objects.get(id=po_id)
                POInfo.vendor=request.data.get("vendor")
                POInfo.order_date=request.data.get("order_date")
                POInfo.delivery_date=request.data.get("delivery_date")
                POInfo.items=request.data.get("items")
                POInfo.quantity=request.data.get("quantity")
                POInfo.save() #updating po

                logger.info(f"{user}-PO Updated Successfully!")
                return Response({"status":True,"msg":"PO Updated Successfully!"})
            else:
                logger.info(f"{user}- {po_id} requested ID have no PO!")
                return Response({"status":False,"msg":"PO Unavailable!"})
        except : # Handles exceptions and provides an appropriate response in case of errors
            logger.exception(f"{request} Something Went wrong!") #log history  
            return Response({"status": False, "msg": "Something went wrong!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class POAcknowledgeDateUpdate(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self,request,po_id):
        try:
            user=request.user
            if not user.is_superuser: # Checks if the user is a superuser for authorization
                logger.info(f" {user} unauthorized access!")
                return Response({"status": False, "msg": "unauthorized access!"}, status=status.HTTP_403_FORBIDDEN)
            
            # Data Validation 
            if PO.objects.filter(id=po_id).count() == 0:
                logger.info(f"{user}-{po_id} Invalid PO!")
                return Response({"status": True, "msg": "Invalid PO!"})

            po = PO.objects.get(id=po_id)
            po.acknowledgment_date=timezone.now()
            po.save()
            # Calculate and update average response time
            completed_pos_with_acknowledgment = PO.objects.filter(
                vendor_id=po.vendor_id,
                acknowledgment_date__isnull=False
            )
            
            #calculation of response time
            response_times=[(order.acknowledgment_date - order.issue_date).total_seconds() for order in completed_pos_with_acknowledgment]
            # print(response_times)
            avg_response_time = sum(response_times) / len(response_times) if len(response_times) > 0 else 0.0
            
            #saving avg response time in vendor table
            vendor = Vendors.objects.get(id=po.vendor_id)
            vendor.average_response_time = avg_response_time
            vendor.save()

            logger.info(f"{user}- {po.po_number} acknowledged successfully!")
            return Response({"status":True,"msg":f"PO acknowledged successfully!"})
        
        except : # Handles exceptions and provides an appropriate response in case of errors
            logger.exception(f"{request} Something Went wrong!") #log history  
            return Response({"status": False, "msg": "Something went wrong!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class POStatusOperation(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request, po_id):
        try:
            user=request.user 
            if not user.is_superuser: # Checks if the user is a superuser for authorization
                logger.info(f" {user} unauthorized access!")
                return Response({"status": False, "msg": "unauthorized access!"}, status=status.HTTP_403_FORBIDDEN)
            

            #PO status 
            status = request.data.get("status") #pending, completed, canceled
            rating=request.data.get("rate") #rating PO 

            # Data Validation Tags
            if PO.objects.filter(id=po_id).count() == 0:
                logger.info(f"{user}-{po_id} Invalid PO!")
                return Response({"status": True, "msg": "Invalid PO!"})

            po = PO.objects.get(id=po_id)

            if po.status == "completed":
                logger.info(f"{user}-{po.po_number} already completed!")
                return Response({"status": True, "msg": "PO already completed!"})

            # Updates the status and quality rating of a PO
            po.status = status
            po.quality_rating=rating
            po.save()

            # Calculate and update on-time delivery rate
            total_completed_pos = PO.objects.filter(
                vendor=po.vendor_id,
                status='completed'
            ).count()
            
            total_vendor_pos = PO.objects.filter(
                vendor=po.vendor_id,
            ).count()

            if total_completed_pos == 0:
                logger.info(f"{user}- No completed POs for the vendor!")
                return Response({"status": True, "msg": "No completed POs for the vendor."})

            completed_pos_on_time = PO.objects.filter(
                vendor_id=po.vendor_id,
                status='completed',
                delivery_date__lte=timezone.now(),
            ).count()

            on_time_completion_percentage = 100 - ((completed_pos_on_time / total_completed_pos) * 100)

            # Calculate and update average quality rating
            completed_pos_with_rating = PO.objects.filter(
                vendor_id=po.vendor_id,
                status='completed',
                quality_rating__isnull=False
            )
            quality_rating_avg = completed_pos_with_rating.aggregate(Avg('quality_rating'))['quality_rating__avg'] or 0.0
            
            # Calculate and update fulfillment rate
            fulfilled_pos = PO.objects.filter(
                vendor_id=po.vendor_id,
                status='completed',
                issue_date__isnull=False
            )
            fulfillment_rate = (fulfilled_pos.count() / total_vendor_pos) * 100 if total_vendor_pos > 0 else 0

            #save to Historic Vendors Table
            vendor = Vendors.objects.get(id=po.vendor_id)
            vendor.on_time_delivery_rate = on_time_completion_percentage
            vendor.quality_rating_avg = quality_rating_avg
            vendor.fulfillment_rate=fulfillment_rate
            vendor.save()

            # save to Historic Vendor performance tbale
            performance = Historic_Performance(
                    vendor=vendor,
                    date=timezone.now(),
                    on_time_delivery_rate=on_time_completion_percentage,
                    quality_rating_avg=quality_rating_avg,
                    average_response_time=vendor.average_response_time,
                    fulfillment_rate=fulfillment_rate
                )
            performance.save()
            logger.info(f"{user}-{po_id} {status} ")
            return Response({"status": True, "msg": f"PO  {status}!"})

        except : # Handles exceptions and provides an appropriate response in case of errors
            logger.exception(f"{request} Something Went wrong!") #log history  
            return Response({"status":False,"msg":"something went wrong!"})

class VendorPerformanceEvaluation(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self,request,vendor_id):
        try:
            user=request.user
            if not user.is_superuser: # Checks if the user is a superuser for authorization
                logger.info(f" {user} unauthorized access!")
                return Response({"status": False, "msg": "unauthorized access!"}, status=status.HTTP_403_FORBIDDEN)
            vendor=Vendors.objects.get(id=vendor_id)
            serializer=VendorPerformanceSerializer(vendor)

            logger.info(f"{user}-{vendor.name} data accessed!")
            return Response({"status":True,"data":serializer.data})
        except : # Handles exceptions and provides an appropriate response in case of errors
            logger.exception(f"{request} Something Went wrong!") #log history  
            return Response({"status": False, "msg": "Something went wrong!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

