import os
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    AbstractUser,
    PermissionsMixin,
    BaseUserManager,
)

# from newapp.categoryModel.category import ShopCategory
# from django.contrib.auth import get_user_model
# User = get_user_model()
from mptt.models import MPTTModel, TreeForeignKey

# from django.contrib.auth import get_user_model

# User = get_user_model()


# Create your models here.
class MainCategory(models.Model):
    parent = models.ForeignKey(
        "self",
        unique=False,
        related_name="children",
        null=True,
        on_delete=models.SET_NULL,
        max_length=50,
        blank=True,
    )
    name = models.CharField(unique=True, null=False,
                            max_length=50, blank=False)
    unique_name = models.CharField(
        unique=True, null=False, max_length=50, blank=False)
    image = models.ImageField(
        unique=False, max_length=200, blank=True, null=True, upload_to="MainCategoryImg"
    )
    index = models.IntegerField(null=True,
                                unique=False,
                                blank=True,)

    class Meta:
        managed = True
        db_table = "maincategory"

    def save(self, *args, **kwargs):
        # Using the regular field, set the value of the read-only field.
        # self.slug = slugify(self.title)
        uniqueName = str(self.name).replace(" ", "_").lower()
        self.unique_name = uniqueName
        # call the parent's save() method
        super(MainCategory, self).save(*args, **kwargs)


class CategoryImage(models.Model):
    image = models.ImageField(
        unique=False, max_length=200, blank=False, null=False, upload_to="ctimg"
    )
    category = models.ForeignKey(
        MainCategory,
        on_delete=models.CASCADE,
        related_name="category_images",
        null=True,
        blank=True,
    )
    primary = models.BooleanField(default=False, null=False, blank=True)

    class Meta:
        managed = True
        db_table = "main_category_image"


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        # user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_shop", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_customer", True)

        if extra_fields.get("is_shop") is not True:
            raise ValueError(_("Superuser must have is_shop=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)

    def are_active(self):
        # use your method to filter results
        print(self.a)
        return 12


class Location(models.Model):
    parent = models.ForeignKey(
        "self",
        unique=False,
        null=True,
        on_delete=models.SET_NULL,
        max_length=50,
        blank=True,
    )
    name = models.CharField(unique=True, null=False,
                            max_length=50, blank=False)
    unique_name = models.CharField(
        unique=True, null=False, max_length=50, blank=False)

    class Meta:
        managed = True
        db_table = "location"

    def save(self, *args, **kwargs):
        # Using the regular field, set the value of the read-only field.
        # self.slug = slugify(self.title)
        # print(self.parent.)
        uniqueName = str(self.name).replace(" ", "_").lower()

        self.unique_name = uniqueName
        # call the parent's save() method
        super(Location, self).save(*args, **kwargs)


def get_upload_path(instance, filename):
    print(instance, "instance")
    print(filename, "filename")
    return os.path.join("logo", "%s" % instance, filename)


def banner_upload_path(instance, filename):
    print(instance, "instance")
    print(filename, "filename")
    return os.path.join("profile_banner", "%s" % instance, filename)


class CustomUser(AbstractUser):
    # first_name = None
    # last_name = None
    # is_staff = None
    username = models.CharField(null=True, max_length=50, blank=True,)
    email = models.EmailField(_("email address"), unique=True, error_messages={
        'unique': _("This email address is already in use."),
    })
    # Other
    is_shop = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=True)
    shopName = models.CharField(
        unique=False, null=True, max_length=50, blank=True,
        error_messages={
            "unique": "unique."
        }
    )
    unique_shopName = models.CharField(
        null=True, max_length=50, blank=True, unique=False,
    )
    shop_logo = models.ImageField(
        blank=True, null=True, upload_to=get_upload_path)
    background_image = models.ImageField(
        unique=False, blank=True, null=True, upload_to=banner_upload_path
    )
    location = models.ForeignKey(
        Location, null=True, blank=True, on_delete=models.SET_NULL
    )
    address = models.CharField(
        unique=False, null=True, max_length=50, blank=True)
    lat = models.FloatField(unique=False, null=True, blank=True)
    long = models.FloatField(unique=False, null=True, blank=True)
    delivery_charge = models.FloatField(unique=False, null=True, blank=True)
    about = models.CharField(unique=False, null=True,
                             max_length=100, blank=True)
    main_category = models.ManyToManyField(MainCategory)
    contact_number = models.CharField(
        max_length=20,
        null=True,
        unique=False,
        blank=True,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        unique_together = [['email']]
        # error_messages = {
        #     'email': {
        #         'unique': _("This email address is already in use."),
        #     }
        # }

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        # Using the regular field, set the value of the read-only field.
        # self.slug = slugify(self.title)
        print(self, "DATA")
        if (self.shopName):
            self.unique_shopName = (
                str(self.shopName).replace(" ", "").replace(
                    "/", "-").lower()+"_"+str(self.id)
            )

        # self.pop("password2")
        # call the parent's save() method
        # if self.company_logo is not None:
        #     old_instance = CustomUser.objects.get(pk=self.pk)
        #     old_image = old_instance.company_logo
        #     new_image = self.company_logo

        #     # Check if the image has changed
        #     if old_image and old_image != new_image:
        #         # Delete the old image file from storage
        #         if os.path.isfile(old_image.path):
        #             os.remove(old_image.path)
        # if self.background_image is not None:
        #     old_instance = CustomUser.objects.get(pk=self.pk)
        #     old_image = old_instance.background_image
        #     new_image = self.background_image

        #     # Check if the image has changed
        #     if old_image and old_image != new_image:
        #         # Delete the old image file from storage
        #         if os.path.isfile(old_image.path):
        #             os.remove(old_image.path)

        super(CustomUser, self).save(*args, **kwargs)
        # try:
        #     this = Photo.objects.get(id=self.id)
        #     if this.image != self.image:
        #         this.image.delete(save=False)
        # except: pass # when new photo then we do nothing, normal case
        # super(Photo, self).save(*args, **kwargs)

    # def delete_old_image(self):
    #     # Check if the instance has an ID (i.e., it's already saved in the database)
    #     print(self, "SELF")
    #     if self.pk:
    #         old_instance = CustomUser.objects.get(pk=self.pk)
    #         old_image = old_instance.company_logo
    #         new_image = self.company_logo

    #         # Check if the image has changed
    #         if old_image and old_image != new_image:
    #             # Delete the old image file from storage
    #             if os.path.isfile(old_image.path):
    #                 os.remove(old_image.path)

    # class Meta:
    #     managed = True
    #     db_table = 'auth_user'


class ShopLikes(models.Model):
    shop = models.ForeignKey(CustomUser, null=True, blank=True,
                             on_delete=models.SET_NULL, related_name='like_shop')
    customer = models.ForeignKey(CustomUser, null=True, blank=True,
                                 on_delete=models.SET_NULL, related_name='like_customer')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_like = models.BooleanField(default=False)
    is_follow = models.BooleanField(default=False)

    class Meta:
        managed = True
        db_table = 'shop_likes'
        unique_together = ('shop', 'customer')  # Ensure uniqueness
