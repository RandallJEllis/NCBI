# -*- coding: utf-8 -*-
"""
Created on Tue Jun 21 10:07:47 2016
@author: ellisrj2
"""

def db_search_count(gene_file, search_term, database):
    from Bio import Entrez
    # ALWAYS tell the NCBI who you are
    Entrez.email = "randalljellis@gmail.com"
    
    import csv
    
    publication_counts = []
    genes = [gene.rstrip('\n') for gene in open(gene_file)]
    genes = list(set(genes))
    
    for gene in genes:
        handle = Entrez.egquery(term=gene + " " + search_term)
        record = Entrez.read(handle)
        
        for row in record["eGQueryResult"]:
            if row["DbName"] == database:
                print(row["Count"])
                publication_counts.append(row["Count"])
                
    rows = zip(genes, publication_counts)
    with open('publication_counts.csv', 'wb') as thefile:
        writer = csv.writer(thefile)
        writer.writerow(['Gene', database])
        for row in rows:
            writer.writerow(row)