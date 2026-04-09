import random
import string

from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User, UserProfile


# ---------------------------------------------------------------------------
# Auth serializers
# ---------------------------------------------------------------------------

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'phone_number', 'password', 'password_confirm']

    def validate(self, attrs):
        if attrs['password'] != attrs.pop('password_confirm'):
            raise serializers.ValidationError({"password_confirm": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        otp = ''.join(random.choices(string.digits, k=6))
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            phone_number=validated_data.get('phone_number', ''),
            password=validated_data['password'],
            otp=otp,
            is_verified=False,
        )
        # Create profile
        UserProfile.objects.create(user=user)

        # TODO: Send OTP via email/SMS
        # For development, the OTP is printed to the console
        print(f"[DEV] OTP for {user.email}: {otp}")

        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        user = authenticate(email=attrs['email'], password=attrs['password'])
        if not user:
            raise serializers.ValidationError("Invalid email or password.")
        if not user.is_verified:
            raise serializers.ValidationError("Please verify your email before logging in.")
        if not user.is_active:
            raise serializers.ValidationError("This account has been deactivated.")

        refresh = RefreshToken.for_user(user)
        return {
            'user': user,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            },
        }


class OTPVerifySerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)

    def validate(self, attrs):
        try:
            user = User.objects.get(email=attrs['email'])
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found.")

        if user.is_verified:
            raise serializers.ValidationError("User is already verified.")

        if user.otp != attrs['otp']:
            raise serializers.ValidationError("Invalid OTP.")

        return attrs

    def save(self):
        user = User.objects.get(email=self.validated_data['email'])
        user.is_verified = True
        user.otp = ''
        user.save(update_fields=['is_verified', 'otp'])
        return user


class ResendOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            user = User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found.")
        if user.is_verified:
            raise serializers.ValidationError("User is already verified.")
        return value

    def save(self):
        user = User.objects.get(email=self.validated_data['email'])
        otp = ''.join(random.choices(string.digits, k=6))
        user.otp = otp
        user.save(update_fields=['otp'])
        # TODO: Send OTP via email/SMS
        print(f"[DEV] Resent OTP for {user.email}: {otp}")
        return user


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("No account found with this email.")
        return value

    def save(self):
        user = User.objects.get(email=self.validated_data['email'])
        otp = ''.join(random.choices(string.digits, k=6))
        user.otp = otp
        user.save(update_fields=['otp'])
        # TODO: Send password reset OTP via email
        print(f"[DEV] Password reset OTP for {user.email}: {otp}")
        return user


class PasswordResetConfirmSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)
    new_password = serializers.CharField(min_length=8)

    def validate(self, attrs):
        try:
            user = User.objects.get(email=attrs['email'])
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found.")
        if user.otp != attrs['otp']:
            raise serializers.ValidationError("Invalid OTP.")
        return attrs

    def save(self):
        user = User.objects.get(email=self.validated_data['email'])
        user.set_password(self.validated_data['new_password'])
        user.otp = ''
        user.save(update_fields=['password', 'otp'])
        return user


# ---------------------------------------------------------------------------
# Profile serializers
# ---------------------------------------------------------------------------

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['address', 'company_name']


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'phone_number', 'role', 'is_verified', 'profile']
        read_only_fields = ['id', 'email', 'role', 'is_verified']

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', None)
        instance.username = validated_data.get('username', instance.username)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.save()

        if profile_data:
            profile, _ = UserProfile.objects.get_or_create(user=instance)
            profile.address = profile_data.get('address', profile.address)
            profile.company_name = profile_data.get('company_name', profile.company_name)
            profile.save()

        return instance
