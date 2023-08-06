#!/bin/bash

#unit tests for amptk
dir=test_results
mkdir $dir

#run through ion tests
ion=ion.test.fastq
cmd="amptk ion -i $ion -o ion"
echo $cmd; eval $cmd
cmd="amptk ion -i $ion -o ion_map -m ion.mapping_file.txt"
echo $cmd; eval $cmd
cmd="amptk ion -i $ion -o ion_2mm --barcode_mismatch 2"
echo $cmd; eval $cmd

#run illumina test
cmd="amptk illumina -i alt_illumina -o miseq --cleanup"
echo $cmd; eval $cmd
cmd="amptk illumina -i alt_illumina -o miseq_map -m miseq.mapping_file.txt --cleanup"
echo $cmd; eval $cmd
cmd="amptk illumina -i alt_illumina -o miseq2 --full_length --cleanup"
echo $cmd; eval $cmd
cmd="amptk illumina -i illumina_no_primers -o miseq3 -f ITS1-F -r ITS2 --cleanup"
echo $cmd; eval $cmd
cmd="amptk illumina -i illumina_no_primers -o miseq3 -f ITS1-F -r ITS2 --require_primer off --cleanup"
echo $cmd; eval $cmd

#illumina2 test
cmd="amptk illumina2 -i test_R1.fastq --reverse test_R2.fastq -f AGATATTGGAACWTTATATTTTATTTTTGG -r WACTAATCAATTWCCAAATCCTCC --barcode_fasta barcode_1.fa --full_length -o illumina2 --reverse_barcode barcode_2.fa --barcode_mismatch 4"
echo $cmd; eval $cmd
#test illumina2
cmd="amptk illumina2 -i Run1_R1.fastq --reverse Run1_R2.fastq -m run1_mapping_file.txt -o illumina2_map"
echo $cmd; eval $cmd

#run clustering, taxonomy, filtering, etc
cd $dir
cmd="amptk cluster -i ../ion.demux.fq.gz -o uparse"
echo $cmd; eval $cmd
cmd="amptk cluster -i ../ion.demux.fq.gz --unoise -o unoise"
echo $cmd; eval $cmd
cmd="amptk cluster -i ../ion.demux.fq.gz --uchime_ref ITS -o uchime"
echo $cmd; eval $cmd
cmd="amptk unoise2 -i ../ion.demux.fq.gz -o unoise2"
echo $cmd; eval $cmd
cmd="amptk dada2 -i ../ion.demux.fq.gz -o dada2"
echo $cmd; eval $cmd
cmd="amptk cluster_ref -i ../ion.demux.fq.gz -d ITS2 -o cr"
echo $cmd; eval $cmd
cmd="amptk cluster_ref -i ../ion.demux.fq.gz -d ITS2 -o cr_closed --closed_ref_only"
echo $cmd; eval $cmd
#throw error
cmd="amptk filter -i uparse.otu_table.txt -f uparse.cluster.otus.fa -b BC.5"
echo $cmd; eval $cmd
#correct
cmd="amptk filter -i uparse.otu_table.txt -f uparse.cluster.otus.fa -b BC.5 --mc mock3 -c in"
echo $cmd; eval $cmd
#one with taxonomy
cmd="amptk filter -i cr.otu_table.txt -f cr.cluster.otus.fa -p 0.002"
echo $cmd; eval $cmd

cmd="amptk taxonomy -i uparse.final.txt -f uparse.filtered.otus.fa -d ITS2"
echo $cmd; eval $cmd
cmd="amptk taxonomy -i uparse.final.txt -f uparse.filtered.otus.fa -m ../ion.mapping_file.txt -o map -d ITS2"
echo $cmd; eval $cmd
#test taxonomy singletons
cmd="amptk taxonomy -i uparse.final.txt -f uparse.filtered.otus.fa -d ITS2 --method usearch -o usearch"
echo $cmd; eval $cmd
cmd="amptk taxonomy -i uparse.final.txt -f uparse.filtered.otus.fa -d ITS2 --method utax -o utax"
echo $cmd; eval $cmd
cmd="amptk taxonomy -i uparse.final.txt -f uparse.filtered.otus.fa -d ITS2 --method sintax -o sintax"
echo $cmd; eval $cmd

#run some utilities
cmd="amptk summarize -i uparse.otu_table.taxonomy.txt -o uparse --graphs --format pdf"
echo $cmd; eval $cmd
cmd="amptk funguild -i uparse.otu_table.taxonomy.txt -d fungi -o funguild"
echo $cmd; eval $cmd
cmd="amptk heatmap -i uparse.otu_table.taxonomy.txt -o test.pdf -d tsv -m heatmap"
echo $cmd; eval $cmd