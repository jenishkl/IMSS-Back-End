from django.apps import AppConfig


class NewappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'newapp'

    def ready(self):
        # Import the models from the "models" subfolders
        import newapp.model_s.shopCategoryModel
        import newapp.model_s.productModels
        import newapp.model_s.checkoutModel
        # import newapp.models.folder2.mymodel2