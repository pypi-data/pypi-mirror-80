from django.db import models
from django.apps import apps
from django_eveonline_connector.services.static.utilities import resolve_type_name_to_type_id


import json, logging

logger = logging.getLogger(__name__)

class EveSkillPlan(models.Model):
    minimum_skills = models.TextField(blank=True, null=True)
    effective_skills = models.TextField(blank=True, null=True)
    fitting = models.OneToOneField("EveFitting", on_delete=models.SET_NULL, null=True, blank=True, related_name="skillplan")

    def __str__(self):
        return self.fitting.name

class EveFitCategory(models.Model):
    name = models.CharField(max_length=128)
    icon = models.URLField()

    def __str__(self):
        return self.name 

class EveDoctrineCategory(models.Model):
    name = models.CharField(max_length=128)
    icon = models.URLField()

    def __str__(self):
        return self.name 

class EveFitting(models.Model):
    name = models.CharField(max_length=32)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey("EveFitCategory", on_delete=models.SET_NULL, null=True, blank=True)
    fitting = models.TextField() # eft format
    ship_id = models.IntegerField(editable=False, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.ship_id = self.get_ship_id()
        super(EveFitting, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    def mod_array(self, mod):
        logger.debug("Resolving mod: %s" % mod)
        resolution = resolve_type_name_to_type_id(mod)
        if resolution:
            return resolution
        else:
            return [0,mod]

    def get_ship_name(self):
         fitting = self.fitting.splitlines()
         line = fitting[0]
         return line[1:-1].split(',')[0].strip()
        
    def get_ship_id(self):
        return self.mod_array(self.get_ship_name())

    def parse_fitting(self):
        fit = {'name':'','ship':'','high':[],'mid':[],'low':[],'rig':[], 'drones':[], 'cargo':[]}
        item = ['name', 'low','mid','high','rig','drones', 'cargo']
        fitting = self.fitting.splitlines()
        fitting.reverse()
        case = 0
        while len(fitting) > 1:
            if (fitting[-1] == '' or fitting[-1].isspace()):
                line = fitting.pop()
                case += 1
                while(fitting[-1].isspace() or fitting[-1] == ""):
                    excess = fitting.pop()
                continue
            else:
                line = fitting.pop()
            # process case 
            if (case == 0):
                fit['name'] = line[1:-1].split(',')[1].strip()
                fit['ship'] = self.mod_array(line[1:-1].split(',')[0].strip())
            elif (case == 1):
                # lowslots
                fit[item[case]].append(self.mod_array(line.split(',')[0]))
            elif (case == 2):
                # midslots
                fit[item[case]].append(self.mod_array(line.split(',')[0]))
            elif (case == 3):
                # highslots
                fit[item[case]].append(self.mod_array(line.split(',')[0]))
            elif (case == 4):
                # rigs 
                fit[item[case]].append(self.mod_array(line.split(',')[0]))
            elif (case == 5):
                # drones 
                if (line.split(",")[0].split(" ")[-1][0] == "x" and line.split(",")[0].split(" ")[-1][1].isnumeric()):
                        for amount in range(0,int(line.split(',')[0].split(" ")[-1][1:])):
                            fit[item[case]].append(self.mod_array(line.split(',')[0][:-3]))
                else:
                    fit[item[case]].append(self.mod_array(line.split(',')[0]))
            elif (case == 6):
                # cargo 
                if (line.split(",")[0].split(" ")[-1][0] == "x" and line.split(",")[0].split(" ")[-1][1].isnumeric()):
                        for amount in range(0,int(line.split(',')[0].split(" ")[-1][1:])):
                            fit[item[case]].append(self.mod_array(line.split(',')[0][:-3]))
                else:
                    fit[item[case]].append(self.mod_array(line.split(',')[0]))
        return fit


class EveDoctrine(models.Model):
    name = models.CharField(max_length=32)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey("EveDoctrineCategory", on_delete=models.SET_NULL, null=True, blank=True)
    fittings = models.ManyToManyField("EveFitting", blank=True)

    def __str__(self):
        return self.name