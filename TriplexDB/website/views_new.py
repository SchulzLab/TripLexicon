import os
from django.shortcuts import render, redirect
from .models import Dna as dna
from .models import Rna as rna
from .models import Triplexaligner as triplexaligner
from django.http import HttpResponse
from django.db.models import Q
from pybedtools import BedTool
import uuid
import logging
import pandas as pd


from django.db.models import OuterRef, Subquery
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .GOEnrichment import go_enrichment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# get logger for my app website
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
            dna_symbol = dna_symbol.strip().upper()
            filter_dna_id = list(
                dna.objects.filter(
                    (Q(genesymbol__exact=dna_symbol) | Q(geneid__exact=dna_symbol))
                ).values_list('dnaid', flat=True)
            )
            triplexes = (
                triplexaligner.objects.filter(Q(dnaid__in=filter_dna_id))
                .distinct()
                .order_by('triplexalignere')
                .values(
                    'rnaid',
                    'rnatriplexstart',
                    'rnatriplexend',
                    'genometriplexchr',
                    'genometriplexstart',
                    'genometriplexend',
                    'rnalength',
                    'dnalength',
                    'triplexalignerscore',
                    'triplexalignerbitscore',
                    'triplexalignere',
                )
            )

            nr_triplexes = triplexes.count()
            rnaids = [triplex['rnaid'] for triplex in triplexes]
            nr_rnas = len(set(rnaids))
            transcripts = rna.objects.filter(rnaid__in=rnaids).values(
                'transcriptid', 'rnaid', 'transcriptgenesymbol'
            )

        elif species == 'Mouse':
            mouse = True
            if dna_symbol.startswith('Ensmu'):
                dna_symbol = dna_symbol.strip().upper()
            filter_dna_id = list(
                dna.objects.using('mouse')
                .filter(Q(genesymbol__exact=dna_symbol) | Q(geneid__exact=dna_symbol))
                .values_list('dnaid', flat=True)
            )

            triplexes = (
                triplexaligner.objects.using('mouse')
                .filter(Q(dnaid__in=filter_dna_id))
                .distinct()
                .order_by('triplexalignere')
                .values(
                    'rnaid',
                    'rnatriplexstart',
                    'rnatriplexend',
                    'genometriplexchr',
                    'genometriplexstart',
                    'genometriplexend',
                    'rnalength',
                    'dnalength',
                    'triplexalignerscore',
                    'triplexalignerbitscore',
                    'triplexalignere',
                )
            )

            nr_triplexes = triplexes.count()
            rnaids = [triplex['rnaid'] for triplex in triplexes]
            nr_rnas = len(set(rnaids))
            transcripts = (
                rna.objects.using('mouse')
                .filter(rnaid__in=rnaids)
                .values('transcriptid', 'rnaid', 'transcriptgenesymbol')
            )

        if triplexes:
            for triplex in triplexes:
                triplex['transcriptid'] = [
                    rna_instance['transcriptid']
                    for rna_instance in transcripts
                    if triplex['rnaid'] == rna_instance['rnaid']
                ][0]
                triplex['rna_symbol'] = [
                    rna_instance['transcriptgenesymbol']
                    for rna_instance in transcripts
                    if triplex['rnaid'] == rna_instance['rnaid']
                ][0]

            return render(
                request,
                'TriplexDB/search_dna_results_values.html',
                {
                    'result': triplexes,
                    'nr_triplexes': nr_triplexes,
                    'nr_rnas': nr_rnas,
                    'dna_symbol': dna_symbol,
                    'mouse': mouse,
                },
            )

        else:
            return render(request, 'TriplexDB/search_dna_results_values.html', {})
    else:
        return render(request, 'TriplexDB/search_dna_results_values.html', {})


def search_rna_results(request):
    return render(request, 'TriplexDB/search_rna_results.html', {})


