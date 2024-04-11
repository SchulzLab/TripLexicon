from django import forms
from django.forms import ModelForm
from .models import rem, rna, triplexaligner
#from .models import DNA, RNA, Triplexaligner

# Create an RNA form

class rna_form(ModelForm):
	class Meta:
		model = triplexaligner
		fields = ('triplexid',)
