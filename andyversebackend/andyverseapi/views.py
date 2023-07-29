import datetime
import secrets
from rest_framework import viewsets
from rest_framework.decorators import action, throttle_classes
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from andyverseapi.models import AndyVerseUser, MovieReview, Message
from andyverseapi.serializers import AndyVerseUserSerializer, MovieReviewSerializer, MessageSerializer

from firebase_admin import auth

from andyverseapi.firebaseauth import isAdmin

# Create your views here.

unauthorizedResponse = Response({'error': 'Unauthorized access'}, status=status.HTTP_401_UNAUTHORIZED)
invalidResponse = Response({'error': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)

class AndyVerseUserViewSet(viewsets.GenericViewSet):
    queryset = AndyVerseUser.objects.all().order_by('created')
    serializer_class = AndyVerseUserSerializer

    #   actions authenticated by firebase_id_token
    #   to check if user has permission is_staff

    def list(self, request):
        firebase_id_token = request.query_params.get('firebase_id_token')
        if isAdmin(firebase_id_token):
            serializer = self.get_serializer(self.queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return unauthorizedResponse
        
    #accepts arguments email and username to create a default user
    @action(detail=False, methods=['post'], url_path='create_dual_user')
    def create_dual_user(self, request):
        firebase_id_token = request.query_params.get('firebase_id_token')
        email = request.data.get('email')
        username = request.data.get('username')
        
        if email is None or firebase_id_token is None or username is None:
            return invalidResponse
        if isAdmin(firebase_id_token):
            try:
                random_password = secrets.token_urlsafe(16)
                new_firebase_user = auth.create_user(email=email, password=random_password)
                new_andy_user = {
                    'uid': new_firebase_user.uid,
                    'username': username,
                    'email': email,
                    'created': datetime.now(),
                    'profile_img': '',
                    'is_staff': False,
                }
                serializer = self.get_serializer(data=new_andy_user)
                if not serializer.is_valid():
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                serializer.save()    
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except auth.EmailAlreadyExistsError:
                return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)
            except:
                return invalidResponse
        else:
            return unauthorizedResponse
            
    #   update any user if admin, update self if not admin
    @action(detail=False, methods=['put', 'patch'], url_path='update_by_uid')
    def update_by_uid(self, request):
        uid = request.query_params.get('uid')
        firebase_id_token = request.query_params.get('firebase_id_token')
        
        if uid is None or firebase_id_token is None:
            return invalidResponse
        user = AndyVerseUser.objects.get(uid=uid)
        decoded_token = auth.verify_id_token(firebase_id_token)
        decoded_uid = decoded_token['uid']
        try:
            if isAdmin(firebase_id_token):
                serializer = self.get_serializer(user, data=request.data, partial=True)
                if not serializer.is_valid():
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                serializer.save()    
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                if decoded_uid != uid or decoded_uid is None:
                    return unauthorizedResponse
                
                # only allow non admin user to edit their username and profile_img
                user_data = request.data.copy()
                user_data.pop('is_staff', None)
                user_data.pop('uid', None)
                user_data.pop('created', None)
                user_data.pop('email', None)
                
                serializer = self.get_serializer(user, data=user_data, partial=True)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                
                return Response(serializer.data, status=status.HTTP_200_OK)
        except AndyVerseUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except auth.InvalidIdTokenError:
            return Response({'error': 'Invalid Firebase ID token'}, status=status.HTTP_401_UNAUTHORIZED)

    #raw creation of a database user    
    def create(self, request):
        firebase_id_token = request.query_params.get('firebase_id_token')
        if isAdmin(firebase_id_token):
            serializer = self.get_serializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()    
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return unauthorizedResponse
        
    #delete user by uid
    @action(detail=False, methods=['delete'], url_path='delete_by_uid')
    def delete_by_uid(self, request):
        uid = request.query_params.get('uid')
        firebase_id_token = request.query_params.get('firebase_id_token')
        
        if uid is None or firebase_id_token is None:
            return invalidResponse
        users = self.queryset.filter(uid=uid)
        if users.exists():
            if isAdmin(firebase_id_token):
                users.delete()
                auth.delete_user(uid=uid)
                return Response({'message': 'Successfully deleted.'}, status=status.HTTP_204_NO_CONTENT)
            else:
                return unauthorizedResponse
        else:
            return Response({'error': 'Review not found.'}, status=status.HTTP_404_NOT_FOUND)
        
    
    @action(detail=False, methods=['get'], url_path='retrieve_from_uid')
    def retrieve_from_uid(self, request):
        #query params
        uid = request.query_params.get('uid')
        firebase_id_token = request.query_params.get('firebase_id_token')
        
        if uid is None or firebase_id_token is None:
            return invalidResponse
        
        try:
            user = AndyVerseUser.objects.get(uid=uid)
            user_data = self.get_serializer(user).data
            decoded_token = auth.verify_id_token(firebase_id_token)
            decoded_uid = decoded_token['uid']
            
            if not isAdmin(firebase_id_token):
                if decoded_uid != uid or decoded_uid is None:
                    return unauthorizedResponse
            return Response(user_data, status=status.HTTP_200_OK)
        except AndyVerseUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except auth.InvalidIdTokenError:
            return Response({'error': 'Invalid Firebase ID token'}, status=status.HTTP_401_UNAUTHORIZED)
        
    

class MovieReviewViewSet(viewsets.GenericViewSet):
    queryset = MovieReview.objects.all().order_by('date_time_reviewed')
    serializer_class = MovieReviewSerializer
    
    #list all reviews for admins
    def list(self, request):
        firebase_id_token = request.query_params.get('firebase_id_token')
        
        if isAdmin(firebase_id_token):
            serializer = self.get_serializer(MovieReview.objects.all().order_by('date_time_reviewed'), many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return unauthorizedResponse
        
    #update review using its movie_id
    @action(detail=False, methods=['put', 'patch'], url_path='update_by_movie_id')
    def update_by_movie_id(self, request):
        movie_id = request.query_params.get('movie_id')
        firebase_id_token = request.query_params.get('firebase_id_token')
        
        if movie_id is None or firebase_id_token is None:
            return invalidResponse
        
        try:
            review = self.queryset.get(movie_id=movie_id)
            
            if isAdmin(firebase_id_token):
                serializer = self.get_serializer(review, data=request.data, partial=True)
                if not serializer.is_valid():
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                serializer.save()    
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return unauthorizedResponse
        except MovieReview.DoesNotExist:
            return Response({'error': 'Review not found'}, status=status.HTTP_404_NOT_FOUND)
        
        
    #allow anyone to retrieve by id, private reviews reserved for admins
    @action(detail=False, methods=['get'], url_path='retrieve_by_movie_id')
    def retrieve_by_movie_id(self, request):
        movie_id = request.query_params.get('movie_id')
        firebase_id_token = request.query_params.get('firebase_id_token')
        
        if movie_id is None:
            return Response({'error': 'Please specify a review by movie_id'})
        
        reviews = self.queryset.filter(movie_id=movie_id)
        if reviews.exists():
            if isAdmin(firebase_id_token):
                review_data = self.get_serializer(reviews, many=True).data
            else:
                public_reviews = reviews.filter(public=True)
                if public_reviews.exists():
                    review_data = self.get_serializer(public_reviews, many=True).data
                    return Response(review_data, status=status.HTTP_200_OK)
                else:
                    return Response({'error' : 'No public reviews.'})
        else:
            return Response({'error': 'Review not found.'}, status=status.HTTP_404_NOT_FOUND)
        
    #allow admins to create reviews    
    def create(self, request):
        firebase_id_token = request.query_params.get('firebase_id_token')
        if isAdmin(firebase_id_token):
            serializer = self.get_serializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()    
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return unauthorizedResponse
        
    #list all reviews where public=True         
    @action(detail=False, methods=['get'], url_path='public_reviews')
    def public_reviews(self, request):
        public_reviews = MovieReview.objects.all().order_by('date_time_reviewed').filter(public=True)
        serializer = self.get_serializer(public_reviews, many=True)
        if public_reviews.none():
            return Response({'error': 'No available reviews'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(serializer.data, status=status.HTTP_200_OK)
        
    #delete review by movie_id
    @action(detail=False, methods=['delete'], url_path='delete_by_movie_id')
    def delete_by_movie_id(self, request):
        movie_id = request.query_params.get('movie_id')
        firebase_id_token = request.query_params.get('firebase_id_token')
        
        reviews = self.queryset.filter(movie_id=movie_id)
        if reviews.exists():
            if isAdmin(firebase_id_token):
                reviews.delete()
                return Response({'message': 'Successfully deleted.'}, status=status.HTTP_204_NO_CONTENT)
            else:
                return unauthorizedResponse
        else:
            return Response({'error': 'Review not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        

        
class MessageViewSet(viewsets.GenericViewSet):
    queryset = Message.objects.all().order_by('date_sent')
    serializer_class = MessageSerializer
    
    def list(self, request):
        firebase_id_token = request.query_params.get('firebase_id_token')
        if firebase_id_token is None:
            return invalidResponse
        if isAdmin(firebase_id_token):
            serializer = self.get_serializer(Message.objects.all().order_by('date_sent'), many=True)
            data = serializer.data
            for item in data:
                item['id'] = str(item['id'])
            return Response(data, status=status.HTTP_200_OK)
        else:
            return unauthorizedResponse
    
    #allow anyone to create a message for contact page and movie suggestions
    #CBA throttling
    def create(self, request):
        ip_address = request.META.get('REMOTE_ADDR')
        data = request.data.copy()
        data['ip_address'] = ip_address
        
        serializer = self.get_serializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()    
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    #read message
    def retrieve(self, request, pk=None):
        firebase_id_token = request.query_params.get('firebase_id_token')
        if firebase_id_token is None:
            return invalidResponse
        if isAdmin(firebase_id_token):
            message = get_object_or_404(self.queryset, pk=pk)
            serializer = MessageSerializer(message)
            return Response(serializer.data)
        else:
            return unauthorizedResponse
    
    #delete message
    def destroy(self, request, pk=None):
        firebase_id_token = request.query_params.get('firebase_id_token')
        if firebase_id_token is None:
            return invalidResponse
        if isAdmin(firebase_id_token):
            message = get_object_or_404(self.queryset, pk=pk)
            message.delete()
            return Response({'message': 'Successfully deleted.'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return unauthorizedResponse
        
    #delete multiple messages
    @action(detail=False, methods=['post'], url_path='delete_messages')
    def delete_messages(self, request):
        firebase_id_token = request.query_params.get('firebase_id_token')
        if firebase_id_token is None:
            return invalidResponse
        if isAdmin(firebase_id_token):
            data = request.data
            message_ids = data.get('ids', [])
            print(message_ids)
            for message_id in message_ids:
                tempMessage = get_object_or_404(self.queryset, pk=message_id)
                tempMessage.delete()
            amount_deleted = len(message_ids)
            return Response({'message': f'Successfully deleted {amount_deleted} messages.'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return unauthorizedResponse
    
    #mark message as read
    @action(detail=True, methods=['patch'], url_path='mark_read')
    def mark_read(self, request, pk=None):
        firebase_id_token = request.query_params.get('firebase_id_token')
        if firebase_id_token is None:
            return invalidResponse
        try:
            message = get_object_or_404(Message, pk=pk)
            if isAdmin(firebase_id_token):
                serializer = self.get_serializer(message, data={'status': 'read'}, partial=True)
                if not serializer.is_valid():
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                serializer.save()    
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return unauthorizedResponse
        except Message.DoesNotExist:
            return Response({'error': 'Message not found'}, status=status.HTTP_404_NOT_FOUND)