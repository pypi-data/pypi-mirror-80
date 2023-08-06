#!/bin/bash 

if (( $7 >= 1 )); then
 echo
 echo "╓─┤ USAGE ├─────────────────────────────────────────────────────────────────────────────────────────────────────╖"
 echo "║                                                                                                               ║"
 echo "║ $ ./run_reduce_snps.sh start_idx end_idx n_snps working_folder atDNA xDNA feedback                            ║"
 echo "║                                                                                                               ║"
 echo "╙───────────────────────────────────────────────────────────────────────────────────────────────────────────────╜"
 echo
 echo "╓─┤ PARAMETERS ├────────────────────────────────────────────────────────────────────────────────────────────────╖"
 echo "║                                                                                                               ║"
 echo "║      start_idx : The starting index identifying the first pedigree to be considered.                          ║"
 echo "║        end_idx : The final index identifying the last pedigree to be considered.                              ║"
 echo "║         n_snps : A list with the number of SNPs reductions.                                                   ║"
 echo "║ working_folder : The reference folder where the simulated pedigrees are stored.                               ║"
 echo "║          atDNA : If set to 1 it performs the SNPs reduction on autosome pedigrees (set to 0 otherwise).       ║"
 echo "║           xDNA : If set to 1 it performs the SNPs reduction on X chromosome pedigrees (set to 0 otherwise).   ║"
 echo "║       feedback : If set to 1 provide additional visual feedback on the process,                               ║"
 echo "║                  otherwise with 0 basic feedback.                                                             ║"
 echo "║                                                                                                               ║"
 echo "╙───────────────────────────────────────────────────────────────────────────────────────────────────────────────╜"
 echo
 echo "╓─┤ DESCRIPTION ├───────────────────────────────────────────────────────────────────────────────────────────────╖"
 echo "║                                                                                                               ║"
 echo "║ Reduce the number of SNPs for a list of pedigrees for autosome and/or X chromosome data.                      ║"
 echo "║ Each pedigree is stored in assumed to be store in a separate folder 'pedigree_n' with n = 1, 2, ...           ║"
 echo "║ The main folder, i.e., 'working_folder' should contains all the pedigrees subfolders.                         ║"
 echo "║                                                                                                               ║"
 echo "║ [kinshipsim version 2020.8]                                                                                   ║"
 echo "║                                                                                                               ║"
 echo "╙───────────────────────────────────────────────────────────────────────────────────────────────────────────────╜"
 echo
 echo "╓─┤ EXAMPLE ├───────────────────────────────────────────────────────────────────────────────────────────────────╖"
 echo "║                                                                                                               ║"
 echo "║ $ ./run_reduce_snps.sh 1 200 [50000,20000,10000,5000] ./pedigrees 1 0 1                                       ║"
 echo "║                                                                                                               ║"
 echo "╙───────────────────────────────────────────────────────────────────────────────────────────────────────────────╜"
 echo
 echo "╓"
 echo "║ Starting from pedigree $1 (pedigree_$1)"
 echo "║          to pedigree $2 (pedigree_$2)"
 echo "║          with reduced SNPs count of $3"
 echo "║ Working folder: $4"
 echo "║"
 echo "║ Apply to..."
 echo "║              Autosome data: $5"
 echo "║          X chromosome data: $6"
 echo "╙"
 echo
 echo "╓"
 echo "║ Scripts Folder: $KINSHIP_SCRIPTS_DIR"
 echo "║ Shell Scripts Folder: $KINSHIP_SHELL_DIR"
 echo "╙"
fi

cmd="$KINSHIP_SCRIPTS_DIR/run_reduce_snps.py"
wd="$4"

for (( i=$1;i<=$2;i++ ))
do
 if (( $7 >= 1 )); then
  echo
  echo "───────────────────────────────────────────────────────────────────────────────────────────────────────────────"
  echo
 fi

 folder="$wd/pedigree_$i"
 file="pedigree_$i.vcf"
 file_x="x_pedigree_$i.vcf"
 #! snp="'$3'"
 snp="($3)"

 if (( $7 >= 1 )); then
  echo "SNPs: $snp"
  echo "Folder: $folder"
 fi

 if (( $5 >= 1 )); then
  if (( $7 >= 1 )); then
   echo
   echo "Autosome VCF File: $file"
  fi
  python "$cmd" --vcf_file $file --n_snps $snp --working_folder "$folder" --feedback "$7" --msg_help 0
 fi
 if (( $6 >= 1 )); then
  if (( $7 >= 1 )); then
   echo
   echo "X Chromosome VCF File: $file_x"
  fi
  python "$cmd" --vcf_file $file_x --n_snps $snp --working_folder "$folder" --feedback "$7" --msg_help 0
 fi
done
