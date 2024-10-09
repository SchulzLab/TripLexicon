from django.shortcuts import render
from .models import Dna as dna
from .models import Rna as rna
from .models import Triplexaligner as triplexaligner
from django_tables2 import SingleTableView
#from .tables import results_table
from django.db.models import Q
#from django.http import Http404
from pybedtools import BedTool
from django.templatetags.static import static
from django.views import generic
import time
import logging
import regex as re

#get logger for my app website
logger = logging.getLogger('website')


# Create your views here.
def search_dna_home(request):
	return render(request, 'TriplexDB/search_dna_home_mouse.html', {})

def search_dna_mouse(request):
	if request.method == 'GET':
		species = request.GET.get('species')
		dna_symbol = request.GET.get('dna_symbol')
		if not dna_symbol[0].isdigit() and 'Rik' not in dna_symbol:
			dna_symbol = dna_symbol.capitalize()
		if species == 'Human':
			mouse = False
			dna_symbol = dna_symbol.upper()
			filter_dna_id = list(dna.objects.filter(genesymbol__exact=dna_symbol).values_list('dnaid', flat=True))
			triplexes = triplexaligner.objects.filter(Q(dnaid__in=filter_dna_id)).distinct().order_by('triplexalignere')\
			.values('rnaid', 'rnatriplexstart', 'rnatriplexend', 'genometriplexchr',
				'genometriplexstart', 'genometriplexend',
				'rnalength', 'dnalength', 'triplexalignerscore', 'triplexalignerbitscore', 'triplexalignere')
			nr_triplexes = triplexes.count()
			rnaids = [triplex['rnaid'] for triplex in triplexes]
			nr_rnas = len(set(rnaids))
			transcripts = rna.objects.filter(rnaid__in=rnaids).values('transcriptid', 'rnaid', 'transcriptgenesymbol')

		elif species == 'Mouse':
			mouse = True
			if dna_symbol.startswith('Ensmu'):
				dna_symbol = dna_symbol.upper()
			filter_dna_id = list(dna.objects.using('mouse').filter(Q(genesymbol__exact=dna_symbol)).values_list('dnaid', flat=True))
			triplexes = triplexaligner.objects.using('mouse').filter(Q(dnaid__in=filter_dna_id)).distinct().order_by('triplexalignere')\
			.values('rnaid', 'rnatriplexstart', 'rnatriplexend', 'genometriplexchr',
				'genometriplexstart', 'genometriplexend',
				'rnalength', 'dnalength', 'triplexalignerscore', 'triplexalignerbitscore', 'triplexalignere')
			nr_triplexes = triplexes.count()
			rnaids = [triplex['rnaid'] for triplex in triplexes]
			nr_rnas = len(set(rnaids))
			transcripts = rna.objects.using('mouse').filter(rnaid__in=rnaids).values('transcriptid', 'rnaid', 'transcriptgenesymbol')
			

		if triplexes:
			for triplex in triplexes:
				triplex['transcriptid'] = [rna_instance['transcriptid'] for rna_instance in transcripts\
							if triplex['rnaid'] == rna_instance['rnaid']][0]
				triplex['rna_symbol'] = [rna_instance['transcriptgenesymbol'] for rna_instance in transcripts\
							if triplex['rnaid'] == rna_instance['rnaid']][0]
	
			return render(request,
			'TriplexDB/search_dna_results_values.html',
			{'result':triplexes,
			'nr_triplexes': nr_triplexes,
			'nr_rnas': nr_rnas,
			'dna_symbol': dna_symbol,
			'mouse': mouse,})

		else:
                	return render(request,
                        'TriplexDB/search_dna_results_values.html',
                        {})
	else:
		return render(request,
			'TriplexDB/search_dna_results_values.html',
			{})

def search_rna_results(request):
	return render(request, 'TriplexDB/search_rna_results.html', {})


