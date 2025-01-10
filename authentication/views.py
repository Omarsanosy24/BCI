from rest_framework import generics, status, permissions
from authentication.serializers import LoginSerializer, UserInfoSer, RegisterSerializer
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    # هنا من الممكن استخدام api key وهذا لزيادة الامان
    # permission_classes = [HasAPIKey]

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data, context={"request": request})
        if serializer.is_valid():
            user = serializer.save()
        else:
            return Response(
                {
                    "status": False,
                    "message": serializer.errors,
                    "data": None,
                },
                status=status.HTTP_200_OK,
            )
        data = serializer.data
        data['token'] = user.get_tokens_for_user()
        return Response(
            {
                "status": True,
                "message": _('all is done'),
                'data': data
            },
            status=status.HTTP_200_OK,
        )


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    # permission_classes = [HasAPIKey]

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={"request": request})
        if serializer.is_valid():
            return Response(
                {
                    "status": True,
                    "message": _("logged successfully"),
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        else:
            # r = serializer.data.get("email")
            return Response(
                {"status": False, "message": serializer.errors, "data": {}}, status=status.HTTP_400_BAD_REQUEST
            )


class UserInfoView(generics.GenericAPIView):
    serializer_class = UserInfoSer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        ser = self.serializer_class(request.user, context={"request": request})
        return Response({
            "status": True,
            "message": _("all is done"),
            "results": ser.data
        })

    def patch(self, request):
        ser = self.serializer_class(data=request.data, instance=request.user, context={"request": request},
                                    partial=True)
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response({
            "status": True,
            "message": _("all is done"),
            "results": ser.data
        })