def search_transcript_values(request):
    if request.method == 'GET':
        species = request.GET.get('species')
        transcript = request.GET.get('transcript').strip().upper()
        if species == 'Mouse':
            mouse = True
            rna_result = (
                rna.objects.using('mouse')
                .filter(transcriptid__exact=transcript)
                .distinct()
                .values('transcriptgenesymbol')
            )
        else:
            mouse = False
            rna_result = (
                rna.objects.filter(transcriptid__exact=transcript)
                .distinct()
                .values('transcriptgenesymbol')
            )
        if rna_result:
            rna_result = rna_result[0]
        if mouse:
            triplexes = (
                triplexaligner.objects.using('mouse')
                .filter(Q(rnaid__transcriptid__exact=transcript))
                .distinct()
                .order_by('triplexalignere')
                .values(
                    'rnaid',
                    'rnatriplexstart',
                    'rnatriplexend',
                    'dnaid',
                    'genometriplexchr',
                    'genometriplexstart',
                    'genometriplexend',
                    'rnalength',
                    'dnalength',
                    'triplexalignerscore',
                    'triplexalignerbitscore',
                    'triplexalignere',
                )
                .annotate(
                dnagenesymbol=Subquery(
                dna.objects.filter(dnaid=OuterRef('dnaid')).values('genesymbol', 'genebiotype')[:1]
                )
                )
            )
            
        else:
            triplexes = (
                triplexaligner.objects.filter(Q(rnaid__transcriptid__exact=transcript))
                .distinct()
                .order_by('triplexalignere')
                .values(
                    'rnaid',
                    'rnatriplexstart',
                    'rnatriplexend',
                    'dnaid',
                    'genometriplexchr',
                    'genometriplexstart',
                    'genometriplexend',
                    'rnalength',
                    'dnalength',
                    'triplexalignerscore',
                    'triplexalignerbitscore',
                    'triplexalignere',
                )
                .annotate(
                dnagenesymbol=Subquery(
                dna.objects.filter(dnaid=OuterRef('dnaid')).values('genesymbol', 'genebiotype')[:1]
                )
                )
            )


        if triplexes:
            nr_triplexes = len(triplexes)
            if nr_triplexes > 10000:
                 triplexes = triplexes[:10000]
            dnaids = set([triplex['dnaid'] for triplex in triplexes])
            dnas_targeted_by_trans = len(dnaids)
            protein_coding_triplexes = [triplex for triplex in triplexes if triplex['genebiotype'] == 'protein_coding']
            toptriplexes = sorted(protein_coding_triplexes, key=lambda x: x['triplexalignere'], reverse=True)[:1000]
            top_dnagenesymbols = [triplex['dnagenesymbol'] for triplex in toptriplexes]
            dna_genes = [triplex['dnagenesymbol'] for triplex in triplexes if triplex['genebiotype'] == 'protein_coding']

            if len(dna_genes) > 1000:
                dna_genes = dna_genes[:1000]

            return render(
                request,
                'TriplexDB/search_rna_results_values.html',
                {
                    'transcript': transcript,
                    'result': triplexes,
                    'nr_triplexes': nr_triplexes,
                    'nr_targets': dnas_targeted_by_trans,
                    'rna_symbol': rna_result['transcriptgenesymbol'],
                    'mouse': mouse,
                    'go_genes': dna_genes,
                },
            )
        else:
            return render(request, 'TriplexDB/search_rna_results_values.html', {})

    else:
        return render(request, 'TriplexDB/search_rna_results_values.html', {})


