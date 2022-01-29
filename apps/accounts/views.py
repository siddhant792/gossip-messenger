from rest_framework import generics as rest_framwork_generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token as AuthToken
from rest_framework import status

from apps.accounts import (
    serializers as accounts_serializers,
    models as accounts_models,
    utils as accounts_utils,
)


class RegisterUserView(rest_framwork_generics.CreateAPIView):
    """
    Register API for users
    """
    serializer_class = accounts_serializers.UserSerializer
    permission_classes = [AllowAny]


class LoginUserView(rest_framwork_generics.CreateAPIView):
    """
    Login API for users
    """
    serializer_class = accounts_serializers.LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        login_serializer = self.serializer_class(data=request.data)
        login_serializer.is_valid(raise_exception=True)
        token = AuthToken.objects.get_or_create(user = login_serializer.validated_data['user'])[0].key
        return Response(
            {
                'token': token,
                'name': login_serializer.validated_data['user'].name,
                'mobile_number': login_serializer.validated_data['user'].mobile_number,
                'profile_pic': login_serializer.validated_data['user'].profile_pic,
            }
        )


class UserProfileView(rest_framwork_generics.RetrieveAPIView):
    """
    Get User profile data 
    """
    serializer_class = accounts_serializers.UserProfileSerializer

    def retrieve(self, request, *args, **kwargs):
        user = request._user
        return_data = dict(self.serializer_class(instance=user).data)
        return Response(return_data)



class LogoutUserView(rest_framwork_generics.DestroyAPIView):
    """
    LogOut the current user
    """
    query_set = AuthToken.objects.all()

    def destroy(self, request, *args, **kwargs):
        token = self.query_set.filter(user=request.user)
        if token:
            token.delete()
            return Response({'message': "Logout Successful"}, status=status.HTTP_200_OK)
        return Response({'message': "Logout Failed"}, status=status.HTTP_400_BAD_REQUEST)


class UpdateUserView(rest_framwork_generics.UpdateAPIView):
    """
    Update the user profile
    """
    serializer_class = accounts_serializers.UserProfileSerializer
    queryset = accounts_models.User.objects.all()

    def partial_update(self, request, *args, **kwargs):
        user = request._user
        user_serializer = self.serializer_class(instance=user, data=request.data, partial=True)
        user_serializer.is_valid(raise_exception=True)
        for field in request.data:
            if field == 'profile_pic_file':
                try:
                    cloud_url = accounts_utils.upload_document(user, request.data['profile_pic_file'])
                    setattr(user, 'profile_pic', cloud_url)
                except:
                    return Response(
                        {'message': "Unexpected error while communicating database"}, 
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )
            else:
                setattr(user, field, request.data[field])
        user.save()
        return_data = dict(self.serializer_class(instance=user).data)
        return Response(return_data)
