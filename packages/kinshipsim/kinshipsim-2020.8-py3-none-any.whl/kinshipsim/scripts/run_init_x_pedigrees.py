"""
Kinship simulation, script for the initialization of X chromosome data for multiple pedigrees:
Generate pedigrees with only the X chromosome.
It requires a source VCF file that contains X chromosome from unrelated individuals.
NOTE: Python script to be launched from the command line.
"""

__version__ = '2020.6'
__author__ = 'Team Neogene'

import os
import random
import sys
import fire
from kinshipsim import lib
from kinshipsim.individual import Individual
from kinshipsim.spinner import Spinner
from kinshipsim.default_pedigree import DefaultPedigree


def init_x_chr_pedigrees(reference_file: str, n_pedigree=1, working_folder=None, feedback=True, msg_help=True):
    """
    Initialize pedigrees (n_pedigree) only with the X chromosome starting from a reference VCF file
    (reference_file) that contains X chromosome data of unrelated individuals.

    :param str reference_file : The reference VCF file that contains X chromosome info of unrelated individuals.
    :param int, optional n_pedigree : The number of pedigrees that should be considered. Optional parameter with default
    value equal to 1.
    :param str, optional working_folder : The folder that where all the pedigrees are stored.
    Optional parameter, when not defined the folders of each pedigree are created in the current working directory.
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
            print(get_msg(reference_file, n_pedigree, working_folder))

    if feedback:
        msg = "\nLoad X chromosome of unrelated individuals "
        sys.stdout.write(msg)
        sys.stdout.flush()

    gender_perm = [[0, 0, 0],
                   [0, 0, 1],
                   [0, 1, 0],
                   [0, 1, 1],
                   [1, 0, 0],
                   [1, 0, 1],
                   [1, 1, 0],
                   [1, 1, 1]]

    unr_xchr = lib.load_population(vcf_file=reference_file,
                                   feedback=False)  # load X chromosome data of the unrelated individuals

    unr_gender = []
    for ind in unr_xchr:
        xchr = ind.chromosomes[0]
        gender = 1
        for snp in xchr:
            strand = snp.split("|")
            if not strand[0] == strand[1]:
                gender = 0
                break
        unr_gender.append(gender)

    # separate X chromosome of males and females
    xchr_male = []
    xchr_male_id = []
    xchr_female = []
    xchr_female_id = []
    for idx_xchr, xchr in enumerate(unr_xchr):
        x = xchr.chromosomes[0]
        if unr_gender[idx_xchr] == 1:  # male
            xchr_male.append(x)
            xchr_male_id.append(xchr.id)
        else:  # female
            xchr_female.append(x)
            xchr_female_id.append(xchr.id)

    if feedback:
        msg_info = "[OK]\n╓\n║ Number of individuals: {}\n║ Females: {}\n║ Males: {}\n╙\n ".format(
            len(unr_gender), len(xchr_female), len(xchr_male))
        sys.stdout.write(msg_info)
        sys.stdout.flush()

    # initialize and randomize the sequences
    random.shuffle(xchr_male)
    random.shuffle(xchr_female)
    idx_m = 0
    idx_f = 0

    # number of X chromosomes samples per gender
    n_male = len(xchr_male)
    n_female = len(xchr_female)

    idx_perm = 0
    for idx_run in range(n_pedigree):
        if feedback:
            msg = "\nInitialize X chromosomes for pedigree {} ".format(idx_run + 1)
            with Spinner(msg):
                gen_x_chr(reference_file, working_folder, idx_run, idx_perm, idx_m, idx_f, n_male, n_female,
                          xchr_male, xchr_female, gender_perm)
            sys.stdout.write("[OK]")
            sys.stdout.flush()
        else:
            gen_x_chr(reference_file, working_folder, idx_run, idx_perm, idx_m, idx_f, n_male, n_female,
                      xchr_male, xchr_female, gender_perm)

        idx_perm = idx_perm + 1
        if idx_perm >= len(gender_perm):
            idx_perm = 0

    if feedback:
        sys.stdout.write("\n")
        sys.stdout.flush()


def gen_x_chr(reference_file: str, working_folder: str, idx_run: int, idx_perm: int, idx_m: int, idx_f: int,
              n_male: int, n_female: int, xchr_male: [str], xchr_female: [str], gender_perm: [[int]]):

    pedigree = DefaultPedigree()

    id_no_gender = ["Offspring3",
                    "Offspring8",
                    "Offspring17"]

    parents_ids = pedigree.get_parents_ids()

    # get the gender for the pedigree and randomize gender for the unknowns
    gender = pedigree.get_pedigree_gender()
    ids = pedigree.get_pedigree_ids()
    ped_male = 0
    ped_female = 0
    for idx_g in range(len(gender)):
        if gender[idx_g] == -1:
            if ids[idx_g] == id_no_gender[0]:
                gender[idx_g] = gender_perm[idx_perm][0]
            elif ids[idx_g] == id_no_gender[1]:
                gender[idx_g] = gender_perm[idx_perm][1]
            elif ids[idx_g] == id_no_gender[2]:
                gender[idx_g] = gender_perm[idx_perm][2]
            else:
                print("Unknown ID: {}".format(ids[idx_g]))
                gender[idx_g] = random.choice([0, 1])

        if gender[idx_g] == 0:
            ped_female = ped_female + 1
        elif gender[idx_g] == 1:
            ped_male = ped_male + 1

    pedigree_str = "pedigree_{}".format(idx_run + 1)
    pedigree_folder = pedigree_str
    if working_folder is not None:
        pedigree_folder = os.path.join(working_folder, pedigree_folder)

    # create folder for the current run
    os.makedirs(pedigree_folder)

    if idx_m + ped_male >= n_male:
        random.shuffle(xchr_male)
        idx_m = 0
    if idx_f + ped_female >= n_female:
        random.shuffle(xchr_female)
        idx_f = 0

    # now we have the female and male candidates
    pedigree = []
    for idx_ind, id_ind in enumerate(ids):
        ind = Individual(ind_id=id_ind)
        ind.set_gender(gender=gender[idx_ind])
        if "Founder" in ind.id:
            if gender[idx_ind] == 0:
                x = xchr_female[idx_f]
                idx_f = idx_f + 1
            else:
                x = xchr_male[idx_m]
                idx_m = idx_m + 1

            ind.set_x_chromosome(x_chromosome=x)
        else:
            ind.set_parents([lib.get_individual(pedigree, parents_ids[idx_ind][0]),
                             lib.get_individual(pedigree, parents_ids[idx_ind][1])])
            ind.x_breed()
        pedigree.append(ind)

    # save the population
    x_pedigree_file = "{}/x_{}.vcf".format(pedigree_folder, pedigree_str)
    lib.export2vcf(
        population=pedigree,
        vcf_header_template=reference_file,
        vcf_file=x_pedigree_file,
        save_all=True,
        x_chromosome=True
    )


def get_msg(reference_file: str, n_pedigree: int, working_folder: str) -> str:
    """
    Format the output message.

    :param str reference_file : The reference VCF file that contains X chromosome data.
    :param int n_pedigree : The number of pedigrees that should be considered. Optional parameter with default
    value equal to 1.
    :param str working_folder : Where to find the pedigrees.

    :return: str : The output message.
    """

    msg = """
