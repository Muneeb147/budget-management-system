from django.contrib import admin
from .models import Brand, Campaign, Spend, DaypartingSchedule

admin.site.register(Brand)
admin.site.register(Campaign)
admin.site.register(Spend)
admin.site.register(DaypartingSchedule)