def search_rna_symbol_values(request):
    if request.method == 'GET':
        species = request.GET.get('species')
        rna_symbol = request.GET.get('rna_symbol').strip()
        if species == 'Mouse':
            mouse = True
            if not rna_symbol[0].isdigit() and 'Rik' not in rna_symbol:
                rna_symbol = rna_symbol.capitalize()
            # dnas_to_exclude = dna.objects.using('mouse').filter(Q(transcriptgenesymbol__exact = rna_symbol) | Q(transcriptgeneid__exact=rna_symbol)).values('dnaid')
            # dnas_to_exclude = [dna_instance['dnaid'] for dna_instance in dnas_to_exclude]
            transcripts = (
                rna.objects.using('mouse')
                .filter(
                    Q(transcriptgenesymbol__exact=rna_symbol)
                    | Q(transcriptgeneid__exact=rna_symbol)
                )
                .values('transcriptid', 'rnaid')
            )
            # transcript_ids = [tid['transcriptid'] for tid in transcripts]
            rnaids = [rnaid['rnaid'] for rnaid in transcripts]
            triplexes = (
                triplexaligner.objects.using('mouse')
                .filter(Q(rnaid__in=rnaids))
                .order_by('triplexalignere')
                .values(
                    'rnaid',
                    'rnatriplexstart',
                    'rnatriplexend',
                    'dnaid',
                    'genometriplexchr',
                    'genometriplexstart',
                    'genometriplexend',
                    'rnalength',
                    'dnalength',
                    'triplexalignerscore',
                    'triplexalignerbitscore',
                    'triplexalignere',
                )
                .annotate(
                dnagenesymbol=Subquery(
                dna.objects.filter(dnaid=OuterRef('dnaid')).values('genesymbol')[:1]
                )
                )
                .annotate(
                transcriptid=Subquery(
                rna.objects.filter(rnaid=OuterRef('rnaid')).values('transcriptid')[:1]
                )
                )
            )
            # .exclude(Q(dnaid__in=dnas_to_exclude))

            nr_triplexes = len(triplexes)

        elif species == 'Human':
            mouse = False
            rna_symbol = rna_symbol.upper()
            # dnas_to_exclude = dna.objects.filter(Q(transcriptgenesymbol__exact = rna_symbol) | Q(transcriptgeneid__exact=rna_symbol)).values('dnaid')
            # dnas_to_exclude = [dna_instance['dnaid'] for dna_instance in dnas_to_exclude]
            transcripts = rna.objects.filter(
                Q(transcriptgenesymbol__exact=rna_symbol)
                | Q(transcriptgeneid__exact=rna_symbol)
            ).values('transcriptid', 'rnaid')
            # transcript_ids = [tid['transcriptid'] for tid in transcripts]
            rnaids = [rnaid['rnaid'] for rnaid in transcripts]
            triplexes = (
                triplexaligner.objects.filter(Q(rnaid__in=rnaids))
                .order_by('triplexalignere')
                .values(
                    'rnaid',
                    'rnatriplexstart',
                    'rnatriplexend',
                    'dnaid',
                    'genometriplexchr',
                    'genometriplexstart',
                    'genometriplexend',
                    'rnalength',
                    'dnalength',
                    'triplexalignerscore',
                    'triplexalignerbitscore',
                    'triplexalignere',
                )
                .annotate(
                dnagenesymbol=Subquery(
                dna.objects.filter(dnaid=OuterRef('dnaid')).values('genesymbol')[:1]
                )
                )
               .annotate(
                transcriptid=Subquery(
                rna.objects.filter(rnaid=OuterRef('rnaid')).values('transcriptid')[:1]
                )
                )
            )

            nr_triplexes = len(triplexes)
            if nr_triplexes > 10000:
                 triplexes = triplexes[:10000]

        if triplexes:
            dna_genes = [triplex['dnagenesymbol'] for triplex in triplexes]
            if len(dna_genes) > 1000:
                dna_genes = dna_genes[:1000]
            dnaids = set([triplex['dnaid'] for triplex in triplexes])
            dnas_targeted_by_trans = len(dnaids)
            return render(
                request,
                'TriplexDB/search_rna_results_values.html',
                {
                    'result': triplexes,
                    'nr_triplexes': nr_triplexes,
                    'nr_targets': dnas_targeted_by_trans,
                    'rna_symbol': rna_symbol,
                    'mouse': mouse,
                    'go_genes': dna_genes,
                },
            )
        else:
            return render(request, 'TriplexDB/search_rna_results_values.html', {})

    else:
        return render(request, 'TriplexDB/search_rna_results_values.html', {})


def search_rna_home(request):
    return render(request, 'TriplexDB/search_rna_home.html', {})


def search_gen_region_home(request):
    chrs = [
        'chr1',
        'chr2',
        'chr3',
        'chr4',
        'chr5',
        'chr6',
        'chr7',
        'chr8',
        'chr9',
        'chr10',
        'chr11',
        'chr12',
        'chr13',
        'chr14',
        'chr15',
        'chr16',
        'chr17',
        'chr18',
        'chr19',
        'chr20',
        'chr21',
        'chrX',
        'chrY',
    ]
    return render(request, 'TriplexDB/search_gen_region_home.html', {'chrs': chrs})


