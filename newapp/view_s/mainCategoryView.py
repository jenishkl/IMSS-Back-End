from rest_framework.response import Response
from rest_framework.decorators import api_view
from newapp.models import MainCategory
from newapp.serializers.maincategorySerializer import MainCategoryGetSerializer


@api_view(["GET"])
def getCategory(request):
    try:
        parent = request.GET.get("parent")
        data = MainCategory.objects.filter(parent__unique_name=parent)
        # print(data)
        serialized_data = MainCategoryGetSerializer(data, many=True)
        return Response(serialized_data.data)
    except Exception as e:
        return Response({"message": "Got some data!", "data": str(e)}, status=400)
