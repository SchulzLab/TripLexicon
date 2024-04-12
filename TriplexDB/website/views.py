from django.shortcuts import render
from .models import rem
#from .models import DNA
from .models import rna
from .models import triplexaligner, rna, rem
from .forms import rna_form
from django_tables2 import SingleTableView
#from .tables import results_table
from django.db.models import Q
from django.http import Http404
from pybedtools import BedTool
from django.templatetags.static import static

# Create your views here.

def search_promoter(request):
	if request.method == "POST":
		searched = request.POST['searched']
		result = triplexaligner.objects.filter(rem__remsymbols=searched).order_by('triplexalignere')
		#result = Triplexaligner.objects.filter(promoter__promotersymbols=searched).order_by('triplexalignere')

		return render(request,
			'TriplexDB/search_promoter.html',
			{'searched':searched,
			'result':result})

	else:
		return render(request,
			'TriplexDB/search_promoter.html',
			{})

def search_rna_results(request):
	return render(request, 'TriplexDB/search_rna_results.html', {})


def search_transcript_values(request):
	if request.method == "POST":
		transcript = request.POST['transcript']
		rna_result = rna.objects.filter(transcriptid__exact = transcript).distinct().values('transcriptgenesymbol')[0]
		triplexes = triplexaligner.objects.filter(Q(rna__exact=transcript)).distinct().order_by('triplexalignere')\
		.values('triplexid','rna', 'transcripttriplexstart', 'transcripttriplexend', 'remtriplexstart', 'rem', 'remtriplexend',\
			'transcriptlength', 'remlength', 'triplexalignerscore', 'triplexalignerbitscore', 'triplexalignere')
		rem_id = [triplex["rem"] for triplex in triplexes]
		rem_result = rem.objects.filter(remid__in = rem_id).values('remsymbols', 'remid')
		for triplex in triplexes:
			triplex['rem_symbol'] = [rem_instance['remsymbols'] for rem_instance in rem_result\
							 if triplex['rem'] == rem_instance['remid']][0]
		
		if triplexes:
			return render(request,
				'TriplexDB/search_rna_results_values.html',
				{'transcript':transcript,
				'result':triplexes,
				'rna_symbol': rna_result['transcriptgenesymbol'],
				})
				# 'table':table})
		else:
			raise Http404("The given transcript cannot be found")

	else:
		return render(request,
			'TriplexDB/search_rna_results_values.html',
			{})


def search_rna_symbol_values(request):
	if request.method == "POST":
		rna_symbol = request.POST['rna_symbol']
		rems_to_exclude = rem.objects.filter(remsymbols__exact = rna_symbol).values('remid')
		rems_to_exclude = [rem_instance['remid'] for rem_instance in rems_to_exclude]
		transcript_ids = rna.objects.filter(transcriptgenesymbol__exact=rna_symbol).values('transcriptid')
		transcript_ids = [tid['transcriptid'] for tid in transcript_ids]
		triplexes = triplexaligner.objects.filter(Q(rna__in=transcript_ids))\
		.exclude(Q(rem__in=rems_to_exclude)).order_by('triplexalignere')[:50]\
		.values('triplexalignerscore', 'triplexalignere', 'rem', 'rna')
		rem_ids = [triplex["rem"] for triplex in triplexes]
		rem_result = rem.objects.filter(remid__in = rem_ids).distinct().values('remsymbols', 'remid')
		for triplex in triplexes:
			triplex['rem_symbol'] = [rem_instance['remsymbols'] for rem_instance in rem_result\
							 if triplex['rem'] == rem_instance['remid']][0]
			
		
		return render(request,
			'TriplexDB/search_rna_results_values.html',
			{'result':triplexes,
			'rna_symbol': rna_symbol,
			#'rem_symbol': rem_result['remsymbols'],
			})

	else:
		return render(request,
			'TriplexDB/search_rna_results_values.html',
			{})



def search_rna_home(request):
	return render(request, 'TriplexDB/search_rna_home.html', {})

def search_gen_region_home(request):
	chrs = ["chr1", "chr2", "chr3", "chr4", "chr5", "chr6","chr7", "chr8", "chr9","chr10", "chr11", "chr12",\
            "chr13", "chr14", "chr15","chr16", "chr17", "chr18","chr19", "chr20", "chr21","chrX", "chrY"]
	return render(request, 'TriplexDB/search_gen_region_home.html', {"chrs": chrs})

def gen_region_search(chromosome, start, end):
	bed_string = chromosome + "\t" + start + "\t" + end + "\n"
	query_region = BedTool(bed_string, from_string=True)
	rem_regions = BedTool('/Users/christina/Documents/triplex/TriplexDB/website/static/rem_regions.bed')
	rem_query_intersection = rem_regions.intersect(query_region, wa = True, f = 0.5)
	rem_query_list = []
	for rem_instance in rem_query_intersection:
		rem_query_list.append(rem_instance.name)

	triplexes = triplexaligner.objects.filter(Q(rem__remid__in=rem_query_list))\
	.values('triplexid','rna', 'transcripttriplexstart', 'transcripttriplexend', 'remtriplexstart', 'rem', 'remtriplexend',\
				'transcriptlength', 'remlength', 'triplexalignerscore', 'triplexalignerbitscore', 'triplexalignere')
	
	#query RNA objects
	transcript_ids = [triplex['rna'] for triplex in triplexes]
	transcript_gene_symbols = rna.objects.filter(transcriptid__in = transcript_ids).distinct().values('transcriptgenesymbol', 'transcriptid')
	
	#query REMs, new rem ids, only the ones having triplexes
	rem_ids = [triplex["rem"] for triplex in triplexes]
	rem_result = rem.objects.filter(remid__in = rem_ids).distinct().values('remsymbols', 'remid')
	for triplex in triplexes:
			triplex['transcriptgenesymbol'] = [rna_instance['transcriptgenesymbol'] for rna_instance in transcript_gene_symbols\
							 if triplex['rna'] == rna_instance['transcriptid']][0]
			triplex['rem_symbol'] = [rem_instance['remsymbols'] for rem_instance in rem_result\
							 if triplex['rem'] == rem_instance['remid']][0]
	return triplexes
	

def search_gen_region_results(request):
	if request.method == 'GET':
		start = request.GET.get('start')
		end =  request.GET.get('end')
		chromosome = request.GET.get('chromosome')
		if start and end and chromosome:
			if int(end)-int(start) < 1000000000:
				triplexes_in_region = gen_region_search(chromosome, start, end)
				return render(request, 'TriplexDB/search_genomic_region_results_values.html', {'result': triplexes_in_region, \
									 "chr": chromosome, "end": end, "start": start})
			else:
				raise Http404("Queried genomic region too big!")
		else:
			raise Http404("Start, end or chromosome missing!")
	else:
		raise Http404("GET method error")


def home(request):
	return render(request, 'TriplexDB/home.html', {})