def search_transcript_values(request):
	if request.method == "POST":
		transcript = request.POST['transcript'].upper()
		rna_result = rna.objects.filter(transcriptid__exact = transcript).distinct().values('transcriptgenesymbol')
		if rna_result:
			rna_result = rna_result[0]
		triplexes = triplexaligner.objects.filter(Q(rnaid__transcriptid__exact=transcript)).distinct().order_by('triplexalignere')\
		.values('rnaid', 'rnatriplexstart', 'rnatriplexend', 'dnaid', 'genometriplexchr', 'genometriplexstart', 'genometriplexend',
			'rnalength', 'dnalength', 'triplexalignerscore', 'triplexalignerbitscore', 'triplexalignere')
		nr_triplexes = len(triplexes)
		dna_id = [triplex['dnaid'] for triplex in triplexes]
		dnas_targeted_by_trans = len(set(dna_id))
		dna_result = dna.objects.filter(dnaid__in = dna_id).values('genesymbol', 'dnaid')
		if triplexes:
			for triplex in triplexes:
				triplex['dnagenesymbol'] = [dna_instance['genesymbol'] for dna_instance in dna_result\
								if triplex['dnaid'] == dna_instance['dnaid']][0]
		
		if triplexes:
			return render(request,
				'TriplexDB/search_rna_results_values.html',
				{'transcript':transcript,
				'result':triplexes,
				'nr_triplexes': nr_triplexes,
				'nr_targets':dnas_targeted_by_trans,
				'rna_symbol': rna_result['transcriptgenesymbol'],
				})
		else:
			return render(request,
                        'TriplexDB/search_rna_results_values.html',
                        {})

	else:
		return render(request,
			'TriplexDB/search_rna_results_values.html',
			{})


def search_rna_symbol_values(request):
	if request.method == 'GET':
		species = request.GET.get('species')
		rna_symbol = request.GET.get('rna_symbol')
		if species == 'Mouse':
			mouse = True
			if not rna_symbol[0].isdigit() and 'Rik' not in rna_symbol:
				rna_symbol = request.POST['rna_symbol'].capitalize()
			dnas_to_exclude = dna.objects.using('mouse').filter(genesymbol__exact = rna_symbol).values('dnaid')
			dnas_to_exclude = [dna_instance['dnaid'] for dna_instance in dnas_to_exclude]
			transcripts = rna.objects.using('mouse').filter(transcriptgenesymbol__exact=rna_symbol).values('transcriptid', 'rnaid')
			transcript_ids = [tid['transcriptid'] for tid in transcripts]
			triplexes = triplexaligner.objects.using('mouse').filter(Q(rnaid__transcriptid__in=transcript_ids))\
			.exclude(Q(dnaid__in=dnas_to_exclude)).order_by('triplexalignere')\
			.values('rnaid', 'rnatriplexstart', 'rnatriplexend', 'dnaid', 'genometriplexchr', 'genometriplexstart', 'genometriplexend',
				'rnalength', 'dnalength', 'triplexalignerscore', 'triplexalignerbitscore', 'triplexalignere')
			nr_triplexes = len(triplexes)
			dna_ids = [triplex['dnaid'] for triplex in triplexes]
			dnas_targeted_by_trans = len(set(dna_ids))
			dna_result = dna.objects.using('mouse').filter(dnaid__in = dna_ids).distinct().values('genesymbol', 'dnaid')
		elif species == 'Human':
			mouse = False
			rna_symbol = rna_symbol.upper()
			dnas_to_exclude = dna.objects.filter(genesymbol__exact = rna_symbol).values('dnaid')
			dnas_to_exclude = [dna_instance['dnaid'] for dna_instance in dnas_to_exclude]
			transcripts = rna.objects.filter(transcriptgenesymbol__exact=rna_symbol).values('transcriptid', 'rnaid')
			transcript_ids = [tid['transcriptid'] for tid in transcripts]
			triplexes = triplexaligner.objects.filter(Q(rnaid__transcriptid__in=transcript_ids))\
			.exclude(Q(dnaid__in=dnas_to_exclude)).order_by('triplexalignere')\
			.values('rnaid', 'rnatriplexstart', 'rnatriplexend', 'dnaid', 'genometriplexchr', 'genometriplexstart', 'genometriplexend',
				'rnalength', 'dnalength', 'triplexalignerscore', 'triplexalignerbitscore', 'triplexalignere')
			nr_triplexes = len(triplexes)
			dna_ids = [triplex['dnaid'] for triplex in triplexes]
			dnas_targeted_by_trans = len(set(dna_ids))
			dna_result = dna.objects.filter(dnaid__in = dna_ids).distinct().values('genesymbol', 'dnaid')
		if triplexes:
			for triplex in triplexes:
				triplex['dnagenesymbol'] = [dna_instance['genesymbol'] for dna_instance in dna_result\
							 if triplex['dnaid'] == dna_instance['dnaid']][0]
				triplex['transcriptid'] = [rna_instance['transcriptid'] for rna_instance in transcripts\
							 if triplex['rnaid'] == rna_instance['rnaid']][0]
			
		
			return render(request,
				'TriplexDB/search_rna_results_values.html',
				{'result':triplexes,
				'nr_triplexes': nr_triplexes,
				'nr_targets':dnas_targeted_by_trans,
				'rna_symbol': rna_symbol,
				'mouse': mouse,
				})
		else:
			return render(request,
                        'TriplexDB/search_rna_results_values.html',
                        {})

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

