from rest_framework import serializers

from .models import CreateUserModel


class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreateUserModel
        fields = ('email', 'user_name', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class UpdateInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreateUserModel
        fields = ('id','user_name', 'first_name', 'about','image')

    # def update(self,instance, validated_data):
    #     instance.user_name = validated_data.get('user_name', instance.user_name)
    #     try:
    #         False
    #     except CreateUserModel.DoesNotExist:
    #         instance.save()
    #     return instance



