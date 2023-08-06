"""
Kinship simulation, script to perform pseudo-haploidization (repeated multiple times) of a given VCF file:
Given a reference VCF file, it generates multiple haploidized versions exported as VCF file as well.
NOTE: Python script to be launched from the command line.
"""

__version__ = '2020.8'
__author__ = 'Team Neogene'

import fire
from kinshipsim import lib


def haploidize(vcf_file: str, n: int, suffix="_haploid", feedback=True, msg_help=True):
    """
    Given a reference VCF file, it generates multiple (n) haploidized versions which are then exported in VCF files.

    :param str vcf_file : The reference VCF file that contains the samples to be haploidized.
    :param int n : The number of times the reference data need to be haploidized.
    :param str, optional suffix : Given the reference VCF file, the suffix is used to create the
    haploidized versions of it (instead of computing it on the fly). Default suffix is '_haploid'.
    Ex. : suffix = "_haploid"
          vcf_file = "path/population.vcf"
          n = 3
          Files to be created with haploidized versions of the population:
          "path/population_haploid1.vcf"
          "path/population_haploid2.vcf"
          "path/population_haploid3.vcf"
    :param bool, optional feedback : If the flag is set to True it will provide a visual feedback of the ongoing
    process, otherwise it will run silently with only minimal output.
    :param bool, optional msg_help : If the flag is set to True it will provide a visual description of the function.
    Default value is True. Whenever the feedback flag is set to False, the msg_help flag is ignored.
    """

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

    if type(n) is str:
        try:
            n = int(n)
        except ValueError:
            n = None

    if feedback:
        print(get_msg(vcf_file=vcf_file, msg_help=msg_help))

    lib.haploidization(vcf_file=vcf_file, n=n, suffix=suffix, feedback=feedback)


def get_msg(vcf_file: str, msg_help=True) -> str:
    """
    Format the output message.

    :param str vcf_file : The VCF file that contains the samples to be studied.
    :param bool, optional msg_help : If the flag is set to True it provides a visual help on how to use the function.
    Default value is True. Whenever the feedback flag is set to False, the msg_help flag is ignored.

    :return: str : The output message.
    """

    msg_info = "╓\n║ VCF file: {}\n╙\n ".format(vcf_file)

    if msg_help:
        msg = """
╓─┤ USAGE ├─────────────────────────────────────────────────────────────────────────────────────────────────────╖
║                                                                                                               ║
║ $ python run_haploidize.py --vcf_file <filename.vcf>                                                          ║
║                            --n <int>                                                                          ║
║                            [--suffix <str>]                                                                   ║
║                            [--feedback 0|1]                                                                   ║
╙───────────────────────────────────────────────────────────────────────────────────────────────────────────────╜\n
╓─┤ PARAMETERS ├────────────────────────────────────────────────────────────────────────────────────────────────╖
║                                                                                                               ║
║    vcf_file : The VCF file that contains the samples to be haploidized.                                       ║
║           n : The number of times the reference data need to be haploidized.                                  ║
║      suffix : If the VCF file is a reference file, the suffix is used to generate the name of the             ║
║               haploidized versions of it. Default suffix is '_haploid'.                                       ║
║               Optional parameter, default value is '_haploid'.                                                ║
║    feedback : If set to 1 provide additional visual feedback on the process, otherwise with 0 basic feedback  ║
║               Optional parameter, default value is 0.                                                         ║
║                                                                                                               ║
╙───────────────────────────────────────────────────────────────────────────────────────────────────────────────╜\n
╓─┤ DESCRIPTION ├───────────────────────────────────────────────────────────────────────────────────────────────╖
║                                                                                                               ║
║ KINSHIP SIMULATION: PSEUDO-HAPLOIDIZATION                                                                     ║
║ Given a reference VCF file, it generates multiple (n) haploidized versions which are then stored as           ║
║ VCF files.                                                                                                    ║
║                                                                                                               ║
╙───────────────────────────────────────────────────────────────────────────────────────────────────────────────╜\n
╓─┤ EXAMPLE ├───────────────────────────────────────────────────────────────────────────────────────────────────╖
║                                                                                                               ║
║ $ python run_haploidize.py --vcf_file samples.vcf --n 10                                                      ║
║ $ python run_haploidize.py --vcf_file samples.vcf --n 10 --suffix hap --feedback 0                            ║
║                                                                                                               ║
╙───────────────────────────────────────────────────────────────────────────────────────────────────────────────╜\n
"""
        msg = msg + msg_info
    else:
        msg = msg_info

    return msg


if __name__ == '__main__':
    fire.Fire(haploidize)
