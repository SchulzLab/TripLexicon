import sys
import sqlite3
import pandas as pd
import numpy as np

db = sys.argv[1]
species = sys.argv[2]
results_df = pd.DataFrame(columns=['Mean', 'Min', 'Max', 'Std'], index=[
                          'RNA transcript', 'RNA gene', 'DNA gene', 'DNA GENE ID'])


# connection to db
connection = sqlite3.connect(db)
cursor = connection.cursor()

# which tables are present in the db
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print('Table names')
for table in tables:
    print(table[0])

# nr of entries per table
for table in tables:
    table_name = table[0]
    cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
    row_count = cursor.fetchone()[0]
    print(f"Table '{table_name}' has {row_count} rows.")


# print colnames for each table
for table in tables:
    table_name = table[0]
    print(f"\nColumns in table '{table_name}':")
    cursor.execute(f"PRAGMA table_info({table_name});")
    columns = cursor.fetchall()
    for column in columns:
        print(f" - {column[1]}")  # column[1] is the column name


################################################################################
# SUMMARY STATS PER RNA TRANSCRIPT #############################################
################################################################################

# get the number of tripelxes per RNA transcript
table_name = 'rna'
column_name = 'TranscriptTriplexCount'

# Query to get summary statistics
query = f"""
SELECT
    AVG({column_name}) AS mean,
    MIN({column_name}) AS min,
    MAX({column_name}) AS max,
    printf("%.2f",
        (AVG(({column_name} - (SELECT AVG({column_name}) FROM {table_name})) *
        ({column_name} - (SELECT AVG({column_name}) FROM {table_name})))
    )) AS variance,
    printf("%.2f",
        sqrt(AVG(({column_name} - (SELECT AVG({column_name}) FROM {table_name})) *
        ({column_name} - (SELECT AVG({column_name}) FROM {table_name})))
    )) AS std_dev
FROM {table_name};
"""

# Execute the query
cursor.execute(query)
result = cursor.fetchone()

# Display results
print(f"Summary statistics for '{column_name}' in table '{table_name}':")
print(f"Mean: {result[0]}")
print(f"Min: {result[1]}")
print(f"Max: {result[2]}")
print(f"Standard Deviation: {result[4]}")


# print('RESULT', result)
results_df.loc['RNA transcript', :] = result[0:3] + result[4:]


################################################################################
# SUMMARY STATS PER RNA GENE####################################################
################################################################################
table_name = 'triplexaligner'
dna_column = 'RNASymbol'

# SQL to compute the counts per DNA
query = f"""
WITH dna_counts AS (
    SELECT {dna_column}, COUNT(*) AS count_per_dna
    FROM {table_name}
    GROUP BY {dna_column}
)
SELECT
    AVG(count_per_dna) AS mean_count,
    MIN(count_per_dna) AS min_count,
    MAX(count_per_dna) AS max_count,
    printf("%.2f",
        sqrt(AVG((count_per_dna - (SELECT AVG(count_per_dna) FROM dna_counts)) *
                 (count_per_dna - (SELECT AVG(count_per_dna) FROM dna_counts)))
        )
    ) AS std_dev
FROM dna_counts;
"""

# Execute the query
cursor.execute(query)
result = cursor.fetchone()

# Display the results
print(f"Mean number of entries per RNA: {result[0]}")
print(f"Min number of entries per RNA: {result[1]}")
print(f"Max number of entries per RNA: {result[2]}")
print(f"Standard Deviation: {result[3]}")

results_df.loc['RNA gene', :] = result


################################################################################
# SUMMARY STATS PER DNA GENE####################################################
################################################################################
table_name = 'triplexaligner'
dna_column = 'DNASymbol'

# SQL to compute the counts per DNA
query = f"""
WITH dna_counts AS (
    SELECT {dna_column}, COUNT(*) AS count_per_dna
    FROM {table_name}
    GROUP BY {dna_column}
)
SELECT
    AVG(count_per_dna) AS mean_count,
    MIN(count_per_dna) AS min_count,
    MAX(count_per_dna) AS max_count,
    printf("%.2f",
        sqrt(AVG((count_per_dna - (SELECT AVG(count_per_dna) FROM dna_counts)) *
                 (count_per_dna - (SELECT AVG(count_per_dna) FROM dna_counts)))
        )
    ) AS std_dev
FROM dna_counts;
"""

# Execute the query
cursor.execute(query)
result = cursor.fetchone()

# Display the results
print(f"Mean number of entries per DNA: {result[0]}")
print(f"Min number of entries per DNA: {result[1]}")
print(f"Max number of entries per DNA: {result[2]}")
print(f"Standard Deviation: {result[3]}")

results_df.loc['DNA gene', :] = result


################################################################################
# SUMMARY STATS PER DNA ENSEMBL ID##############################################
################################################################################
# count interactions per DNAid, then mrge with dna table to get mapping to
# GeneID(=EnsmeblID), then groupby and sum

query = """
WITH InteractionCounts AS (
    SELECT DNAid, COUNT(*) as interaction_count
    FROM triplexaligner
    GROUP BY DNAid
)
SELECT dna.GeneID, SUM(ic.interaction_count) as total_interactions
FROM dna
JOIN InteractionCounts ic ON dna.DNAid = ic.DNAid
GROUP BY dna.GeneID;
"""

cursor.execute(query)
results = cursor.fetchall()

# Extract the triplexcounts, second entry is count, while first is ID
interaction_counts = [row[1] for row in results]


# Calculate summary statistics for counts
mean_count = np.mean(interaction_counts)
median_count = np.median(interaction_counts)
max_count = np.max(interaction_counts)
stddev_count = np.std(interaction_counts)


print(f"Mean interactions per Ensembl ID: {mean_count}")
print(f"Median interactions per Ensembl ID: {median_count}")
print(f"Max interactions per Ensembl ID: {max_count}")
print(f"Standard deviation of interactions: {stddev_count}")

results_df.loc['DNA GENE ID', :] = [mean_count, 1, max_count, stddev_count]
print(results_df)
results_df.to_csv(f'summary_stats_table_{species}.csv')

connection.close()
