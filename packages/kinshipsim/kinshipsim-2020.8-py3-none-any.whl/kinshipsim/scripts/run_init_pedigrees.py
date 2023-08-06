"""
Kinship simulation, script to initialize multiple pedigrees:
Generate multiple pedigrees for autosomal data, X chromosome data or both given source VCF files that contains founder
individuals.
NOTE: Python script to be launched from the command line.
"""

__version__ = '2020.8'
__author__ = 'Team Neogene'

import os
import sys
import fire
import random
from kinshipsim import lib
from kinshipsim.spinner import Spinner
from kinshipsim.individual import Individual
from kinshipsim.default_pedigree import DefaultPedigree


def init_pedigrees(atDNA_reference=None, xDNA_reference=None, n_pedigree=1, output_folder=None,
                   feedback=True, msg_help=True):
    """
        Generate multiple pedigrees (n_pedigree) starting from a reference VCF file that contains candidate founders
        from which the pedigrees are developed. The built pedigree can be defined on autosome data (atDNA_reference as
        the VCF source of unrelated individuals), on x chromosome data (xDNA_reference as the VCF source of unrelated
        individuals) or by both autosome and x data. Please note that at least one reference should be provided.

        :param str, optional atDNA_reference : The reference VCF file that contains autosome candidate founders for the
        pedigrees to be generated. Default None, i.e., not considered.
        :param str, optional xDNA_reference : The reference VCF file that contains x chromosome candidate founders for
        the pedigrees to be generated. Default None, i.e., not considered.
        :param int, optional n_pedigree : The number of pedigrees that should be created. Optional parameter with
        default value equal to 1.
        :param str, optional output_folder : An output folder that should be created where all the pedigrees are stored.
        Optional parameter, when not defined the folders of each pedigree are created in the current working directory.
        N.B. The output folder should not exists. It will be created during the process. If the folder already exists,
        the script will terminate with an error.
        :param bool, optional feedback : If the flag is set to True it will provide a visual feedback of the ongoing
        process, otherwise it will run silently with only minimal output.
        :param bool, optional msg_help : If the flag is set to True it provides visual help on how to use the function.
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
            print(get_msg(atDNA_reference, xDNA_reference, n_pedigree, output_folder))

    if atDNA_reference is not None:
        init_autosome_pedigrees(founders_file=atDNA_reference, n_pedigree=n_pedigree, output_folder=output_folder,
                                feedback=feedback)
        if xDNA_reference is not None:
            init_x_chr(reference_file=xDNA_reference, n_pedigree=n_pedigree, working_folder=output_folder,
                       feedback=feedback)
    elif xDNA_reference is not None:
        init_x_pedigrees(reference_file=xDNA_reference, n_pedigree=n_pedigree, working_folder=output_folder,
                         feedback=feedback)


def init_autosome_pedigrees(founders_file: str, n_pedigree=1, output_folder=None, feedback=True):
    """
    Generate multiple autosome pedigrees (n_pedigree) starting from a reference VCF file (founders_file) that contains
    candidate founders from which the pedigrees are developed.

    :param str founders_file : The autosome reference VCF file that contains candidate founders for the pedigrees.
    :param int, optional n_pedigree : The number of pedigrees that should be created. Optional parameter with default
    value equal to 1.
    :param str, optional output_folder : An output folder that should be created where all the pedigrees are stored.
    Optional parameter, when not defined the folders of each pedigree are created in the current working directory.
    N.B. The output folder should not exists. It will be created during the process. If the folder already exists,
    the script will terminate with an error.
    :param bool, optional feedback : If the flag is set to True it will provide a visual feedback of the ongoing
    process, otherwise it will run silently with only minimal output.
    """

    # create output folder if necessary
    if output_folder is not None:
        if feedback:
            msg = "Initializing output folder '{}'".format(output_folder)
            sys.stdout.write(msg)
            sys.stdout.flush()

        os.makedirs(output_folder)  # create output folder

        if feedback:
            sys.stdout.write(" [OK]")
            sys.stdout.flush()

    name, file_extension = os.path.splitext(founders_file)  # separate filename and extension

    if feedback:
        msg = "\nLoad candidate founders"
        sys.stdout.write(msg)
        sys.stdout.flush()

    unrelated_id = lib.individuals_in_vcf(founders_file)  # IDs of unrelated individuals
    random.shuffle(unrelated_id)  # random shuffling of the unrelated individuals to be selected as founders

    # check of having a sufficient number of unrelated individuals (i.e., 8) for the standard pedigree
    if len(unrelated_id) < 8:
        raise ValueError(
            "The population of unrelated individuals should have at least 8 members."
        )

    if feedback:
        sys.stdout.write(" [OK]\n")
        sys.stdout.flush()

    pedigree = DefaultPedigree()
    offset = 0  # used to select different founders for each run (reshuffle when all unrelated individuals are used)
    for idx_run in range(n_pedigree):
        if feedback:
            msg = "\nInitialization of pedigree {} ".format(idx_run + 1)
            with Spinner(msg):

                # create folder for the current run
                run_folder = "pedigree_{}".format(idx_run + 1)
                if output_folder is not None:
                    run_folder = os.path.join(output_folder, run_folder)
                os.makedirs(run_folder)

                # random selection of founders
                if 8 * offset + 8 >= len(unrelated_id):  # reached end of the list, cannot find additional 8 founders
                    offset = 0  # restart the selection
                    random.shuffle(unrelated_id)  # new shuffling of unrelated individuals to be selected as founders
                founder = unrelated_id[8 * offset: 8 * offset + 8]

                # create the population based on the defined pedigree for the current run
                run_pop = pedigree.get_pedigree(founders_file, founder)

            sys.stdout.write("[OK]")
            sys.stdout.flush()

            msg = "\nSave pedigree {} in folder '{}'".format(idx_run + 1, run_folder)
            sys.stdout.write(msg)
        else:
            # create folder for the current run
            run_folder = "pedigree_{}".format(idx_run + 1)
            if output_folder is not None:
                run_folder = os.path.join(output_folder, run_folder)
            os.makedirs(run_folder)

            # random selection of founders
            if 8 * offset + 8 >= len(unrelated_id):  # the end of the list was reached, cannot find addition 8 founders
                offset = 0  # restart the selection
                random.shuffle(unrelated_id)  # new random shuffling of unrelated individuals to be selected as founders
            founder = unrelated_id[8 * offset: 8 * offset + 8]

            # create the population based on the defined pedigree for the current run
            run_pop = pedigree.get_pedigree(founders_file, founder)

        # save the population
        pedigree_file = "pedigree_{}{}".format(idx_run + 1, file_extension)
        population_file = "pedigree_{}{}".format(idx_run + 1, ".pop")
        lib.export2vcf(
            population=run_pop,
            vcf_header_template=founders_file,
            vcf_file=os.path.join(run_folder, pedigree_file)
        )

        lib.save_object(run_pop, os.path.join(run_folder, population_file))

        if feedback:
            sys.stdout.write(" [OK]\n")
            sys.stdout.flush()

        offset = offset + 1

    if feedback:
        sys.stdout.write("\n")
        sys.stdout.flush()


def init_x_pedigrees(reference_file: str, n_pedigree=1, working_folder=None, feedback=True):
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
    """

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
                gen_x_ped(reference_file, working_folder, idx_run, idx_perm, idx_m, idx_f, n_male, n_female,
                          xchr_male, xchr_female, gender_perm)
            sys.stdout.write("[OK]")
            sys.stdout.flush()
        else:
            gen_x_ped(reference_file, working_folder, idx_run, idx_perm, idx_m, idx_f, n_male, n_female,
                      xchr_male, xchr_female, gender_perm)

        idx_perm = idx_perm + 1
        if idx_perm >= len(gender_perm):
            idx_perm = 0

    if feedback:
        sys.stdout.write("\n")
        sys.stdout.flush()


