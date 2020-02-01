from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

from django_countries.serializer_fields import CountryField
from django_countries.serializers import CountryFieldMixin

from core.models import UserProfile, Doctor, Languages, Speciality


class ProfileSerializer(CountryFieldMixin, serializers.ModelSerializer):
    """Serializer for user profile"""
    country = CountryField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    city = serializers.CharField(required=True)
    primary_language = serializers.ChoiceField(
        choices=Languages.LANGUAGE_IN_LANGUAGE_CHOICES,
        required=True
    )

    class Meta:
        model = UserProfile
        fields = ('first_name', 'last_name', 'phone',
                  'date_of_birth', 'city', 'country',
                  'postal_code', 'address', 'image',
                  'primary_language', 'secondary_language',
                  'tertiary_language')
        read_only_fields = ('image', )
        extra_kwargs = {
            'primary_language': {'required': True}
        }


class SpecialitySerializer(serializers.ModelSerializer):
    """Serializer for speciality model"""

    class Meta:
        model = Speciality
        fields = ('id', 'name')
        read_only_fields = ('id', )


class DoctorProfileSerializer(serializers.ModelSerializer):
    """Serializer for doctor model"""
    speciality1 = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Speciality.objects.all(),
        required=False
    )
    speciality2 = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Speciality.objects.all(),
        required=False
    )
    speciality3 = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Speciality.objects.all(),
        required=False
    )
    speciality4 = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Speciality.objects.all(),
        required=False
    )

    class Meta:
        model = Doctor
        fields = ('experience', 'qualification', 'highlights',
                  'speciality1', 'speciality2', 'speciality3',
                  'speciality4')


class CreateDoctorSerializer(serializers.ModelSerializer):
    """Serializer for creating doctor user"""
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password', 'placeholder': 'Password'},
        min_length=8
    )
    profile = ProfileSerializer(required=True)
    doctor_profile = DoctorProfileSerializer(required=False)

    class Meta:
        model = get_user_model()
        fields = (
            'email', 'password', 'username',
            'profile', 'doctor_profile', 'is_active',
            'is_doctor', 'is_staff'
        )
        read_only_fields = ('is_active', 'is_doctor', 'is_staff')

    def create(self, validated_data):
        """Create a new user with encrypted password and return it."""
        profile_data = validated_data.pop('profile', None)
        doc_profile_data = validated_data.pop('doctor_profile', None)
        doctor = get_user_model().objects.create_doctor(**validated_data)

        # Trying to save additional details of doctor
        # Saving profile data if persent
        if profile_data:
            profile = UserProfile.objects.get(user=doctor)
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

        # Check to prevent user from uploading doctor details
        # Saving doctor profile data if present
        if doc_profile_data:
            doc_pro = Doctor.objects.get(user=doctor)
            doc_pro.qualification = doc_profile_data.get(
                'qualification', doc_pro.qualification
            )
            doc_pro.experience = doc_profile_data.get(
                'experience', doc_pro.experience
            )
            doc_pro.highlights = doc_profile_data.get(
                'highlights', doc_pro.highlights
            )
            doc_pro.save()

            # Saving many to many field data if present
            if doc_profile_data.get('speciality1', None):
                doc_pro.speciality1.set(doc_profile_data.get(
                    'speciality1'))

            if doc_profile_data.get('speciality2', None):
                doc_pro.speciality2.set(doc_profile_data.get(
                    'speciality2'))

            if doc_profile_data.get('speciality3', None):
                doc_pro.speciality3.set(doc_profile_data.get(
                    'speciality3'))

            if doc_profile_data.get('speciality4', None):
                doc_pro.speciality4.set(doc_profile_data.get(
                    'speciality4'))

            doc_pro.save()

        # Refreshing the object with latest saved data
        doctor.refresh_from_db()

        return doctor


class ManageDoctorUserSerializer(serializers.ModelSerializer):
    """Serializer for editing users details and profile details"""
    profile = ProfileSerializer(required=False)
    doctor_profile = DoctorProfileSerializer(required=False)

    class Meta:
        model = get_user_model()
        fields = (
            'id', 'email',
            'username', 'created_date', 'profile', 'doctor_profile'
        )
        read_only_fields = ('id', 'email', 'created_date', )

    def update(self, instance, validated_data):
        """Add or modify details of user"""
        user_profile_data = validated_data.pop('profile', None)
        doctor_profile_data = validated_data.pop('doctor_profile', None)
        profile = instance.profile
        doc_profile = instance.doctor_profile

        user = super().update(instance, validated_data)
        user.save()

        # Updating profile data is profile data is present
        if user_profile_data:
            profile.first_name = user_profile_data.get(
                'first_name', profile.first_name)
            profile.last_name = user_profile_data.get(
                'last_name', profile.last_name)
            profile.city = user_profile_data.get(
                'city', profile.city)
            profile.country = user_profile_data.get(
                'country', profile.country)
            profile.primary_language = user_profile_data.get(
                'primary_language', profile.primary_language)
            profile.phone = user_profile_data.get(
                'phone', profile.phone)
            profile.date_of_birth = user_profile_data.get(
                'date_of_birth', profile.date_of_birth)
            profile.postal_code = user_profile_data.get(
                'postal_code', profile.postal_code)
            profile.address = user_profile_data.get(
                'address', profile.address)
            profile.secondary_language = user_profile_data.get(
                'secondary_language', profile.secondary_language)
            profile.tertiary_language = user_profile_data.get(
                'tertiary_language', profile.tertiary_language)

            profile.save()

        # Updating doctor profile data if data is present
        # and doctor is trying to update their details
        if doctor_profile_data and doc_profile:
            doc_profile.qualification = doctor_profile_data.get(
                'qualification', doc_profile.qualification
            )
            doc_profile.experience = doctor_profile_data.get(
                'experience', doc_profile.experience
            )
            doc_profile.highlights = doctor_profile_data.get(
                'highlights', doc_profile.highlights
            )

            # Saving many to many field data if present
            if doctor_profile_data.get('speciality1', None):
                doc_profile.speciality1.set(doctor_profile_data.get(
                    'speciality1'))

            if doctor_profile_data.get('speciality2', None):
                doc_profile.speciality2.set(doctor_profile_data.get(
                    'speciality2'))

            if doctor_profile_data.get('speciality3', None):
                doc_profile.speciality3.set(doctor_profile_data.get(
                    'speciality3'))

            if doctor_profile_data.get('speciality4', None):
                doc_profile.speciality4.set(doctor_profile_data.get(
                    'speciality4'))

            doc_profile.save()

        return instance


class MinimalUserSerializerImageUpload(serializers.ModelSerializer):
    """Minimal serializer supporting doctor user image upload field"""

    class Meta:
        model = get_user_model()
        fields = ('username', )


class DoctorImageUploadSerializer(serializers.ModelSerializer):
    """Serializer for doctor user image upload"""
    user = MinimalUserSerializerImageUpload(read_only=True)
    image = serializers.ImageField(allow_null=True, use_url=True)

    class Meta:
        model = UserProfile
        fields = ('id', 'user', 'image')
        read_only_fields = ('id', 'user')


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for user authentication object"""
    email = serializers.EmailField()
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

        # If user is not authenticated
        if not user:
            msg = _('Unable to authenticate with provided credentials.')

            try:
                doctor = get_user_model().objects.get(email=email)
                valid_user = doctor.check_password(password)

                # Creating custom error message if user is inactive but valid
                if valid_user:
                    msg = _('Account is inactive. Please wait for activation.')
            except:
                pass

            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user
        return attrs
