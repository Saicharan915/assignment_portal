from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from db__connection import db
import json
from bson.objectid import ObjectId

admins_collection = db['admins']
assignments_collection = db['assignments']

@csrf_exempt
def register_admin(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data['username']
            password = data['password']

            if admins_collection.find_one({'username': username}):
                return JsonResponse({'error': 'Admin already exists'}, status=400)

            admins_collection.insert_one({'username': username, 'password': password})
            return JsonResponse({'message': 'Admin registered successfully'}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
def login_admin(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data['username']
            password = data['password']

            admin = admins_collection.find_one({'username': username, 'password': password})
            if admin:
                return JsonResponse({'message': 'Login successful'}, status=200)
            else:
                return JsonResponse({'error': 'Invalid credentials'}, status=401)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

def view_assignments(request):
    if request.method == 'GET':
        try:
            admin_username = request.GET.get('admin')
            assignments = list(assignments_collection.find({'admin': admin_username}))
            for assignment in assignments:
                assignment['_id'] = str(assignment['_id'])
            return JsonResponse({'assignments': assignments}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
def update_assignment_status(request, assignment_id, status):
    if request.method == 'POST':
        try:
            assignments_collection.update_one(
                {'_id': ObjectId(assignment_id)},
                {'$set': {'status': status}}
            )
            return JsonResponse({'message': f'Assignment {status} successfully'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