def get_bed(chromosome, start, end):
    bed_string = chromosome + '\t' + start + '\t' + end + '\n'
    query_region = BedTool(bed_string, from_string=True)
    return query_region


def gen_region_search(query_bedtool, mouse=False):
    if mouse:
        dna_regions = BedTool('website/static/dna_mouse_regions_enhancers.bed')
    else:
        dna_regions = BedTool('website/static/dna_regions.bed')
    dna_query_list = []
    try:
        dna_query_intersection = dna_regions.intersect(query_bedtool, wa=True, f=0.5)
        for dna_instance in dna_query_intersection:
            dna_query_list.append(dna_instance.name)
    except:
        return None
    if mouse:
        triplexes = (
            triplexaligner.objects.using('mouse')
            .filter(Q(dnaid__in=dna_query_list))
            .values(
                'triplexid',
                'rnaid',
                'rnatriplexstart',
                'rnatriplexend',
                'dnaid',
                'genometriplexchr',
                'genometriplexstart',
                'genometriplexend',
                'rnalength',
                'dnalength',
                'triplexalignerscore',
                'triplexalignerbitscore',
                'triplexalignere',
            )
        )
        # query RNA objects
        rna_ids = [triplex['rnaid'] for triplex in triplexes]
        transcript_gene_symbols = (
            rna.objects.using('mouse')
            .filter(rnaid__in=rna_ids)
            .distinct()
            .values('transcriptgenesymbol', 'transcriptid', 'rnaid')
        )

        # query REMs, new rem ids, only the ones having triplexes
        dna_ids = [triplex['dnaid'] for triplex in triplexes]
        dna_result = (
            dna.objects.using('mouse')
            .filter(dnaid__in=dna_ids)
            .distinct()
            .values('genesymbol', 'dnaid')
        )
    else:
        triplexes = triplexaligner.objects.filter(Q(dnaid__in=dna_query_list)).values(
            'triplexid',
            'rnaid',
            'rnatriplexstart',
            'rnatriplexend',
            'dnaid',
            'genometriplexchr',
            'genometriplexstart',
            'genometriplexend',
            'rnalength',
            'dnalength',
            'triplexalignerscore',
            'triplexalignerbitscore',
            'triplexalignere',
        )
        # query RNA objects
        rna_ids = [triplex['rnaid'] for triplex in triplexes]
        transcript_gene_symbols = (
            rna.objects.filter(rnaid__in=rna_ids)
            .distinct()
            .values('transcriptgenesymbol', 'transcriptid', 'rnaid')
        )

        # query REMs, new rem ids, only the ones having triplexes
        dna_ids = [triplex['dnaid'] for triplex in triplexes]
        dna_result = (
            dna.objects.filter(dnaid__in=dna_ids)
            .distinct()
            .values('genesymbol', 'dnaid')
        )

    for triplex in triplexes:
        triplex['transcriptgenesymbol'] = [
            rna_instance['transcriptgenesymbol']
            for rna_instance in transcript_gene_symbols
            if triplex['rnaid'] == rna_instance['rnaid']
        ][0]
        triplex['transcriptid'] = [
            rna_instance['transcriptid']
            for rna_instance in transcript_gene_symbols
            if triplex['rnaid'] == rna_instance['rnaid']
        ][0]
        triplex['dnagenesymbol'] = [
            dna_instance['genesymbol']
            for dna_instance in dna_result
            if triplex['dnaid'] == dna_instance['dnaid']
        ][0]
    return triplexes


def gen_region_search_file(uploaded_file):
    uploaded_regions = uploaded_file.read().decode('utf-8').splitlines()
    bed_string = ''
    for interval in uploaded_regions:
        if 'chr' in interval:
            subset_start = interval.find('chr')
            # print(interval[subset_start:].strip('\\\n')+'\n')
            bed_string += interval[subset_start:].strip('\\\n') + '\n'
    uploaded_regions = BedTool(bed_string, from_string=True)
    print(bed_string)
    return uploaded_regions


