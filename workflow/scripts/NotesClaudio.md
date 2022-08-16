# Notebook for surfaceome evolution analysis



## Downloading files



>python3.8 workflow/scripts/download_ncbi_genomes.py -l resources/drosophila_urls.csv -f resources/genomes/


Then 
>gzip -d resources/genomes/*cds*

To filter the orthogroups according to the orthgroups related with adhesion molecules I used this table:

http://prodata.swmed.edu/FlyXCDB/domains/classB.geneids.html

I filtered from the cds of Dmel with the longest isoform, using the list of the gene name


>grep -f resources/DmelGenes_B-XC-domains_binding_GeneNameList results/drosophila_melanogaster_cds_filt.fna -c
>2533



>```
grep ">" -c results/drosophila_melanogaster_cds_filt.fna

>13995

But there are more genes than expected, the list of genes from the surfaceome is 759.

To see what was going on I did the following:

>```
for i in $(cat DmelGenes_B-XC-domains_binding_GeneNameList)
do 
grep "$i" ../results/drosophila_melanogaster_cds_filt.fna -c | tee -a HowManyDuplicatesGeneList
done


and then

>```
paste -d ',' DmelGenes_B-XC-domains_binding_GeneNameList HowManyDuplicatesGeneList | tee DmelGenes_B-XC-domains_binding_GeneNameList-DUPLICATES.csv | mv DmelGenes_B-XC-domains_binding_GeneNameList-DUPLICATES.csv HowManyDuplicatesGeneList

>```
grep -E ",1$" HowManyDuplicatesGeneList -c


>713

>```
grep -vE ",1$" HowManyDuplicatesGeneList -c

>46

those are the genes that for some reason match more than one isoform

|GeneName|replic|
|--------|------|
|CG1136  |6     |
|ckd     |2     |
|CG3348  |8     |
|mtg     |2     |
|serp    |29    |
|Tequila |0     |
|Cht3    |0     |
|verm    |2     |
|fw      |5     |
|Clect27 |0     |
|CG1124  |7     |
|to      |1435  |
|CG3246  |5     |
|ect     |91    |
|CG3216  |6     |
|TwdlBeta|0     |
|Tb      |7     |
|ort     |198   |
|pHCl    |2     |
|stan    |14    |
|eys     |2     |
|kon     |7     |
|wb      |4     |
|axo     |7     |
|sli     |8     |
|CadN    |2     |
|trol    |2     |
|ft      |21    |
|b6      |5     |
|kug     |2     |
|Tsp     |36    |
|Mp      |9     |
|sca     |28    |
|CG1791  |7     |
|emp     |9     |
|pes     |4     |
|Drs     |7     |
|CG4398  |3     |
|CG4409  |5     |
|Dpt     |2     |
|a10     |7     |
|Rfabg   |0     |
|a5      |15    |
|Dl      |9     |
|Ser     |15    |
|tsl     |2     |


>```
for i in $(cat DmelGenes_B-XC-domains_binding_GeneNameList)
do 
echo $i"]" | tee -a DmelGenes_B-XC-domains_ExactMatch
done

I runed the previous script to get the exact name of the Genes, now I have to check on by one

|Gene    |Duplicates|
|--------|----------|
|Tequila |0         |
|Cht3    |0         |
|fw      |2         |
|Clect27 |0         |
|to      |11        |
|ect     |2         |
|TwdlBeta|0         |
|ort     |2         |
|pHCl    |0         |
|wb      |2         |
|ft      |4         |
|b6      |3         |
|sca     |3         |
|emp     |2         |
|pes     |2         |
|Dpt     |0         |
|Rfabg   |0         |
|a5      |10        |

Clect27 is not easy to find



