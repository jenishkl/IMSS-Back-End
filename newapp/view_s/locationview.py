from rest_framework import status, viewsets
from rest_framework import serializers, status
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from newapp.models import Location
from django.db.models import Q, F, ExpressionWrapper, FloatField, Value
from newapp.serializers.locationSerializer import (
    LocationSerializer,
    LocationSerializer2,
    NestedLocationSerializer,
)


class LocationView(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

    def list(self, request):
        print((self.request, "JKJJH"))
        country = request.GET.get("country")
        state = request.GET.get("state")
        city = request.GET.get("city")
        print(country)
        if country:
            root_categories = Location.objects.filter(
                Q(unique_name=country) & Q(parent=None)
            )
        elif state:
            root_categories = Location.objects.filter(parent__unique_name=state)
        elif city:
            root_categories = Location.objects.filter(parent__unique_name=city)
        else:
            root_categories = Location.objects.filter(parent=None)
        serialized_data = NestedLocationSerializer(
            root_categories, many=True, context={"children": False}
        ).data
        # queryset = Location.objects.all().prefetch_related("category_images")
        # serializer = LocationSerializer(queryset, many=True)
        return Response({"data": serialized_data}, status=200)

    def retrieve(self, request, pk):
        locations = []
        if(pk=="null"):
            nullParents = Location.objects.filter(parent=None)
            serialized_data=LocationSerializer2(nullParents, many=True).data
            return Response([{"options":serialized_data}])
        else:
            root_categories = Location.objects.filter(unique_name=pk)
            root_categories2 = Location.objects.filter(parent__unique_name=pk)
            serialized_data = LocationSerializer(root_categories, many=True).data
            childrens = LocationSerializer2(root_categories2, many=True).data
            locations.append({"options": childrens})
        # queryset = Location.objects.all().prefetch_related("category_images")
        # serializer = LocationSerializer(queryset, many=True)
        
        # for item in childrens:
        
            def interate(serialized_dat):
                # print((dict(serialized_dat[0])['options']),"PARAMS")
                if(True):
                    for item in serialized_dat:
                        locations.append({"label": item["name"],"value":item["unique_name"], "options": item["options"]})
                        if((dict(serialized_dat[0])["parent"]) is not None):
                            interate([item["parent"]])

            interate(serialized_data)
            print(locations.reverse(), "LOCATIONS")
            return Response(locations)