def init_x_chr(reference_file: str, n_pedigree=1, working_folder=None, feedback=True):
    """
    Generate the X chromosome for already initialized pedigrees (n_pedigree) starting from a reference VCF file
    (reference_file) that contains X chromosome information of unrelated individuals.

    :param str reference_file : The reference VCF file that contains X chromosome info of unrelated individuals.
    :param int, optional n_pedigree : The number of pedigrees that should be considered. Optional parameter with default
    value equal to 1.
    :param str, optional working_folder : The folder that where all the pedigrees are found.
    Optional parameter, when not defined the folders of each pedigree are created in the current working directory.
    :param bool, optional feedback : If the flag is set to True it will provide a visual feedback of the ongoing
    process, otherwise it will run silently with only minimal output.
    """

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

    def_pedigree = DefaultPedigree()

    id_no_gender = ["Offspring3",
                    "Offspring8",
                    "Offspring17"]

    parents_ids = def_pedigree.get_parents_ids()

    # get the gender for the pedigree and randomize gender for the unknowns
    gender = def_pedigree.get_pedigree_gender()
    ids = def_pedigree.get_pedigree_ids()
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
    pedigree_file = "{}/{}.vcf".format(pedigree_folder, pedigree_str)

    pedigree = lib.load_population(vcf_file=pedigree_file, load_all=False, feedback=False)

    if idx_m + ped_male >= n_male:
        random.shuffle(xchr_male)
        idx_m = 0
    if idx_f + ped_female >= n_female:
        random.shuffle(xchr_female)
        idx_f = 0

    # now we have the female and male candidates in candid_female and candid_male respectively
    for idx_ind, ind in enumerate(pedigree):
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

    # save the population
    x_pedigree_file = "{}/x_{}.vcf".format(pedigree_folder, pedigree_str)
    lib.export2vcf(
        population=pedigree,
        vcf_header_template=reference_file,
        vcf_file=x_pedigree_file,
        save_all=True,
        x_chromosome=True
    )


