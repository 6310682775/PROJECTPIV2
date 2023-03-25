from django.contrib import admin
from .models import Task, Loop, VehicleCount, LoopResult

admin.site.register(Task)
admin.site.register(Loop)
admin.site.register(VehicleCount)
admin.site.register(LoopResult)
