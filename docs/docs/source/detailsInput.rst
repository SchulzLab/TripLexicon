
=======================================
Querying TripLexicon
=======================================

The structure of TripLexicon allows querying of predicted triplexes by the RNA involved, the predicted target gene, or by a given genomic region. More details on these queries are outlined below:

Querying TripLexicon by RNA
===================================

TripLexicon can be queried by RNA in two different modes. The search input can be either the gene name of the RNAs to be searched, or the transcript ID that is specifically interesting to the user for more precise predictions.

Searching for triplexes by RNA gene symbol
------------------------------------------

To query TripLexicon by an RNA gene symbol, the symbol of interest should be entered in the search field with the header: **Search for predicted triplexes by RNA gene symbol (results will include all annotated transcripts)**. The result will be a table of statistically significant predicted triplexes for every annotated transcript of the RNA gene of interest with genome-wide gene promoters and REMs. The results tables are sorted by the *E* value for the predicted triplex as calculated by TriplexAligner by default, placing the most statistically significant triplexes at the top of the table.

Searching for triplexes by transcript ID
----------------------------------------

To search TripLexicon by Ensembl transcript ID, the appropriate ID should be provided in the search field denoted by **Search for predicted triplexes by RNA transcript ID (Ensembl format)**. This search will return a results table containing predicted triplexes between the transcript matching the ID provided and predicted target genes. The target genes will be those where any annotated promoter or REM linked to said gene is predicted to be involved in the formation of a statistically significant triplex with the transcript by TriplexAligner. The results tables are sorted by the *E* value for the predicted triplex as calculated by TriplexAligner by default, placing the most statistically significant triplexes at the top of the table.

Querying TripLexicon by predicted target gene
=============================================

In the case that the user would like to find out which lncRNAs are most likely to target a gene of interest, TripLexicon can be queried by target gene symbol. This is done via the **Target query** tab. The gene symbol of interest can then be provided in the search field. The resulting table will contain all statistically significant predicted triplexes between all annotated human lncRNAs and any promoter of REM annotated to the provided target gene. The results tables are sorted by the *E* value for the predicted triplex as calculated by TriplexAligner by default, placing the most statistically significant triplexes at the top of the table.

Querying TripLexicon by target genomic region
=============================================

If the user has a genomic region of interest, this can also be used to query TripLexicon for triplexes predicted to be formed in the given region. This query can be carried out in two ways. The first is to use the search fields on the **Region query** tab, where the chromosome of interest can be chosen from a dropdown menu, and start and stop coordinates (in base pairs) can be provided to the search fields. This will query TripLexicon for any statistically significant triplexes predicted to form between any lncRNA and promoter/REMs falling within the search area.

Alternatively, if the user wishes to query TripLexicon for triplexes predicted to form in multiple regions e.g. peaks resulting from ATAC-sequencing/ChIP-sequencing/CUT&RUN etc., then a BED file can be supplied to TripLexicon. Each region in the BED file will be used to query TripLexicon for predicted triplexes between any lncRNA and promoters/REMs falling within the region. To do this, the user should select **Choose file** on the **Region query** tab, which will open the native file explorer for their operating system, where the appropriate BED file can be selected for upload.

The BED file used to query TripLexicon should fulfill the following formatting requirements:

* At least three columns (chromosome, start, stop)

* Tab-separated

* Chromosome numbers should be prefixed with "chr" (i.e. "chr1" rather than "1")

* Start and end positions must be in range of the appropriate chromosome, out of range values will throw an error

* Extra columns (e.g. name, strand, score etc.) can be included, but are not used in the query



