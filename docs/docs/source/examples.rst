===========================
Example TripLexicon queries
===========================

In this section, we will provide specific examples for each of the possible TripLexicon queries. 



Querying by RNA
=========================
Summary query by RNA gene symbol
---------------------------
This example reflects a scenario where the user has an RNA of interest, but might not have in mind which specific transcript of the RNA gene is of interest. In this case, they can query TripLexicon by the RNA gene symbol, and the results will be the predicted triplexes of the respective RNA gene summarized at the transcript level. They will be ordered such that the transcript forming the most predicted triplexes is listed first. This query is supposed to help the user get an overview of the different transcripts belonging to an RNA gene and how often they are involved in predicted triplex forming events.

For this query mode, the user should navigate to the :kbd:`RNA-query` tab. 

.. image:: ../RNA_query.png
  :alt: RNA query


Here 3 query options are presented. In order to run the summary query by RNA gene symbol, the RNA gene of interest needs to be provided to the first input field :kbd:`Search for triplex summary by RNA genesymbol`. Before the user starts any of the TripLexicon queries, the organism needs to be chosen. The current options are :kbd:`Human` and :kbd:`Mouse` which can be chosen at the start of each query. The default organism is Human.

.. image:: ../human_mouse_selection.png
  :alt: Choice of organism

Upon clicking :kbd:`Search`, the query will begin to run. For example, the user may be interested in the known triplex-forming lncRNA *MEG3*.

.. image:: ../RNA_summary_search_MEG3.png
  :alt: Summary query by RNA gene MEG3

Once the query has successfully run, the results table should load automatically. At the top of the page, a summary statement should state how many predicted triplexes there are for the RNA gene which was used for the query. In the case of *MEG3*, this reads 1605, as of the current version of TripLexicon. The results table is sorted by the number of predicted triplexes for each transcript. For MEG3 the transcript with the most predicted tripelxes is ENST00000522771. Of the transcript with the most predicted triplexes, a plot of the triplex forming region prediction for the maximally scoring transcript is shown at the bottom of the page together with a circos plot of the DNA regions with which the transcript is predicted to form triplexes. The user may also sort the table by other fields by clicking on the column header, or can search the table for specific terms by using the search bar at the top right of the table. Which columns are shown can also be modified by the user via the :kbd:`Column visibility` dropdown. The results table can be copied to the clipboard, or exported to :kbd:`Excel` or :kbd:`CSV` formats using the buttons at the top of the table.

.. image:: ../RNA_summary_results_MEG3.png
  :alt: Summary query results for RNA gene MEG3

The transcript IDs in the :kbd:`Transcript ID` column are linked to detail pages of the respective transcripts. Upon clicking the transcript ID, the user is redirected to the transcript detail page where information of the particular transcript is provided. A plot of the triplex forming region prediction for the respective transcript is shown on the detail page togehter with a circos plot of the DNA regions with which the transcript is predicted to form triplexes.

.. image:: ../transcript_detail.png
  :alt: Transcript detail example for ENST00000556407

The  :kbd:`Transcripttriplexcount` column indicates how many triplexes the respective transcript is predicted to form. Upon clicking on it the user is redirected to the same results page as searching for the respective transcript ID with the **Extended query by RNA transcript ID** explained in a section below.

The last column :kbd:`Binding sites in UCSC` holds links to the UCSC genome browser. 

.. image:: ../click_UCSC.png
  :alt: Click on Binding sites in UCS to be redirected to UCSC to see DNA bindign sites of the RNA gene of interest.

When clicking on it, the user is redirected to UCSC with a track of the DNA regions predicted to be bound by the RNA gene of interest to form triplexes.

.. image:: ../UCSC_MEG3_view.png
  :alt: UCSC genome browser view of predicted DNA interaction sites for RNA gene MEG3.

If the interactions of several RNA genes are of interest, they can be displayed in UCSC as different tracks in the same view. For this the user can just click on several links and the previous tracks will be shown as well, see below.

.. image:: ../UCSC_several_tracks.png
  :alt: UCSC genome browser view of several tracks of RNA gene interaction sites.

If several tracks want to be seen but in separate sessions of the UCSC genome browser, we recommend to use the incognito/private mode of the internet browser.

Extended query by RNA gene symbol
---------------------------
The query by RNA gene symbol reflects a similar scenario to the one for the summary query by RNA gene symbol decsribed above. The user has an RNA of interest, but might not have in mind which specific transcript of the RNA gene is of interest. Instead of querying the database such that the predicted triplexes per transcript are summarized, each single predicted triplex is listed and can be investigated in more detail. In this case, they can query TripLexicon by the RNA gene symbol in the detailed mode, and the results will include statistically significant predicted triplexes for all of the annotated transcripts for that RNA gene.

