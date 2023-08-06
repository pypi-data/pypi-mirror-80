#!/bin/bash

if (( $5 >= 1 )); then
 echo
 echo "╓─┤ USAGE ├─────────────────────────────────────────────────────────────────────────────────────────────────────╖"
 echo "║                                                                                                               ║"
 echo "║ $ ./run_haploidize.sh start_idx end_idx working_folder n feedback snp1 snp2 ...                               ║"
 echo "║                                                                                                               ║"
 echo "╙───────────────────────────────────────────────────────────────────────────────────────────────────────────────╜"
 echo
 echo "╓─┤ PARAMETERS ├────────────────────────────────────────────────────────────────────────────────────────────────╖"
 echo "║                                                                                                               ║"
 echo "║      start_idx : The starting index identifying the first pedigree to be considered.                          ║"
 echo "║        end_idx : The final index identifying the last pedigree to be considered.                              ║"
 echo "║ working_folder : The reference folder where the simulated pedigrees are stored.                               ║"
 echo "║              n : The data are haploidized and the process is repeated multiple times, as specified by its     ║"
 echo "║                  value.                                                                                       ║"
 echo "║       feedback : If set to 1 provides additional visual feedback on the process, otherwise with 0 basic       ║"
 echo "║                  feedback. By default is set to 1, i.e. visual feedback is active.                            ║"
 echo "║  snp1 snp2 ... : A list of SNPs reductions.                                                                   ║"
 echo "║                                                                                                               ║"
 echo "╙───────────────────────────────────────────────────────────────────────────────────────────────────────────────╜"
 echo
 echo "╓─┤ DESCRIPTION ├───────────────────────────────────────────────────────────────────────────────────────────────╖"
 echo "║                                                                                                               ║"
 echo "║ Haploidize n times a list of autosomal pedigrees (also considering the different SNPs reduction).             ║"
 echo "║                                                                                                               ║"
 echo "║ [kinshipsim version 2020.8]                                                                                   ║"
 echo "║                                                                                                               ║"
 echo "╙───────────────────────────────────────────────────────────────────────────────────────────────────────────────╜"
 echo
 echo "╓─┤ EXAMPLE ├───────────────────────────────────────────────────────────────────────────────────────────────────╖"
 echo "║                                                                                                               ║"
 echo "║ $ ./run_haploidize.sh 1 200 ./pedigrees 20 1 50000 20000 10000 5000                                           ║"
 echo "║                                                                                                               ║"
 echo "╙───────────────────────────────────────────────────────────────────────────────────────────────────────────────╜"
 echo
 echo "╓"
 echo "║ Starting from pedigree $1 (pedigree_$1)"
 echo "║          to pedigree $2 (pedigree_$2)"
 echo "║ Working folder: $3"
 echo "║ Number of iteration: $4"
 echo "╙"
 echo
 echo "╓"
 echo "║ Scripts Folder: $KINSHIP_SCRIPTS_DIR"
 echo "║ Shell Scripts Folder: $KINSHIP_SHELL_DIR"
 echo "╙"
 echo
fi

cmd="$KINSHIP_SCRIPTS_DIR/run_haploidize.py"
wd="$3"

for (( i=$1;i<=$2;i++ ))
do
 folder="$wd/pedigree_$i"
 file="pedigree_$i.vcf"

 python "$cmd" --vcf_file "$folder"/$file --n "$4" --feedback "$5" --msg_help 0
 j=1
 for snp in "$@"
 do
  if (( j >= 6 )); then
   file="pedigree_$i""_$snp""_SNPs.vcf"
   python "$cmd" --vcf_file "$folder"/"$file" --n "$4" --feedback "$5" --msg_help 0
  fi
  j=$((j+1))
 done
done
