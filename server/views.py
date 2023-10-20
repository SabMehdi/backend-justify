from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt

from django.core.exceptions import ObjectDoesNotExist


from .serializers import UserSerializer
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .models import WordCount

from rest_framework.views import APIView


@api_view(['POST'])
def login(request):
    user = get_object_or_404(User, email=request.data['email'])
    if not user.check_password(request.data['password']):
        return Response({"detail": "wrong password"}, status=status.HTTP_400_BAD_REQUEST)
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(instance=user)
    return Response({"token": token.key, "email": serializer.data['email'], "username": serializer.data['username']})


@api_view(['POST'])
def signup(request):
    email = request.data.get('email')  
    try:
        existing_user = User.objects.get(email=email)
        return Response({"error": "email already exist"}, status=status.HTTP_400_BAD_REQUEST)
    except ObjectDoesNotExist:
   
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = User.objects.get(username=request.data['username']) 
            user.set_password(request.data['password'])  
            user.save()
            token = Token.objects.create(user=user)
            return Response({"token": token.key, "email": serializer.data['email'], "username": serializer.data['username']})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    return Response("passed!")

class JustifyTextView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        #print(user.id)

        word_count, created = WordCount.objects.get_or_create(user=user)
        
        if word_count.count >= 80000:

            return Response({"detail": "payment required"}, status=status.HTTP_402_PAYMENT_REQUIRED)

        text = request.body.decode('utf-8')

        justified_text = justify_text(text) 
        print(len(text))
        word_count.count += len(justified_text)
        word_count.save()

        return Response({"justified_text": justified_text})

def justify_text(text):
    lines=""
    line=""
    #print("words: "+str(len(text.split())))
    for word in text.split():
        if(len(line)<=80):
            if((len(line)+len(word))<=80):
                line+=word
                if(len(line)<80):
                    line+=" "
            else:
                while(len(line)<80):
                    line+=" "
                lines+=line+"\\n"
                line=word+" "       
    lines+=line
    return lines