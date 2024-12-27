from django.db import models

from django.db import models

class ExtractedData(models.Model):
    key = models.CharField(max_length=255)
    value = models.TextField()

    def __str__(self):
        return f"{self.key}: {self.value}"


# class wisper(models.Model):
#     text = models.CharField(max_length=1000, verbose_name='text')



