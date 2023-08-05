
[![PyPI version](https://badge.fury.io/py/django-singleton-admin-2.svg)](https://badge.fury.io/py/django-singleton-admin-2) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/django-singleton-admin-2)

# Django Singleton Admin
In dynamic applications, it can be somewhat of a pain to have static settings that *have* to be set in `settings.py`. Django Singleton Admin adds an easy way to edit singleton models (e.g a SiteSetting model) to allow administrators to change configuration on the fly.

This is great for things like OAuth settings for third parties, or dynamic settings that you need to pull for your site. 

# Installation
1. Install with Pip `pip install django-singleton-admin-2`
2. Add `django_singleton_admin` to `INSTALLED_APPS`

# Influenced By
* https://github.com/RacingTadpole/django-singleton-admin
* https://github.com/lazybird/django-solo

# Example
```
# models.py
from django.db import models

class SiteSettings(models.Model):
    site_title = models.CharField(max_length=32)
    site_domain = models.CharField(max_length=32)
    site_description = models.CharField(max_length=32)

    @staticmethod
    def get_instance():
        return SiteSettings.objects.get_or_create(pk=0)
        
    def __str__(self):
        return "Site settings"
```

```
# admin.py
from django.contrib import admin
from .models import SiteSettings
from django_singleton_admin.admin import DjangoSingletonModelAdmin

admin.site.register(SiteSettings, DjangoSingletonModelAdmin)
```