╓─┤ USAGE ├─────────────────────────────────────────────────────────────────────────────────────────────────────╖
║                                                                                                               ║
║ $ python run_insert_x_pedigrees.py --reference_file <filename.vcf>                                            ║
║                                   [--n_pedigree <int>]                                                        ║
║                                   [--working_folder <folder_name>]                                            ║
║                                   [--feedback 0|1]                                                            ║
╙───────────────────────────────────────────────────────────────────────────────────────────────────────────────╜\n
╓─┤ PARAMETERS ├────────────────────────────────────────────────────────────────────────────────────────────────╖
║                                                                                                               ║
║ reference_file : The reference VCF file that contains X chromosome data of unrelated individuals.             ║
║     n_pedigree : The number of pedigrees that should be considered. Optional parameter with default           ║
║                 value equal to 1.                                                                             ║
║ working_folder : Folder where all the pedigrees are stored.                                                   ║
║                  Optional parameter, when not defined the folders of each pedigree are considered to be in    ║
║                  the current directory.                                                                       ║
║       feedback : If set to 1 provide additional visual feedback on the process, otherwise with 0 basic        ║
║                  feedback. Optional parameter, default value is 1.                                            ║
║                                                                                                               ║
╙───────────────────────────────────────────────────────────────────────────────────────────────────────────────╜\n
╓─┤ DESCRIPTION ├───────────────────────────────────────────────────────────────────────────────────────────────╖
║                                                                                                               ║
║ KINSHIP SIMULATION: INITIALIZE X CHROMOSOME PEDIGREES                                                         ║
║ Simulate X chromosome data, by generating a series of pedigrees, given a source VCF file that contains        ║
║ X chromosome information of a set of unrelated                                                                ║
║                                                                                                               ║
╙───────────────────────────────────────────────────────────────────────────────────────────────────────────────╜\n
╓─┤ EXAMPLE ├───────────────────────────────────────────────────────────────────────────────────────────────────╖
║                                                                                                               ║
║ $ python run_insert_x_pedigrees.py --reference_file unrelated_x_chromosome.vcf --n_pedigree 10                ║
║                                    --working_folder simulation -- feedback 0                                  ║
║                                                                                                               ║
╙───────────────────────────────────────────────────────────────────────────────────────────────────────────────╜\n
"""
    msg_folder = working_folder
    if msg_folder is None:
        msg_folder = "."
    msg_info = "╓\n║ Reference file: {}\n║ Number of pedigrees: {}\n║ Working folder: {}\n╙\n ".format(
        reference_file, n_pedigree, msg_folder)

    return msg + msg_info


if __name__ == '__main__':
    fire.Fire(init_x_chr_pedigrees)
