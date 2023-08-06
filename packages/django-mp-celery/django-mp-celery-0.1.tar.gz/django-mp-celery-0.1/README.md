# MP-celery

Django celery app.

### Installation

Install with pip:

```
pip install django-mp-celery
```

core/\_\_init\_\_.py
```
 
from __future__ import absolute_import
 
from core.celery_app import celery_app
 
 
__all__ = ['celery_app']
 
```

core/celery_app.py

```

import cbsettings
 
from django.conf import settings
 
from celery import Celery
 
 
__all__ = ['celery_app']
 
 
cbsettings.configure('core.settings.Settings')
 
celery_app = Celery('core', backend='redis://localhost', broker='pyamqp://')
 
celery_app.config_from_object('django.conf:settings')
celery_app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
 
```

core/common_settings.py
```
from mpcelery.settings import CelerySettings
```
