#!/bin/bash

if (( $7 >= 1 )); then
 echo
 echo "╓─┤ USAGE ├─────────────────────────────────────────────────────────────────────────────────────────────────────╖"
 echo "║                                                                                                               ║"
 echo "║ $ ./run_ngs.sh start_idx end_idx working_folder atDNA xDNA haploidized feedback snp1 snp2 ...                 ║"
 echo "║                                                                                                               ║"
 echo "╙───────────────────────────────────────────────────────────────────────────────────────────────────────────────╜"
 echo
 echo "╓─┤ PARAMETERS ├────────────────────────────────────────────────────────────────────────────────────────────────╖"
 echo "║                                                                                                               ║"
 echo "║      start_idx : The starting index identifying the first pedigree to be considered.                          ║"
 echo "║        end_idx : The final index identifying the last pedigree to be considered.                              ║"
 echo "║ working_folder : The reference folder where the simulated pedigrees are stored.                               ║"
 echo "║          atDNA : If set to 1 it calls ngsRelate on autosome pedigrees (set to 0 otherwise).                   ║"
 echo "║           xDNA : If set to 1 it calls ngsRelate on X chromosome pedigrees (set to 0 otherwise).               ║"
 echo "║    haploidized : If set to 0 there is no haploidization, otherwise the data are haploidized and the process   ║"
 echo "║                  is repeated multiple times as specified by its value (i.e., haploidized=N, the process is    ║"
 echo "║                  repeated N times). It only works with autosome DNA.                                          ║"
 echo "║       feedback : If set to 1 provides additional visual feedback on the process, otherwise with 0 minimal     ║"
 echo "║                  feedback. By default is set to 1, i.e. visual feedback is active.                            ║"
 echo "║  snp1 snp2 ... : A list of SNPs reductions.                                                                   ║"
 echo "║                                                                                                               ║"
 echo "╙───────────────────────────────────────────────────────────────────────────────────────────────────────────────╜"
 echo
 echo "╓─┤ DESCRIPTION ├───────────────────────────────────────────────────────────────────────────────────────────────╖"
 echo "║                                                                                                               ║"
 echo "║ Estimate the ngsRelate parameters for a list of pedigrees (autosome, X chromosome or both). If the parameter  ║"
 echo "║ 'haploidized' is bigger than zero (e.g., haploidized=N), haploidized data which were previously stored in     ║" 
 echo "║ external files are loaded and analyzed by ngsRelate. Importantly, the haploidization is only considered for   ║"
 echo "║ autosome data (i.e., with atDNA set to 1).                                                                    ║"
 echo "║                                                                                                               ║"
 echo "║ [kinshipsim version 2020.8]                                                                                   ║"
 echo "║                                                                                                               ║"
 echo "╙───────────────────────────────────────────────────────────────────────────────────────────────────────────────╜"
 echo
 echo "╓─┤ EXAMPLE ├───────────────────────────────────────────────────────────────────────────────────────────────────╖"
 echo "║                                                                                                               ║"
 echo "║ $ ./run_ngs.sh 1 200 ./pedigrees 1 0 20 1 50000 20000 10000 5000                                              ║"
 echo "║ $ ./run_ngs.sh 1 200 ./pedigrees 1 1 20 0                                                                     ║"
 echo "║                                                                                                               ║"
 echo "╙───────────────────────────────────────────────────────────────────────────────────────────────────────────────╜"
 echo
 echo "╓"
 echo "║ Starting from pedigree $1 (pedigree_$1)"
 echo "║          to pedigree $2 (pedigree_$2)"
 echo "║ Working folder: $3"
 echo "║ Haploidization: $6"
 echo "║"
 echo "║ Apply to..."
 echo "║              Autosome data: $4"
 echo "║          X chromosome data: $5"
 echo "╙"
 echo
 echo "╓"
 echo "║ Scripts Folder: $KINSHIP_SCRIPTS_DIR"
 echo "║ Shell Scripts Folder: $KINSHIP_SHELL_DIR"
 echo "║ NgsRelate Folder: $NGSRELATE_DIR"
 echo "╙"
 echo
fi

cmd="$NGSRELATE_DIR/ngsRelate"
wd="$3"

if (( $7 >= 1 )); then
 if (( $6 >= 1 )); then
  if (( $4 == 0 )); then
   echo
   echo "Ignoring haploidized parameter as atDNA is not set"
  fi
 fi
fi

for (( i=$1;i<=$2;i++ ))
do
 folder="$wd/pedigree_$i"
 file="pedigree_$i.vcf"
 file_x="x_pedigree_$i.vcf"
 output="pedigree_$i.res"
 output_x="x_pedigree_$i.res"
 if (( $4 >= 1 )); then
  if (( $7 >= 1 )); then
   echo
   echo "Autosome VCF File(s)"
  fi
  $cmd -h "$folder"/$file -T GT -O "$folder"/$output -c 1
  for (( k=1;k<=$6;k++ ))
  do
   file="pedigree_$i""_haploid$k.vcf"
   output="pedigree_$i""_haploid$k.res"
   $cmd -h "$folder"/$file -T GT -O "$folder"/$output -c 1
  done
 fi
 if (( $5 >= 1 )); then
  if (( $7 >= 1 )); then
   echo
   echo "X Chromosome VCF File(s)"
  fi
  $cmd -h "$folder"/$file_x -T GT -O "$folder"/$output_x -c 1
 fi
 j=1
 for snp in "$@"
 do
  if (( j >= 8 )); then
   file="pedigree_$i""_$snp""_SNPs.vcf"
   file_x="x_pedigree_$i""_$snp""_SNPs.vcf"
   output="pedigree_$i""_$snp""_SNPs.res"
   output_x="x_pedigree_$i""_$snp""_SNPs.res"
   if (( $4 >= 1 )); then
    if (( $7 >= 1 )); then
     echo
     echo "Autosome VCF File(s)"
    fi
    $cmd -h "$folder"/"$file" -T GT -O "$folder"/"$output" -c 1
    for (( k=1;k<=$6;k++ ))
    do
     file="pedigree_$i""_$snp""_SNPs_haploid$k.vcf"
     output="pedigree_$i""_$snp""_SNPs_haploid$k.res"
     $cmd -h "$folder"/"$file" -T GT -O "$folder"/"$output" -c 1
    done
   fi
   if (( $5 >= 1 )); then
    if (( $7 >= 1 )); then
     echo
     echo "X Chromosome VCF File(s)"
    fi
    $cmd -h "$folder"/"$file_x" -T GT -O "$folder"/"$output_x" -c 1
   fi
  fi
  j=$((j+1))
 done
done