def gen_x_ped(reference_file: str, working_folder: str, idx_run: int, idx_perm: int, idx_m: int, idx_f: int,
              n_male: int, n_female: int, xchr_male: [str], xchr_female: [str], gender_perm: [[int]]):

    def_pedigree = DefaultPedigree()

    id_no_gender = ["Offspring3",
                    "Offspring8",
                    "Offspring17"]

    parents_ids = def_pedigree.get_parents_ids()

    # get the gender for the pedigree and randomize gender for the unknowns
    gender = def_pedigree.get_pedigree_gender()
    ids = def_pedigree.get_pedigree_ids()
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


def get_msg(atDNA_reference: str, xDNA_reference: str, n_pedigree: int, output_folder: str) -> str:
    """
    Format the output message.

    :param str atDNA_reference : The reference VCF file that contains candidate autosome data of founders for the
    pedigrees.
    :param str xDNA_reference : The reference VCF file that contains candidate x chromosome data of founders for the
    pedigrees.
    :param int n_pedigree : The number of pedigrees that should be created. Optional parameter with default
    value equal to 1.
    :param str output_folder : An output folder that should be created where all the pedigrees are stored.
    Optional parameter, when not defined the folders of each pedigree are created in the current working directory.
    N.B. The output folder should not exists. It will be created during the process. If the folder already exists,
    the script will terminate with an error.

    :return: str : The output message.
    """

    msg = """
╓─┤ USAGE ├─────────────────────────────────────────────────────────────────────────────────────────────────────╖
║                                                                                                               ║
║ $ python run_init_pedigrees.py [--atDNA_reference <filename.vcf>]                                             ║
║                                [--xDNA_reference <filename.vcf>]                                              ║
║                                [--n_pedigree <int>]                                                           ║
║                                [--output_folder <folder_name>]                                                ║
║                                [--feedback 0|1]                                                               ║
╙───────────────────────────────────────────────────────────────────────────────────────────────────────────────╜\n
╓─┤ PARAMETERS ├────────────────────────────────────────────────────────────────────────────────────────────────╖
║                                                                                                               ║
║ atDNA_reference : The autosome reference VCF file that contains candidate founders for the pedigrees.         ║
║  xDNA_reference : The x chromosome reference VCF file that contains candidate founders for the pedigrees.     ║
║      n_pedigree : The number of pedigrees that should be created. Optional parameter with default             ║
║                   value equal to 1.                                                                           ║
║   output_folder : An output folder that should be created where all the pedigrees are stored.                 ║
║                   Optional parameter, when not defined the folders of each pedigree are created in the        ║
║                   current working directory.                                                                  ║
║                   N.B. The output folder should not exist. It will be created during the process.             ║
║                   If the folder already exists, the script will terminate with an error.                      ║
║        feedback : If set to 1 provide additional visual feedback on the process, otherwise with 0 basic       ║
║                   feedback. Optional parameter, default value is 1.                                           ║
║                                                                                                               ║
╙───────────────────────────────────────────────────────────────────────────────────────────────────────────────╜\n
╓─┤ DESCRIPTION ├───────────────────────────────────────────────────────────────────────────────────────────────╖
║                                                                                                               ║
║ KINSHIP SIMULATION: INITIALIZE PEDIGREES                                                                      ║
║ Generate multiple autosomal, x chromosome or both type pedigrees given source VCF file(s) that contains       ║
║ founder individuals.                                                                                          ║
║                                                                                                               ║
╙───────────────────────────────────────────────────────────────────────────────────────────────────────────────╜\n
╓─┤ EXAMPLE ├───────────────────────────────────────────────────────────────────────────────────────────────────╖
║                                                                                                               ║
║ $ python run_init_pedigrees.py --atDNA_reference at_founders.vcf --xDNA_reference x_founders.vcf              ║
║                                --n_pedigree 10 --output_folder simulation -- feedback 0                       ║
║                                                                                                               ║
╙───────────────────────────────────────────────────────────────────────────────────────────────────────────────╜\n
"""
    msg_folder = output_folder
    if msg_folder is None:
        msg_folder = "."
    at_file = atDNA_reference
    if atDNA_reference is None:
        at_file = "None"
    x_file = xDNA_reference
    if xDNA_reference is None:
        x_file = "None"

    msg_info = "╓\n║ Autosome founders file: {}\n║ X chromosome founders file: {}\n║ Number of pedigrees: {}\n║ " \
               "Output folder: {}\n╙\n ".format(at_file, x_file, n_pedigree, msg_folder)

    return msg + msg_info


if __name__ == '__main__':
    fire.Fire(init_pedigrees)
