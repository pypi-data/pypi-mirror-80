from django.contrib import admin
from guardian.admin import GuardedModelAdmin
from django.db import models
from .models import Poll

admin.site.register(Poll, GuardedModelAdmin)
    
