from django.apps import AppConfig as _AppConfig

class AppConfig(_AppConfig):

    # This class can be used to add one time
    # initialization code and other hooks

    name = 'app'
    label = 'app'
    