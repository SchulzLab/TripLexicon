from django.contrib import admin
from .models import Dna as dna
#from .models import DNA
from .models import Rna as rna
from .models import Triplexaligner as triplexaligner

# Register your models here.

admin.site.register(dna)
#admin.site.register(DNA)
admin.site.register(rna)
admin.site.register(triplexaligner)
