"""
Kinship simulation, script to import the results:
Read and export the ngsRelate results for all pedigrees and for the desired data type, i.e., autosome data, X chromosome
data or both.
NOTE: Python script to be launched from the command line.
"""

__version__ = '2020.8'
__author__ = 'Team Neogene'

import os
import math
import fire
import numpy as np
import pandas as pd
from kinshipsim import lib
from kinshipsim.default_pedigree import DefaultPedigree


def sim_results(working_folder: str, info_type: str, snps=None, n_ped=1, idx_haploid=-1,
                feedback=True, msg_help=True):
    """
    Collect the results from the simulated pedigrees given the degree/relationships of interest for autosome or X DNA
    data. Also individual haploidized versions can be selected.

    :param str working_folder: The reference folder where the VCF files are saved.
    :param str info_type: Defines the type of results to be shown, i.e., atDNA_deg (autosome DNA for the 1st, 2nd and 3rd
    degrees and unrelated samples), atDNA_rel (autosome DNA for siblings, parent-offspring, half-siblings and
    aunt|uncle-niece|nephew relationships) or xDNA (X chromosome DNA for the half-brothers, mother-daughter, mother-son,
    father-daughter, father-son, sisters, brothers, sister-brother and uncle-nephew relationships).
    :param [int], optional snps: A list of integers that defines the number of SNPs to be considered.
    :param int, optional n_ped: The number of pedigrees that should be considered. Default value is 1.
    :param int, optional idx_haploid: Identifies which haploidized version should be considered. Default value is -1,
    i.e. no haploidization is considered.
    :param bool, optional feedback: If the flag is set to True it will provide a visual feedback of the ongoing process,
    otherwise it will run silently with only minimal output. Default value is True.
    :param bool, optional msg_help: If the flag is set to True it provides visual help on how to use the function.
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

    if type(n_ped) is str:
        n_ped = int(n_ped)

    if type(idx_haploid) is str:
        idx_haploid = int(idx_haploid)

    if snps is None:
        snps = []

    if feedback:
        if msg_help:
            print(get_msg(working_folder=working_folder, info_type=info_type, n_ped=n_ped, idx_haploid=idx_haploid))

    if "atDNA" in info_type:
        autosome_pedigrees(working_folder=working_folder, snps=snps, n_ped=n_ped, info_type=info_type,
                           idx_haploid=idx_haploid, feedback=feedback)
    else:
        x_chromosome_pedigrees(working_folder=working_folder, snps=snps, n_ped=n_ped)


def get_msg(working_folder: str, info_type: str, n_ped: int, idx_haploid: int) -> str:
    """
    Format the output message.

    :param str working_folder : The reference folder where the VCF files are saved.
    :param str info_type : Defines the type of results to be shown, i.e., atDNA_deg (autosome DNA for the 1st, 2nd and 3rd
    degrees and unrelated samples), atDNA_rel (autosome DNA for siblings, parent-offspring, half-siblings and
    aunt|uncle-niece|nephew relationships) or xDNA (X chromosome DNA for the half-brothers, mother-daughter, mother-son,
    father-daughter, father-son, sisters, brothers, sister-brother and uncle-nephew relationships).
    :param int n_ped : The number of pedigrees that should be considered. Default value is 1.
    i.e. no haploidization is considered.
    :param int idx_haploid: Identifies which haploidized version should be considered. Default value is -1,
    i.e. no haploidization is considered.

    :return: str : The output message.
    """

    msg = """
