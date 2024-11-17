from datetime import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from db__connection import db
import json
from bson.objectid import ObjectId

users_collection = db['users']
assignments_collection = db['assignments']
admins_collection = db['admins']

@csrf_exempt
def register_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data['username']
            password = data['password']

            if users_collection.find_one({'username': username}):
                return JsonResponse({'error': 'User already exists'}, status=400)

            users_collection.insert_one({'username': username, 'password': password})
            return JsonResponse({'message': 'User registered successfully'}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data['username']
            password = data['password']

            user = users_collection.find_one({'username': username, 'password': password})
            if user:
                return JsonResponse({'message': 'Login successful'}, status=200)
            else:
                return JsonResponse({'error': 'Invalid credentials'}, status=401)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
def upload_assignment(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_id = data['userId']
            task = data['task']
            admin = data['admin']

            # Validate admin exists
            if not admins_collection.find_one({'username': admin}):
                return JsonResponse({'error': 'Admin not found'}, status=400)

            assignments_collection.insert_one({
                'userId': user_id,
                'task': task,
                'admin': admin,
                'status': 'pending',
                'timestamp': datetime.now()
            })
            return JsonResponse({'message': 'Assignment uploaded successfully'}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

def get_all_admins(request):
    if request.method == 'GET':
        try:
            admins = list(admins_collection.find({}, {'_id': 0, 'username': 1}))
            return JsonResponse({'admins': admins}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
