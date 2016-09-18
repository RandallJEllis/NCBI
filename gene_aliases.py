# -*- coding: utf-8 -*-
"""
Created on Tue Jun 28 13:39:32 2016
@author: ellisrj2

Input a list of genes and query the NCBI for all aliases of these genes. Output is a CSV.
""""

def gene_alias(gene_file):
    from Bio import Entrez
    import csv
    
    Entrez.email = "randalljellis@gmail.com"
    genes = [gene.rstrip('\n') for gene in open(gene_file)]
    
    ids = []
    aliases = []
    
    for gene in genes:
        #retrieve gene ID
        handle = Entrez.esearch(db="gene", term="Mus musculus[Orgn] AND " + gene + "[Gene]")
        record = Entrez.read(handle)
        
        if len(record["IdList"]) > 0:
            ids.append(record["IdList"][0])
            
            #retrieve aliases
            record_with_aliases = Entrez.efetch(db="gene",id=record["IdList"][0],retmode="json")
            entry = record_with_aliases.read()
            entry_lines = entry.splitlines()
            for i in range(len(entry_lines)):
                while 'This record was replaced with GeneID:' in entry_lines[i]:
                   new_id = entry_lines[i][38:]
                   record_with_aliases = Entrez.efetch(db="gene",id=new_id ,retmode="json")
                   entry = record_with_aliases.read()
                   entry_lines = entry.splitlines()
                    
               
            firstline = entry.splitlines()[1]
            if gene.lower() == firstline[3:].lower():
                thirdline = entry.splitlines()[3]
                fourthline = entry.splitlines()[4]
                if thirdline[0:13] == 'Other Aliases':
                    aliases.append(thirdline[15:])
                elif fourthline == 'This record was discontinued.':
                    aliases.append(fourthline)
                else:
                    aliases.append('no aliases')
            else:
                aliases.append(firstline[3:])

        else:
            ids.append(gene + ' is not in Gene')
            aliases.append(gene + ' is not in Gene')
        
    rows = zip(genes, ids, aliases)
    with open('gene_aliases.csv', 'wb') as thefile:
        writer = csv.writer(thefile)
        writer.writerow(['Gene', 'ID', 'Aliases'])
        for row in rows:
            writer.writerow(row)
