from django.db import models


class Directory(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    dn = models.CharField(max_length=100)
    dc = models.GenericIPAddressField()
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    ldaps = models.BooleanField(default=False)

    def __str__(self):
        return self.dn

    class Meta:
        # verbose_name = 'Directory'
        verbose_name_plural = 'directories'