# todo/todo_api/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import Task
from .serializers import TaskSerializer
from rest_framework.decorators import  api_view
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.exceptions import AuthenticationFailed


@api_view(['GET'])
def validateToken(request):
    token = request.headers.get('Authorization')
    if not token:
        return Response({"status": "Token not provided"}, status=401)
    token = token.replace('Bearer ', '')
    try:
        AccessToken(token)
    except Exception as e:
        return Response({"status": 'invalid'}, status=status.HTTP_401_UNAUTHORIZED)

    return Response({"status": "OK"}, status=status.HTTP_200_OK)


class TaskListApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        List all the tasks items for given requested user
        """
        user = request.user
        all_tasks = Task.objects.all()
        tasks_completed = Task.objects.filter(user=user, stage=4)
        tasks_incomplete = Task.objects.filter(user=user, stage=2)
        tasks_backlog = Task.objects.filter(user=user, stage=1)
        tasks_in_review = Task.objects.filter(user=user, stage=3)

        serializer_all = TaskSerializer(all_tasks, many=True)
        serializer_completed = TaskSerializer(tasks_completed, many=True)
        serializer_incomplete = TaskSerializer(tasks_incomplete, many=True)
        serializer_backlog = TaskSerializer(tasks_backlog, many=True)
        serializer_in_review = TaskSerializer(tasks_in_review, many=True)

        response_data = {
            'all_tasks': serializer_all.data,
            'completed': serializer_completed.data,
            'incomplete': serializer_incomplete.data,
            'backlog': serializer_backlog.data,
            'in_review': serializer_in_review.data
        }
        return Response(response_data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """
        Create the task with given task data
        """
        user = request.user
        for task_data in request.data.get('tasks'):
            task_serializer = TaskSerializer(data=task_data)

            if task_serializer.is_valid():
                task_id = task_serializer.initial_data.get('id')
                task = Task.objects.filter(id=task_id, user=user)
                if task.exists():
                    task.update(**task_serializer.validated_data)
                else:
                    Task.objects.create(user=user, **task_serializer.validated_data)
                    # return Response({'msg': 'Esta tarea ya no existe'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'msg': 'OKEYT'}, status=status.HTTP_201_CREATED)


#   before send
#   {'completed': True, 'created': '2024-08-30T00:58:23.928401Z', 'id': 1, 'name': 'tarea 1', 'stage': 4, 'updated': '2024-08-30T00:58:29.505089Z'}
#   on recept
#   {'completed': True, 'created': '2024-08-30T00:58:23.928401Z', 'id': 1, 'name': 'tarea 1 a', 'stage': 4, 'updated': '2024-08-30T00:58:29.505089Z'}