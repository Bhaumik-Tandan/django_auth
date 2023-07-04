from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from .models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver
from .serializers import UserSerializer
from .models import generate_access_code
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User


from rest_framework.renderers import JSONRenderer



# api to get all users
@api_view(['GET'])
def get_users(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def calculate_incentive(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found.'}, status=404)

    incentive = calculate_incentive_recursive(user)
    return Response({'incentive': incentive})


def calculate_incentive_recursive(user):
    children = User.objects.filter(parent=user.id)
    if not children:
        return 0
    
    incentive = 0
    for child in children:
        incentive += calculate_incentive_recursive(child)/2+0.01*float(child.payment)
    
    return incentive
    




@receiver(pre_save, sender=User)
def generate_referral_code(sender, instance, **kwargs):
    if not instance.referral_code:
        instance.referral_code = generate_access_code()

@api_view(['POST'])
def signup(request):
    parent_referral_code=request.data.get('referral')
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        if parent_referral_code:
            try:
                parent_user = User.objects.get(referral_code=parent_referral_code)
                serializer.validated_data['parent'] = parent_user
            except User.DoesNotExist:
                pass  # No parent user found, proceed without attaching the parent ID
        
        user = serializer.save()
        referral_code = user.referral_code
        return Response({'message': 'User registered successfully.', 'referral_code': referral_code}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return Response({'message': 'Login successful.'}, status=status.HTTP_200_OK)
    return Response({'message': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)
