from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import permissions, status, generics
from rest_framework.response import Response
from .serializers import UserCreateSerializer, UserSerializer, ViewPasswordSerializer
from .models import saved_password, secureKeys
from django.contrib.auth.hashers import make_password
from cryptography.fernet import Fernet
import string
import secrets
import base64
import rsa

class RegisterView(APIView):
    def post(self, request):
        data = request.data
        user_serializer = UserCreateSerializer(data=data)
        if not user_serializer.is_valid():
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        user = user_serializer.create(user_serializer.validated_data)
        user.is_active = True
        user.save()
        serializer = UserSerializer(user)
        user = serializer.data
        # getting tokens
        return Response(user, status=status.HTTP_201_CREATED)
    

class RetrieveUserView(APIView):    
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        user = UserSerializer(user)
        return Response(user.data, status=status.HTTP_200_OK)
    

def generate_key():
    # Generate a Fernet key
    key = Fernet.generate_key()
    return key


def encrypt_string(string_to_encrypt, key):
    cipher_suite = Fernet(key)
    encrypted_text = cipher_suite.encrypt(string_to_encrypt.encode())
    return encrypted_text


def decrypt_string(encrypted_text, key):
    try:
        cipher_suite = Fernet(key)
        decrypted_text = cipher_suite.decrypt(encrypted_text).decode()
        return decrypted_text
    except Exception as e:
        print(f"Decryption error: {e}")
        return None
    

class SavePassword(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        data = request.data
        user = request.user
        account_type = data.get('account_type')
        password = data.get('password')
        
        if secureKeys.objects.filter(user=user).exists():
            user_key = secureKeys.objects.get(user=user)
            key = user_key.s_key
        else:
            s_key = generate_key()
            uk = secureKeys(user=user, s_key=s_key)
            uk.save()
            key = uk.s_key
        hashed_password = encrypt_string(password, key)
        if hashed_password:
            sp = saved_password(user=user, account_type=account_type, password=hashed_password)
            sp.save()  
            return Response({"message": "Password saved"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "Error encrypting password"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    


class ViewSavedPassword(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        password_list = saved_password.objects.filter(user=user)
        decrypted_passwords = []
        if secureKeys.objects.filter(user=user).exists():
            user_key = secureKeys.objects.get(user=user)
            key = user_key.s_key

        for password in password_list:
            decrypted_password = decrypt_string(password.password, key)
            decrypted_data = {
                'id': password.id,
                'account_type': password.account_type,
                'password': decrypted_password
            }
            decrypted_passwords.append(decrypted_data)

        return Response({"passwords": decrypted_passwords}, status=status.HTTP_200_OK)
        


class DeleteSavedPassword(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def delete(self, request, id):
        try:
            sp = saved_password.objects.get(id=id)
            sp.delete()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_304_NOT_MODIFIED)


