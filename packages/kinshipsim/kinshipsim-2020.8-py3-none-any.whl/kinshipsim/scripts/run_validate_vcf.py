"""
Kinship simulation, VCF validation script:
Check integrity and consistency of the VCF file.
NOTE: Python script to be launched from the command line.
"""

__version__ = '2020.8'
__author__ = 'Team Neogene'

import logging
import os
import sys
import fire
from kinshipsim import lib


def validate(filename: str, feedback=True, msg_help=True):
    """
    Validate the structure of the VCF file (filename). If any error is found it attempts to fix it.

    :param str filename : The name of the VCF file to be validated.
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
            print(get_msg(filename))

    name, file_extension = os.path.splitext(filename)  # separate filename and extension
    summ = lib.summary(filename, feedback)  # analyze the VCF file and produce a summary
    print_summary("SUMMARY REPORT", summ)  # simple printout of the summary

    # if any issues are found ask user to allow an attempt to fix the reference file
    if len(summ["misplaced_entry"]) > 0 or len(summ["duplicate_entry"]) > 0:
        msg = "The reference file '{}' has inconsistencies that will affect the simulation.\nDo you want to " \
              "attempt to fix the file? (Y)es or (N)o: ".format(filename)
        done = False
        a = ""
        while not done:  # wait for proper input from user
            a = input(msg)
            a = a.upper()
            if a == "Y" or a == "N":
                done = True
            else:
                msg = "Press Y for Yes or N for No: "

        if a == "Y":
            sys.stdout.write("\nAttempting to fix the file...")
            sys.stdout.flush()
            new_file = "{}_fix{}".format(name, file_extension)
            lib.fix_vcf(filename, new_file, summ)
            summ_fix = lib.summary(new_file, feedback)
            sys.stdout.write(" [OK]\n\n")
            sys.stdout.flush()
            print_summary("SUMMARY REPORT", summ_fix)  # simple printout of the summary
            if len(summ_fix["misplaced_entry"]) > 0 or len(summ_fix["duplicate_entry"]) > 0:  # failed to fix
                msg = "The attempt to fix the reference file '{}' did not succeed.".format(filename)
                raise ValueError(msg)
            else:  # successfully fixed
                msg = "Reference file successfully fixed and saved as '{}'.".format(new_file)
                logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
                logging.info(msg)


def get_msg(vcf_file: str) -> str:
    """
    Format the output message.

    :param str vcf_file : The VCF file where to add the frequency values.

    :return: str : The output message.
    """

    msg = """
╓─┤ USAGE ├─────────────────────────────────────────────────────────────────────────────────────────────────────╖
║                                                                                                               ║
║ $ python run_validate_vcf.py --filename <filename.vcf>                                                        ║
║                              [--feedback 0|1]                                                                 ║
╙───────────────────────────────────────────────────────────────────────────────────────────────────────────────╜\n
╓─┤ PARAMETERS ├────────────────────────────────────────────────────────────────────────────────────────────────╖
║                                                                                                               ║
║ filename : The VCF file that need to be checked.                                                              ║
║ feedback : If set to 1 provide additional visual feedback on the process, otherwise with 0 basic feedback.    ║
║            Optional parameter, default value is 1.                                                            ║
║                                                                                                               ║
╙───────────────────────────────────────────────────────────────────────────────────────────────────────────────╜\n
╓─┤ DESCRIPTION ├───────────────────────────────────────────────────────────────────────────────────────────────╖
║                                                                                                               ║
║ KINSHIP SIMULATION: VALIDATE VCF FILE                                                                         ║
║ Check integrity and consistency of the VCF file.                                                              ║
║                                                                                                               ║
╙───────────────────────────────────────────────────────────────────────────────────────────────────────────────╜\n
╓─┤ EXAMPLE ├───────────────────────────────────────────────────────────────────────────────────────────────────╖
║                                                                                                               ║
║ $ python run_validate_vcf.py --filename dataset.vcf --feedback 1                                              ║
║                                                                                                               ║
╙───────────────────────────────────────────────────────────────────────────────────────────────────────────────╜\n
"""

    msg_info = "╓\n║ VCF file: {}\n╙\n".format(vcf_file)

    return msg + msg_info


def print_summary(title: str, summary: dict):
    """
    Simple printout of the summary.

    :param str title: The title of the summary.
    :param dict summary: The dictionary that summarize the VCF check.
    """

    print("\n╓─┤ {} ├───────────────────────────────────────────────────────────────────────────────────────────────────╖".format(title))
    print("║ SNPs: {}".format(summary["snps"]))
    chromosomes = summary["chromosome"]
    print("║ Chromosomes: {}".format(chromosomes))
    positions = summary["position"]
    tot_snps = 0
    for p in positions:
        for idx_entry in range(len(p)):
            tot_snps = tot_snps + 1
    print("║ Verified SNPs: {}".format(tot_snps))
    print("║ Number of duplicate entries: {}".format(len(summary["duplicate_entry"])))
    buffer_msg = "─" * (len(title) + 2)
    print("║ Number of misplaced entries: {}\n╙─{}─────────────────────────────────────────────────────────────────────────────────────────────────────╜\n".format(
        len(summary["misplaced_entry"]), buffer_msg))


if __name__ == '__main__':
    fire.Fire(validate)
