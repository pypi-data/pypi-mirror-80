from django.contrib import admin

from django.contrib import admin
from .models import EveFitting, EveDoctrine, EveSkillPlan, EveFitCategory, EveDoctrineCategory

admin.site.register(EveDoctrine)
admin.site.register(EveFitting)
admin.site.register(EveSkillPlan)
admin.site.register(EveFitCategory)
admin.site.register(EveDoctrineCategory)