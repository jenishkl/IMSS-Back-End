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
        
    def __str__(self):
        return str(self.shop.id)
    def delete(self, *args, **kwargs):
        print("hhhh")
        # Remove the file from storage before deleting the model instance
        storage, path = self.image.storage, self.image.path
        if storage and path:
            if storage.exists(path):
                storage.delete(path)
        super(MyCategory, self).delete(*args, **kwargs)
    def save(self, *args, **kwargs):
        # Using the regular field, set the value of the read-only field.
        # self.slug = slugify(self.title)
        print("juyhgg")
        uniqueName = (
             str(self.name).replace(" ", "_").lower()
        )
        self.unique_name = uniqueName
        # call the parent's save() method
        print(self.pk,"SELF")
        if self.image is not None and self.pk:
            print(self.image,"DDD")
            old_instance = MyCategory.objects.get(pk=self.pk)
            old_image = old_instance.image
            new_image = self.image

            # Check if the image has changed
            if old_image and old_image != new_image:
                # Delete the old image file from storage
                if os.path.isfile(old_image.path):
                    os.remove(old_image.path)

        super(MyCategory, self).save(*args, **kwargs)
        