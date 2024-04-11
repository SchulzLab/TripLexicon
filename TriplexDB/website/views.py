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
			rna_result = rna.objects.filter(transcriptid__exact = transcript).distinct().values('transcriptgenesymbol')
			transcriptgenesymbol = rna_result.first()['transcriptgenesymbol']
			triplexes = triplexaligner.objects.filter(Q(rna__transcriptid__exact=transcript)).distinct().order_by('triplexalignere')\
			.values('triplexid','rna', 'transcripttriplexstart', 'transcripttriplexend', 'remtriplexstart', 'rem', 'remtriplexend',\
				'transcriptlength', 'remlength', 'triplexalignerscore', 'triplexalignerbitscore', 'triplexalignere')

			triplex_info = {}
			for triplex in triplexes:
				triplex_info[triplex["rem"]] = {}
				#rem_result = rem.objects.filter(rem_triplexid__triplexid__exact =triplex['triplexid']).values('remsymbols')
				#print(rna_result)
				triplex_info[triplex["rem"]]['transcriptgenesymbol']=transcriptgenesymbol
				triplex_info[triplex["rem"]]['transcriptid']=transcript
				triplex_info[triplex["rem"]]['transcripttriplexstart']=triplex['transcripttriplexstart']
				triplex_info[triplex["rem"]]['transcripttriplexend']=triplex['transcripttriplexend']
				triplex_info[triplex["rem"]]['remtriplexstart']=triplex['remtriplexstart']
				triplex_info[triplex["rem"]]['remtriplexend']=triplex['remtriplexend']
				triplex_info[triplex["rem"]]['transcriptlength']=triplex['transcriptlength']
				triplex_info[triplex["rem"]]['remlength']=triplex['remlength']
				triplex_info[triplex["rem"]]['triplexalignerscore']=triplex['triplexalignerscore']
				triplex_info[triplex["rem"]]['triplexalignerbitscore']=triplex['triplexalignerbitscore']
				triplex_info[triplex["rem"]]['triplexalignere']=triplex['triplexalignere']
				triplex_info[triplex["rem"]]['remsymbols']=triplex["rem"]
			
			if triplex_info:
				return render(request,
					'TriplexDB/search_rna_results_values.html',
					{'transcript':transcript,
					'result':triplex_info,})
					# 'table':table})
			else:
				raise Http404("The given transcript cannot be found")

	else:
			return render(request,
				'TriplexDB/search_rna_results_values.html',
				{})


def search_transcript(request):
	if request.method == "POST":
			transcript = request.POST['transcript']
			result = triplexaligner.objects.filter(rna__transcriptid__exact=transcript).order_by('triplexalignere')

			# class rna_results_table(SingleTableView):
			# 	model = Triplexaligner
			# 	table_class = results_table
			# 	template_name = 'TriplexDB/search_rna_results.html'

			# table = rna_results_table(result)

			return render(request,
				'TriplexDB/search_rna_results.html',
				{'transcript':transcript,
				'result':result,})
				# 'table':table})

	else:
			return render(request,
				'TriplexDB/search_rna_results.html',
				{})

def search_rna_symbol_values(request):
	if request.method == "POST":
			rna_symbol = request.POST['rna_symbol']
			#rna_result = rna.objects.filter(transcriptgenesymbol__exact = rna_symbol).distinct().values('transcriptgenesymbol')
			triplexes = triplexaligner.objects.filter(Q(rna__transcriptgenesymbol__exact=rna_symbol))\
			.exclude(Q(rem__remsymbols__exact=rna_symbol)).order_by('triplexalignere')[:50]\
			.values('triplexalignerscore', 'triplexalignere', 'rem', 'rna')
			
			return render(request,
				'TriplexDB/search_rna_results_values.html',
				{'result':triplexes,
	 			'rna_symbol': rna_symbol,
				})

	else:
			return render(request,
				'TriplexDB/search_rna_results_values.html',
				{})

def search_rna_symbol(request):
	if request.method == "POST":
			rna_symbol = request.POST['rna_symbol']
			result = triplexaligner.objects.filter(rna__transcriptgenesymbol=rna_symbol).exclude(rem__remsymbols=rna_symbol).order_by('triplexalignere')[:50]
			#result = Triplexaligner.objects.filter(rna__transcriptgenesymbol=rna_symbol).exclude(promoter__promotersymbols=rna_symbol).order_by('triplexalignere')[:50]

			return render(request,
				'TriplexDB/search_rna_results.html',
				{'rna_symbol':rna_symbol,
				'result':result})

	else:
			return render(request,
				'TriplexDB/search_rna_results.html',
				{})


def search_rna_home(request):
	return render(request, 'TriplexDB/search_rna_home.html', {})

def search_gen_region_home(request):
	chrs = ["chr1", "chr2", "chr3", "chr4", "chr5", "chr6","chr7", "chr8", "chr9","chr10", "chr11", "chr12",\
            "chr13", "chr14", "chr15","chr16", "chr17", "chr18","chr19", "chr20", "chr21","chrX", "chrY"]
	return render(request, 'TriplexDB/search_gen_region_home.html', {"chrs": chrs})

def home(request):
	return render(request, 'TriplexDB/home.html', {})
