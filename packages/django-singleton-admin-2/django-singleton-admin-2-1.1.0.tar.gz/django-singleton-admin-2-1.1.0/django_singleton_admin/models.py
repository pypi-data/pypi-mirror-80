from django.db import models

class DjangoSingleton(models.Model):
    def save(self, *args, **kwargs):
        self.pk = 1
        super(DjangoSingleton, self).save(*args, **kwargs)

    class Meta:
        abstract = True 