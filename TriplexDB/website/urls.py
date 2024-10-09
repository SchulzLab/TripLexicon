"""
URL configuration for TriplexDB project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = "home"),
    path('search_rna_symbol', views.search_rna_symbol_values, name="search_rna_symbol"),
    path('search_dna_home', views.search_dna_home, name="search_dna_home"),
    #path('search_dna', views.search_dna, name="search_dna"),
    path('search_dna_mouse', views.search_dna_mouse, name="search_dna_mouse"),
    path('search_transcript', views.search_transcript_values, name="search_transcript"),
    path('search_rna_home', views.search_rna_home, name="search_rna_home"),
    path('search_rna_results', views.search_rna_results, name="search_rna_results"),
    path('search_gen_region_home', views.search_gen_region_home, name="search_gen_region_home"),
    path('search_gen_region_results', views.search_gen_region_results, name="search_gen_region_results"),
    path('Gene_detail/<pk>/', views.gene_detail, name = 'gene_detail'),
    path('Gene_detail_search/', views.gene_detail_search, name = 'gene_detail_search'),
    path('transcript_detail/<pk>/', views.transcript_detail, name = 'transcript_detail'),
]
