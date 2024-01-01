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
    name = models.CharField(unique=True, null=False, max_length=50, blank=False)
    unique_name = models.CharField(unique=True, null=False, max_length=50, blank=False)

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


from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


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
    name = models.CharField(unique=True, null=False, max_length=50, blank=False)
    unique_name = models.CharField(unique=True, null=False, max_length=50, blank=False)

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


import os


def get_upload_path(instance, filename):
    print(instance, "instance")
    print(filename, "filename")
    return os.path.join("logo", "%s" % instance, filename)


def banner_upload_path(instance, filename):
    print(instance, "instance")
    print(filename, "filename")
    return os.path.join("profile_banner", "%s" % instance, filename)


class CustomUser(AbstractUser):
    first_name = None
    last_name = None
    is_staff = None
    username = models.CharField(null=True, max_length=50, blank=True)
    email = models.EmailField(_("email address"), unique=True)
    is_shop = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    shopName = models.CharField(
        unique=True, null=True, max_length=50, blank=False, default=""
    )
    unique_shopName = models.CharField(
        null=True, max_length=50, blank=True, unique=True
    )
    company_logo = models.ImageField(blank=True, null=True, upload_to=get_upload_path)
    background_image = models.ImageField(
        unique=False, blank=True, null=True, upload_to=banner_upload_path
    )
    location = models.ForeignKey(
        Location, null=True, blank=True, on_delete=models.SET_NULL
    )
    address = models.CharField(unique=False, null=True, max_length=50, blank=True)
    lat = models.FloatField(unique=False, null=True, blank=True)
    long = models.FloatField(unique=False, null=True, blank=True)
    about = models.CharField(unique=False, null=True, max_length=100, blank=True)
    main_category = models.ManyToManyField(MainCategory)
    contact_number = models.IntegerField(
        null=True,
        unique=False,
        blank=True,
    )

    USERNAME_FIELD = "unique_shopName"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        # Using the regular field, set the value of the read-only field.
        # self.slug = slugify(self.title)
        print(self, "DATA")
        self.unique_shopName = (
            str(self.shopName).replace(" ", "").replace("/", "-").lower()
        )
        # self.pop("password2")
        # call the parent's save() method
        if self.company_logo is not None:
            old_instance = CustomUser.objects.get(pk=self.pk)
            old_image = old_instance.company_logo
            new_image = self.company_logo

            # Check if the image has changed
            if old_image and old_image != new_image:
                # Delete the old image file from storage
                if os.path.isfile(old_image.path):
                    os.remove(old_image.path)
        if self.background_image is not None:
            old_instance = CustomUser.objects.get(pk=self.pk)
            old_image = old_instance.background_image
            new_image = self.background_image

            # Check if the image has changed
            if old_image and old_image != new_image:
                # Delete the old image file from storage
                if os.path.isfile(old_image.path):
                    os.remove(old_image.path)

        super(CustomUser, self).save(*args, **kwargs)
        # try:
        #     this = Photo.objects.get(id=self.id)
        #     if this.image != self.image:
        #         this.image.delete(save=False)
        # except: pass # when new photo then we do nothing, normal case
        # super(Photo, self).save(*args, **kwargs)

    def delete_old_image(self):
        # Check if the instance has an ID (i.e., it's already saved in the database)
        print(self, "SELF")
        if self.pk:
            old_instance = CustomUser.objects.get(pk=self.pk)
            old_image = old_instance.company_logo
            new_image = self.company_logo

            # Check if the image has changed
            if old_image and old_image != new_image:
                # Delete the old image file from storage
                if os.path.isfile(old_image.path):
                    os.remove(old_image.path)

    # class Meta:
    #     managed = True
    #     db_table = 'auth_user'


class ShopProfile(models.Model):
    #     STATES =[
    #     ("AN","Andaman and Nicobar Islands"),
    #     ("AP","Andhra Pradesh"),
    #     ("AR","Arunachal Pradesh"),
    #     ("AS","Assam"),
    #     ("BR","Bihar"),
    #     ("CG","Chandigarh"),
    #     ("CH","Chhattisgarh"),
    #     ("DN","Dadra and Nagar Haveli"),
    #     ("DD","Daman and Diu"),
    #     ("DL","Delhi"),
    #     ("GA","Goa"),
    #     ("GJ","Gujarat"),
    #     ("HR","Haryana"),
    #     ("HP","Himachal Pradesh"),
    #     ("JK","Jammu and Kashmir"),
    #     ("JH","Jharkhand"),
    #     ("KA","Karnataka"),
    #     ("KL","Kerala"),
    #     ("LA","Ladakh"),
    #     ("LD","Lakshadweep"),
    #     ("MP","Madhya Pradesh"),
    #     ("MH","Maharashtra"),
    #     ("MN","Manipur"),
    #     ("ML","Meghalaya"),
    #     ("MZ","Mizoram"),
    #     ("NL","Nagaland"),
    #     ("OR","Odisha"),
    #     ("PY","Puducherry"),
    #     ("PB","Punjab"),
    #     ("RJ","Rajasthan"),
    #     ("SK","Sikkim"),
    #     ("TN","Tamil Nadu"),
    #     ("TS","Telangana"),
    #     ("TR","Tripura"),
    #     ("UP","Uttar Pradesh"),
    #     ("UK","Uttarakhand"),
    #     ("WB","West Bengal")
    # ]

    user_id = models.OneToOneField(
        CustomUser, null=True, blank=False, on_delete=models.CASCADE
    )
    shop_name = models.CharField(
        unique=True, null=False, max_length=50, blank=False, default=""
    )
    company_logo = models.ImageField(blank=True, null=True, upload_to="logo")
    backgroud_image = models.ImageField(
        unique=True, blank=True, null=True, upload_to="background"
    )
    location = models.ForeignKey(
        Location, null=True, blank=True, on_delete=models.CASCADE
    )
    address = models.CharField(unique=False, null=True, max_length=50, blank=True)
    lat = models.CharField(unique=False, null=True, max_length=100, blank=True)
    long = models.CharField(unique=False, null=True, max_length=100, blank=True)
    about = models.CharField(unique=False, null=True, max_length=100, blank=True)
    main_category = models.ForeignKey(MainCategory, on_delete=models.PROTECT)





#     class Meta:
#         managed = True
#         db_table = 'ShopProfile'


# class UserAccountManager(BaseUserManager):
#     def create_user(self, email, name, password=None):
#         if not email:
#             raise ValueError('Users must have an email address')

#         email = self.normalize_email(email)
#         email = email.lower()

#         user = self.model(
#             email=email,
#             name=name
#         )

#         user.set_password(password)
#         user.save(using=self._db)

#         return user

#     def create_realtor(self, email, name, password=None):
#         user = self.create_user(email, name, password)

#         user.is_realtor = True
#         user.save(using=self._db)

#         return user

#     def create_superuser(self, email, name, password=None):
#         user = self.create_user(email, name, password)

#         user.is_superuser = True
#         user.is_shop = True

#         user.save(using=self._db)

#         return user

# class CustomUser(AbstractUser,PermissionsMixin):
#   #Boolean fields to select the type of account.
#     email = models.EmailField(max_length=255, unique=True)
#     is_shop = models.BooleanField(default=False)
#     is_customer = models.BooleanField(default=False)


#     # class meta(AbstractUser.Meta):
#     #     swappable = "AUTH_USER_MODEL"


#     objects = UserAccountManager()

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['name']

#     def __str__(self):
#         return self.email
