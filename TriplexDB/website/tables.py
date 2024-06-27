import django_tables2 as tables
from.models import triplexaligner

class results_table(tables.Table):
	class Meta:
		model = triplexaligner
		template_name = "django_tables2/bootstrap5-responsive.html"
		fields = ("rna__transcriptgenesymbol", "dna__promotersymbols", "triplexalignerscore", "triplexalignere", )