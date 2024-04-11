from django.contrib import admin
from .models import rem
#from .models import DNA
from .models import rna
from .models import triplexaligner

# Register your models here.

admin.site.register(rem)
#admin.site.register(DNA)
admin.site.register(rna)
admin.site.register(triplexaligner)