def get_bed(chromosome, start, end):
	bed_string = chromosome + "\t" + start + "\t" + end + "\n"
	query_region = BedTool(bed_string, from_string=True)
	return query_region

def gen_region_search(query_bedtool):
	dna_regions = BedTool('website/static/dna_regions.bed')
	dna_query_list = []
	try:
		dna_query_intersection = dna_regions.intersect(query_bedtool, wa = True, f = 0.5)
		for dna_instance in dna_query_intersection:
			dna_query_list.append(dna_instance.name)
	except:
		return None

	triplexes = triplexaligner.objects.filter(Q(dnaid__in=dna_query_list))\
	.values('triplexid','rnaid', 'rnatriplexstart', 'rnatriplexend', 'dnaid', 'genometriplexchr', 'genometriplexstart', 'genometriplexend',
				'rnalength', 'dnalength', 'triplexalignerscore', 'triplexalignerbitscore', 'triplexalignere')
	#query RNA objects
	rna_ids = [triplex['rnaid'] for triplex in triplexes]
	transcript_gene_symbols = rna.objects.filter(rnaid__in = rna_ids).distinct().values('transcriptgenesymbol', 'transcriptid', 'rnaid')

	#query REMs, new rem ids, only the ones having triplexes
	dna_ids = [triplex['dnaid'] for triplex in triplexes]
	dna_result = dna.objects.filter(dnaid__in = dna_ids).distinct().values('genesymbol', 'dnaid')
	for triplex in triplexes:
			triplex['transcriptgenesymbol'] = [rna_instance['transcriptgenesymbol'] for rna_instance in transcript_gene_symbols\
							 if triplex['rnaid'] == rna_instance['rnaid']][0]
			triplex['transcriptid'] = [rna_instance['transcriptid'] for rna_instance in transcript_gene_symbols\
							 if triplex['rnaid'] == rna_instance['rnaid']][0]
			triplex['dnagenesymbol'] = [dna_instance['genesymbol'] for dna_instance in dna_result\
							 if triplex['dnaid'] == dna_instance['dnaid']][0]
	return triplexes




def gen_region_search_file(uploaded_file):
	uploaded_regions = uploaded_file.read().decode('utf-8').splitlines()
	bed_string = ""
	for interval in uploaded_regions:
		if "chr" in interval:
			subset_start = interval.find("chr")
			#print(interval[subset_start:].strip("\\\n")+"\n")
			bed_string += interval[subset_start:].strip("\\\n")+"\n"
	uploaded_regions = BedTool(bed_string, from_string = True)
	return uploaded_regions

def search_gen_region_results(request):
	if request.method =='POST':
		uploaded_file = request.FILES['bed_file']
		#uploaded_file_content = do_th_with_file_to_get_content_as_String(uploaded_file)
		query_regions = gen_region_search_file(uploaded_file)
		triplexes_in_region = gen_region_search(query_regions)
		return render(request, 'TriplexDB/search_genomic_region_results_values.html', {'result': triplexes_in_region,
												'nr_triplexes': len(triplexes_in_region)})
	elif request.method == 'GET':
		start = request.GET.get('start')
		end =  request.GET.get('end')
		chromosome = request.GET.get('chromosome')
		if start and end and chromosome:
			try:
				if int(end)-int(start) < 1000000000:
					query_region = get_bed(chromosome, start, end)
					triplexes_in_region = gen_region_search(query_region)
					return render(request, 'TriplexDB/search_genomic_region_results_values.html', {'result': triplexes_in_region,
														'nr_triplexes': len(triplexes_in_region),
														   'chr':chromosome, 'start': start, 'end':end})
				else:
					return render(request, 'TriplexDB/search_genomic_region_results_values.html', {'to_large': True})
			except:
				return render(request, 'TriplexDB/search_genomic_region_results_values.html', {'to_large': True})
		else:
			return render(request, 'TriplexDB/search_genomic_region_results_values.html', {'incomplete_region': True})
			#raise Http404("Start, end or chromosome missing!")
	else:
		#raise Http404("GET method error")
		return render(request, 'TriplexDB/search_genomic_region_results_values.html', {})