Keeping the known triplex-forming lncRNA *MEG3* as our example, the user again needs to navigate to the :kbd:`RNA query` tab. To query TripLexicon for triplexes that are predicted to be formed between any transcript of *MEG3* and genome-wide promoters/REMs, they can provide ´MEG3´ to the second search field, **Search for predicted triplexes by RNA gene symbol, gene ID or transcript ID (results will list all interactions line by line)**. Submitting the query by clicking :kbd:`Search`, will initiate the search. Once the query has successfully run, the results table should load automatically. At the top of the page, a summary statement should state how many predicted triplexes there are for the RNA gene which was used for the query. In the case of *MEG3*, this reads 1605, as of the current version of TripLexicon.

.. image:: ../RNA_gene_sym_query.png
  :alt: Query by RNA gene MEG3

The results table is - by default - sorted by the *E* value for the predicted triplexes, as calculated by TriplexAligner. If more than 10 000 triplexes are predicted, the results are truncated to the top 10 000 predicted triplexes based on the *E* value. The most statistically significant predicted triplexes are placed at the top of the table. In the case of *MEG3*, the most significant predicted interaction is with the gene *MIR770*.  The sorting, column visibility and export options are identical to those described above in the example for **Summary query by RNA gene symbol**. 


.. image:: ../RNA_gene_sym_result.png
  :alt: Results for RNA gene MEG3

The transcript IDs in the :kbd:`Transcript ID` column are linked to detail pages of the respective transcripts. Upon clicking the transcript ID, the user is redirected to the transcript detail page where information of the particular transcript is provided. A plot of the triplex forming region prediction for the respective transcript is shown on the detail page together with a circos plot of the genomic regions the transcript performs triplex formation with. The gene symbol names are linked to the summary query results page of that RNA gene symbol. The information given with this detail page is described in the previous section. The button :kbd:`GO enrichment of DNA gene set` performs a GO enrichment analysis with g:Profiler (publication `g:Profiler <https://academic.oup.com/nar/article/51/W1/W207/7152869>`_ and `g:Profiler Webserver <https://biit.cs.ut.ee/gprofiler/gost>`_) and renders dotplots of the enriched terms as well as a table of the GO terms found to be significant with accompanying information.

.. image:: ../GO_enrichment.png
  :alt: GO enrichment

In order to perform the GO analysis on the DNA gene set with which the RNA gene or transcript forms triplexes, the DNA genes are filtered for protein coding genes and provided to the g:Profiler functionality of the :kbd:`gprofiler-official` python implementation. A buffer will appear until the results page can be rendered which should not exceed the duration of one minute.

.. image:: ../GO_results.png
  :alt: GO results

A table containing the information g:Profiler used to calculate the GO enrichments can be downloaded when clicking on the :kbd:`Download full results table as CSV` button.

.. image:: ../GO_download.png
  :alt: GO download results as CSV

The :kbd:`Target Gene` column is linked to the query results page of the respective target gene which is identical to performing **Querying by predicted target gene** explained in a section below.

The :kbd:`View Alignment` column links the user to an alignment detail page with details about the alignment of the respective transcript with the target gene forming the triplex of interest.

.. image:: ../click_view_alignment.png
  :alt: Clicking on :kbd:`View Alignment`.

The alignment detail page exists for each triplex. It contains a table with information about the RNA and DNA elements involved in the triplex formation as well as the statistical scores of the triplex. The alignment of RNA with the DNA element is visualized below the table together with the scoring scheme applied for the alignment.

.. image:: ../view_alignment.png
  :alt: Alignment detail page for the triplex of interest.


Extended query by RNA transcript ID
-----------------------------
This example reflects a scenario where the user has an RNA of interest, and is interested in the predicted triplex formation of a specific transcript of that RNA (e.g. that which is dominantly expressed in their cell type of interest, or a specific splice variant). In this case, they can query TripLexicon by the RNA transcript ID (in Ensembl format), and the results will include statistically significant predicted triplexes for only the specified transcript for that RNA gene.

Sticking to the example of *MEG3*, but this time the user is only interested in the canonical Ensembl transcript, which has the ID *ENST00000556407*. In this case, the user would again navigate to the :kbd:`RNA query` tab of the TripLexicon web interface, and this time would enter *ENST00000556407* into the same seach field as for the previous query **Search for predicted triplexes by RNA gene symbol, gene ID or transcript ID (results will list all interactions line by line)**. 

.. image:: ../transcript_search.png
  :alt: Query by transcript ENST00000556407

After clicking :kbd:`Search`, the query will begin to run. Upon completion, the results table for predicted triplexes between *ENST00000556407* and GRCh38 promoters/REMs will be rendered. Again, a summary statement at the top of the results table will summarise how many predicted triplexes there are for the supplied transcript. If more than 10 000 triplexes are predicted, the results are truncated to the top 10 000 predicted triplexes based on the *E* value. In the case of *ENST00000556407*, for the current version of TripLexicon, this should read "ENST00000556407 is predicted to be involved in the formation of 6 triplexes.". The sorting, column visibility and export options are identical to those described above in the example for **Summary query by RNA gene symbol**. Upon clicking the :kbd:`GO enrichment of DNA gene set` button, GO enrichment with g:Profiler is performed as explained for the RNA gene symbol search. 

