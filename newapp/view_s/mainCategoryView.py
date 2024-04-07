from rest_framework.response import Response
from rest_framework.decorators import api_view
from newapp.models import MainCategory
from newapp.serializers.maincategorySerializer import (
    MainCategoryGetSerializer,
    MainCategorySerializer,
    MainCategorySerializer2,
)


@api_view(["GET"])
def getCategory(request):
    try:
        parent = request.GET.get("parent")
        data = MainCategory.objects.filter(parent__unique_name=parent)
        parent = MainCategory.objects.filter(unique_name=parent)
        # print(data)
        serialized_data = MainCategorySerializer2(data, many=True)
        return Response({'sub_categories':serialized_data.data,'parent':parent.values().first()})
    except Exception as e:
        return Response({"message": "Got some data!", "data": str(e)}, status=400)


@api_view(["GET"])
def filterMainCategory(request, pk):
    locations = []
    if(pk=="null"):
        nullParents = MainCategory.objects.filter(parent=None)
        serialized_data=MainCategorySerializer2(nullParents, many=True).data
        return Response([{"options":serialized_data}])
    else:
        root_categories = MainCategory.objects.filter(unique_name=pk)
        root_categories2 = MainCategory.objects.filter(parent__unique_name=pk)
        serialized_data = MainCategorySerializer(root_categories, many=True).data
        childrens = MainCategorySerializer2(root_categories2, many=True).data
        # queryset = Location.objects.all().prefetch_related("category_images")
        # serializer = LocationSerializer(queryset, many=True)
        locations = []
        # for item in childrens:
        locations.append({"options": childrens})

        def interate(serialized_dat):
            # print((dict(serialized_dat[0])['options']),"PARAMS")
            if True:
                for item in serialized_dat:
                    locations.append(
                        {
                            "label": item["name"],
                            "value": item["unique_name"],
                            "options": item["options"],
                        }
                    )
                    if (dict(serialized_dat[0])["parent"]) is not None:
                        interate([item["parent"]])

        interate(serialized_data)
        print(locations.reverse(), "LOCATIONS")
        return Response(locations)
        # root_categories = MainCategory.objects.filter(id=pk)
        # serialized_data = MainCategorySerializer(root_categories, many=True).data
        # # queryset = MainCategory.objects.all().prefetch_related("category_images")
        # # serializer = MainCategorySerializer(queryset, many=True)
        # return Response({"data": serialized_data})

    # root_categories = MainCategory.objects.filter(id=pk)
    # serialized_data = MainCategorySerializer(root_categories, many=True).data
    # # queryset = MainCategory.objects.all().prefetch_related("category_images")
    # # serializer = MainCategorySerializer(queryset, many=True)
    # return Response({"data": serialized_data})
