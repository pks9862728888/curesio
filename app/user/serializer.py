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
                  'postal_code', 'address', 'primary_language',
                  'secondary_language', 'tertiary_language')


class CreateUserSerializer(serializers.ModelSerializer):
    """Serializer for users object"""
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password', 'placeholder': 'Password'},
        min_length=8
    )

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'username')

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        validated_data.pop('profile', None)
        return get_user_model().objects.create_user(**validated_data)


class ManageUserSerializer(serializers.ModelSerializer):
    """Serializer for users object"""
    profile = ProfileSerializer(required=False)
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password', 'placeholder': 'Password'},
        min_length=8
    )

    class Meta:
        model = get_user_model()
        fields = (
            'id', 'email', 'password',
            'username', 'created_date', 'profile'
        )
        read_only_fields = ('id', 'created_date', )

    def update(self, instance, validated_data):
        """Add or modify details of user"""
        password = validated_data.pop('password', None)
        profile_data = validated_data.pop('profile', None)
        profile = instance.profile

        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        # Updating profile data is profile data is present
        if profile_data:
            profile.first_name = profile_data.get(
                'first_name', profile.first_name)
            profile.last_name = profile_data.get(
                'last_name', profile.last_name)
            profile.phone = profile_data.get(
                'phone', profile.phone)
            profile.date_of_birth = profile_data.get(
                'date_of_birth', profile.date_of_birth)
            profile.city = profile_data.get(
                'city', profile.city)
            profile.country = profile_data.get(
                'country', profile.country)
            profile.postal_code = profile_data.get(
                'postal_code', profile.postal_code)
            profile.address = profile_data.get(
                'address', profile.address)
            profile.primary_language = profile_data.get(
                'primary_language', profile.primary_language)
            profile.secondary_language = profile_data.get(
                'secondary_language', profile.secondary_language)
            profile.tertiary_language = profile_data.get(
                'tertiary_language', profile.tertiary_language)

            profile.save()

        return instance


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
