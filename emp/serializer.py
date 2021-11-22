from rest_framework.serializers import ModelSerializer
from .models import Enquiry, User

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'usertype']


class EnquirySerializer(ModelSerializer):

    claimed_by = UserSerializer(required=False)

    class Meta:
        model = Enquiry
        #fields = '__all__'
        exclude = ['public']
        depth = 1