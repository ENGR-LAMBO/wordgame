from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers

class CustomRegisterSerializer(RegisterSerializer):
    email = serializers.EmailField(required=True)

    def get_cleaned_data(self):
        data_dict = super().get_cleaned_data()
        data_dict['email'] = self.validated_data.get('email', '')
        return data_dict
