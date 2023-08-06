"""
Kinship simulation, merge frequency values script:
Add frequency values (loaded from FRQ and MAP files) to a VCF file through the TAG 'AFngsrelate'.
NOTE: Python script to be launched from the command line.
"""

__version__ = '2020.8'
__author__ = 'Team Neogene'


import sys
import fire
from kinshipsim import lib
from kinshipsim.spinner import Spinner


def merge(vcf_file: str, maf_file: str, map_file=None, feedback=True, msg_help=True):
    """
    Add the frequency values to the specified VCF file.

    :param str vcf_file : The VCF file where to add the frequency values.
    :param str maf_file : The file containing the frequency values.
    :param str, optional map_file : The MAP file with positional references.
    :param bool, optional feedback : If the flag is set to True it will provide a visual feedback of the ongoing
    process, otherwise it will run silently with only minimal output.
    :param bool, optional msg_help : If the flag is set to True it provides a visual help on how to use the function.
    Default value is True. Whenever the feedback flag is set to False, the msg_help flag is ignored.
    """

    # Parameters configuration:
    #
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
            msg = get_msg(vcf_file, maf_file, map_file)
        else:
            msg = "╓\n║ Frequency file: {}\n║ Map file: {}\n║ Destination file: {}\n╙\nMerging ".format(
                maf_file, map_file, vcf_file)
        with Spinner(msg):
            lib.maf2vcf(maf_file, vcf_file, map_file)
        sys.stdout.write("[OK]\n")
        sys.stdout.flush()
    else:
        lib.maf2vcf(maf_file, vcf_file, map_file)


def get_msg(vcf_file: str, maf_file: str, map_file: str) -> str:
    """
    Format the output message.

    :param str vcf_file : The VCF file where to add the frequency values.
    :param str maf_file : The file containing the frequency values.
    :param str map_file : The MAP file with positional references.

    :return: The output message.
    """

    msg = """
╓─┤ USAGE ├─────────────────────────────────────────────────────────────────────────────────────────────────────╖
║                                                                                                               ║
║ $ python run_maf2vcf.py --vcf_file <filename.vcf>                                                             ║
║                         --maf_file <filename.frq>                                                             ║
║                        [--map_file <filename.map>]                                                            ║
║                        [--feedback 0|1]                                                                       ║
╙───────────────────────────────────────────────────────────────────────────────────────────────────────────────╜\n
╓─┤ PARAMETERS ├────────────────────────────────────────────────────────────────────────────────────────────────╖
║                                                                                                               ║
║ vcf_file : The VCF file where to add the frequency values.                                                    ║
║ maf_file : The file containing the frequency values.                                                          ║
║ map_file : The MAP file with positional references. Optional if all information are store into the maf_file.  ║
║ feedback : If set to 1 provide additional visual feedback on the process, otherwise with 0 basic feedback.    ║
║            Optional parameter, default value is 1.                                                            ║
║                                                                                                               ║
╙───────────────────────────────────────────────────────────────────────────────────────────────────────────────╜\n
╓─┤ DESCRIPTION ├───────────────────────────────────────────────────────────────────────────────────────────────╖
║                                                                                                               ║
║ KINSHIP SIMULATION: INSERT FREQUENCY VALUES                                                                   ║
║ Add frequency values (loaded from FRQ and MAP files) to a VCF file through the TAG 'AFngsrelate'.             ║
║                                                                                                               ║
╙───────────────────────────────────────────────────────────────────────────────────────────────────────────────╜\n
╓─┤ EXAMPLE ├───────────────────────────────────────────────────────────────────────────────────────────────────╖
║                                                                                                               ║
║ $ python run_maf2vcf.py --vcf_file population.vcf --maf_file freqs.frq --map_file freqs.map --feedback 0      ║
║                                                                                                               ║
╙───────────────────────────────────────────────────────────────────────────────────────────────────────────────╜\n
"""

    msg_info = "╓\n║ Frequency file: {}\n║ Map file: {}\n║ Destination file: {}\n╙\nMerging ".format(
        maf_file, map_file, vcf_file)

    return msg + msg_info


if __name__ == '__main__':
    fire.Fire(merge)
