"""
Kinship simulation, script to reduce the number of SNPs in a given VCF file:
Given a VCF file, it generates alternative versions with reduced SNPs.
NOTE: Python script to be launched from the command line.
"""

__version__ = '2020.8'
__author__ = 'Team Neogene'

import ast
import os
import sys
import fire
from kinshipsim import lib
from kinshipsim.spinner import Spinner


def reduce_snps(vcf_file: str, n_snps: [int], working_folder=None, feedback=True, msg_help=True):
    """
    Reduce the number of SNPs of the samples in a given VCF file.

    :param str vcf_file : The reference VCF file that contains the samples.
    :param [int] n_snps : A list of integers that defines the number of SNPs to retain.
    :param str, optional working_folder : A reference folder where the newly generate VCF files (with reduced SNPs)
    are saved. Optional parameter, when not defined the current folder is considered the working directory.
    :param bool, optional feedback : If the flag is set to True it will provide a visual feedback of the ongoing
    process, otherwise it will run silently with only minimal output.
    :param bool, optional msg_help : If the flag is set to True it will provide a visual help on how to use the function.
    Default value is True. Whenever the feedback flag is set to False, the msg_help flag is ignored.
    """

    if type(n_snps) is str:
        n_snps = ast.literal_eval(n_snps)

    if type(feedback) is str:
        if feedback == '1':
            feedback = True
        else:
            feedback = False

    if type(msg_help) is str:
        if msg_help == '1':
            msg_help = True
        else:
            msg_help = False

    if feedback:
        if msg_help:
            print(get_msg(vcf_file, n_snps, working_folder))

    name, file_extension = os.path.splitext(vcf_file)  # separate filename and extension

    # the current population
    if working_folder is not None:
        vcf_file = os.path.join(working_folder, vcf_file)

    for snp in n_snps:
        if not (snp == -1):  # -1 means retains all SNPs

            # reduce the number of SNPs of the reference file
            if feedback:
                msg = "\nFrom {} reduce SNPs to {} ".format(vcf_file, snp)
                with Spinner(msg):

                    # file for the reduced SNPs
                    snp_file = "{}_{}_SNPs{}".format(name, snp, file_extension)
                    if working_folder is not None:
                        snp_file = os.path.join(working_folder, snp_file)

                    lib.reduce_snps(input_file=vcf_file, output_file=snp_file, n_snps=snp)

                sys.stdout.write("[OK]")
                sys.stdout.flush()
            else:

                # file for the reduced SNPs
                snp_file = "{}_{}_SNPs{}".format(name, snp, file_extension)
                if working_folder is not None:
                    snp_file = os.path.join(working_folder, snp_file)

                lib.reduce_snps(input_file=vcf_file, output_file=snp_file, n_snps=snp)
    if feedback:
        sys.stdout.write("\n")
        sys.stdout.flush()


def get_msg(vcf_file: str, n_snps: [int], working_folder: str) -> str:
    """
    Format the output message.

    :param str vcf_file : The reference VCF file that contains the population of the pedigree.
    :param [int] n_snps : A list of integers that defining the number of SNPs to retain.
    :param str, optional working_folder : A reference folder where the newly generate VCF files (with reduced SNPs)
    are saved. Optional parameter, when not defined the current folder is considered the working directory.

    :return: str : The output message.
    """

    msg = """
╓─┤ USAGE ├─────────────────────────────────────────────────────────────────────────────────────────────────────╖
║                                                                                                               ║
║ $ python run_reduce_snps.py --vcf_file <filename.vcf>                                                         ║
║                             --n_snps <[int]>                                                                  ║
║                             [--working_folder <folder_name>]                                                  ║
║                             [--feedback 0|1]                                                                  ║
╙───────────────────────────────────────────────────────────────────────────────────────────────────────────────╜\n
╓─┤ PARAMETERS ├────────────────────────────────────────────────────────────────────────────────────────────────╖
║                                                                                                               ║
║       vcf_file : The reference VCF file that contains the population of the pedigree.                         ║
║         n_snps : A list of integers that defining the number of SNPs to retain.                               ║
║ working_folder : A reference folder where the newly generate VCF files (with reduced SNPs) are saved.         ║
║                  Optional parameter, when not defined the current folder is considered the working directory. ║
║       feedback : If set to 1 provide additional visual feedback on the process, otherwise with 0 basic        ║
║                  feedback. Optional parameter, default value is 1.                                            ║
║                                                                                                               ║
╙───────────────────────────────────────────────────────────────────────────────────────────────────────────────╜\n
╓─┤ DESCRIPTION ├───────────────────────────────────────────────────────────────────────────────────────────────╖
║                                                                                                               ║
║ KINSHIP SIMULATION: REDUCE SNPs                                                                               ║
║ Given a dataset stored in a VCF file, it generates alternative versions with reduced SNPs.                    ║
║                                                                                                               ║
╙───────────────────────────────────────────────────────────────────────────────────────────────────────────────╜\n
╓─┤ EXAMPLE ├───────────────────────────────────────────────────────────────────────────────────────────────────╖
║                                                                                                               ║
║ $ python run_reduce_snps.py --vcf_file samples.vcf                                                            ║
║                             --n_snps [50000,20000,10000,5000]                                                 ║
║                             --working_folder simulation                                                       ║
║                                                                                                               ║
╙───────────────────────────────────────────────────────────────────────────────────────────────────────────────╜\n
"""
    msg_folder = working_folder
    if msg_folder is None:
        msg_folder = "."
    msg_info = "╓\n║ Founders file: {}\n║ Number of pedigrees: {}\n║ Output folder: {}\n╙\n ".format(
        vcf_file, n_snps, msg_folder)

    return msg + msg_info


if __name__ == '__main__':
    fire.Fire(reduce_snps)
