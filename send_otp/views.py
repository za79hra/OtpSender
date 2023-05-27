from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404



from django.contrib.auth.models import User
from .serializers import OtpSerializer, VerifySerializer,PostSerializer
from redis import Redis
from .models import PostModel
from .permissions import IsOwnerOrReadOnly
from . import tasks
from .tasks import send_sms, random_otp




redis_connection = Redis(host='localhost', port=6002, db=0, charset='utf-8', decode_responses=True)


class LoginOtpView(APIView):
    def post(self, request, *args, **kwgrgs):
        serializer_data = OtpSerializer(data=request.data)
        serializer_data.is_valid(raise_exception=True)
        phone_number = serializer_data.validated_data.get('phone_number')
        otp = random_otp
        redis_connection.set(phone_number, random_otp, ex=120)
        tasks.send_sms(phone_number)
          
        return Response({'message':f"{otp}"}, status=status.HTTP_200_OK)
        
  


class VerifyOtp(APIView):
    def post(self, request, *args, **kwgrgs):
        serializer = VerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data.get('phone_number')
        otp_code = serializer.validated_data.get('otp')
        expected_otp = redis_connection.get(phone_number)
        
        print(otp_code)
        print(expected_otp)

        if otp_code ==  expected_otp:
            
            user, created =User.objects.get_or_create(username=phone_number)
    

            refresh_token = RefreshToken().for_user(user)
            access_token = refresh_token.access_token
            
            data={
                'access_token': str(access_token),
                'refresh_token': str(refresh_token)
                }
            return Response(data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class UserAuth(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):

        return Response({'message': 'welcome to home :)<-< ' },status=status.HTTP_200_OK)
    
    


class UserCreateView(APIView):
    permission_classes = [IsOwnerOrReadOnly]

    def post(self,request, *args, **kwargs):
        serializer = PostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        serializer.save(owner=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)



class UserGetView(APIView):
    permission_classes = [IsOwnerOrReadOnly]
    
    def get(self, request, *args, **kwargs):
        owner = PostModel.objects.all()
        serializer = PostSerializer(instance=owner, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserUpdateView(APIView):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
     
    def put(self, request, slug, *args, **kwargs):
        
        owner = PostModel.objects.get(slug=slug)
        self.check_object_permissions(request, owner)


        serializer = PostSerializer(instance=owner, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
        
        

class UserdeleteView(APIView):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    

    def delete(self,request, slug, *args, **kwargs):
        owner = get_object_or_404(PostModel, slug=slug)
        self.check_object_permissions(request, owner)
        owner.delete()
        return Response({'message': 'deleted'}, status=status.HTTP_204_NO_CONTENT)

        

    

