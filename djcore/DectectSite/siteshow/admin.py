from django.contrib import admin
from siteshow import models
# Register your models here.
admin.site.register(models.TMalware)
admin.site.register(models.TPhish)
admin.site.register(models.TZeustracker)
admin.site.register(models.TVirusapi)
admin.site.register(models.TSafebrowsing)
admin.site.register(models.TWhois)