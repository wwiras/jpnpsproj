from django.contrib import admin
from .models import Letter, LAssignTo,LHistory

admin.site.register(Letter)
admin.site.register(LAssignTo)
admin.site.register(LHistory)
