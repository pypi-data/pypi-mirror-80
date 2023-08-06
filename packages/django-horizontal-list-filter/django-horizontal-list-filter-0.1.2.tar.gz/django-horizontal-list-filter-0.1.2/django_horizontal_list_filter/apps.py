from django.apps import AppConfig


class DjangoHorizontalListFilterConfig(AppConfig):
    name = 'django_horizontal_list_filter'

    def ready(self):
        # inject our css&js into media
        from django.contrib.admin import ModelAdmin
        from django import forms

        ModelAdmin.__django_horizontal_list_filter_old_media = ModelAdmin.media

        @property
        def media(self):
            return self.__django_horizontal_list_filter_old_media + forms.Media(css={
                "all": [
                    "django-horizontal-list-filter/css/django-horizontal-list-filter.css",
                ],
            }, js=[
                "admin/js/vendor/jquery/jquery.js",
                "django-horizontal-list-filter/js/django-horizontal-list-filter.js",
                "admin/js/jquery.init.js",
            ])

        ModelAdmin.media = media