.. image:: ../transcript_result.png
  :alt: Query result by transcript ENST00000556407

Querying by predicted target gene
=================================
This use case reflects a scenario where the user has a gene of interest (e.g. a differentally expressed gene from RNA-sequencing), and is interested in knowing whether the gene might be subject to regulation via triplex formation by a lncRNA. Here, the user would navigate to the :kbd:`Target query` tab of TripLexicon.

.. image:: ../Target_query.png
  :alt: Target Query

There the user can supply their target gene symbol of interest to the search field e.g. "*GAPDH*". Upon clicking :kbd:`Search`, the query will begin to run.

.. image:: ../target_search.png
  :alt: Target Search

Upon completion, the results table for statistically significant triplexes predicted to form between human lncRNAs and promoters/REMs associated with *GAPDH* will render. A statement at the top of the results table will summarise the total number of triplexes predicted to form at gene regulatory elements of *GAPDH*, and for the current version of TripLexicon this should read "Human gene GAPDH is predicted to be targeted by different RNAs to form 16 triplexes.". The sorting, column visibility and export options are identical to those described above in the example for **Summary query by RNA gene symbol**. The transcript and RNA gene links render the transcript and gene detail pages, respectively, as described for **Querying by RNA gene symbol**.

.. image:: ../target_result.png
  :alt: Target Result

Querying by a genomic region
============================
In order to query Triplexicon for target elements located in defined genomic regions, the user needs to navigate to the **Region query** tab.

.. image:: ../Region_query.png
  :alt: Region Query

Single region
-------------
If the user has an interest in a single region of the genome (e.g. a topologically associating domain identified in Hi-C data), then they can use the dropdown and search fields of the **Region query** tab of TripLexicon to provide the coordinates. For example, if a user was interested in a region of approximately 1 megabase around the gene locus of *ACTB*, they could use the :kbd:`Chromosome` dropdown to select :kbd:`chr1`, and then the :kbd:`Start position in chromosome` and :kbd:`Stop position in chromosome` text fields to input :kbd:`10` and :kbd:`1000000`, respectively. The maximum size of the supplied region is 1 000 000 bp.

.. image:: ../single_reg_search.png
  :alt: Single region search

After selecting/entering the appropriate values, the user can start the query by clicking :kbd:`Search`. Upon completion of the query, the results table containing all statistically significant triplexes predicted between lncRNAs and gene regulatory elements falling within the specified region will be rendered. The sorting, column visibility and export options are identical to those described above in the example for **Summary query by RNA gene symbol**. The transcript and RNA gene links render the transcript and gene detail pages, respectively, as described for **Querying by RNA gene symbol**.

.. image:: ../single_reg_results.png
  :alt: Single region results

Multiple regions
----------------
More often the user may want to query many genomic regions at once for which they would like to obtain triplex predictions. For example, these could be peaks which are the result of other assays, such as ATAC-sequencing, ChIP-sequencing/CUT&RUN, or specific sets of promoters of genes which are differentially expressed in an RNA-sequencing experiment. In this case, rather than querying individual regions, a BED file can be used to query multiple regions simultaneously. The BED file should have a minimum of three columns (chromosome, start, stop), with a "chr" prefix. Extra columns are permitted, but are not used in the query. An example BED file is available from the `TripLexicon GitHub repository <https://github.com/SchulzLab/TripLexicon/blob/main/TriplexDB/Test_bed_file_for_triplexaligner.bed>`_ , and is also shown below in table format.


.. list-table:: Example BED file format
   :widths: 25 25 25
   :header-rows: 0

   * - chr1
     - 1
     - 10000
   * - chr5
     - 10000
     - 20000
   * - chr7
     - 30000
     - 40000
   * - chr8
     - 40000
     - 50000
   * - chr10
     - 50000
     - 60000


To upload the BED file, the user should click the :kbd:`Choose File` button on the **Region query** tab of TriplexAligner.

.. image:: ../choose_file.png
  :alt: Choose file

This should bring up the operating system-dependent file explorer, where the user can point to the appropriate file for the regions of interest e.g. :kbd:`regions_of_interest.bed`. Following this, the user can click :kbd:`Submit file` to upload and the chosen BED file for querying. This should start the TripLexicon query.

.. image:: ../submit_file.png
  :alt: Submit file

Upon completion, the results table containing the predicted triplexes between lncRNAs and gene regulatory elements residing in the supplied regions will be rendered. Depending on the size of the supplied regions, this query might take some time to run. The sorting, column visibility and export options are identical to those described above in the example for **Querying by RNA gene symbol**.

.. image:: ../bed_results.png
  :alt: Bed results