def home(request):
	return render(request, 'TriplexDB/home.html', {})


def gene_detail(request, pk):
	try:
		rna_result = rna.objects.using('mouse').filter(transcriptgenesymbol__exact = pk).distinct().order_by('transcripttriplexcount').values()[::-1]
		if len(rna_result) > 0:
			mouse = True
			nr_triplexes = [rna['transcripttriplexcount'] for rna in rna_result]
			nr_triplexes = sum(nr_triplexes)
			high_triplex_rna = rna_result[0]['transcriptid']
			plot_path = 'transcript_plots_mouse/' + high_triplex_rna + '.png'
		else:
			mouse = False
			rna_result = rna.objects.filter(transcriptgenesymbol__exact = pk).distinct().order_by('transcripttriplexcount').values()[::-1]
			nr_triplexes = [rna['transcripttriplexcount'] for rna in rna_result]
			nr_triplexes = sum(nr_triplexes)
			high_triplex_rna = rna_result[0]['transcriptid']
			plot_path = 'transcript_plots/' + high_triplex_rna + '.png'
		return render(request, 'TriplexDB/gene_detail.html' , {'object': rna_result,
														    'plot_path': plot_path,
														    'nr_triplexes': nr_triplexes, 
															'gene': pk,
															'mouse': mouse})
	except:
		return render(request, 'TriplexDB/gene_detail.html' , {})


def gene_detail_search(request):
	if request.method =='GET':
		try:
			species = request.GET.get('species')
			gene_symbol = request.GET.get('gene_symbol')
			if not gene_symbol[0].isdigit() and 'Rik' not in gene_symbol:
				gene_symbol = gene_symbol.capitalize()
			if gene_symbol.startswith('ENS'):
				gene_symbol = gene_symbol.upper()
			if species == 'Mouse':
				rna_result = rna.objects.using('mouse').filter(transcriptgenesymbol__exact = gene_symbol).distinct().order_by('transcripttriplexcount').values()[::-1]
				mouse = True
			else:
				gene_symbol = gene_symbol.upper()
				rna_result = rna.objects.filter(transcriptgenesymbol__exact = gene_symbol).distinct().order_by('transcripttriplexcount').values()[::-1]
				mouse = False
			nr_triplexes = [rna['transcripttriplexcount'] for rna in rna_result]
			nr_triplexes = sum(nr_triplexes)
			if len(rna_result) > 0:
				high_triplex_rna = rna_result[0]['transcriptid']
				if mouse == False:
					plot_path = 'transcript_plots/' + high_triplex_rna + '.png'
				else:
					plot_path = 'transcript_plots_mouse/' + high_triplex_rna + '.png'
				return render(request, 'TriplexDB/gene_detail.html' , {'object': rna_result,
														    'plot_path': plot_path,
															'gene': gene_symbol,
															'nr_triplexes': nr_triplexes,
															'mouse': mouse,
															})
			else:
		 		return render(request, 'TriplexDB/gene_detail.html' , {})
		except:
			return render(request, 'TriplexDB/gene_detail.html' , {})




def transcript_detail(request, pk):
	if pk.startswith('ENSMU'):
		mouse = True
		rna_result = rna.objects.using('mouse').filter(transcriptid__exact = pk).distinct().order_by('transcripttriplexcount').values()
		plot_path = 'transcript_plots_mouse/' + pk + '.png'
	else:
		mouse = False
		rna_result = rna.objects.filter(transcriptid__exact = pk).distinct().order_by('transcripttriplexcount').values()
		plot_path = 'transcript_plots/' + pk + '.png'
	return render(request, 'TriplexDB/transcript_detail.html' , {'object': rna_result,
															    'plot_path': plot_path,
																'transcript': pk,
																'mouse': mouse,
																})


