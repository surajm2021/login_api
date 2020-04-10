from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from user.backend import MyAuthBackend
from user.models import User


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        user_id = request.POST.get('user_id')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        re_password = request.POST.get('re_password')
        name = request.POST.get('name')
        if password == re_password:
            if len(password) < 8:
                message = 'password short please enter at least 8 character'
                error = 'True'
            elif len(name) < 3:
                message = 'name should not letter'
                error = 'True'
            elif len(phone) == 10:
                if User.objects.filter(username=username).exists() or username is None:
                    message = 'username already exist or empty!! try another username'
                    error = 'True'
                elif User.objects.filter(email=email).exists():
                    message = 'email already exist or empty!! try another email id '
                    error = 'True'
                elif not User.objects.filter(username=username).exists():
                    user = User.objects.create_new_user(username, name, email, phone, password, user_id)
                    user.save()
                    message = 'registration successful'
                    error = 'False'
                else:
                    message = 'username already exist !! try another username'
                    error = 'True'
            else:
                message = 'phone no must be 10 digit'
                error = 'True'

        else:
            message = 'password and re_enter password not match'
            error = 'True'
    data = {'message': message, 'error': error}
    return Response(data)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = MyAuthBackend.authenticate(request, username=username, password=password)
        if user is not None:
            # login(request, user)
            message = 'user login successfully'
            user_obj = User.objects.get(username=username)
            name = user_obj.Name
            email = user_obj.email
            phone_no = user_obj.phone
            user_id = user_obj.user_id
            error = 'False'
            data = {'message': message, 'error': error, 'name': name, 'email': email, 'phone_no': phone_no,
                    'user_id': user_id}
            return Response(data)
        else:
            data = {'message': 'username and password not match ', 'error': 'True', 'token': 'empty'}
            print(data)
            return Response(data)
