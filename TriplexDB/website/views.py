from django.shortcuts import render
from .models import Dna as dna
from .models import Rna as rna
from .models import Triplexaligner as triplexaligner
from django_tables2 import SingleTableView
#from .tables import results_table
from django.db.models import Q
from django.http import Http404
from pybedtools import BedTool
from django.templatetags.static import static
from django.views import generic

# Create your views here.
def search_dna_home(request):
	return render(request, 'TriplexDB/search_dna_home.html', {})


def search_dna(request):
	if request.method == "POST":
		dna_symbol = request.POST['dna_symbol']
	triplexes = triplexaligner.objects.filter(dnaid__genesymbol=dna_symbol).distinct().order_by('triplexalignere')\
	.values('rnaid', 'rnatriplexstart', 'rnatriplexend', 'dnatriplexstart', 'dnaid', 'dnatriplexend',\
		'rnalength', 'dnalength', 'triplexalignerscore', 'triplexalignerbitscore', 'triplexalignere')
	rnaids = [triplex['rnaid'] for triplex in triplexes]
	transcripts = rna.objects.filter(rnaid__in=rnaids).values('transcriptid', 'rnaid', 'transcriptgenesymbol')
	if triplexes:
		for triplex in triplexes:
			triplex['transcriptid'] = [rna_instance['transcriptid'] for rna_instance in transcripts\
							if triplex['rnaid'] == rna_instance['rnaid']][0]
			triplex['rna_symbol'] = [rna_instance['transcriptgenesymbol'] for rna_instance in transcripts\
							if triplex['rnaid'] == rna_instance['rnaid']][0]

		
		return render(request,
			'TriplexDB/search_dna_results_values.html',
			{'result':triplexes,
			'dna_symbol': dna_symbol})

	else:
		return render(request,
			'TriplexDB/search_dna_results_values.html',
			{})

def search_rna_results(request):
	return render(request, 'TriplexDB/search_rna_results.html', {})


def search_transcript_values(request):
	if request.method == "POST":
		transcript = request.POST['transcript']
		rna_result = rna.objects.filter(transcriptid__exact = transcript).distinct().values('transcriptgenesymbol')
		if rna_result:
			rna_result = rna_result[0]
		triplexes = triplexaligner.objects.filter(Q(rnaid__transcriptid__exact=transcript)).distinct().order_by('triplexalignere')\
		.values('rnaid', 'rnatriplexstart', 'rnatriplexend', 'dnatriplexstart', 'dnaid', 'dnatriplexend',\
			'rnalength', 'dnalength', 'triplexalignerscore', 'triplexalignerbitscore', 'triplexalignere')
		dna_id = [triplex['dnaid'] for triplex in triplexes]
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
		dnas_to_exclude = dna.objects.filter(genesymbol__exact = rna_symbol).values('dnaid')
		dnas_to_exclude = [dna_instance['dnaid'] for dna_instance in dnas_to_exclude]
		transcripts = rna.objects.filter(transcriptgenesymbol__exact=rna_symbol).values('transcriptid', 'rnaid')
		transcript_ids = [tid['transcriptid'] for tid in transcripts]
		triplexes = triplexaligner.objects.filter(Q(rnaid__transcriptid__in=transcript_ids))\
		.exclude(Q(dnaid__in=dnas_to_exclude)).order_by('triplexalignere')\
		.values('rnaid', 'rnatriplexstart', 'rnatriplexend', 'dnatriplexstart', 'dnaid', 'dnatriplexend',\
			'rnalength', 'dnalength', 'triplexalignerscore', 'triplexalignerbitscore', 'triplexalignere')
		dna_ids = [triplex['dnaid'] for triplex in triplexes]
		dna_result = dna.objects.filter(dnaid__in = dna_ids).distinct().values('genesymbol', 'dnaid')
		for triplex in triplexes:
			triplex['dnagenesymbol'] = [dna_instance['genesymbol'] for dna_instance in dna_result\
							 if triplex['dnaid'] == dna_instance['dnaid']][0]
			triplex['transcriptid'] = [rna_instance['transcriptid'] for rna_instance in transcripts\
							 if triplex['rnaid'] == rna_instance['rnaid']][0]
			
		
		return render(request,
			'TriplexDB/search_rna_results_values.html',
			{'result':triplexes,
			'rna_symbol': rna_symbol,
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

def get_bed(chromosome, start, end):
	bed_string = chromosome + "\t" + start + "\t" + end + "\n"
	query_region = BedTool(bed_string, from_string=True)
	return query_region

def gen_region_search(query_bedtool):
	dna_regions = BedTool('/Users/christina/Documents/triplex/TriplexDB/website/static/dna_regions.bed')
	dna_query_intersection = dna_regions.intersect(query_bedtool, wa = True, f = 0.5)
	dna_query_list = []
	for dna_instance in dna_query_intersection:
		print(dna_instance.name)
		dna_query_list.append(dna_instance.name)

	triplexes = triplexaligner.objects.filter(Q(dnaid__in=dna_query_list))\
	.values('triplexid','rnaid', 'rnatriplexstart', 'rnatriplexend', 'dnatriplexstart', 'dnaid', 'dnatriplexend',\
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
		return render(request, 'TriplexDB/search_genomic_region_results_values.html', {'result': triplexes_in_region})
	elif request.method == 'GET':
		start = request.GET.get('start')
		end =  request.GET.get('end')
		chromosome = request.GET.get('chromosome')
		if start and end and chromosome:
			if int(end)-int(start) < 1000000000:
				query_region = get_bed(chromosome, start, end)
				triplexes_in_region = gen_region_search(query_region)
				return render(request, 'TriplexDB/search_genomic_region_results_values.html', {'result': triplexes_in_region,\
																				   'chr':chromosome, 'start': start, 'end':end})
			else:
				raise Http404("Queried genomic region too big!")
			
		else:
			raise Http404("Start, end or chromosome missing!")
	else:
		raise Http404("GET method error")


def home(request):
	return render(request, 'TriplexDB/home.html', {})


def gene_detail(request, pk):
	rna_result = rna.objects.filter(transcriptgenesymbol__exact = pk).distinct().order_by('transcripttriplexcount').values()
	high_triplex_rna = rna_result[0]['transcriptid']
	plot_path = 'transcript_plots/' + high_triplex_rna + '.png'
	return render(request, 'TriplexDB/gene_detail.html' , {'object': rna_result, 'plot_path': plot_path})