def search_gen_region_results(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['bed_file']
        species = request.POST.get('species')
        if uploaded_file:
            if species == 'Mouse':
                mouse = True
            else:
                mouse = False
            query_regions = gen_region_search_file(uploaded_file)
            triplexes_in_region = gen_region_search(query_regions, mouse)
            return render(
                request,
                'TriplexDB/search_genomic_region_results_values.html',
                {
                    'result': triplexes_in_region,
                    'nr_triplexes': len(triplexes_in_region),
                    'mouse': mouse,
                },
            )

    elif request.method == 'GET':
        species = request.GET.get('species')
        start = request.GET.get('start').strip()
        end = request.GET.get('end').strip()
        chromosome = request.GET.get('chromosome')
        if start and end and chromosome:
            try:
                if int(end) - int(start) < 1000000000:
                    query_region = get_bed(chromosome, start, end)
                    if species == 'Mouse':
                        mouse = True
                        triplexes_in_region = gen_region_search(query_region, mouse)
                    else:
                        triplexes_in_region = gen_region_search(query_region)
                        mouse = False
                    if triplexes_in_region:
                        return render(
                            request,
                            'TriplexDB/search_genomic_region_results_values.html',
                            {
                                'result': triplexes_in_region,
                                'nr_triplexes': len(triplexes_in_region),
                                'chr': chromosome,
                                'start': start,
                                'end': end,
                                'mouse': mouse,
                            },
                        )
                    else:
                        # raise Http404('GET method error')
                        return render(
                            request,
                            'TriplexDB/search_genomic_region_results_values.html',
                            {},
                        )

                else:
                    return render(
                        request,
                        'TriplexDB/search_genomic_region_results_values.html',
                        {'to_large': True},
                    )
            except:
                return render(
                    request,
                    'TriplexDB/search_genomic_region_results_values.html',
                    {'to_large': True},
                )
        else:
            return render(
                request,
                'TriplexDB/search_genomic_region_results_values.html',
                {'incomplete_region': True},
            )
            # raise Http404('Start, end or chromosome missing!')
    else:
        # raise Http404('GET method error')
        return render(
            request, 'TriplexDB/search_genomic_region_results_values.html', {}
        )


def home(request):
    return render(request, 'TriplexDB/home.html', {})


def gene_detail(request, pk):
    try:
        rna_result = (
            rna.objects.using('mouse')
            .filter(transcriptgenesymbol__exact=pk)
            .distinct()
            .order_by('transcripttriplexcount')
            .values()[::-1]
        )
        if len(rna_result) > 0:
            mouse = True
            nr_triplexes = [rna['transcripttriplexcount'] for rna in rna_result]
            nr_triplexes = sum(nr_triplexes)
            high_triplex_rna = rna_result[0]['transcriptid']
            plot_path = 'transcript_plots_mouse/' + high_triplex_rna + '.png'
            circos_path = 'ggCircos_mm39/' + high_triplex_rna + '.png'
        else:
            mouse = False
            rna_result = (
                rna.objects.filter(transcriptgenesymbol__exact=pk)
                .distinct()
                .order_by('transcripttriplexcount')
                .values()[::-1]
            )
            nr_triplexes = [rna['transcripttriplexcount'] for rna in rna_result]
            nr_triplexes = sum(nr_triplexes)
            high_triplex_rna = rna_result[0]['transcriptid']
            plot_path = 'transcript_plots/' + high_triplex_rna + '.png'
            circos_path = 'ggCircos_hg38/' + high_triplex_rna + '.png'
        return render(
            request,
            'TriplexDB/gene_detail.html',
            {
                'object': rna_result,
                'plot_path': plot_path,
                'nr_triplexes': nr_triplexes,
                'gene': pk,
                'mouse': mouse,
                'circos_path': circos_path,
            },
        )
    except:
        return render(request, 'TriplexDB/gene_detail.html', {})


def gene_detail_search(request):
    if request.method == 'GET':
        try:
            species = request.GET.get('species')
            gene_symbol = request.GET.get('gene_symbol').strip()
            if not gene_symbol[0].isdigit() and 'Rik' not in gene_symbol:
                gene_symbol = gene_symbol.capitalize()
            if gene_symbol.startswith('ENS'):
                gene_symbol = gene_symbol.upper()
            if species == 'Mouse':
                rna_result = (
                    rna.objects.using('mouse')
                    .filter(
                        Q(transcriptgenesymbol__exact=gene_symbol)
                        | Q(transcriptgeneid__exact=gene_symbol)
                    )
                    .distinct()
                    .order_by('transcripttriplexcount')
                    .values()[::-1]
                )
                mouse = True
            else:
                gene_symbol = gene_symbol.upper()
                rna_result = (
                    rna.objects.filter(
                        Q(transcriptgenesymbol__exact=gene_symbol)
                        | Q(transcriptgeneid__exact=gene_symbol)
                    )
                    .distinct()
                    .order_by('transcripttriplexcount')
                    .values()[::-1]
                )
                mouse = False
            nr_triplexes = [rna['transcripttriplexcount'] for rna in rna_result]
            nr_triplexes = sum(nr_triplexes)
            if len(rna_result) > 0:
                high_triplex_rna = rna_result[0]['transcriptid']
                if mouse == False:
                    plot_path = 'transcript_plots/' + high_triplex_rna + '.png'
                    circos_path = 'ggCircos_hg38/' + high_triplex_rna + '.png'
                else:
                    plot_path = 'transcript_plots_mouse/' + high_triplex_rna + '.png'
                    circos_path = 'ggCircos_mm39/' + high_triplex_rna + '.png'
                return render(
                    request,
                    'TriplexDB/gene_detail.html',
                    {
                        'object': rna_result,
                        'plot_path': plot_path,
                        'gene': gene_symbol,
                        'nr_triplexes': nr_triplexes,
                        'mouse': mouse,
                        'circos_path': circos_path,
                    },
                )
            else:
                return render(request, 'TriplexDB/gene_detail.html', {})
        except:
            return render(request, 'TriplexDB/gene_detail.html', {})


def transcript_detail(request, pk):
    if pk.startswith('ENSMU'):
        mouse = True
        rna_result = (
            rna.objects.using('mouse')
            .filter(transcriptid__exact=pk)
            .distinct()
            .order_by('transcripttriplexcount')
            .values()
        )
        plot_path = 'transcript_plots_mouse/' + pk + '.png'
        circos_path = 'ggCircos_mm39/' + pk + '.png'
    else:
        mouse = False
        rna_result = (
            rna.objects.filter(transcriptid__exact=pk)
            .distinct()
            .order_by('transcripttriplexcount')
            .values()
        )
        plot_path = 'transcript_plots/' + pk + '.png'
        circos_path = 'ggCircos_hg38/' + pk + '.png'
    return render(
        request,
        'TriplexDB/transcript_detail.html',
        {
            'object': rna_result,
            'plot_path': plot_path,
            'transcript': pk,
            'mouse': mouse,
            'circos_path': circos_path,
        },
    )


def go_enrichment_results(request):
    if request.method == 'POST':
        go_genes = request.POST['go_genes']
        rna_symbol = request.POST.get('rna_symbol')
        mouse = request.POST.get('mouse')
        transcript = request.POST.get('transcript')
        go_genes = go_genes.split(',')
        #if len(go_genes) > 500:
        #    go_genes = go_genes[:500]
        filename = f'{uuid.uuid4()}'
        filepath = os.path.join('media', 'temp_plots', filename)  #'media',
        if mouse == 'False':
            df, filenames = go_enrichment(
                go_genes={'human': list(go_genes)}, out_tag=filepath
            )
            gprofiler_table = df['human']
            mouse = False
        elif mouse == "True":
            df, filenames = go_enrichment(
                go_genes={'mouse': list(go_genes)}, 
                organism="mmusculus",
                out_tag=filepath
            )
            gprofiler_table = df['mouse']
        request.session['gprofiler_df'] = gprofiler_table.to_json()
        gprofiler_table = gprofiler_table.drop(
            [
                'Gene fraction',
                'significant',
                'description',
                'query',
            ],
            axis=1,
        )
        gprofiler_table = gprofiler_table.round(
            {'p_value': 3, 'precision': 3, 'recall': 3}
        )
        # headers = list(gprofiler_table.keys())
        headers = gprofiler_table.columns.to_list()
        # rows = zip(*gprofiler_table.values())
        rows = gprofiler_table.to_dict(orient='records')
        # table_html = df['human'].to_html(classes='table table-striped', index=False)
        if len(filenames) > 0:
            return render(
                request,
                'TriplexDB/go_enrichment.html',
                {
                    'rna_symbol': rna_symbol,
                    'plot_paths': filenames,
                    'headers': headers,
                    'rows': rows,
                    'mouse': mouse,
                    'transcript': transcript,
                    #'MEDIA_URL': '/media/',
                },
            )
        else:
            return render(
                request,
                'TriplexDB/go_enrichment.html',
                {
                    'rna_symbol': rna_symbol,
                    'transcript': transcript,
                    'plot_paths': None,
                    'mouse': None,
                    #'table_html': table_html,
                    #'MEDIA_URL': '/media/',
                },
            )
    else:
        return render(request, 'TriplexDB/go_enrichment.html', {})


@require_POST
def delete_temp_plot(request):
    import json

    data = json.loads(request.body)
    filename = data.get('filename')

    if filename:
        if os.path.exists(filename):
            os.remove(filename)
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'message': 'File not found'})
    return JsonResponse({'status': 'error', 'message': 'No filename provided'})