╓─┤ USAGE ├─────────────────────────────────────────────────────────────────────────────────────────────────────╖
║                                                                                                               ║
║ $ python run_sim_results.py --working_folder <folder_name>                                                    ║
║                             --info_type <'atDNA_deg' or 'atDNA_rel' or 'xDNA'>                                ║
║                             [--snps <[int]>]                                                                  ║
║                             [--n_ped <int>]                                                                   ║
║                             [--idx_haploid <int>]                                                             ║
║                             [--feedback 0|1]                                                                  ║
╙───────────────────────────────────────────────────────────────────────────────────────────────────────────────╜\n
╓─┤ PARAMETERS ├────────────────────────────────────────────────────────────────────────────────────────────────╖
║                                                                                                               ║
║ working_folder : The reference folder where the VCF files are saved.                                          ║
║      info_type : Defines the type of results to be shown, i.e., atDNA_deg (autosome DNA for the 1st, 2nd and  ║
║                  3rd degrees and unrelated samples), atDNA_rel (autosome DNA for siblings, parent-offspring,  ║
║                  half-siblings and aunt|uncle-niece|nephew relationships) or xDNA (X chromosome DNA for the   ║
║                  half-brothers, mother-daughter, mother-son, father-daughter, father-son, sisters, brothers,  ║
║                  sister-brother and uncle-nephew relationships).                                              ║
║           snps : The number of pedigrees that should be created. Optional parameter with default value equal  ║
║                  to 1.                                                                                        ║
║          n_ped : An output folder that should be created where all the pedigrees are stored.                  ║
║                  Optional parameter, when not defined the folders of each pedigree are created in the         ║
║                  current working directory.                                                                   ║
║                  N.B. The output folder should not exist. It will be created during the process.              ║
║                  If the folder already exists, the script will terminate with an error.                       ║
║    idx_haploid : Identifies which haploidized version should be considered. Default value is -1,              ║
║                  i.e. no haploidization is considered.                                                        ║
║       feedback : If set to 1 provide additional visual feedback on the process, otherwise with 0 basic        ║
║                  feedback. Optional parameter, default value is 1.                                            ║
║                                                                                                               ║
╙───────────────────────────────────────────────────────────────────────────────────────────────────────────────╜\n
╓─┤ DESCRIPTION ├───────────────────────────────────────────────────────────────────────────────────────────────╖
║                                                                                                               ║
║ KINSHIP SIMULATION: SIMULATION RESULTS                                                                        ║
║ Read and export the ngsRelate results for all pedigrees and for the desired data type, i.e., autosome data,   ║ 
║ X chromosome data or both.                                                                                    ║
║                                                                                                               ║
╙───────────────────────────────────────────────────────────────────────────────────────────────────────────────╜\n
╓─┤ EXAMPLE ├───────────────────────────────────────────────────────────────────────────────────────────────────╖
║                                                                                                               ║
║ $ python run_sim_results.py --working_folder simulation --info_type atDNA_deg --n_ped 10 --feedback 0         ║
║                                                                                                               ║
╙───────────────────────────────────────────────────────────────────────────────────────────────────────────────╜\n
"""

    if idx_haploid == -1:
        msg_info = "╓\n║ Working folder: {}\n║ Type of analysis: {}\n║ Number of pedigrees: {}\n╙\n ".format(working_folder,
                                                                                                             info_type,
                                                                                                             n_ped)
    else:
        msg_info = "╓\n║ Working folder: {}\n║ Type of analysis: {}\n║ Haploidized run number: {}\n║ Number of pedigrees: {}\n╙\n ".format(
            working_folder, info_type, idx_haploid, n_ped)

    return msg + msg_info


def autosome_pedigrees(working_folder: str, snps: [int], n_ped=1, info_type="atDNA_deg", idx_haploid=-1, feedback=True):
    """
    Collect the results from the simulated pedigrees given the degree/relationships of interest for autosome DNA data.
    Also individual haploidized versions can be selected.

    :param str working_folder: The reference folder where the VCF files are saved.
    :param [int] snps: A list of integers that defines the number of SNPs to be considered.
    :param int, optional n_ped: The number of pedigrees that should be considered. Default value is 1.
    :param str, optional info_type: Defines the type of results to be shown, i.e., atDNA_deg (autosome DNA for the 1st,
    2nd and 3rd degrees and unrelated samples)or atDNA_rel (autosome DNA for siblings, parent-offspring, half-siblings
    and aunt|uncle-niece|nephew relationships). Default value is 'atDNA_deg'.
    :param int, optional idx_haploid: Identifies which haploidized version should be considered. Default value is -1.
    :param bool, optional feedback: If the flag is set to True it will provide a visual feedback of the ongoing process,
    otherwise it will run silently with only minimal output. Default value is True.
    """

    pedigree = DefaultPedigree()
    ids = pedigree.get_pedigree_ids()  # IDs of individuals from the standard pedigree
    deg_1st = pedigree.get_aut_chr_groups(n=1,
                                          population=ids)  # all couples and sub-groups from first degree relationships
    deg_2nd = pedigree.get_aut_chr_groups(n=2,
                                          population=ids)  # all couples and sub-groups from second degree relationships
    deg_3rd = pedigree.get_aut_chr_groups(n=3,
                                          population=ids)  # all couples and sub-groups from third degree relationships
    deg_unr = pedigree.get_aut_chr_groups(n=-1, population=ids)  # all couples that are unrelated

    # merge all IDs from first degree relationships
    if feedback:
        print("Merge first degree groups:")
    idx_1st = []
    idx_par_off = []
    idx_sib = []
    for key, value in deg_1st.items():
        if value["txt"] == "Siblings":
            for idx in value["idx"]:
                idx_sib.append([int(idx[0]), int(idx[1])])
        if value["txt"] == "Parent-Offspring":
            for idx in value["idx"]:
                idx_par_off.append([int(idx[0]), int(idx[1])])
        if "inbred" in value["txt"] or "inbreeding" in value["txt"]:
            if feedback:
                print("   Skipping {}...".format(value["txt"]))
        else:
            if feedback:
                print("   Including {}...".format(value["txt"]))
            for idx in value["idx"]:
                idx_1st.append([int(idx[0]), int(idx[1])])

    # merge all IDs from second degree relationships
    if feedback:
        print("Merge second degree groups:")
    idx_2nd = []
    idx_half_sib = []
    idx_unc_nep = []
    for key, value in deg_2nd.items():
        if value["txt"] == "Half-sibling":
            for idx in value["idx"]:
                idx_half_sib.append([int(idx[0]), int(idx[1])])

        if value["txt"] == "Aunt|Uncle-Niece|Nephew":
            for idx in value["idx"]:
                idx_unc_nep.append([int(idx[0]), int(idx[1])])

        if "inbred" in value["txt"] or "inbreeding" in value["txt"]:
            if feedback:
                print("   Skipping {}...".format(value["txt"]))
        else:
            if feedback:
                print("   Including {}...".format(value["txt"]))
            for idx in value["idx"]:
                idx_2nd.append([int(idx[0]), int(idx[1])])

    # merge all IDs from third degree relationships
    if feedback:
        print("Merge third degree groups:")
    idx_3rd = []
    for key, value in deg_3rd.items():
        if "inbred" in value["txt"] or "inbreeding" in value["txt"]:
            if feedback:
                print("   Skipping {}...".format(value["txt"]))
        else:
            if feedback:
                print("   Including {}...".format(value["txt"]))
            for idx in value["idx"]:
                idx_3rd.append([int(idx[0]), int(idx[1])])

    # merge all IDs of unrelated couples
    if feedback:
        print("Merge unrelated couples:")
    idx_unr = []
    for key, value in deg_unr.items():
        if "inbred" in value["txt"] or "inbreeding" in value["txt"]:
            if feedback:
                print("   Skipping {}...".format(value["txt"]))
        else:
            if feedback:
                print("   Including {}...".format(value["txt"]))
            for idx in value["idx"]:
                idx_unr.append([int(idx[0]), int(idx[1])])

    # init full resolution and SNPs-reduced results variables
    res_1st_full = None
    res_sib_full = None
    res_par_off_full = None
    res_2nd_full = None
    res_half_sib_full = None
    res_unc_nep_full = None
    res_3rd_full = None
    res_unr_full = None
    res_1st_snps = [None] * len(snps)
    res_sib_snps = [None] * len(snps)
    res_par_off_snps = [None] * len(snps)
    res_2nd_snps = [None] * len(snps)
    res_half_sib_snps = [None] * len(snps)
    res_unc_nep_snps = [None] * len(snps)
    res_3rd_snps = [None] * len(snps)
    res_unr_snps = [None] * len(snps)

    for i_ped in range(n_ped):  # for each pedigree
        pedigree_folder = "pedigree_{}".format(i_ped + 1)
        if idx_haploid == -1:
            file_name = "pedigree_{}.res".format(i_ped + 1)  # file name to be read
        else:
            file_name = "pedigree_{}_haploid{}.res".format(i_ped + 1, idx_haploid)  # file name to be read

        res = lib.import_ngs_results(os.path.join(working_folder, pedigree_folder, file_name))  # import from full resolution results

        if res_1st_full is None:
            res_1st_full = lib.filter_results(res, idx_1st)
        else:
            res_1st_full = res_1st_full.append(lib.filter_results(res, idx_1st))

        if res_sib_full is None:
            res_sib_full = lib.filter_results(res, idx_sib)
        else:
            res_sib_full = res_sib_full.append(lib.filter_results(res, idx_sib))

        if res_par_off_full is None:
            res_par_off_full = lib.filter_results(res, idx_par_off)
        else:
            res_par_off_full = res_par_off_full.append(lib.filter_results(res, idx_par_off))

        if res_2nd_full is None:
            res_2nd_full = lib.filter_results(res, idx_2nd)
        else:
            res_2nd_full = res_2nd_full.append(lib.filter_results(res, idx_2nd))

        if res_half_sib_full is None:
            res_half_sib_full = lib.filter_results(res, idx_half_sib)
        else:
            res_half_sib_full = res_half_sib_full.append(lib.filter_results(res, idx_half_sib))

        if res_unc_nep_full is None:
            res_unc_nep_full = lib.filter_results(res, idx_unc_nep)
        else:
            res_unc_nep_full = res_unc_nep_full.append(lib.filter_results(res, idx_unc_nep))

        if res_3rd_full is None:
            res_3rd_full = lib.filter_results(res, idx_3rd)
        else:
            res_3rd_full = res_3rd_full.append(lib.filter_results(res, idx_3rd))

        if res_unr_full is None:
            res_unr_full = lib.filter_results(res, idx_unr)
        else:
            res_unr_full = res_unr_full.append(lib.filter_results(res, idx_unr))

        idx_snp = 0
        for snp in snps:
            if idx_haploid == -1:
                file_name = "pedigree_{}_{}_SNPs.res".format(i_ped + 1, snp)  # file name to be read
            else:
                file_name = "pedigree_{}_{}_SNPs_haploid{}.res".format(i_ped + 1, snp, idx_haploid)  # file to be read

            res = lib.import_ngs_results(os.path.join(working_folder, pedigree_folder, file_name))  # import SNPs result

            if res_1st_snps[idx_snp] is None:
                res_1st_snps[idx_snp] = lib.filter_results(res, idx_1st)
            else:
                res_1st_snps[idx_snp] = res_1st_snps[idx_snp].append(lib.filter_results(res, idx_1st))

            if res_sib_snps[idx_snp] is None:
                res_sib_snps[idx_snp] = lib.filter_results(res, idx_sib)
            else:
                res_sib_snps[idx_snp] = res_sib_snps[idx_snp].append(lib.filter_results(res, idx_sib))

            if res_par_off_snps[idx_snp] is None:
                res_par_off_snps[idx_snp] = lib.filter_results(res, idx_par_off)
            else:
                res_par_off_snps[idx_snp] = res_par_off_snps[idx_snp].append(lib.filter_results(res, idx_par_off))

            if res_2nd_snps[idx_snp] is None:
                res_2nd_snps[idx_snp] = lib.filter_results(res, idx_2nd)
            else:
                res_2nd_snps[idx_snp] = res_2nd_snps[idx_snp].append(lib.filter_results(res, idx_2nd))

            if res_half_sib_snps[idx_snp] is None:
                res_half_sib_snps[idx_snp] = lib.filter_results(res, idx_half_sib)
            else:
                res_half_sib_snps[idx_snp] = res_half_sib_snps[idx_snp].append(
                    lib.filter_results(res, idx_half_sib))

            if res_unc_nep_snps[idx_snp] is None:
                res_unc_nep_snps[idx_snp] = lib.filter_results(res, idx_unc_nep)
            else:
                res_unc_nep_snps[idx_snp] = res_unc_nep_snps[idx_snp].append(lib.filter_results(res, idx_unc_nep))

            if res_3rd_snps[idx_snp] is None:
                res_3rd_snps[idx_snp] = lib.filter_results(res, idx_3rd)
            else:
                res_3rd_snps[idx_snp] = res_3rd_snps[idx_snp].append(lib.filter_results(res, idx_3rd))

            if res_unr_snps[idx_snp] is None:
                res_unr_snps[idx_snp] = lib.filter_results(res, idx_unr)
            else:
                res_unr_snps[idx_snp] = res_unr_snps[idx_snp].append(lib.filter_results(res, idx_unr))

            idx_snp = idx_snp + 1

    if info_type == "atDNA_deg":
        label_1 = "1st Degree"
        label_2 = "2nd Degree"
        label_3 = "3rd Degree"
        label_4 = "Unrelated"
        sheet_1 = res_1st_full
        sheet_2 = res_2nd_full
        sheet_3 = res_3rd_full
        sheet_4 = res_unr_full
        sheet_1_snps = res_1st_snps
        sheet_2_snps = res_2nd_snps
        sheet_3_snps = res_3rd_snps
        sheet_4_snps = res_unr_snps
    else:
        label_1 = "Siblings"
        label_2 = "Parent-Offspring"
        label_3 = "Half-Siblings"
        label_4 = "Aunt|Uncle-Niece|Nephew"
        sheet_1 = res_sib_full
        sheet_2 = res_par_off_full
        sheet_3 = res_half_sib_full
        sheet_4 = res_unc_nep_full
        sheet_1_snps = res_sib_snps
        sheet_2_snps = res_par_off_snps
        sheet_3_snps = res_half_sib_snps
        sheet_4_snps = res_unc_nep_snps
    output_file_name = os.path.join(working_folder, "atDNA_results_full_SNPs.xlsx")
    writer = pd.ExcelWriter(output_file_name, engine='xlsxwriter')
    sheet_1.to_excel(writer, sheet_name=label_1, index=False)
    sheet_2.to_excel(writer, sheet_name=label_2, index=False)
    sheet_3.to_excel(writer, sheet_name=label_3, index=False)
    sheet_4.to_excel(writer, sheet_name=label_4, index=False)
    writer.save()

    idx_snp = 0
    for snp in snps:
        file_name = os.path.join(working_folder, "atDNA_results_{}_SNPs.xlsx".format(snp))
        writer = pd.ExcelWriter(file_name, engine='xlsxwriter')
        sheet_1_snps[idx_snp].to_excel(writer, sheet_name=label_1, index=False)
        sheet_2_snps[idx_snp].to_excel(writer, sheet_name=label_2, index=False)
        sheet_3_snps[idx_snp].to_excel(writer, sheet_name=label_3, index=False)
        sheet_4_snps[idx_snp].to_excel(writer, sheet_name=label_4, index=False)
        writer.save()
        idx_snp = idx_snp + 1

    quantiles = [0.025, 0.975, 0.95]
    n = min([len(sheet_1), len(sheet_2), len(sheet_3), len(sheet_4)])

    params = ["theta", "k0", "k1", "k2"]

    if info_type == "atDNA_deg":
        label_1st = [label_1
                     ]
        data_1st_full = [sheet_1
                         ]
        data_1st_snps = [sheet_1_snps
                         ]

        label_2nd = [label_2
                     ]
        data_2nd_full = [sheet_2
                         ]
        data_2nd_snps = [sheet_2_snps
                         ]

        label_3rd = [label_3]
        data_3rd_full = [sheet_3]
        data_3rd_snps = [sheet_3_snps]

        label_4th = [label_4]
        data_4th_full = [sheet_4]
        data_4th_snps = [sheet_4_snps]
    else:
        label_1st = [label_1,
                     label_2
                     ]
        data_1st_full = [sheet_1,
                         sheet_2
                         ]
        data_1st_snps = [sheet_1_snps,
                         sheet_2_snps
                         ]

        label_2nd = [label_3,
                     label_4
                     ]
        data_2nd_full = [sheet_3,
                         sheet_4
                         ]
        data_2nd_snps = [sheet_3_snps,
                         sheet_4_snps
                         ]

        label_3rd = []
        data_3rd_full = []
        data_3rd_snps = []

        label_4th = []
        data_4th_full = []
        data_4th_snps = []

    for param in params:
        print("\n╓───────────────────────────────────────────────────────────────────────────────────────────────────────────────╖")
        print("║ {} ESTIMATE\n║ mean ± margin (95% range) for N={}".format(param.upper(), n))
        print("║\n║ Full SNPs:")
        print("║\n║ 1st Degree Relationships:")
        for idx, val in enumerate(label_1st):
            [mean_samples, left_limit, right_limit, std_samples] = ranges(dataset=data_1st_full[idx], param=param,
                                                                          quantiles=[quantiles[0], quantiles[1]], n=n)
            print("║         - {}: {:.4f} with range [{:.4f}, {:.4f}]\n║           (std. dev. = {:.4f})".format(val,
                                                                                                                mean_samples,
                                                                                                                left_limit,
                                                                                                                right_limit,
                                                                                                                std_samples))
        print("║\n║ 2nd Degree Relationships:")
        for idx, val in enumerate(label_2nd):
            [mean_samples, left_limit, right_limit, std_samples] = ranges(dataset=data_2nd_full[idx], param=param,
                                                                          quantiles=[quantiles[0], quantiles[1]], n=n)
            print("║         - {}: {:.4f} with range [{:.4f}, {:.4f}]\n║           (std. dev. = {:.4f})".format(val,
                                                                                                                mean_samples,
                                                                                                                left_limit,
                                                                                                                right_limit,
                                                                                                                std_samples))

        if len(label_3rd) > 0:
            print("║\n║ 3rd Degree Relationships:")
            for idx, val in enumerate(label_3rd):
                [mean_samples, left_limit, right_limit, std_samples] = ranges(dataset=data_3rd_full[idx], param=param,
                                                                              quantiles=[quantiles[0], quantiles[1]], n=n)
                print("║         - {}: {:.4f} with range [{:.4f}, {:.4f}]\n║           (std. dev. = {:.4f})".format(val,
                                                                                                                    mean_samples,
                                                                                                                    left_limit,
                                                                                                                    right_limit,
                                                                                                                    std_samples))

        if len(label_4th) > 0:
            print("║\n║ Unrelated:")
            for idx, val in enumerate(label_4th):
                [mean_samples, _, right_limit, std_samples] = ranges(dataset=data_4th_full[idx], param=param,
                                                                     quantiles=[quantiles[0], quantiles[2]], n=n)
                print("║         - {}: {:.4f} with range [{:.4f}, {:.4f}]\n║           (std. dev. = {:.4f})".format(val,
                                                                                                                    mean_samples,
                                                                                                                    0,
                                                                                                                    right_limit,
                                                                                                                    std_samples))

        for idx_snp in range(len(snps)):
            print("║\n║ SNPs = {}:".format(snps[idx_snp]))
            print("║\n║ 1st Degree Relationships:")
            for idx, val in enumerate(label_1st):
                [mean_samples, left_limit, right_limit, std_samples] = ranges(dataset=data_1st_snps[idx][idx_snp],
                                                                              param=param,
                                                                              quantiles=[quantiles[0], quantiles[1]],
                                                                              n=n)
                print("║         - {}: {:.4f} with range [{:.4f}, {:.4f}]\n║           (std. dev. = {:.4f})".format(val,
                                                                                                                    mean_samples,
                                                                                                                    left_limit,
                                                                                                                    right_limit,
                                                                                                                    std_samples))
            print("║\n║ 2nd Degree Relationships:")
            for idx, val in enumerate(label_2nd):
                [mean_samples, left_limit, right_limit, std_samples] = ranges(dataset=data_2nd_snps[idx][idx_snp],
                                                                              param=param,
                                                                              quantiles=[quantiles[0], quantiles[1]],
                                                                              n=n)
                print("║         - {}: {:.4f} with range [{:.4f}, {:.4f}]\n║           (std. dev. = {:.4f})".format(val,
                                                                                                                    mean_samples,
                                                                                                                    left_limit,
                                                                                                                    right_limit,
                                                                                                                    std_samples))

            if len(label_3rd) > 0:
                print("║\n║ 3rd Degree Relationships:")
                for idx, val in enumerate(label_3rd):
                    [mean_samples, left_limit, right_limit, std_samples] = ranges(dataset=data_3rd_snps[idx][idx_snp],
                                                                                  param=param,
                                                                                  quantiles=[quantiles[0], quantiles[1]],
                                                                                  n=n)
                    print("║         - {}: {:.4f} with range [{:.4f}, {:.4f}]\n║           (std. dev. = {:.4f})".format(val,
                                                                                                                        mean_samples,
                                                                                                                        left_limit,
                                                                                                                        right_limit,
                                                                                                                        std_samples))

            if len(label_4th) > 0:
                print("║\n║ Unrelated:")
                for idx, val in enumerate(label_4th):
                    [mean_samples, _, right_limit, std_samples] = ranges(dataset=data_4th_snps[idx][idx_snp], param=param,
                                                                         quantiles=[quantiles[0], quantiles[2]], n=n)
                    print("║         - {}: {:.4f} with range [{:.4f}, {:.4f}]\n║           (std. dev. = {:.4f})".format(val,
                                                                                                                        mean_samples,
                                                                                                                        0,
                                                                                                                        right_limit,
                                                                                                                        std_samples))


def x_chromosome_pedigrees(working_folder: str, snps: [int], n_ped=1):
    """
    Collect the results from the simulated pedigrees given the relationships of interest for X chromosome DNA data.

    :param str working_folder: The reference folder where the VCF files are saved.
    :param [int] snps: A list of integers that defines the number of SNPs to be considered.
    :param int, optional n_ped: The number of pedigrees that should be considered. Default value is 1.
    """

    pedigree = DefaultPedigree()
    ids = pedigree.get_pedigree_ids()  # IDs of individuals from the standard pedigree
    deg_1st_x_chr_rel = pedigree.get_x_chr_groups(n=1,
                                                  population=ids)  # all couples/groups for 1st X chromosome relations
    deg_2nd_x_chr_rel = pedigree.get_x_chr_groups(n=2,
                                                  population=ids)  # all couples/groups for 2nd X chromosome relations
    idx_mother_daughter = []
    idx_mother_son = []
    idx_father_daughter = []
    idx_father_son = []
    idx_sisters = []
    idx_brothers = []
    idx_sister_brother = []
    for key, value in deg_1st_x_chr_rel.items():
        if value["txt"] == "Mother-Daughter":
            for idx in value["idx"]:
                idx_mother_daughter.append([int(idx[0]), int(idx[1])])
        elif value["txt"] == "Mother-Son":
            for idx in value["idx"]:
                idx_mother_son.append([int(idx[0]), int(idx[1])])
        elif value["txt"] == "Father-Daughter":
            for idx in value["idx"]:
                idx_father_daughter.append([int(idx[0]), int(idx[1])])
        elif value["txt"] == "Father-Son":
            for idx in value["idx"]:
                idx_father_son.append([int(idx[0]), int(idx[1])])
        elif value["txt"] == "Sisters":
            for idx in value["idx"]:
                idx_sisters.append([int(idx[0]), int(idx[1])])
        elif value["txt"] == "Brothers":
            for idx in value["idx"]:
                idx_brothers.append([int(idx[0]), int(idx[1])])
        elif value["txt"] == "Sister-Brother":
            for idx in value["idx"]:
                idx_sister_brother.append([int(idx[0]), int(idx[1])])
        else:
            raise ValueError("Unknown 1st relationship entry. Verify your pedigree class.")

    idx_half_bros = []
    idx_uncle_nephew = []
    for key, value in deg_2nd_x_chr_rel.items():
        if value["txt"] == "Half-Brothers":
            for idx in value["idx"]:
                idx_half_bros.append([int(idx[0]), int(idx[1])])
        elif value["txt"] == "Uncle-Nephew":
            for idx in value["idx"]:
                idx_uncle_nephew.append([int(idx[0]), int(idx[1])])
        else:
            raise ValueError("Unknown 2nd relationship entry. Verify your pedigree class.")

    # init full resolution and SNPs-reduced results variables
    res_mother_daughter_full = None
    res_mother_son_full = None
    res_father_daughter_full = None
    res_father_son_full = None
    res_sisters_full = None
    res_brothers_full = None
    res_sister_brother_full = None
    res_half_bros_full = None
    res_uncle_nephew_full = None

    res_mother_daughter_snps = [None] * len(snps)
    res_mother_son_snps = [None] * len(snps)
    res_father_daughter_snps = [None] * len(snps)
    res_father_son_snps = [None] * len(snps)
    res_sisters_snps = [None] * len(snps)
    res_brothers_snps = [None] * len(snps)
    res_sister_brother_snps = [None] * len(snps)
    res_half_bros_snps = [None] * len(snps)
    res_uncle_nephew_snps = [None] * len(snps)

    for i_ped in range(n_ped):  # for each pedigree
        pedigree_folder = "pedigree_{}".format(i_ped + 1)
        file_name = "x_pedigree_{}.res".format(i_ped + 1)  # file name to be read

        res = lib.import_ngs_results(
            os.path.join(working_folder, pedigree_folder, file_name))  # import from full resolution results

        if res_mother_daughter_full is None:
            res_mother_daughter_full = lib.filter_results(res, idx_mother_daughter)
        else:
            res_mother_daughter_full = res_mother_daughter_full.append(
                lib.filter_results(res, idx_mother_daughter))

        if res_mother_son_full is None:
            res_mother_son_full = lib.filter_results(res, idx_mother_son)
        else:
            res_mother_son_full = res_mother_son_full.append(lib.filter_results(res, idx_mother_son))

        if res_father_daughter_full is None:
            res_father_daughter_full = lib.filter_results(res, idx_father_daughter)
        else:
            res_father_daughter_full = res_father_daughter_full.append(
                lib.filter_results(res, idx_father_daughter))

        if res_father_son_full is None:
            res_father_son_full = lib.filter_results(res, idx_father_son)
        else:
            res_father_son_full = res_father_son_full.append(lib.filter_results(res, idx_father_son))

        if res_sisters_full is None:
            res_sisters_full = lib.filter_results(res, idx_sisters)
        else:
            res_sisters_full = res_sisters_full.append(lib.filter_results(res, idx_sisters))

        if res_brothers_full is None:
            res_brothers_full = lib.filter_results(res, idx_brothers)
        else:
            res_brothers_full = res_brothers_full.append(lib.filter_results(res, idx_brothers))

        if res_sister_brother_full is None:
            res_sister_brother_full = lib.filter_results(res, idx_sister_brother)
        else:
            res_sister_brother_full = res_sister_brother_full.append(
                lib.filter_results(res, idx_sister_brother))

        if res_half_bros_full is None:
            res_half_bros_full = lib.filter_results(res, idx_half_bros)
        else:
            res_half_bros_full = res_half_bros_full.append(lib.filter_results(res, idx_half_bros))

        if res_uncle_nephew_full is None:
            res_uncle_nephew_full = lib.filter_results(res, idx_uncle_nephew)
        else:
            res_uncle_nephew_full = res_uncle_nephew_full.append(lib.filter_results(res, idx_uncle_nephew))

        idx_snp = 0
        for snp in snps:
            file_name = "x_pedigree_{}_{}_SNPs.res".format(i_ped + 1, snp)  # file name to be read
            res = lib.import_ngs_results(
                os.path.join(working_folder, pedigree_folder, file_name))  # import SNPs result

            if res_mother_daughter_snps[idx_snp] is None:
                res_mother_daughter_snps[idx_snp] = lib.filter_results(res, idx_mother_daughter)
            else:
                res_mother_daughter_snps[idx_snp] = res_mother_daughter_snps[idx_snp].append(
                    lib.filter_results(res, idx_mother_daughter))

            if res_mother_son_snps[idx_snp] is None:
                res_mother_son_snps[idx_snp] = lib.filter_results(res, idx_mother_son)
            else:
                res_mother_son_snps[idx_snp] = res_mother_son_snps[idx_snp].append(
                    lib.filter_results(res, idx_mother_son))

            if res_father_daughter_snps[idx_snp] is None:
                res_father_daughter_snps[idx_snp] = lib.filter_results(res, idx_father_daughter)
            else:
                res_father_daughter_snps[idx_snp] = res_father_daughter_snps[idx_snp].append(
                    lib.filter_results(res, idx_father_daughter))

            if res_father_son_snps[idx_snp] is None:
                res_father_son_snps[idx_snp] = lib.filter_results(res, idx_father_son)
            else:
                res_father_son_snps[idx_snp] = res_father_son_snps[idx_snp].append(
                    lib.filter_results(res, idx_father_son))

            if res_sisters_snps[idx_snp] is None:
                res_sisters_snps[idx_snp] = lib.filter_results(res, idx_sisters)
            else:
                res_sisters_snps[idx_snp] = res_sisters_snps[idx_snp].append(
                    lib.filter_results(res, idx_sisters))

            if res_brothers_snps[idx_snp] is None:
                res_brothers_snps[idx_snp] = lib.filter_results(res, idx_brothers)
            else:
                res_brothers_snps[idx_snp] = res_brothers_snps[idx_snp].append(
                    lib.filter_results(res, idx_brothers))

            if res_sister_brother_snps[idx_snp] is None:
                res_sister_brother_snps[idx_snp] = lib.filter_results(res, idx_sister_brother)
            else:
                res_sister_brother_snps[idx_snp] = res_sister_brother_snps[idx_snp].append(
                    lib.filter_results(res, idx_sister_brother))

            if res_half_bros_snps[idx_snp] is None:
                res_half_bros_snps[idx_snp] = lib.filter_results(res, idx_half_bros)
            else:
                res_half_bros_snps[idx_snp] = res_half_bros_snps[idx_snp].append(
                    lib.filter_results(res, idx_half_bros))

            if res_uncle_nephew_snps[idx_snp] is None:
                res_uncle_nephew_snps[idx_snp] = lib.filter_results(res, idx_uncle_nephew)
            else:
                res_uncle_nephew_snps[idx_snp] = res_uncle_nephew_snps[idx_snp].append(
                    lib.filter_results(res, idx_uncle_nephew))

            idx_snp = idx_snp + 1

    sheet_mother_daughter = "Mother-Daughter Relationships"
    sheet_mother_son = "Mother-Son Relationships"
    sheet_father_daughter = "Father-Daughter Relationships"
    sheet_father_son = "Father-Son Relationships"
    sheet_sisters = "Sisters"
    sheet_brothers = "Brothers"
    sheet_sister_brother = "Sister-Brother"

    file_name = os.path.join(working_folder, "xDNA_1st_deg_results_full_SNPs.xlsx")
    writer = pd.ExcelWriter(file_name, engine='xlsxwriter')
    res_mother_daughter_full.to_excel(writer, sheet_name=sheet_mother_daughter, index=False)
    res_mother_son_full.to_excel(writer, sheet_name=sheet_mother_son, index=False)
    res_father_daughter_full.to_excel(writer, sheet_name=sheet_father_daughter, index=False)
    res_father_son_full.to_excel(writer, sheet_name=sheet_father_son, index=False)
    res_sisters_full.to_excel(writer, sheet_name=sheet_sisters, index=False)
    res_brothers_full.to_excel(writer, sheet_name=sheet_brothers, index=False)
    res_sister_brother_full.to_excel(writer, sheet_name=sheet_sister_brother, index=False)
    writer.save()

    idx_snp = 0
    for snp in snps:
        file_name = os.path.join(working_folder, "xDNA_1st_deg_results_{}_SNPs.xlsx".format(snp))
        writer = pd.ExcelWriter(file_name, engine='xlsxwriter')
        res_mother_daughter_snps[idx_snp].to_excel(writer, sheet_name=sheet_mother_daughter, index=False)
        res_mother_son_snps[idx_snp].to_excel(writer, sheet_name=sheet_mother_son, index=False)
        res_father_daughter_snps[idx_snp].to_excel(writer, sheet_name=sheet_father_daughter, index=False)
        res_father_son_snps[idx_snp].to_excel(writer, sheet_name=sheet_father_son, index=False)
        res_sisters_snps[idx_snp].to_excel(writer, sheet_name=sheet_sisters, index=False)
        res_brothers_snps[idx_snp].to_excel(writer, sheet_name=sheet_brothers, index=False)
        res_sister_brother_snps[idx_snp].to_excel(writer, sheet_name=sheet_sister_brother, index=False)
        writer.save()
        idx_snp = idx_snp + 1

    sheet_half_bros = "Half-Brothers Relationships"
    sheet_uncle_nephew = "Uncle-Nephew Relationships"

    file_name = os.path.join(working_folder, "xDNA_2nd_deg_results_full_SNPs.xlsx")
    writer = pd.ExcelWriter(file_name, engine='xlsxwriter')
    res_half_bros_full.to_excel(writer, sheet_name=sheet_half_bros, index=False)
    res_uncle_nephew_full.to_excel(writer, sheet_name=sheet_uncle_nephew, index=False)
    writer.save()

    idx_snp = 0
    for snp in snps:
        file_name = os.path.join(working_folder, "xDNA_2nd_deg_results_{}_SNPs.xlsx".format(snp))
        writer = pd.ExcelWriter(file_name, engine='xlsxwriter')
        res_half_bros_snps[idx_snp].to_excel(writer, sheet_name=sheet_half_bros, index=False)
        res_uncle_nephew_snps[idx_snp].to_excel(writer, sheet_name=sheet_uncle_nephew, index=False)
        writer.save()
        idx_snp = idx_snp + 1

    quantiles = [0.025, 0.975, 0.95]
    n = min([len(res_mother_daughter_full), len(res_mother_son_full),
             len(res_father_daughter_full), len(res_father_son_full),
             len(res_sisters_full), len(res_brothers_full),
             len(res_sister_brother_full), len(res_half_bros_full), len(res_uncle_nephew_full)])

    params = ["theta", "k0", "k1", "k2"]
    label_1st = ["Mother-Daughter",
                 "Mother-Son",
                 "Father-Daughter",
                 "Father-Son",
                 "Sisters",
                 "Brothers",
                 "Sister-Brother"]
    data_1st_full = [res_mother_daughter_full,
                     res_mother_son_full,
                     res_father_daughter_full,
                     res_father_son_full,
                     res_sisters_full,
                     res_brothers_full,
                     res_sister_brother_full]
    data_1st_snps = [res_mother_daughter_snps,
                     res_mother_son_snps,
                     res_father_daughter_snps,
                     res_father_son_snps,
                     res_sisters_snps,
                     res_brothers_snps,
                     res_sister_brother_snps]
    label_2nd = ["Half-Brothers",
                 "Uncle-Nephew"]
    data_2nd_full = [res_half_bros_full,
                     res_uncle_nephew_full]
    data_2nd_snps = [res_half_bros_snps,
                     res_uncle_nephew_snps]
    for param in params:
        print("\n╓───────────────────────────────────────────────────────────────────────────────────────────────────────────────╖")
        print("║ {} ESTIMATE\n║ mean ± margin (95% range) for N={}".format(param.upper(), n))
        print("║\n║ Full SNPs:")
        print("║\n║ 1st Degree Relationships:")
        for idx, val in enumerate(label_1st):
            [mean_samples, left_limit, right_limit, std_samples] = ranges(dataset=data_1st_full[idx], param=param,
                                                                          quantiles=[quantiles[0], quantiles[1]], n=n)
            print("║         - {}: {:.4f} with range [{:.4f}, {:.4f}]\n║           (std. dev. = {:.4f})".format(val,
                                                                                                                mean_samples,
                                                                                                                left_limit,
                                                                                                                right_limit,
                                                                                                                std_samples))
        print("║\n║ 2nd Degree Relationships:")
        for idx, val in enumerate(label_2nd):
            [mean_samples, left_limit, right_limit, std_samples] = ranges(dataset=data_2nd_full[idx], param=param,
                                                                          quantiles=[quantiles[0], quantiles[1]], n=n)
            print("║         - {}: {:.4f} with range [{:.4f}, {:.4f}]\n║           (std. dev. = {:.4f})".format(val,
                                                                                                                mean_samples,
                                                                                                                left_limit,
                                                                                                                right_limit,
                                                                                                                std_samples))

        for idx_snp in range(len(snps)):
            print("║\n║ SNPs = {}:".format(snps[idx_snp]))
            print("║\n║ 1st Degree Relationships:")
            for idx, val in enumerate(label_1st):
                [mean_samples, left_limit, right_limit, std_samples] = ranges(dataset=data_1st_snps[idx][idx_snp],
                                                                              param=param,
                                                                              quantiles=[quantiles[0], quantiles[1]],
                                                                              n=n)
                print("║         - {}: {:.4f} with range [{:.4f}, {:.4f}]\n║           (std. dev. = {:.4f})".format(val,
                                                                                                                    mean_samples,
                                                                                                                    left_limit,
                                                                                                                    right_limit,
                                                                                                                    std_samples))
            print("║\n║ 2nd Degree Relationships:")
            for idx, val in enumerate(label_2nd):
                [mean_samples, left_limit, right_limit, std_samples] = ranges(dataset=data_2nd_snps[idx][idx_snp],
                                                                              param=param,
                                                                              quantiles=[quantiles[0], quantiles[1]],
                                                                              n=n)
                print("║         - {}: {:.4f} with range [{:.4f}, {:.4f}]\n║           (std. dev. = {:.4f})".format(val,
                                                                                                                    mean_samples,
                                                                                                                    left_limit,
                                                                                                                    right_limit,
                                                                                                                    std_samples))


def data_stat(data_in: [float], n: int) -> [[float], float, float]:
    if len(data_in) == n:
        data = data_in
        mean_data = np.mean(data_in)
        std_data = np.std(data_in)
    elif len(data_in) > n:
        data = []
        perm = np.random.permutation(n)
        for idx in perm:
            data.append(data_in[idx])
        mean_data = np.mean(data)
        std_data = np.std(data)
    else:
        data = None
        mean_data = None
        std_data = None

    return data, mean_data, std_data


def mar_of_err(conf_coeff: float, std_dev: float, n: int) -> float:
    return conf_coeff * std_dev / math.sqrt(n)


def ranges(dataset: pd.DataFrame, param: str, quantiles: [float, float], n=0) -> [float, float, float, float]:
    """
    Returns mean value, left and right limit for the given quantiles and standard deviation.
    """

    if n == 0:
        n = dataset.size
    [samples, mean_samples, std_samples] = data_stat(dataset[param].to_list(), n)
    left_limit = np.quantile(samples, quantiles[0])
    right_limit = np.quantile(samples, quantiles[1])

    return [mean_samples, left_limit, right_limit, std_samples]


if __name__ == '__main__':
    fire.Fire(sim_results)
