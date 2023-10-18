from rest_framework import serializers
from django.contrib.auth.models import User
#mapping des models json à partir des api 
class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = ['id', 'username', 'password', 'email']
