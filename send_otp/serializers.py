from rest_framework import serializers
from .models import PostModel


class OtpSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=13, min_length=11, required=True)

    def validate_phone_number(self, value):
        if not value.isnumeric() and len(value) != 11 and not value.startswith('09'):
            raise serializers.ValidationError("Invalid phone number")
        return value


class VerifySerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=13, min_length=11, required=True)
    otp = serializers.CharField(max_length=6, required=True)

    def validate_phone_number(self, value):
        if not value.isnumeric() and len(value) != 11 and not value.startswith('09'):
            raise serializers.ValidationError("Invalid phone number")
        return value

    def validate_otp(self, value):
        if not str(value).isnumeric() and len(str(value)) != 6:
            raise serializers.ValidationError('Invalid OTP code')
        return value


class PostSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=225)
    text = serializers.CharField(max_length=250)
    owner_name = serializers.SerializerMethodField()
    class Meta:
        model = PostModel
        fields = ['title', 'text', 'owner', 'owner_name', 'created', 'modifiled', 'is_deleted', 'slug']
        read_only_fields = ['owner', 'slug', 'created', 'modified', 'owner_name']



    def get_owner_name(self, obj):
        return obj.owner.username


    """ this is for when have slug repetitious"""
    def create(self,validated_data):
        if PostModel.objects.filter(title=validated_data['title']).exists():
            raise serializers.ValidationError("This title was existed")
        return PostModel.objects.create(**validated_data)


