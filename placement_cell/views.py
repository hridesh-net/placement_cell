from rest_framework.views import APIView
from rest_framework.response import Response

class GoogleAuthCallbackView(APIView):
    def get(self, request, *args, **kwargs):
        print(request)
        print(request.data)
        print(request.query_params)
        return Response(status=200)