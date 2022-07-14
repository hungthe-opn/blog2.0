# from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from api.utils import custom_response
# Create your views here.
from .models import CreateUserModel, Follow
from .serializers import RegisterUserSerializer, UpdateInformationSerializer, UserInformationSerializer, \
    UserFollowSerializer, ViewUserSerializer


class CustomUserCreate(APIView):
    permission_classes = [AllowAny]

    def post(self, request):

        email = request.data['email']
        user_name = request.data['user_name']
        try:
            user = CreateUserModel.objects.get(email=email)
            user_name = CreateUserModel.objects.get(user_name=user_name)

            return Response(status=status.HTTP_400_BAD_REQUEST)
        except CreateUserModel.DoesNotExist:
            reg_serializer = RegisterUserSerializer(data=request.data)
            if reg_serializer.is_valid():
                reg_serializer.save()
                return Response(custom_response(reg_serializer.data, msg_display='Tạo tài khoản thành công!'),
                                status=status.HTTP_201_CREATED)
            return Response(custom_response(reg_serializer.errors, response_code=400, response_msg='ERROR',
                                            msg_display='Thêm không thành công, vui lòng thử lại'),
                            status=status.HTTP_400_BAD_REQUEST)


class UpdateInformationView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = CreateUserModel.objects.filter(id=request.user.id).first()
        serializer = UpdateInformationSerializer(queryset)
        return Response(custom_response(serializer.data, msg_display='Hiển thị thành công'),
                        status=status.HTTP_200_OK)

    def patch(self, request):
        print(request.data.get('user_name'))
        forms = request.data
        data = {
            'id': request.user.id,
            'user_name': forms.get('user_name'),
            'first_name': forms.get('first_name'),
            'about': forms.get('about'),
            'image': forms.get('image')
        }
        user_name = CreateUserModel.objects.filter(user_name=forms.get('user_name')).exclude(id=request.user.id)
        if len(user_name) != 0:
            print(1111111111111111111)
            return Response({'message': 'Tên đăng nhập đã tồn tại, vui lòng thử lại!'},
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            query = CreateUserModel.objects.filter(id=request.user.id).first()
            serializer = UpdateInformationSerializer(query, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(custom_response(serializer.data, msg_display='Cập nhật thông tin thành công!'),
                                status=status.HTTP_201_CREATED)
            return Response(custom_response(serializer.errors, response_code=400, response_msg='ERROR',
                                            msg_display='Thông tin cập nhật sai, vui lòng thử lại!'),
                            status=status.HTTP_400_BAD_REQUEST)


class BlacklistTokenView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserInforView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = CreateUserModel.objects.filter(id=request.user.id).first()
        serializer = UserInformationSerializer(queryset)
        return Response(custom_response(serializer.data, msg_display='Hiển thị thành công'),
                        status=status.HTTP_201_CREATED)


class UserDetailsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request,pk):
        queryset = CreateUserModel.objects.filter(id=pk).first()
        serializer = ViewUserSerializer(queryset)
        return Response(custom_response(serializer.data, msg_display='Hiển thị thành công'),
                        status=status.HTTP_201_CREATED)


class UserFollowerView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        query = Follow.objects.create(from_user=request.user.id, to_user=request.follow.id, id=pk)
        serializer = UserFollowSerializer(query)
        if serializer.is_valid():
            serializer.save()
            return Response(custom_response(serializer.data, msg_display='Chỉnh sửa thành công'),
                            status=status.HTTP_201_CREATED)
        return Response(custom_response(serializer.errors, response_code=400, response_msg='ERROR',
                                        msg_display='Cập nhật bài viết thuất bại, vui lòng thử lại sau'),
                        status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        queryset = Follow.objects.filter(from_user=request.user.id, to_user=request.follow.id, id=pk)
        serializer = UserFollowSerializer(queryset)
        queryset.delete()
        return Response(custom_response(serializer.data, list=False, msg_display='Xóa bài viết h công'))


class UserFollow(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        queryset = CreateUserModel.objects.get(id=pk)
        queryset.from_user.all()
        queryset.to_user.all()
        serializer = UserFollowSerializer(queryset, many=True)
        return Response(custom_response(serializer.data, msg_display='Hiển thị thành công'),
                        status=status.HTTP_201_CREATED)
