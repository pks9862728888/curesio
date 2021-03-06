from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

from django_countries.serializer_fields import CountryField
from django_countries.serializers import CountryFieldMixin

from core.models import UserProfile


class ProfileSerializer(CountryFieldMixin, serializers.ModelSerializer):
    """Serializer for user profile"""
    country = CountryField()

    class Meta:
        model = UserProfile
        fields = ('first_name', 'last_name', 'phone',
                  'date_of_birth', 'city', 'country',
                  'postal_code', 'address', 'image',
                  'primary_language', 'secondary_language',
                  'tertiary_language')
        read_only_fields = ('image', )


class CreateUserSerializer(serializers.ModelSerializer):
    """Serializer for creating user"""
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password', 'placeholder': 'Password'},
        min_length=8
    )

    class Meta:
        model = get_user_model()
        fields = (
            'email', 'password', 'username',
            'is_active', 'is_doctor', 'is_staff'
        )
        read_only_fields = ('is_active', 'is_doctor', 'is_staff')

    def create(self, validated_data):
        """Create a new user with encrypted password and return it."""
        validated_data.pop('profile', None)
        return get_user_model().objects.create_user(**validated_data)


class ManageUserSerializer(serializers.ModelSerializer):
    """Serializer for editing users details and profile details"""
    profile = ProfileSerializer(required=False)

    class Meta:
        model = get_user_model()
        fields = (
            'id', 'email',
            'username', 'created_date', 'profile'
        )
        read_only_fields = ('id', 'email', 'created_date', )

    def update(self, instance, validated_data):
        """Add or modify details of user"""
        validated_data.pop('password', None)
        user_profile_data = validated_data.pop('profile', None)
        validated_data.pop('doctor_profile', None)
        validated_data.pop('email', None)
        profile = instance.profile

        user = super().update(instance, validated_data)
        user.save()

        # Updating profile data is profile data is present
        if user_profile_data:
            profile.first_name = user_profile_data.get(
                'first_name', profile.first_name)
            profile.last_name = user_profile_data.get(
                'last_name', profile.last_name)
            profile.phone = user_profile_data.get(
                'phone', profile.phone)
            profile.date_of_birth = user_profile_data.get(
                'date_of_birth', profile.date_of_birth)
            profile.city = user_profile_data.get(
                'city', profile.city)
            profile.country = user_profile_data.get(
                'country', profile.country)
            profile.postal_code = user_profile_data.get(
                'postal_code', profile.postal_code)
            profile.address = user_profile_data.get(
                'address', profile.address)
            profile.primary_language = user_profile_data.get(
                'primary_language', profile.primary_language)
            profile.secondary_language = user_profile_data.get(
                'secondary_language', profile.secondary_language)
            profile.tertiary_language = user_profile_data.get(
                'tertiary_language', profile.tertiary_language)

            profile.save()

        return instance


class UserSerializerImageUpload(serializers.ModelSerializer):
    """Minimal serializer for supporting user image upload field"""

    class Meta:
        model = get_user_model()
        fields = ('username', )


class UserImageUploadSerializer(serializers.ModelSerializer):
    """Serializer for user image upload"""
    user = UserSerializerImageUpload(read_only=True)
    image = serializers.ImageField(allow_null=True, use_url=True)

    class Meta:
        model = UserProfile
        fields = ('id', 'user', 'image')
        read_only_fields = ('id', 'user')


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for user authentication object"""
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """Validate and authenticate user"""
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            email=email,
            password=password
        )

        if not user:
            msg = _('Unable to authenticate with provided credentials.')
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user
        return attrs
