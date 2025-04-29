from rest_framework import status, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Professor, ModuleInstance, Rating, Module
from .serializers import ProfessorSerializer, ModuleInstanceSerializer, RatingSerializer
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models import Avg
from django.contrib.auth import authenticate


@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, email=email, password=password)
        return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)

# 登录
@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')
        
        # 验证用户凭证
        user = authenticate(username=username, password=password)
        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)
              # 返回生成的 access 和 refresh token
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        
        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

# 登出
@api_view(['POST'])
def logout(request):
    return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)

# 查看所有module实例
@api_view(['GET'])
def modules(request):
    if request.method == 'GET':
        modules = ModuleInstance.objects.all()
        serializer = ModuleInstanceSerializer(modules, many=True)
        return Response(serializer.data)

# 查看所有教授评分
@api_view(['GET'])
def professors_ratings(request):
    if request.method == 'GET':
        professors = Professor.objects.all()
        ratings = {}
        for professor in professors:
            total_rating = Rating.objects.filter(professor=professor)
            avg_rating = total_rating.aggregate(Avg('rating'))['rating__avg']
            ratings[professor.professor_id] = round(avg_rating) if avg_rating else 0
        return Response(ratings)

# 查看某个教授在某个课程的评分
@api_view(['GET'])
def professor_rating_in_module(request, professor_id, module_code):
    if request.method == 'GET':
        professor = Professor.objects.get(professor_id=professor_id)
        module = Module.objects.get(code=module_code)
        module_instances = ModuleInstance.objects.filter(module=module)

        ratings = []
        for instance in module_instances:
            rating = Rating.objects.filter(professor=professor, module_instance=instance)
            avg_rating = rating.aggregate(Avg('rating'))['rating__avg']
            ratings.append(round(avg_rating) if avg_rating else 0)

        return Response(ratings)

# # 给教授打分
# @api_view(['POST'])
# def rate(request):
#     if request.method == 'POST':
#         professor_id = request.data.get('professor_id')
#         code = request.data.get('code')
#         year = request.data.get('year')
#         semester = request.data.get('semester')
#         rating = request.data.get('rating')
        
#         professor = Professor.objects.get(professor_id=professor_id)
#         module = Module.objects.get(code=code)
#         module_instance = ModuleInstance.objects.get(module=module, year=year, semester=semester)

#         user = request.user
#         rating = Rating.objects.create(user=user, professor=professor, module_instance=module_instance, rating=rating)

#         return Response({"message": "Rating submitted successfully"}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def rate(request):
    user = request.user  # 获取当前用户
    professor_id = request.data['professor_id']
    code = request.data['code']
    year = request.data['year']
    semester = request.data['semester']
    rating_value = request.data['rating']

    module = Module.objects.get(code=code)

    # 查找模块实例
    try:
        module_instance = ModuleInstance.objects.get(module=module, year=year, semester=semester)
    except ModuleInstance.DoesNotExist:
        return Response({'error': 'Module instance not found.'}, status=404)

    # 查找教授
    try:
        professor = Professor.objects.get(professor_id=professor_id)
    except Professor.DoesNotExist:
        return Response({'error': 'Professor not found.'}, status=404)

    # 查找现有评分记录
    created = Rating.objects.update_or_create(
        user=user,
        professor=professor,
        module_instance=module_instance,
        defaults={'rating': rating_value}  # 如果已有记录，则更新评分
    )

    if created:
        return Response({'message': 'Successfully rated the professor.'}, status=201)
    else:
        return Response({'message': 'Rating updated successfully.'}, status=200)