def download_csv(request):
    # Retrieve the DataFrame from the session
    df_json = request.session.get(
        'gprofiler_df'
    )  # Get the JSON-encoded DataFrame from the session
    if df_json:
        # Convert the JSON back into a DataFrame
        df = pd.read_json(df_json)
        # Create the HTTP response with CSV content-type
        response = HttpResponse(content_type='text/csv')
        # Name the downloaded file
        response['Content-Disposition'] = (
            'attachment; filename="full_GO_results_gprofiler.csv"'
        )
        # Convert the DataFrame to CSV and write it to the response
        df.to_csv(path_or_buf=response, index=False)
        return response
    else:
        return HttpResponse('No data available for download.', status=400)


"""def loading_view(request):
	if request.method == 'POST':
		go_genes = request.POST['go_genes']
		rna_symbol = request.POST.get('rna_symbol')
		if rna_symbol and go_genes:
            # Save to session
			request.session['rna_symbol'] = rna_symbol
			request.session['go_genes'] = go_genes
            # Redirect to loading view (this will trigger GET request)
			return render(request, 'TriplexDB/loading.html', {})
		else:
            # Return an error if data is missing
			return render(request,
			'TriplexDB/go_enrichment.html',
			{
				'rna_symbol': 'shitty',
				#'table_html': table_html,
				#'MEDIA_URL': '/media/',
			})

def go_enrichment_results(request):
	rna_symbol = request.session.get('rna_symbol')
	filenames = request.session.get('filenames', [])
	headers = request.session.get('headers', [])
	rows = request.session.get('rows', [])
	if len(filenames) > 0:
		return render(request,
			'TriplexDB/go_enrichment.html',
			{
				'rna_symbol': rna_symbol,
				'plot_paths': filenames,
				'headers' : headers,
				'rows' : rows,
			})
	else:
		return render(request,
			'TriplexDB/go_enrichment.html',
			{
				'rna_symbol': 'no plots',
			})

def go_calculation(request):
	rna_symbol = request.session.get('rna_symbol')
	go_genes = request.session.get('go_genes')
	if not rna_symbol or not go_genes:
		return render(request,
			'TriplexDB/go_enrichment.html',
			{
				'rna_symbol': 'no data for calculation',
			})

	go_genes = go_genes.split(',')
	filename = f'{uuid.uuid4()}'
	filepath = os.path.join('media','temp_plots', filename)#'media',
	df, filenames = go_enrichment(go_genes = {'human': list(go_genes)}, out_tag=filepath)
	gprofiler_table = df['human']
	request.session['gprofiler_df'] = gprofiler_table.to_json()
	gprofiler_table = gprofiler_table.drop(['Gene fraction', 'intersections', 'evidences', 'significant', 
										'description',  'query'], axis = 1)
	#headers = list(gprofiler_table.keys())
	headers = gprofiler_table.columns.to_list()
	#rows = zip(*gprofiler_table.values())
	rows = gprofiler_table.to_dict(orient='records')  
	#table_html = df['human'].to_html(classes='table table-striped', index=False)
	request.session['filenames'] = filenames
	request.session['headers'] = headers
	request.session['rows'] = rows
	request.session['rna_symbol'] = rna_symbol
	return JsonResponse({'status': 'completed'})"""
