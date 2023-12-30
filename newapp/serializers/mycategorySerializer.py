from newapp.model_s.shopCategoryModel import MyCategory
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class MyCategorySerializer2(serializers.ModelSerializer):
    unique_name = serializers.CharField(read_only=True)
    # name = serializers.CharField(read_only=True)
    # parent = serializers.PrimaryKeyRelatedField(
    #     queryset=MyCategory.objects.all(), required=False
    # )
    # shop = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(),required=False)

    class Meta:
        model = MyCategory
        fields = "__all__"
        # depth = 10

    # def get_children(self, obj):
    #     children = MyCategory.objects.filter(parent=obj)
    #     return NestedMyCategorySerializer(children, many=True).data


# class NestedMyCategorySerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     parent = serializers.PrimaryKeyRelatedField(
#         queryset=MyCategory.objects.all(), required=False
#     )
#     label = serializers.CharField(source="name")
#     value = serializers.CharField(read_only=True, source="unique_name")
#     shop = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
#     children = serializers.SerializerMethodField("get_children")

#     def get_children(self, obj):
#         children = MyCategory.objects.filter(parent=obj)
#         return NestedMyCategorySerializer(children, many=True).data


class MyCategorySerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=MyCategory.objects.all(), required=False
    )
    unique_name = serializers.CharField(read_only=True)
    parent = serializers.PrimaryKeyRelatedField(
        queryset=MyCategory.objects.all(), required=False, write_only=True
    )
    # parent =  serializers.CharField(read_only=True)
    parent = serializers.SerializerMethodField("get_parent", read_only=True)
    options = serializers.SerializerMethodField("get_options", read_only=True)

    class Meta:
        model = MyCategory
        fields = "__all__"
        depth = 2

    def get_options(self, obj):
        # print(getattr(obj, "parent").id, "ID")
        if getattr(obj, "parent") is not None:
            print(getattr(obj, "parent").id, "Pa2")
        if True:
            if getattr(obj, "parent") is not None:
                parent = MyCategory.objects.filter(parent=getattr(obj, "parent").id)
                print(parent, "options")
                # if  == 0:
                #     return 0
                # dat = False

                return MyCategorySerializer2(parent, many=True).data
            else:
                # dat = False
                parent = MyCategory.objects.filter(parent=None)
                print(parent, "options2")
                # if  == 0:
                #     return 0
                # dat = False

                return MyCategorySerializer2(parent, many=True).data

    def get_parent(self, obj):
        # print(getattr(obj, "parent").id, "ID")
        print(obj.parent, "Pa")
        # dat = True
        if obj.parent is not None:
            parent = MyCategory.objects.get(id=getattr(obj, "parent").id)
            print(parent, "Parent")
            # if  == 0:
            #     return 0
            # dat = False

            return MyCategorySerializer(parent, many=False).data

