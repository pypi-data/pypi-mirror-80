

class CelerySettings(object):

    @property
    def INSTALLED_APPS(self):
        return super().INSTALLED_APPS + ['django_celery_beat']
