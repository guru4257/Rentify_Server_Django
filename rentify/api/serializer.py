from rest_framework import serializers
from api.models import User, Listing
import json

# serializer for user model
class UserSerializer(serializers.ModelSerializer):
    
    # here mentioning this for while fetching to client side the firstname and lastname should like below
    firstname = serializers.CharField(source='first_name')
    lastname = serializers.CharField(source='last_name')
    _id = serializers.SerializerMethodField()
    username = serializers.CharField(required=False)
    
    class Meta:
        model = User
        fields = ["_id","username","firstname","password","lastname","phoneNumber","email","avatar"]
        extra_kwargs = {
            
            'password':{'write_only':True},
            
        }
        
    def create(self, validated_data):
        
        password = validated_data.pop('password', None)

        try:
            user = User.objects.create_user(
                username=f"{validated_data['first_name']}_{validated_data['last_name']}",
                first_name = validated_data['first_name'],
                last_name = validated_data['last_name'],
                phoneNumber = validated_data['phoneNumber'],
                email = validated_data['email'],
                avatar = validated_data.get('avatar',"https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png")
            )
            
            if password:
                user.set_password(password)
                user.save()
                   
            return user
        
        except Exception as e:
            print(f"Error during User Creation {e}")
            raise
    
    def update(self, instance, validated_data):
        
        try:
            username = validated_data['username']
            if 'first_name' in validated_data and 'last_name' in validated_data:
                username = f"{validated_data['first_name']}_{validated_data['last_name']}"
                
            instance.username = username
            instance.first_name = validated_data.get('first_name',instance.first_name)
            instance.last_name = validated_data.get('last_name',instance.last_name)
            instance.phoneNumber = validated_data.get('phoneNumber',instance.phoneNumber)
            instance.email = validated_data.get('email',instance.email)
            instance.avatar = validated_data.get('avatar',instance.avatar) 
            
            if 'password' in validated_data:
                
                instance.set_password(validated_data['password'])
            
            instance.save()
            
            return instance
        except Exception as e:
            print(f"Error during User update {e}")
            raise
        
    def get__id(self,obj):
        return str(obj.id)        

# serializer for Listing Model
class ListingSerializer(serializers.ModelSerializer):
    
    imageUrls = serializers.ListField(
        child=serializers.URLField(), 
        write_only=True
    )
    _id = serializers.SerializerMethodField()
    
    class Meta:
        model = Listing
        fields = ['_id','name','description','address','regularPrice','discountPrice','bathrooms','bedrooms','furnished','parking','type','offer','imageUrls','createdAt','userRef']
    
    def create(self, validated_data):
        imageUrls = validated_data.pop('imageUrls', [])
        listing = Listing.objects.create(**validated_data)
        listing.imageUrls = json.dumps(imageUrls)
        listing.save()
        return listing
    
    def update(self, instance, validated_data):
        imageUrls = validated_data.pop('imageUrls', instance.get_imageUrls())
        instance.name = validated_data.get('name',instance.name)
        instance.description = validated_data.get('description',instance.description)
        instance.address =  validated_data.get('address',instance.address)
        instance.regularPrice = validated_data.get('regularPrice',instance.regularPrice)
        instance.discountPrice = validated_data.get('discountPrice',instance.discountPrice)
        instance.bathrooms = validated_data.get('bathrooms',instance.bathrooms)
        instance.bedrooms = validated_data.get('bedrooms',instance.bedrooms)
        instance.furnished = validated_data.get('furnished',instance.furnished)
        instance.parking = validated_data.get('parking',instance.parking)
        instance.type = validated_data.get('type',instance.type) 
        instance.offer = validated_data.get('offer',instance.offer)
        instance.imageUrls = json.dumps(imageUrls)
        
        instance.save()
        
        return instance
    
    def get__id(self,obj):
        return str(obj.id)
    
    def to_representation(self, instance):
        """Override the default to_representation method to convert JSON string back to list for output. while providing the data to the API"""
        representation = super().to_representation(instance)
        representation['imageUrls'] = instance.get_imageUrls()  # Convert the JSON string back to a list for output
        return representation

    def get_imageUrls(self,obj):

        return obj.get_imageUrls()
        