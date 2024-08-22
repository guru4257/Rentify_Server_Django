from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view,permission_classes
from api.serializer import ListingSerializer, UserSerializer
from api.models import Listing, User
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework.permissions import IsAuthenticated
from dotenv import load_dotenv  
from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env file
dotenv_path = BASE_DIR / '.env'
load_dotenv(dotenv_path=dotenv_path)

is_production = True if str(os.environ['is_production']) == '1' else False

# view function for listing all houses based on the filters
@api_view(['GET'])
def get_listings(request):
    
    
    try:
        # Extracting the query params from request
        limit = int(request.query_params.get('limit',9))
        start_index = int(request.query_params.get('startIndex',0))
        offer = request.query_params.get('offer',None)
        furnished = request.query_params.get('furnished',None)
        parking = request.query_params.get('parking',None)
        type = request.query_params.get('type',None)
        search_term = request.query_params.get('searchTerm','')
        sort = request.query_params.get('sort','createdAt')
        order = request.query_params.get('order','desc')
        
        # Applying filters based on the conditions
        offer_filter = Q(offer__in=[False,True]) if offer is None or offer == 'false' else Q(offer = offer.lower() == 'true')
        furnished_filter = Q(furnished__in=[False,True]) if furnished is None or furnished == 'false' else Q(furnished = furnished.lower() == 'true')
        parking_filter = Q(parking__in = [False,True]) if parking is None or parking == 'false' else Q(parking = parking.lower() == 'true')
        type_filter = Q(type__in=['rent','sale']) if type is None or type == 'all' else Q(type = type)
        search_filter = Q(name__icontains=search_term)
        
        sort = 'createdAt' if sort == 'created_at' else sort
        
        # ordering the sort order
        ordering = f'-{sort}' if order == 'desc' else sort
        
        # Querying from the DB ----> this Q and filter method will acceptable for sql databases which django ORM supports
        listings = Listing.objects.filter(
            offer_filter &
            furnished_filter &
            parking_filter &
            type_filter &
            search_filter
        ).order_by(ordering)[start_index:start_index+limit]
        
        serializer = ListingSerializer(listings, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    except Exception as e:
        print(f"Error during fetching Listings {e}")
        return Response({'success': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)   
    

# view function for creating Listing  of houses    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_listing(request):
    
    try:
           
        try:
            listingSerializer = ListingSerializer(data=request.data)
        except Exception as e:
            print(e)
            
        if listingSerializer.is_valid():
            
            listingSerializer.save()
            print(listingSerializer.data)
            return JsonResponse({"_id":listingSerializer.data['_id'],"success":True,"message":"Listing Created Successfully"},status=status.HTTP_200_OK)
        
        return JsonResponse({"success":False,"message":"Listing Creation Failed, Try Again"},status = status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(f"Error during Listing Creation {e}")
        return JsonResponse({'success':False,'message':'Internal Server Error'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

# view function for getting the particular Listing detail
@api_view(['GET'])
def get_listing(request,id):
    
    try:
        if id is not None:
            listing = get_object_or_404(Listing,id=id)
            serializer = ListingSerializer(listing)
            
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return JsonResponse({"success":False,"message":"check listing id, is not valid"},status=status.HTTP_406_NOT_ACCEPTABLE)
            
    except Exception as e:   
        print(f"Error during fetching Listing {e}")
        return JsonResponse({'success':False,'message':'Internal Server Error'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
   
# view function for getting the particular user detail 
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user(request,id):
    
    try:
        
        if id is not None:
            user = get_object_or_404(User, id=id)
            userSerializer = UserSerializer(user)
            
            return Response(userSerializer.data, status=status.HTTP_200_OK)
        else:
            return JsonResponse({"success":False,"message":"check User id, is not valid"},status=status.HTTP_406_NOT_ACCEPTABLE)
        
    except Exception as e:   
        print(f"Error during fetching user {e}")
        return JsonResponse({'success':False,'message':'Internal Server Error'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)    


# view function for getting the Listings for particular User
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_listings(request,id):
    
    try:
        if id is not None:
            
            listing = Listing.objects.filter(userRef = id)
            serializer = ListingSerializer(listing, many=True)
            
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return JsonResponse({"success":False,"message":"check user id, is not valid"},status=status.HTTP_406_NOT_ACCEPTABLE)
            
    except Exception as e:   
        print(f"Error during fetching Listing {e}")
        return JsonResponse({'success':False,'message':'Internal Server Error'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
#view function for updating the Listing
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_listing(request,id):
    
    try:
        
        try:
            listing = Listing.objects.get(pk=id)
        except Exception as e:
            print("Error during getting Listing from DB",e)
            return JsonResponse({"success":False,"message":"Listing is not found"},status=status.HTTP_404_NOT_FOUND)
        
        # allowing partial update for not expecting the all fields for update
        listingSerializer = ListingSerializer(listing,data=request.data,partial=True)
        
        if listingSerializer.is_valid():
            
            listingSerializer.save()
            return JsonResponse({"_id":listingSerializer.data['_id'],"success":True,"message":"Listing Updated Successfully"},status=status.HTTP_200_OK)
        
        return JsonResponse({"success":False,"message":"Invalid data"},status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:   
        print(f"Error during fetching Listing {e}")
        return JsonResponse({'success':False,'message':'Internal Server Error'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)    


# view function for delete listing
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_listing(request,id):
    
    try:
    
        try:
            
            listing = Listing.objects.get(pk=id)
        except User.DoesNotExist:
            print("Error during listing fetching from DB")
            return JsonResponse({"success":False,"message":"Listing doest not exit"}, status = status.HTTP_404_NOT_FOUND)
        
        listing.delete()
        
        return JsonResponse({"success":True,"message":"Listing Deleted Successfully"},status=status.HTTP_200_OK)
    
    except Exception as e:
        print(f"Error during User Login {e}")
        return JsonResponse({'success':False,'message':'Internal Server Error'},status=status.HTTP_500_INTERNAL_SERVER_ERROR) 