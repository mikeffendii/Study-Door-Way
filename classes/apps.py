from django.apps import AppConfig


class ClassesConfig(AppConfig):
    name = 'classes'

    def ready(self):
    	import classes.signals