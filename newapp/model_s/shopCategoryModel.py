from django.db import models

# from newapp.models import CustomUser
from django.contrib.auth import get_user_model

User = get_user_model()
import os

def get_upload_path(instance, filename):
    print(instance, "instance")
    print(filename, "filename")
    return os.path.join("mycategory", "%s" % instance, filename)


class MyCategory(models.Model):
    parent = models.ForeignKey(
        "self",
        unique=False,
        related_name="children",
        null=True,
        on_delete=models.SET_NULL,
        max_length=50,
        blank=True,
    )
    name = models.CharField(unique=True, null=False, max_length=50, blank=False)
    unique_name = models.CharField(unique=True, null=False, max_length=50, blank=False)
    shop = models.ForeignKey(
        User,
        unique=False,
        related_name="my_category",
        null=True,
        on_delete=models.CASCADE,
    )
    image = models.ImageField(
        unique=False, blank=True, null=True, upload_to=get_upload_path
    )

    class Meta:
        managed = True
        db_table = "myCategory"

    def save(self, *args, **kwargs):
        # Using the regular field, set the value of the read-only field.
        # self.slug = slugify(self.title)
        uniqueName = (
            self.shop.unique_shopName + "/" + str(self.name).replace(" ", "_").lower()
        )
        self.unique_name = uniqueName
        # call the parent's save() method
        super(MyCategory, self).save(*args, **kwargs)
