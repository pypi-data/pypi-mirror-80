"""
Kinship simulation, library:
- Load and save Python objects using 'pickle'.
- Check type and ranges of variables.
- All the functionality useful to import/export pedigrees and VCF dataset in general.
- Allele sharing coefficient.
"""

__version__ = '2020.8'
__author__ = 'Team Neogene'

import os
import ast
import sys
import math
import pickle
import random
import shutil
import logging
import statistics
import pandas as pd
from pathlib import Path
from numbers import Number
from kinshipsim.spinner import Spinner
from kinshipsim.individual import Individual


def save_object(obj, filename: str):
    """
    Save a Python object to a file.
    IMPORTANT: If the given filename corresponds to an existing file, it automatically overwrites it.

    :param obj : The Python object to be saved.
    :param str filename : The name of the file to be created.
    """

    with open(filename, 'wb') as o:  # overwrites any existing file.
        pickle.dump(obj, o, pickle.HIGHEST_PROTOCOL)


def load_object(filename: str) -> object:
    """
    Load a Python object from a file.

    :param str filename : The name of the file to be loaded.

    :return: object : The loaded Python object.
    """

    with open(filename, 'rb') as i:
        obj = pickle.load(i)

    return obj


def is_unique(c_list: list) -> bool:
    """
    Check if the values in a list are unique or if there are repetitions.

    :param list c_list : the list to be checked

    :return: bool :  True if the list contains unique (non repeated) values.
    """

    return len(c_list) == len(set(c_list))


def check_data(var: str, val, type_val: type,
               min_val=None, max_val=None, set_val=None,
               unique=False, ordinal=False, equals=False, err=True):
    """
    Check the consistency of the data assigned to a variable.

    Control that the variable of interest ('val') is of the correct type ('type_val') and optionally verify that
    the value ('val') falls within a specified range ('min_val', 'max_val') or belongs to a set of values ('set_val').

    :param str var : The name of the variable to be checked.
    :param val : The value of the variable ('var').
    :param type type_val : The type that the variable ('var') should have.
    :param Numbers.number, optional min_val : If set, it identifies the min acceptable value for the variable ('var').
    :param Numbers.number, optional max_val : If set, it identifies the max acceptable value for the variable ('var').
    :param list, optional set_val : If set, it identifies the list of acceptable values for the variable ('var').
    :param bool, optional unique : Given a list, it will verify that its values are unique (with unique=True).
    :param bool, optional ordinal : Given a list, it will verify that its values are in ascending order (ordinal=True).
    :param bool, optional equals : Given a list, it will check if all values are equals.
    :param bool, optional err : If set to 'False' it returns 'None' without raising an error. Default is 'True'.

    :return: object : The value ('val') that was checked.

    :raises ValueError : If the variable ('var') has a value ('val') of the wrong type (i.e., not 'type_val') or,
        optionally, it is outside of the set range, not in a list of values, or the list contains repetitions.
    """

    checked = val

    if not isinstance(val, type_val):
        if err:
            msg = "'{}' was found to be of the type '{}' while it should be '{}'.".format(var, type(val), type_val)
            raise ValueError(msg)
        else:
            checked = None
    if not (min_val is None) and val < min_val:
        if not (max_val is None):
            if err:
                msg = "'{}' was found to be equal to '{}' while its value should be within the range [{}, {}].".\
                    format(var, val, min_val, max_val)
                raise ValueError(msg)
            else:
                checked = None
        else:
            if err:
                msg = "'{}' was found to be equal to '{}' while it should be bigger or equal to '{}'.".\
                    format(var, val, min_val)
                raise ValueError(msg)
            else:
                checked = None
    if not (max_val is None) and val > max_val:
        if not (min_val is None):
            if err:
                msg = "'{}' was found to be equal to '{}' while its value should be within the range [{}, {}].".\
                    format(var, val, min_val, max_val)
                raise ValueError(msg)
            else:
                checked = None
        else:
            if err:
                msg = "'{}' was found to be equal to '{}' while it should be smaller or equal to '{}'.".format(
                        var, val, max_val)
                raise ValueError(msg)
            else:
                checked = None
    if not (set_val is None) and not (val in set_val):
        if err:
            msg = "'{}' was found to be equal to '{}' which is not an accepted value. Possible values are: '{}'.".\
                format(var, val, set_val)
            raise ValueError(msg)
        else:
            checked = None

    if type_val == list and unique and not(is_unique(val)):
        msg = "The {} '{}' contains repeated values ('{}').".format(type_val, var, val)
        raise ValueError(msg)

    if type_val == list and equals:
        if len(set(val)) == 1:
            msg = "The values in the {} '{}' are all equals ('{}').".format(type_val, var, val)
            raise ValueError(msg)

    if type_val == list and ordinal:  # if it is a list and we need to check the ascending order

        # let's first check that all the values in the list are a Number
        if isinstance(val[0], Number):
            check_ord = True
        else:
            check_ord = False
        idx = 1
        while check_ord and idx < len(val):
            if isinstance(val[idx], Number) and val[idx] > val[idx - 1]:
                idx = idx + 1
            else:
                check_ord = False

        if not check_ord:  # The list is not in ascending order or there are values that are not a Number
            msg = "The {} '{}' is not in ascending order or there is a value that is not a 'Number' ({}).".format(
                type_val, var, val)
            raise ValueError(msg)

    return checked


def individuals_in_vcf(vcf_file: str) -> [str]:
    """
    Return the list of individuals/samples found in the given VCF file.

    :param str vcf_file : The VCF input file.

    :return: [str] : The IDs of the individuals within the given vcf file.
    """

    ids = []
    vcf = open(vcf_file, "r")
    for line in vcf:
        if line.startswith("#CHROM"):
            ids = line.split()  # decompose the line
            ids = ids[9:]  # remove the first 9 parameters of the header which are not IDs of individuals
    vcf.close()

    return ids


def export2vcf(population: [Individual], vcf_header_template: str, vcf_file: str, save_all=False, x_chromosome=False):
    """
    Save the current population to a VCF file. It requires the reference VCF file (from which the population was
    originally generated) to retrieve the header and the parameter columns.

    :param [Individual] population : The list of Individual defining the population.
    :param str vcf_header_template : The VCF reference file from which the population originated.
    :param str vcf_file : The output file.
    :param bool, optional save_all : If True it saves also the crossover, strand selections, pedigree relationships
    in additional files with the same name of the VCF file but with extensions CHR (for autosome) or
    XCH (for x chromosome). Default is False.
    :param bool, optional x_chromosome : If True it will export the x chromosome. Default is False.
    """

    # id of individuals to strings separated by tab
    pop_txt = "\t".join(census(population))

    # rows of snps of individuals, each row is a sequence of strings separated by a tab
    snps = population_snps(population, x_chromosome)
    snps_txt = []
    for idx in range(len(snps)):
        snps_txt.append("\t".join(snps[idx]))

    template = open(vcf_header_template, "r")
    vcf = open(vcf_file, "w")

    idx_snp = 0
    for line in template:
        if line.startswith("##"):  # header: copy it to the new file
            vcf.write(line)
        elif line.startswith("#CHROM"):  # column header: we need to add the new columns for each individual
            header = line.split()  # decompose the line

            # retain only the first 9 parameters of the header and reassemble them
            # from 0 to 8 thus the last index should be 9 as it is not included, i.e. [0, 9).
            header = "\t".join(header[0:9])

            line = "{}\t{}\n".format(header, pop_txt)  # merge with the individuals of the population
            vcf.write(line)  # write on the output file
        else:  # data row: we need to select the reference info and add the new columns for each individual
            snps_row = line.split()  # decompose the line

            # retain only the first 9 parameters of the line and reassemble them
            # from 0 to 8 thus the last index should be 9 as it is not included, i.e. [0, 9).
            snps_row = "\t".join(snps_row[0:9])

            line = "{}\t{}\n".format(snps_row, snps_txt[idx_snp])  # merge with the values of the individuals
            vcf.write(line)  # write on the output file
            idx_snp = idx_snp + 1  # prepare to use the next location

    template.close()
    vcf.close()

    if save_all:
        file_name, _ = os.path.splitext(vcf_file)
        if x_chromosome:
            pop_file = "{}.xch".format(file_name)
        else:
            pop_file = "{}.chr".format(file_name)
        data_pop = []
        for ind in population:
            ind_data = {"id": ind.id}

            if x_chromosome:
                ind_data["gender"] = ind.gender

                ind_data["x_crossover"] = []
                if ind.x_crossover:
                    ind_data["x_crossover"] = ind.x_crossover

                ind_data["x_strand"] = []
                if ind.x_strand:
                    ind_data["x_strand"] = ind.x_strand
            else:
                ind_data["crossover"] = []
                if ind.crossover(0):
                    ind_data["crossover"] = [ind.crossover(0), ind.crossover(1)]

                ind_data["strand"] = []
                if ind.strand(0):
                    ind_data["strand"] = [ind.strand(0), ind.strand(1)]

            ind_data["parents"] = []
            if ind.parents:
                ind_data["parents"] = [ind.parents[0].id, ind.parents[1].id]

            ind_data["offsprings"] = []
            if ind.offsprings:
                for offspring in ind.offsprings:
                    ind_data["offsprings"].append(offspring.id)

            data_pop.append(ind_data)
        save_object(data_pop, pop_file)


def id2txt(population: [Individual], file_name: str):
    """
    Export the IDs of the population to a specified file.

    :param [Individual] population : The population of interest.
    :param str file_name : The file name where the IDs will be written.
    """

    txt = open(file_name, "w")
    for ind in population:
        txt.write("{}\n".format(ind.id))
    txt.close()


def census(population: [Individual]) -> [str]:
    """
    Collects all the IDs of the Individual within the given population.

    :param [Individual] population : The list of individuals, i.e., [Individual].

    :return: [str] : The list of the IDs of all the individuals, i.e., [str].
    """

    register = []
    for individual in population:
        register.append(individual.id)

    return register


def population_snps(population: [Individual], x_chromosome=False) -> [[str]]:
    """
    Collects all the SNPs of the population (each row a list of one SNP for all the individuals).

    :param [Individual] population : The list of individuals.
    :param bool, optional x_chromosome : If True it will collect the x chromosome information. Default is False.

    :return: [[str]] The list of SNPs for all individuals. Note: Each SNP is defined by a list of values.
    """

    snps = []
    n_pop = len(population)  # size of population
    if n_pop > 0:
        if x_chromosome:
            n_chr = 1
        else:
            n_chr = len(population[0].chromosomes)  # number of chromosomes
        for idx_chr in range(n_chr):  # loop through all chromosomes
            if x_chromosome:
                n_snp = len(population[0].x_chromosome)  # number of snps within the x chromosome
            else:
                n_snp = len(population[0].chromosomes[idx_chr])  # number of snps within the current chromosome
            for idx_snp in range(n_snp):  # loop through all SNPs of the current chromosome
                row_snp = []  # SNPs of the individuals within the current chromosome
                for idx_ind in range(n_pop):  # loop through all individuals
                    if x_chromosome:
                        c = population[idx_ind].x_chromosome[idx_snp]
                    else:
                        c = population[idx_ind].chromosomes[idx_chr][idx_snp]
                    row_snp.append(c)
                snps.append(row_snp)

    return snps


def load_population(vcf_file: str, population=None, x_chromosome=False, load_all=False, feedback=True) -> [Individual]:
    """
    Load the entire set of individuals stored in a VCF file.

    :param str vcf_file : The file from which the individuals are loaded.
    :param [Individual], optional population : If a population is already available, the loaded data will be integrated
    in it (e.g., load x chromosome data in a population that already contains the autosomal data).
    :param bool, optional x_chromosome : If True it will consider the VCF data as x chromosome information.
    :param bool, optional load_all : If True it will load also the additional data stored in the CHR or XCH files.
    :param bool, optional feedback : If the flag is set to True it will provide a visual feedback of the ongoing
    process, otherwise it will run silently with only minimal output.

    :return: [Individual] : The loaded population.
    """

    # load genetic information from the VCF file
    if feedback:
        with Spinner("Reading GT data from VCF file "):
            [ids, chr_id, gt_array] = __read_vcf(vcf_file)
        sys.stdout.write(" [OK]\n")
        sys.stdout.flush()
    else:
        [ids, chr_id, gt_array] = __read_vcf(vcf_file)

    # if required load additional information for crossover, strand, ...
    pop_data = []
    if load_all:
        file_name, _ = os.path.splitext(vcf_file)
        if x_chromosome:
            extension = "xch"
        else:
            extension = "chr"
        pop_file = "{}.{}".format(file_name, extension)
        if feedback:
            msg = "Reading pedigree details from {} file ".format(extension.upper())
            with Spinner(msg):
                pop_data = load_object(pop_file)
            sys.stdout.write(" [OK]\n")
            sys.stdout.flush()
        else:
            pop_data = load_object(pop_file)

    # structure the genetic data for each individual
    loaded_population = []
    for idx in range(len(ids)):
        if feedback:
            msg = "Loading '{}' ({}/{}) ".format(ids[idx], idx + 1, len(ids))
            with Spinner(msg):
                chrs = __extract_chromosomes(ids, chr_id, gt_array, idx)
                loaded_population.append(Individual(ids[idx], chrs))
            sys.stdout.write("[OK]\n")
            sys.stdout.flush()
        else:
            chrs = __extract_chromosomes(ids, chr_id, gt_array, idx)
            loaded_population.append(Individual(ids[idx], chrs))

    # merge loaded data with passed population and include pedigree information
    if x_chromosome:  # work with x chromosome data

        # move the x chromosome loaded data into the correct fields
        if population is None:  # no previous population existed
            for ind in loaded_population:
                ind.set_x_chromosome(ind.chromosomes[0])
                ind.set_chromosomes(None)
        else:  # integrate the loaded x chromosome information into the correct fields of the passed population
            for ind in population:
                tmp = get_individual(loaded_population, ind.id)
                tmp = tmp.chromosomes[0]
                ind.set_x_chromosome(tmp)
            loaded_population = population

        # if additional information was loaded, it needs to be integrated into the population data
        for ind in pop_data:
            curr = get_individual(loaded_population, ind["id"])  # individual to be updated

            # update x chromosome specific fields
            curr.set_gender(ind["gender"])
            curr.set_x_crossover(ind["x_crossover"])
            curr.set_x_strand(ind["x_strand"])

            # check consistency with parents
            if ind["parents"]:
                tmp_parents = [get_individual(loaded_population, ind["parents"][0]),
                               get_individual(loaded_population, ind["parents"][1])]
                if curr.parents and \
                        ((not curr.parents[0].id == tmp_parents[0].id) or
                         (not curr.parents[1].id == tmp_parents[1].id)):
                    raise ValueError("Parents of individual '{}' are not consistent with the loaded ones.".format(
                        curr.id))
                else:
                    curr.set_parents(tmp_parents)

            # check consistency with offsprings
            if ind["offsprings"]:
                tmp_offsprings = []
                for o in ind["offsprings"]:
                    tmp_offsprings.append(get_individual(loaded_population, o))
                if curr.offsprings:
                    if len(curr.offsprings) == len(ind["offsprings"]):
                        stop = False
                        for o in curr.offsprings:
                            if o.id not in ind["offsprings"]:
                                stop = True
                                break
                    else:
                        stop = True
                    if stop:
                        raise ValueError("Offsprings of individual '{}' are different from the loaded ones.".format(
                            curr.id))
                else:
                    curr.set_offsprings(tmp_offsprings)
    else:  # work with the 22 chromosomes
        if population:  # integrate the loaded information withing the passed population
            for ind in population:
                tmp = get_individual(loaded_population, ind.id)
                ind.set_chromosomes(tmp.chromosomes)
            loaded_population = population

        # if additional information was loaded, it needs to be integrated into the population data
        for ind in pop_data:
            curr = get_individual(loaded_population, ind["id"])  # individual to be updated

            # update specific fields of the 22 chromosomes
            if ind["crossover"]:
                curr.set_crossover(ind["crossover"][0], ind["crossover"][1])
            if ind["strand"]:
                curr.set_strand(ind["strand"][0], ind["strand"][1])

            # check consistency with parents
            if ind["parents"]:
                tmp_parents = [get_individual(loaded_population, ind["parents"][0]),
                               get_individual(loaded_population, ind["parents"][1])]
                if curr.parents and \
                        ((not curr.parents[0].id == tmp_parents[0].id) or
                         (not curr.parents[1].id == tmp_parents[1].id)):
                    raise ValueError("Parents of individual '{}' are not consistent with the loaded ones.".format(
                        curr.id))
                else:
                    curr.set_parents(tmp_parents)

            # check consistency with offsprings
            if ind["offsprings"]:
                tmp_offsprings = []
                for offspring in ind["offsprings"]:
                    tmp_offsprings.append(get_individual(loaded_population, offspring))
                if curr.offsprings:
                    if len(curr.offsprings) == len(ind["offsprings"]):
                        stop = False
                        for check_offspring in curr.offsprings:
                            if check_offspring.id not in ind["offsprings"]:
                                stop = True
                                break
                    else:
                        stop = True
                    if stop:
                        raise ValueError("Offsprings of individual '{}' are different from the loaded ones.".format(
                            curr.id))
                    else:
                        curr.set_offsprings(tmp_offsprings)
                else:
                    curr.set_offsprings(tmp_offsprings)

    return loaded_population


def extract_chromosomes(vcf_file: str, individual) -> [[str]]:
    """
    Extract chromosomes data of an individual/sample (defined by its ID) from a VCF file.

    :param str vcf_file : The file from which the data are extracted.
    :param str, int individual : The individual's ID (as string) or as column index (int) with 0 as the column
    of the first individual.

    :return: [[str]] : The sequence of chromosomes.
    """

    gt_array = []  # holds GT info of all samples for all loci, like a matrix
    chr_id = []  # retains the chromosome id for each row

    in_file = open(vcf_file, "r")

    id_idx = -1  # initialize id_idx has not found
    for line in in_file:  # read GT data
        if line.startswith("#CHR"):  # heather with column identifiers
            line_cols = line.split()
            sample_list = line_cols[9:]
            if isinstance(individual, str):
                id_idx = sample_list.index(individual)  # identify column numbers of the individual
            elif isinstance(individual, int):
                id_idx = check_data("individual", individual, int, 0, len(line_cols) - 10)
            else:
                raise ValueError("Unsupported type for an individual. Either ID (as str) or index (as int)")
        elif not line.startswith("##"):  # not a comment and not heather, save the data
            line_cols = line.split()
            chr_id.append(line_cols[0])
            gt_array.append(line_cols[9:])
    in_file.close()

    # define the chromosomes of the individual (GT over all locations)
    if not id_idx == -1:  # a match was found
        chromosomes = []
        chr_idx = 0  # index of the chromosome (N.B. Not the ID)
        chr_seq = []  # will retain the sequence of SNPs for a given chromosome
        for val in gt_array:

            # if there is a change to a new chromosome, store the current sequence and initialize a new empty one
            if chr_idx > 0 and not (chr_id[chr_idx] == chr_id[chr_idx - 1]):
                chromosomes.append(chr_seq)
                chr_seq = []

            chr_seq.append(val[id_idx])
            chr_idx = chr_idx + 1
        chromosomes.append(chr_seq)  # append the last sequence too
    else:
        msg = "Couldn't match the ID within the VCF file (id = {})".format(individual)
        raise ValueError(msg)

    return chromosomes


def extract_id(vcf_file: str, idx_individual: int) -> str:
    """
    Extract the ID of an individual given its index from a specified VCF file.

    :param str vcf_file : The file from which the data are extracted.
    :param int idx_individual : The column index (int) associated with the individual with 0 as the column
    of the first individual.

    :return: [str] : The associated ID.
    """

    in_file = open(vcf_file, "r")
    id_individual = None
    for line in in_file:  # read the lines of the file
        if line.startswith("#CHR"):  # heather with column identifiers
            line_cols = line.split()

            # verify correctness of the given index
            idx = check_data("idx_individual", idx_individual, int, 0, len(line_cols) - 10) + 9

            id_individual = line_cols[idx]  # id string associated with the given index
            break

    in_file.close()

    return id_individual


def cmp_chromosome(chromosome1: [str], chromosome2: [str]) -> bool:
    """
    Compare two chromosome sequences and return True if they match, False otherwise.

    :param [str] chromosome1 : The first chromosome sequence.
    :param [str] chromosome2 : The second chromosome sequence.

    :return: bool : True if the chromosome sequences match, False otherwise.
    """

    match = False
    n = len(chromosome1)
    if len(chromosome2) == n:
        match = True
        idx = 0
        while match and idx < n:
            if chromosome1[idx] == chromosome2[idx]:
                idx = idx + 1
            else:
                match = False

    return match


def cmp_chromosomes(chromosomes1: [[str]], chromosomes2: [[str]]) -> bool:
    """
    Compare two sequences of multiple chromosomes and return True if they match, False otherwise.

    :param [[str]] chromosomes1 : The first sequence of multiple chromosomes.
    :param [[str]] chromosomes2 : The second sequence of multiple chromosomes.

    :return: bool : True if the sequences of multiple chromosomes match, False otherwise.
    """

    match = False
    n = len(chromosomes1)  # number of chromosomes to compare
    if len(chromosomes2) == n:
        match = True
        idx = 0
        while match and idx < n:
            match = cmp_chromosome(chromosomes1[idx], chromosomes2[idx])
            idx = idx + 1

    return match


def count_snps(vcf_file: str) -> int:
    """
    Count the number of SNPs in a given VCF file. It trivially counts the "non-comment" lines.

    :param str vcf_file : The file from which we want to count the number of SNPs.

    :return: int : The number of SNPs in the given file.
    """

    vcf = open(vcf_file, "r")
    n_snps = 0
    for line in vcf:
        if not (line.startswith("#")):  # not a comment line
            n_snps = n_snps + 1
    vcf.close()

    return n_snps


def distribute_snps(n_snps: int, chromosomes_weights: [int]) -> [int]:
    """
    Given a number of SNPs to be retained and the size (i.e., number of SNPs) of each chromosome, distribute
    proportionally the number of SNPs to be retained across all the chromosomes.

    :param int n_snps : The number of SNPs to be retained.
    :param [int] chromosomes_weights : The current number of SNPs for each chromosome.

    :return: [int] : The SNPs to be randomly selected across each chromosome in order to retain the original ratio.
    """

    distributed_amounts = []
    total_weights = sum(chromosomes_weights)
    for weight in chromosomes_weights:
        weight = float(weight)
        p = weight / total_weights
        distributed_amount = round(p * n_snps)
        distributed_amounts.append(distributed_amount)
        total_weights -= weight
        n_snps -= distributed_amount

    return distributed_amounts


def reduce_snps(input_file: str, output_file: str, n_snps: int):
    """
    Reduce the number of SNPs of a given VCF file.

    :param str input_file : Filename of the VCF file from which reducing the SNPs.
    :param str output_file : Filename of the new VCF file that will be created with reduced SNPs.
    :param int n_snps : The number of SNPs to be retained.
    """

    # the summary also provides feedback on the correctness of the dataset and additional parameters we will use later
    source_summary = summary(input_file)

    # continue only if there are no misplaced or duplicate entries
    if len(source_summary["misplaced_entry"]) == 0 and len(source_summary["duplicate_entry"]) == 0:

        # get the number of SNPs of each chromosome (from the input file)
        positions = source_summary["position"]
        chr_snps = []
        for idx_pos in range(len(positions)):
            chr_snps.append(len(positions[idx_pos]))

        # distribute the amount of SNPs to be retained across all the chromosomes (proportionally)
        dist_snps = distribute_snps(n_snps, chr_snps)

        # randomly select the appropriate amount of SNPs to be retained (for each chromosome)
        snps = []
        for idx in range(len(chr_snps)):
            snps.append(sorted(random.sample(range(0, chr_snps[idx]), dist_snps[idx])))

        template = open(input_file, "r")
        vcf = open(output_file, "w")

        chromosomes = source_summary["chromosome"]  # chromosome numbers found in the input file
        last_chr = -1  # index of the chromosome found in the previous line
        snp_cnt = 0  # counter of lines for the current chromosome
        for line in template:
            if line.startswith("#"):  # do not count comment lines and just write them to the new file
                vcf.write(line)
            else:
                line_cols = line.split()
                idx_chr = chromosomes.index(int(line_cols[0]))  # index of the chromosome on the current line
                if not (idx_chr == last_chr):  # if it is different from the previous one, reset the SNPs counter
                    last_chr = idx_chr
                    snp_cnt = 0
                if snp_cnt in snps[idx_chr]:
                    vcf.write(line)
                snp_cnt = snp_cnt + 1

        template.close()
        vcf.close()


def find_siblings(population: [Individual], ind=None):
    """
    Given a population, returns the couples of indices identifying the siblings within the population or,
    given a specific individual, a list of its siblings.

    :param [Individual] population : The population from which the siblings are identified.
    :param int, optional ind : Index of an individual of the population.

    :return: [[int, int]] or [int] : A list of couples of indices identifying the siblings within the population or,
        given a specific individual, a list of its siblings.
    """

    siblings = []
    if ind is None:
        for idx_individual in range(len(population) - 1):
            for idx_sibling in range(idx_individual + 1, len(population)):
                if population[idx_individual].is_sibling(population[idx_sibling]):
                    siblings.append([idx_individual, idx_sibling])
    else:
        for idx_individual in range(len(population)):
            if not (idx_individual == ind):
                if population[idx_individual].is_sibling(population[ind]):
                    siblings.append(idx_individual)

    return siblings


def find_parent_offspring(population: [Individual]) -> [[int, int]]:
    """
    Given a population, returns the indices identifying couples of parent/offspring within the population.
    N.B. offsprings which are not part of the given population are not included.

    :param [Individual] population : The population from which the parent/offspring couples are identified.

    :return: [[int, int]] : A list of couples of indices identifying the parent/offspring individuals of the population.
    """

    parent_offspring = []
    for idx_individual1 in range(len(population) - 1):
        for idx_individual2 in range(idx_individual1 + 1, len(population)):
            if population[idx_individual1].is_parent(population[idx_individual2]) \
                    or population[idx_individual1].is_offspring(population[idx_individual2]):
                parent_offspring.append([idx_individual1, idx_individual2])

    return parent_offspring


def ind2index(ind: Individual, population: [Individual]) -> int:
    """
    Given an individual and population, returns the index of the individual within the population.
    Returns -1 if the individual is not part of the population.

    :param Individual ind : The individual of interest.
    :param [Individual] population : The population to be searched.

    :return: int : The index associated with the individual (-1 if it is not found).
    """

    idx = 0
    found = False
    while not found and idx < len(population):
        if population[idx].id == ind.id:
            found = True
        else:
            idx = idx + 1

    if not found:
        idx = -1

    return idx


def id2index(id_ind: str, population: [str]) -> int:
    """
    Given an individual ID and a population of IDs, returns the index of the individual ID within the population of IDs.
    Returns -1 if the individual ID is not part of the population of IDs.

    :param str id_ind : The ID of the individual of interest.
    :param [str] population : The population of IDs to be searched.

    :return: int : The index associated with the individual ID (-1 if it is not found).
    """

    idx = 0
    found = False
    while not found and idx < len(population):
        if population[idx] == id_ind:
            found = True
        else:
            idx = idx + 1

    if not found:
        idx = -1

    return idx


def import_ngs_results(ngs_output: str, idx_cols=None, label_cols=None, type_cols=None) -> pd.DataFrame:
    """
    Import from a file the results generated by the ngsRelate program.

    :param str ngs_output : The name of the file from which results are imported.
    :param [int], optional idx_cols : The indices of the columns of interest (to be retained).
    :param [str], optional label_cols : The label to rename the columns of interest.
    :param [type], optional type_cols : The type to be assigned to each column of interest.

    :return: DataFrame : A table containing all the requested information.
    """

    # load default parameters if necessary
    if idx_cols is None:
        idx_cols = [0, 1, 2, 3, 4, 5, 13, 14, 15]

    if label_cols is None:
        label_cols = ["idx_individual_1", "idx_individual_2", "n_sites", "k0", "k1", "k2", "Fa", "Fb", "theta"]

    if type_cols is None:
        type_cols = [int, int, int, float, float, float, float, float, float]

    ngs = open(ngs_output, "r")  # open the ngsRelate result text file
    res = pd.DataFrame(columns=label_cols)
    header = False
    for line in ngs:
        values = line.split()  # decompose the line
        if not header:  # first line contains the header thus we skip it and add our own header to the table
            header = True
        else:  # a line of data from which we select the columns of interest
            # values = [float(values[idx]) for idx in idx_cols]
            values = [values[idx] for idx in idx_cols]
            values = zip(label_cols, values)  # create a zip object from the two lists
            dict_of_data = dict(values)  # create a dictionary from zip object
            res = res.append(
                dict_of_data, ignore_index=True
            )  # add the data row to the DataFrame

    ngs.close()

    # set the type associated with each column
    for idx in range(len(label_cols)):
        res = res.astype({label_cols[idx]: type_cols[idx]})

    return res


def filter_results(results: pd.DataFrame, indices: [[int, int]],
                   col_1="idx_individual_1", col_2="idx_individual_2", copy=True) -> pd.DataFrame:
    """
    Select the result rows, which are of interest, by providing the couples of indices (each identifying the individuals
    within the studied population). Optionally, identify the columns of the DataFrame where the indices of the
    individuals are stored and if the selection should be applied on the passed DataFrame or on a separate copy of it.

    :param DataFrame results : The table containing the results of the ngsRelate analysis.
    :param [[int, int]] indices : The list with the couples of indices (identifying individuals in the population).
    :param str, optional col_1 : The column name identifying the first column containing indices of the individuals.
    :param str, optional col_2 : The column name identifying the second column containing indices of the individuals.
    :param bool, optional copy : If True applies the selection of the rows of the table on a copy, otherwise it works
    directly on the passed DataFrame.

    :return: DataFrame : The table containing the records pertaining to the selected couples of individuals.
    """

    idx_drop = []  # rows to be dropped from the DataFrame
    for index, row in results.iterrows():
        couple = [int(row[col_1]), int(row[col_2])]  # identify the couple of individuals of the current row
        if couple not in indices:  # mark the row index to be dropped if the couple is not in the given list of indices
            idx_drop.append(index)
    if copy:  # drop the rows in a copy of the DataFrame without affecting the original DataFrame
        sel_df = results.copy().drop(idx_drop)
    else:  # drop the rows by directly modifying the original DataFrame
        sel_df = results.drop(idx_drop)

    return sel_df


def threshold(samples: [float], p: int) -> float:
    """
    Returns the threshold value under which lays a given percentage of the samples.

    :param [float] samples : A list of values from which the threshold needs to be determined.
    :param int p : The percentage (i.e. a value between 1 and 100) from which the threshold is calculated.

    :return: float : The threshold value, i.e., the value under which lays p percent of the dataset s.
    """

    samples.sort()
    idx = math.floor(p * len(samples) / 100)

    return samples[idx]


def summary(vcf_file: str, feedback=False) -> dict:
    """
    Verifies that the sequence of chromosomes (and their locations) is in an ascending order and if there are any
    duplicate entries. It returns a dictionary with a general summary of the dataset, i.e. the list of all chromosomes
    and recorded positions, total number of SNPs alongside with all the misplaced and duplicate entries, i.e., line
    number (the counting starts from 0) plus the line itself (as a string).

    Specification of the keys returned within dictionary:
    int, snps : Total number of SNPs found in the VCF file. N.B. This value accounts also for the misplaced entries.
    [int], chromosome : A list of all the chromosomes found within the VCF file.
    [[int]], position : A list identifying all the positions of each chromosome. Given idx the index of the chromosome
        of interest in the "chromosome" key of the dictionary, all its positions are stored in position[idx].
        N.B. Duplicate entries (if any) are not counted!

        Ex.: idx = dict.chromosome.index(1), i.e., the index for chromosome 1
             dict.position[idx] contains all the positions associated with chromosome 1 (except for duplicate entries)

    :param str vcf_file : The file from which the sequence will be verified.
    :param bool, optional feedback : If the flag is set to True it will provide a visual feedback of the ongoing
    process, otherwise it will run silently with only minimal output.

    :return: dict : line numbers (starting from 0 as first line) and the lines themselves as strings
    (an empty list if the file is fully ordered).
    """

    summary_dict = {}  # the returned dictionary

    misplaced_entry = []  # the output variable with the lines out of sequence
    duplicate_entry = []  # keeps track of duplicate entries (same chromosome and position number)
    chromosome = []  # keeps track of the found chromosomes
    position = []  # keeps track of all positions for each chromosome
    snps = 0  # keep count of the SNPs (not counting the possible duplicates)

    reference = -1  # the reference chromosome throughout the sequence
    reference_position = -1  # the position of the reference chromosome

    idx_line = 0  # line index

    misplaced = False  # the flag is set whenever a misplaced entry is found
    duplicate = False  # the flag is set whenever a duplicate entry is found
    duplicate_warning = False  # duplicate flag used for "short" warning feedback
    misplaced_warning = False  # misplaced flag used for "short" warning feedback

    vcf = open(vcf_file, "r")
    for line in vcf:
        if not (line.startswith("#")):  # not a comment line, hence a line to examine
            line_cols = line.split()  # separate the columns
            current_chromosome = int(line_cols[0])  # chromosome number for the current line
            current_position = int(line_cols[1])  # position number for the current chromosome
            if current_chromosome == reference:  # same chromosome
                idx = chromosome.index(current_chromosome)

                # if the position is increasing it is ok. Continue to the new position and update the summary
                if current_position > reference_position:
                    position[idx].append(current_position)
                    reference_position = current_position
                    snps = snps + 1  # a new SNP was found
                else:
                    # the position in not increasing thus violating the order of the sequence,
                    # or the position was already recorded thus we found a duplicate entry
                    if current_position in position[idx]:  # duplicate (and do not increase the SNP count)
                        duplicate = True
                    else:  # misplaced (and increase the SNP count)
                        position[idx].append(current_position)
                        misplaced = True
                        snps = snps + 1  # a new SNP was found (though misplaced)
            else:  # different chromosome
                if current_chromosome in chromosome:  # data pertaining to a previously encountered chromosome
                    idx = chromosome.index(current_chromosome)

                    # it is again a misplaced or duplicate entry
                    if current_position in position[idx]:  # duplicate (and do not increase the SNP count)
                        duplicate = True
                    else:  # misplaced (and increase the SNP count)
                        misplaced = True
                        position[idx].append(current_position)
                        snps = snps + 1  # a new SNP was found (though misplaced)
                else:  # we are just starting to explore a new chromosome
                    chromosome.append(current_chromosome)  # add the chromosome to the summary list
                    position.append([])  # initialize the list for the positions of the chromosome
                    position[-1].append(current_position)
                    reference = current_chromosome
                    reference_position = current_position
                    snps = snps + 1  # a new SNP was found

            if misplaced:  # update summary for misplaced entries (and feedback if required)
                misplaced_warning = True
                misplaced_entry.append([idx_line, line])
                if feedback:
                    msg = "Chromosome entry misplaced: [{}] #CHROM {}, POS {} (reference #CHROM {}, POS {})".format(
                        idx_line, current_chromosome, current_position, reference, reference_position)
                    logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
                    logging.info(msg)

            if duplicate:  # update summary for duplicate entries (and feedback if required)
                duplicate_warning = True
                duplicate_entry.append([idx_line, line])
                if feedback:
                    msg = "Duplicate chromosome entry: [{}] #CHROM {}, POS {}".format(idx_line,
                                                                                      current_chromosome,
                                                                                      current_position)
                    logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
                    logging.info(msg)

            duplicate = False
            misplaced = False

        idx_line = idx_line + 1
    vcf.close()

    # populate the dictionary to be returned
    summary_dict["snps"] = snps
    summary_dict["chromosome"] = chromosome
    summary_dict["position"] = position
    summary_dict["misplaced_entry"] = misplaced_entry
    summary_dict["duplicate_entry"] = duplicate_entry

    if not feedback:
        if duplicate_warning:
            n = len(duplicate_entry)
            msg = "A duplicate chromosome entry was found."
            if n > 1:
                msg = "Duplicate chromosome entries were found ({}).".format(n)
            logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
            logging.info(msg)
        if misplaced_warning:
            n = len(misplaced_entry)
            msg = "A misplaced chromosome entry was found."
            if n > 1:
                msg = "Misplaced chromosome entries were found ({}).".format(n)
            logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
            logging.info(msg)
        if duplicate_warning or misplaced_warning:
            msg = "Try to call the function ""fix_vcf"" in order to restructure the dataset."
            logging.basicConfig(format='%(message)s', level=logging.INFO)
            logging.info(msg)

    return summary_dict


def fix_vcf(vcf_in: str, vcf_out: str, vcf_summary=None):
    """
    Given a VCF file and its summary dictionary (obtained via summary call) generate a new VCF file where all misplaced
    entries are rearranged and duplicate entries are discarded.

    :param str vcf_in : The input VCF file (to be fixed).
    :param str vcf_out : The name of the (fixed) output VCF file.
    :param dict, optional vcf_summary : A dictionary with the summary details (obtained via summary call). If None the
    summary is generated by the function itself.
    """

    if vcf_summary is None:
        vcf_summary = summary(vcf_in)

    fixed = True
    duplicates = vcf_summary["duplicate_entry"]
    misplaced = vcf_summary["misplaced_entry"]
    skip = []
    if len(duplicates) > 0:
        fixed = False
        duplicates = entries2tab(duplicates)  # these lines are discarded as containing duplicates
        skip = duplicates["line"].tolist()
    if len(misplaced) > 0:
        fixed = False
        misplaced = entries2tab(misplaced)

    if not fixed:
        last_chromosome = -1
        vcf_raw = open(vcf_in, "r")
        vcf_fix = open(vcf_out, "w")
        idx_line = -1
        for line in vcf_raw:
            idx_line = idx_line + 1
            if line.startswith("#"):  # comment line, rewrite it
                vcf_fix.write(line)
            elif not (
                    idx_line in skip):  # the line needs to be written but we may add some misplaced lines before

                # select the chromosome and position of the current line
                values = line.split()
                line_chromosome = int(values[0])
                line_position = int(values[1])

                # if the line_chromosome is different from the previous written chromosome we need to be sure that
                # we add all the remaining misplaced entries of the previous chromosome (last_chromosome)
                if len(misplaced) > 0:
                    if not (line_chromosome == last_chromosome):
                        misplaced_chromosome = misplaced.loc[misplaced["chr"] == last_chromosome]
                        for idx, row in misplaced_chromosome.iterrows():
                            misplaced_line = vcf_summary["misplaced_entry"][row["idx"]][1]  # misplaced line to write
                            vcf_fix.write(misplaced_line)  # write it on file
                            skip.append(row["line"])  # add the original line to the skip list not to write it again

                        # drop all the entries of last_chromosome from the misplaced DataFrame
                        misplaced = misplaced[misplaced.chr != last_chromosome]

                        last_chromosome = line_chromosome

                    # select all the misplaced entries related to the line_chromosome
                    misplaced_chromosome = misplaced.loc[misplaced["chr"] == line_chromosome]

                    # if the line_position, i.e., the position of the current file entry is smaller than
                    # the first misplaced then write the current file entry and continue to the next line,
                    # otherwise loop through the misplaced entries and insert them in the output file until
                    # the line_position can be inserted
                    while len(misplaced_chromosome) > 0 and line_position > misplaced_chromosome.iloc[0][3]:
                        idx_row = misplaced_chromosome.iloc[0][0]
                        misplaced_line = vcf_summary["misplaced_entry"][idx_row][1]  # misplaced line to be written
                        vcf_fix.write(misplaced_line)  # write it on file
                        skip.append(
                            misplaced_chromosome.iloc[0][1])  # add original line to the skip list not to write it again

                        # drop the inserted entry from both misplaced (the whole set)
                        # and misplaced_chromosome (the current one)
                        curr_line = misplaced_chromosome.iloc[0][1]
                        misplaced_chromosome = misplaced_chromosome[
                            misplaced_chromosome.line != curr_line]
                        misplaced = misplaced[misplaced.line != curr_line]

                vcf_fix.write(line)  # write the current line
        vcf_raw.close()
        vcf_fix.close()
    else:
        msg = "The VCF file '{}' does not contain misplaced or duplicate entries.".format(vcf_in)
        logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
        logging.info(msg)


def entries2tab(entries: [int, str]) -> pd.DataFrame:
    """
    Given the misplaced_entry or duplicate_entry of the summary dictionary,
    returns a DataFrame with the chromosomes and positions sorted.

    :param [int, str] entries : The key of the summary dictionary where the first column identify the line
        number in the VCF file from which it was generated and str is the line itself.

    :return: DataFrame : The table defined as follows:
        idx : The reference index of the misplaced_entry or duplicate_entry list.
        line : The line number associated with the relative misplaced/duplicate entry.
        chr : The chromosome number pertinent to the text line of the misplaced/duplicate entry.
        pos : The position of the chromosome pertinent to the text line of the misplaced/duplicate entry.
    """

    d = pd.DataFrame(0, index=list(range(len(entries))), columns=["idx", "line", "chr", "pos"])
    for idx in range(len(entries)):
        d.iloc[idx][0] = idx
        d.iloc[idx][1] = entries[idx][0]
        values = entries[idx][1].split()
        d.iloc[idx][2] = int(values[0])
        d.iloc[idx][3] = int(values[1])
    d = d.sort_values(["chr", "pos"])

    return d


def get_chromosomes(vcf_file: str) -> [int]:
    """
    Given a VCF file, it returns the list of available chromosomes.

    :param str vcf_file : The file from which we want to obtain the list of the chromosomes.

    :return: [int] : The list of chromosomes that are found in the VCF file.
    """

    chromosome = []  # list of found chromosomes
    current = -1  # most recent found chromosome
    vcf = open(vcf_file, "r")
    for line in vcf:
        if not (line.startswith("#")):  # not a comment line
            line_cols = line.split()
            read = int(line_cols[0])
            if not (read == current) and read not in chromosome:
                chromosome.append(read)
                current = read

    vcf.close()

    return chromosome


def get_individual(population: [Individual], ind_id: str) -> Individual:
    """
    Return an individual from the population given its ID (if exists), None otherwise.

    :param [Individual] population : The list of individuals.
    :param str ind_id : The ID of the individual to be retrieved.

    :return: Individual : The individual if it has been found (None otherwise).
    """

    ind = None
    idx = 0
    while ind is None and idx < len(population):
        if population[idx].id == ind_id:
            ind = population[idx]
        idx = idx + 1

    # noinspection PyTypeChecker
    return ind


def match_snp(snp: str, div_snp="|", feedback=True) -> int:
    """
    Convert the diallelic or haploidized SNP, with the genotype coding system of 0, 1, 2.
    Recognized values are the following: 0|0, 0|1, 1|0, 0|0 or 0 and 1 (the separator could
    either be | or /). It returns -1 if it is unrecognized, unsupported, or contains a missing value.
    Missing values are identified by a "." sign or, following haploidization, by a value of "-1".

    :param str snp : The SNP to be converted.
    :param str, optional div_snp : Standard SNP divider.
    :param bool, optional feedback : If the flag is set to True it will provide a visual feedback of the ongoing
    process, otherwise it will run silently with only minimal output.

    :return: int : The genotype as coding system of 0, 1, 2. It returns -1 if it is unrecognized, unsupported,
    or contains a missing value.
    """

    if len(snp) == 1:  # haploidized SNP
        orig = snp  # reference string to report in case of warnings
        snp = "{0}{1}{0}".format(snp,
                                 div_snp)
    else:  # diallelic SNP
        orig = None

        # Parse the SNP:
        #
        div_snp = snp_sep(snp)  # identify the separator character
        spl_snp = split_snp(snp)  # separate the two strands of the SNP

        if len(spl_snp) == 2:  # it is a recognized format

            # Parse now the two strands:
            #
            s1 = __fix_snp(spl_snp[0])
            s2 = __fix_snp(spl_snp[1])

            snp = "{}{}{}".format(s1, div_snp, s2)
        else:
            msg = "Unknown SNP format (snp = {}). Expected 'val1{}val2'".format(snp, div_snp)
            raise ValueError(msg)

    # Match the SNP value with its code:
    #
    if snp == "0{}0".format(div_snp):
        code = 0
    elif snp == "1{}0".format(div_snp) or snp == "0{}1".format(div_snp):
        code = 1
    elif snp == "1{}1".format(div_snp):
        code = 2
    else:  # unrecognized format, provide feedback for it
        if feedback:
            if orig is None:  # haploidized SNP
                if "." in snp or "-1" in snp:
                    msg = "Missing value for SNP: '{}'".format(snp)
                else:
                    msg = "Unrecognized SNP: '{}'".format(snp)
            else:  # diallelic SNP
                if orig == ".":
                    msg = "Missing value for haploidized SNP: '{}'".format(orig)
                else:
                    msg = "Unrecognized haploidized SNP: '{}'".format(orig)
            logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
            logging.info(msg)
        code = -1

    return code


def allele_sharing_coeff(ind1, ind2, freq: [float], min_maf=0, mask=None) -> [float, int]:
    """
    Allele sharing coefficient (asc) estimation given two individuals and the frequency of minor alleles.
    Accepted SNPs strings are: "0|0", "0|1", "1|0", "1|1" or "0/0", "0/1", "1/0", "1/1" alternatively.
    Currently missing values (e.g., ".|0"), SNPs with frequency of minor allele equal to zero and encodings
    that differ from the aforementioned cases are discarded. Additional information (e.g., 0|0:xxx) is
    automatically discarded.

    :param Individual or [int] ind1 : The first individual as instance of Individual or as a list of integers
    if haploidized.
    :param Individual or [int] ind2 : The second individual as instance of Individual or as a list of integers
    if haploidized.
    :param [float] freq : The list of frequency of minor alleles.
    :param float, optional min_maf : Minimum frequency value that is retained (default, all values > 0)
    :param [bool], optional mask : A list of flags for the SNPs to consider. If the value is True the SNP at that
    location is considered in the calculation, if False it is ignored. Default is None meaning all SNPs are considered.

    :return: [float, int] : The allele sharing coefficient estimate and the number of considered SNPs.
    """

    if mask is None:
        mask = [True] * len(freq)

    asc = -1  # allele sharing coefficient
    n = -1  # number of positions that were considered in computing the coefficient
    if type(ind1) == list and type(ind2) == list and len(ind1) == len(ind2) and len(ind1) == len(
            freq):  # haploidized individuals

        # Verify data consistency:
        #
        # for v in ind1:
        #     _ = kinship_check_data("ind1", v, int, set_val=[0, 1, -1], err=False)

        # for v in ind2:
        #     _ = kinship_check_data("ind2", v, int, set_val=[0, 1, -1], err=False)

        idx = 0  # reference index for the location of interest
        asc = 0  # allele sharing coefficient
        skipped = 0  # keeps track of the positions that are discarded
        while idx < len(ind1):  # loop throughout all the sequence
            if mask[idx]:
                snp1 = str(ind1[idx])  # haploidized SNP for the first individual
                snp2 = str(ind2[idx])  # haploidized SNP for the second individual
                s1 = match_snp(snp1, feedback=False)  # convert to the 0,1,2 code
                s2 = match_snp(snp2, feedback=False)  # convert to the 0,1,2 code

                if freq[idx] < min_maf or s1 == -1 or s2 == -1:
                    # discard positions for which there are unknown codes (i.e., s1 and s2)
                    # or a frequency value smaller than threshold or non defined (i.e., -1)
                    skipped = skipped + 1  # keep the count of the discarded positions
                else:
                    coeff1 = (s1 - 2 * freq[idx]) / math.sqrt(
                        2 * freq[idx] * (1 - freq[idx]))  # coefficient for individual 1
                    coeff2 = (s2 - 2 * freq[idx]) / math.sqrt(
                        2 * freq[idx] * (1 - freq[idx]))  # coefficient for individual 2
                    asc = asc + (coeff1 * coeff2)  # update the ASC sum considering the current position
            else:
                skipped = skipped + 1
            idx = idx + 1  # move to the next position

        n = len(freq) - skipped  # total number of considered position
        if n == 0:
            asc = -1
        else:
            asc = asc / n  # average the ASC by the total number of considered position
    else:  # diallelic individuals

        # Verify the data type (as Individual):
        #
        ind1 = check_data("ind1", ind1, Individual)
        ind2 = check_data("ind2", ind2, Individual)

        if len(ind1.chromosomes) == len(ind2.chromosomes):  # individuals should have same lengths
            idx_freq = 0  # index for the frequency vector
            idx_chr = 0  # index for the studied chromosome
            asc = 0  # allele sharing coefficient
            skipped = 0  # keeps track of the positions that are discarded
            while idx_chr < len(ind1.chromosomes):  # for each chromosome
                chr1 = ind1.chromosomes[idx_chr]  # chromosome for individual 1
                chr2 = ind2.chromosomes[idx_chr]  # chromosome for individual 2
                idx_snp = 0  # index for SNP in the current chromosome
                while idx_snp < len(chr1):  # go through all the SNPs
                    s1 = match_snp(chr1[idx_snp], feedback=False)  # current SNP for individual 1
                    s2 = match_snp(chr2[idx_snp], feedback=False)  # current SNP for individual 2
                    if freq[idx_freq] < min_maf or freq[idx_freq] == 0 or s1 == -1 or s2 == -1:
                        # discard positions for which there are unknown codes (i.e., s1 and s2)
                        # or a frequency value equal to zero or non defined (i.e., -1)
                        skipped = skipped + 1
                    else:
                        coeff1 = (s1 - 2 * freq[idx_freq]) / math.sqrt(
                            2 * freq[idx_freq] * (1 - freq[idx_freq]))  # coefficient for individual 1
                        coeff2 = (s2 - 2 * freq[idx_freq]) / math.sqrt(
                            2 * freq[idx_freq] * (1 - freq[idx_freq]))  # coefficient for individual 2
                        asc = asc + (coeff1 * coeff2)  # update the ASC sum considering the current position
                    idx_snp = idx_snp + 1  # move to the next SNP...
                    idx_freq = idx_freq + 1  # ...and frequency
                idx_chr = idx_chr + 1  # time for the next chromosome

            n = len(freq) - skipped  # total number of considered position
            if n == 0:
                asc = -1
            else:
                asc = asc / n  # average the ASC by the total number of considered position

    return [asc, n]  # return both ASC estimate and the number of considered position


def extract_freq(info: str, tag="AFngsrelate", feedback=True) -> float:
    """
    Given a string containing a series of tag, it extracts the frequency tag returning its floating value.

    :param str info : The string containing one or more tags (each separated by ';').
    :param str, optional tag : The TAG that defines the frequency value. Default 'AFngsrelate'.
    :param bool, optional feedback : If the flag is set to True it will provide a visual feedback of the ongoing
    process, otherwise it will run silently with only minimal output.

    :return: float : The frequency value found in the info string.
    """

    idx = info.find(tag)
    val = float(-1)
    if not idx == -1:  # if TAG not present idx is -1
        start = idx + len(tag) + 1
        end = info[start:].find(";")

        # Extract the relevant string for the value
        if end == -1:
            val = info[start:]
        else:
            val = info[start: start + end]
        try:
            val = float(val)  # convert the string to number
        except ValueError:
            if feedback:
                msg = "Unrecognized freq. value: {}Assigning -1.".format(val)
                logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
                logging.info(msg)
            val = float(-1)

    return val


def import_freq(freq_file: str, feedback=True) -> [float]:
    """
    Load frequency of minor alleles  from a given VCF file.  N.B.  The frequency values can be stored in a separate file
    (no header, just one value on each row, the order follows the SNPs sequence of the associated VCF file)  or they can
    be stored within the VCF file itself, in the INFO column, with the TAG  'AFngsrelate'  (this approach was adopted to
    maintain the consistency of the data structure across the two different analyses, i.e., ngsRelate and allele sharing
    coefficient analyses.

    :param str freq_file : The file name from which the frequency of minor alleles are loaded.
    :param bool, optional feedback : If the flag is set to True it will provide a visual feedback of the ongoing
    process, otherwise it will run silently with only minimal output.

    :return: [float] : The frequency of minor alleles.
    """

    file_name, file_extension = os.path.splitext(os.path.basename(freq_file))  # separate file name and extension
    vcf = False
    tag = False
    if "vcf" in file_extension.lower():
        vcf = True

    f = open(freq_file, "r")
    freq = []
    info_idx = -1
    for line in f:
        if vcf:
            if line.startswith("##"):  # header
                if not tag:
                    if line.lower().\
                            rstrip() == "##info=<id=afngsrelate,number=a,type=float,description=\"allele frequency\">":
                        tag = True
            elif line.startswith("#CHROM"):  # column header
                if not tag:
                    f.close()
                    raise ValueError("Could not find INFO TAG definition of AFngsrelate for frequency values.")
                header = line.split()  # decompose the line

                # Identify the index of the INFO column:
                #
                info_idx = 0
                found = False
                while not found and info_idx < len(header):
                    if header[info_idx] == "INFO":
                        found = True
                    else:
                        info_idx = info_idx + 1

                if not found:  # the INFO column is not in the file, throw an error
                    f.close()
                    msg = "INFO column not found in the VCF file '{}'".format(freq_file)
                    raise ValueError(msg)
            else:  # data row
                entry = line.split()  # decompose the line
                freq.append(extract_freq(entry[info_idx], feedback=feedback))
        else:
            try:
                freq.append(float(line))
            except ValueError:
                if feedback:
                    msg = "Unrecognized freq. value: {}; Assigning -1.".format(line)
                    logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
                    logging.info(msg)
                freq.append(float(-1))
    f.close()

    return freq


def maf(vcf_file: str, freq_file: str, map_file: str, working_folder=None, feedback=True):
    """
    Given a frequency file for a whole set of SNPs, create a new frequency file for the given population dataset
    according to its available SNPs. If a MAP file exists along side with the frequency file, the SNPs are selected
    according to their specific location, otherwise only by considering the associated SNP ID. The output file will
    be named as the VCF file with FRQ extension instead and stored in the working folder (or current folder).

    N.B. It is expected that both VCF and frequency files are sorted by SNP position (with chromosomes listed in the
    same order). This speedup the selection process without need to continuously search throughout the frequency file
    for each single SNP.

    Structure of the main frequency file:
    First line contains the header,
    CHR    SNP    A1    A2    MAF    NCHROBS
    where CHR identify chromosome number, SNP is the ID of the SNP and MAF is the frequency of minor alleles.

    The MAP file associated with the frequency file is expected to be structured as follows:
    No header and four columns where the column of interest are the first column, which identifies the chromosome
    number; the second column for the SNP ID and the fourth column for the SNP position.

    The generated frequency file will be stored in the working folder (if any, otherwise the current folder) and
    it will have a unique column (no header) with the relevant MAF values.

    :param str vcf_file : The population dataset.
    :param str freq_file : The main reference frequency file.
    :param str map_file : The map file with positional references.
    :param str, optional working_folder : The location where the created file will be saved.
    :param bool, optional feedback : If the flag is set to True it will provide a visual feedback of the ongoing
    process, otherwise it will run silently with only minimal output.
    """

    name, file_extension = os.path.splitext(vcf_file)
    pedigree_freq_file = name + ".frq"
    pedigree_file = vcf_file
    if working_folder is not None:
        pedigree_file = os.path.join(working_folder, vcf_file)
        pedigree_freq_file = os.path.join(working_folder, pedigree_freq_file)

    vcf_chr = []
    vcf_id = []
    vcf_pos = []
    vcf = open(pedigree_file, "r")
    for line in vcf:
        if not line.startswith("#"):
            tmp = line.split()  # decompose the line
            vcf_chr.append(tmp[0])  # append the chromosome number
            vcf_pos.append(tmp[1])  # append the position in the chromosome
            vcf_id.append(tmp[2])  # append the snp id
    vcf.close()
    vcf_frq = [-1] * len(vcf_id)
    frq_val = []
    frq_chr = []
    frq_id = []
    frq_pos = []
    frq = open(freq_file, "r")
    frq_map = open(map_file, "r")
    idx = 0
    for line in frq:
        tmp = line.split()
        if not tmp[0] == "CHR":
            map_line = frq_map.readline()
            tmp_map = map_line.split()

            frq_id.append(tmp[1])
            frq_val.append(tmp[4])
            frq_chr.append(tmp[0])
            frq_pos.append(tmp_map[3])
            if idx < len(vcf_frq) and vcf_chr[idx] == tmp[0] and vcf_pos[idx] == tmp_map[3]:
                if not vcf_id[idx] == tmp[1]:
                    print("Possible ambiguity in the frequency records: CHR {}; POS {}; CHR ID: {}".format(tmp[0],
                                                                                                           tmp_map[3],
                                                                                                           tmp[1]))
                vcf_frq[idx] = float(tmp[4])
                idx = idx + 1
    frq.close()

    # Look for missing values and find the match if possible
    for idx in range(len(vcf_frq)):
        if vcf_frq[idx] == -1:  # missing value, look for a match
            start_idx = 0
            done = False
            while not done:  # until it is not found (or it doesn't exist)
                try:
                    frq_src = frq_pos[start_idx:]
                    found_idx = frq_src.index(vcf_pos[idx])  # find index for same position
                    if frq_chr[found_idx] == vcf_chr[idx]:  # if also the chromosome coincide we find the match
                        vcf_frq[idx] = frq_pos[found_idx]  # update the value
                        done = True
                    else:  # the chromosome was different, it is not the value we were looking for
                        start_idx = found_idx  # update the starting point of the list and continue the search
                except ValueError:  # a match for the position was not found
                    if feedback:
                        print("Missing frequency value for chromosome {} at the position {}.".format(vcf_chr[idx],
                                                                                                     vcf_pos[idx]))
                    done = True

    if -1 in vcf_frq:  # there are still missing values
        msg = "Found missing frequency values."
        raise ValueError(msg)
    else:  # no missing values, we can save the frequencies
        freq_file = open(pedigree_freq_file, "w")
        for val in vcf_frq:
            freq_file.write("{}\n".format(val))
        freq_file.close()


def __format_haploid_snp(haploid: [[int]], idx: int, single=False, div_snp="|") -> str:
    """
    Format a specified SNP for the VCF file accounting for all samples.

    :param [[int]] haploid : The haploidized samples.
    :param int idx : The index of the SNP of interest.
    :param bool, optional single : Consider single SNP formatting or retain the two-strains format.
    :param str, optional div_snp : The separator to be used in the two-strains format.

    :return: The text line formatted for VCF file, for the specified SNP and accounting for all samples.
    """

    cols = []
    for h in haploid:
        val = h[idx]
        if val == -1:
            snp = "."
        else:
            snp = str(val)

        if not single:
            snp = snp + div_snp + snp

        cols.append(snp)
    line = "\t".join(cols)

    return line


def haploidization(vcf_file: str, n: int, suffix="_haploid", feedback=True):
    """

    :param str vcf_file : Reference samples to be haploidized.
    :param int n : The number of different haploidizations.
    :param str, optional suffix : If the VCF file is a reference file, the suffix is used to name the haploidized
    versions of it. Default suffix is '_haploid'.
    Ex. : suffix = "_haploid"
          vcf_file = "path/population.vcf"
          n = 3
          Files to be created containing haploidized versions of the population:
          "path/population_haploid1.vcf"
          "path/population_haploid2.vcf"
          "path/population_haploid3.vcf"
    :param bool, optional feedback : If the flag is set to True it will provide a visual feedback of the ongoing
        process, otherwise it will run silently with only minimal output.
    """

    [population, _] = __load_data(vcf_file, vcf_file, feedback)
    for idx_run in range(n):  # haploidization process is repeated N times
        # Haploidize the data:
        #
        h = []
        idx_h = 0
        for ind in population:
            idx_h = idx_h + 1
            if feedback:
                msg = "Run {}/{}: haploidize the data, sample {}/{} ".format(idx_run + 1, n, idx_h, len(population))
                with Spinner(msg):
                    h.append(ind.haploidize())
                sys.stdout.write("[OK]\n")
                sys.stdout.flush()
            else:
                h.append(ind.haploidize())

        # Write the VCF file for the haploidized
        #
        file_name, file_extension = os.path.splitext(vcf_file)
        hap_file = file_name + suffix + "{}".format(idx_run + 1) + file_extension
        hap = open(hap_file, "w")
        vcf = open(vcf_file, "r")
        idx_snp = 0
        for line in vcf:
            if line.startswith("#"):  # part of the header, copy to the haploidized file
                hap.write(line)
            else:  # SNP line
                line_cols = line.split()
                info_line = "\t".join(line_cols[0: 9])
                data_line = __format_haploid_snp(h, idx_snp)
                new_line = info_line + "\t" + data_line + "\n"
                hap.write(new_line)
                idx_snp = idx_snp + 1
        vcf.close()
        hap.close()

    if feedback:
        print("\n")


def estimate_asc(vcf_file: str, frq_file=None,
                 haploidized=None, suffix="_haploid", load=False, min_maf=0, feedback=True):
    """
    Compute the allele sharing  coefficient for a given population (passed as VCF file).  If the parameter 'haploidized'
    is defined (e.g., haploidized=N),  the allele sharing coefficient estimate is computed over haploidized data. As the
    process of haploidization is randomized, the process can be repeated multiple times (e.g., N).

    :param str vcf_file : The VCF file that contains the population to be studied.
    :param str frq_file : The allele frequencies. If not set it will look for the frequency values
        within the VCF file itself.
    :param int haploidized : If defined the data are haploidized and the process is repeated multiple times
        as specified by this value (i.e., haploidized=N the process is repeated N times).
    :param str, optional suffix : If the VCF file is a reference file, the suffix is used to reconstruct the name of the
    haploidized versions of it (instead of computing it on the fly). Default suffix is '_haploid'.
    Ex. : suffix = "_haploid"
          vcf_file = "path/population.vcf"
          haploidized = 3
          load = True
          Files to be loaded containing haploidized versions of the population:
          "path/population_haploid1.vcf"
          "path/population_haploid2.vcf"
          "path/population_haploid3.vcf"
    :param bool, optional load : If the flag is set to True then the haploidized samples will be loaded from the files.
    Ex. : suffix = "_haploid"
          vcf_file = "path/population.vcf"
          haploidized = 3
          load = True
          Files to be loaded containing haploidized versions of the population:
          "path/population_haploid1.vcf"
          "path/population_haploid2.vcf"
          "path/population_haploid3.vcf"
    :param float, optional min_maf : Minimum frequency value that is retained (default, all values > 0)
    :param bool, optional feedback : If the flag is set to True it will provide a visual feedback of the ongoing
        process, otherwise it will run silently with only minimal output.
    """

    template = "{}\t{}\t{}\t{}\t{}\t{}\n"

    if type(load) is str:
        if load == '1':
            load = True
        else:
            load = False

    if type(feedback) is str:
        if feedback == '1':
            feedback = True
        else:
            feedback = False

    if type(haploidized) is str:
        haploidized = ast.literal_eval(haploidized)

    if haploidized == 0:
        haploidized = None

    if haploidized is None and load:
        load = False
        logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
        logging.info("The flag 'load' is used only for haploidization: Ignored")

    file_name, file_extension = os.path.splitext(os.path.basename(vcf_file))  # separate file name and extension
    asc_file = vcf_file.replace(file_extension, ".asc")  # output file (the results will be written here)
    if frq_file is None:
        frq_file = vcf_file  # the allele frequency values are stored directly in the VCF file

    res = open(asc_file, "w")
    if haploidized is None:
        line = "Index 1\tIndex 2\tIndividual 1\tIndividual 2\tPositions\tAllele Sharing Coefficient\n"
        msg = "\nCompute allele sharing coefficient for {}\n".format(vcf_file)
    else:
        line = "Index 1\tIndex 2\tIndividual 1\tIndividual 2\tPositions\tAllele Sharing Coefficient"
        msg = "\nCompute allele sharing coefficient following haploidization, repeated {} time(s), for {}\n".format(
            haploidized, vcf_file)
        if haploidized > 1:
            line = line + "\tStandard Deviation"
            for col in range(haploidized):
                line = line + "\tRun {}".format(col + 1)
        line = line + "\n"
    res.write(line)

    if load:
        pop = vcf_file
        frq = None
    else:
        [pop, frq] = __load_data(vcf_file, frq_file, feedback)

    if feedback:
        print(msg)

    if load:
        pop_mask = None
    else:
        pop_mask = __parse_data(pop, frq, feedback=feedback)  # create a mask to identify valid samples (True)

    if haploidized is not None:
        vals = __run_haploidized(population=pop, freq=frq, min_maf=min_maf, mask=pop_mask, n=haploidized,
                                 suffix=suffix, feedback=feedback)
        __write_report(vals, res)
    else:
        if feedback:
            idx_1 = 0
            while idx_1 < len(pop):
                idx_2 = idx_1 + 1
                while idx_2 < len(pop):
                    msg = "Estimate allele sharing coefficient for {} and {} ".format(pop[idx_1].id, pop[idx_2].id)
                    with Spinner(msg):
                        [asc, pos] = allele_sharing_coeff(ind1=pop[idx_1], ind2=pop[idx_2],
                                                          freq=frq, min_maf=min_maf, mask=pop_mask)
                        res.write(template.format(idx_1, idx_2, pop[idx_1].id, pop[idx_2].id, pos, asc))
                    msg = " [{} ({})]\n".format(asc, pos)
                    sys.stdout.write(msg)
                    sys.stdout.flush()
                    idx_2 = idx_2 + 1
                idx_1 = idx_1 + 1
            res.close()
        else:
            idx_1 = 0
            while idx_1 < len(pop):
                idx_2 = idx_1 + 1
                while idx_2 < len(pop):
                    [asc, pos] = allele_sharing_coeff(ind1=pop[idx_1], ind2=pop[idx_2],
                                                      freq=frq, min_maf=min_maf, mask=pop_mask)
                    res.write(template.format(idx_1, idx_2, pop[idx_1].id, pop[idx_2].id, pos, asc))
                    idx_2 = idx_2 + 1
                idx_1 = idx_1 + 1
            res.close()


def maf2vcf(frq_file: str, vcf_file: str, map_file=None):
    """
    Insert the frequency values stored in a file into the VCF file. If inconsistencies about the sequence are seen,
    it reverts to the original VCF file.

    :param str frq_file : The file that contains the frequency values.
    :param str vcf_file : The VCF file where the frequency values will be added.
    :param str, optional map_file : The file containing the mapping of the frequency values and SNP positions.
    """
    info_header = "##INFO=<ID=AFngsrelate,Number=A,Type=Float,Description=\"Allele Frequency\">\n"  # ngsRelate TAG
    af_defined = False  # flag to avoid to insert twice the ngsRelate TAG if already there

    old_file = vcf_file + ".old"  # backup/old file name
    shutil.copy(vcf_file, old_file)  # copy the original file (so it is not lost)
    frq = open(frq_file, "r")  # frequency file pointer
    if map_file is not None:
        frq_map = open(map_file, "r")  # frequency mapping file pointer
    else:
        frq_map = None
    vcf_in = open(old_file, "r")  # input VCF file pointer
    vcf_out = open(vcf_file, "w")  # output VCF file pointer

    if map_file is None:
        is_map = False
        is_pos = False
    else:
        _, map_extension = os.path.splitext(map_file)
        if map_extension.lower() == ".map":
            is_map = True
            is_pos = False
        else:
            is_map = False
            if map_extension.lower() == ".pos":
                is_pos = True
            else:
                is_pos = False

    info_idx = -1  # will contain the index for the INFO column
    entry_line = 0
    # frq_end = False
    # map_end = False
    for line in vcf_in:   # for each line in the file
        if line.startswith("##"):  # header: copy it to the new file
            if line.startswith("##INFO") and "ID=AFngsrelate" in line:  # TAG was already in the header
                af_defined = True
            vcf_out.write(line)
        elif line.startswith("#CHROM"):  # column header: we need to find the index for the INFO column
            if not af_defined:  # before adding the column names, if necessary add the TAG line
                vcf_out.write(info_header)
            header = line.split()  # decompose the line

            # Identify the index of the INFO column:
            #
            info_idx = 0
            found = False
            while not found and info_idx < len(header):
                if header[info_idx] == "INFO":
                    found = True
                else:
                    info_idx = info_idx + 1

            if not found:  # the INFO column is not in the file, throw an error
                # Close the opened files:
                #
                vcf_in.close()
                vcf_out.close()
                frq.close()

                if frq_map is not None:
                    frq_map.close()

                __restore_vcf(vcf_file)  # restore the original file

                msg = "INFO column not found in the VCF file '{}'".format(vcf_file)
                raise ValueError(msg)

            vcf_out.write(line)  # write on the output file
        else:  # data row: we need to select the INFO field and add the frequency value
            entry_line = entry_line + 1
            # Read the VCF line details:
            #
            entry = line.split()  # decompose the line
            vcf_chr = entry[0]
            vcf_pos = entry[1]
            vcf_snp = entry[2]
            prv_value = entry[info_idx]  # previous INFO value

            # Read the frequency details:
            #
            frq_entry = frq.readline()
            if frq_entry.startswith("#"):  # header, discard and read the next line
                frq_entry = frq.readline()  # read (and discard) the header of the frequency file which won't be used

            frq_entry = frq_entry.split()  # decompose the line

            try:
                _ = float(frq_entry[0])  # check if it is really a data line
            except ValueError:  # an header without the #, read and split the next line
                frq_entry = frq.readline()
                frq_entry = frq_entry.split()  # decompose the line

            if len(frq_entry) == 1:
                frq_chr = None
                frq_snp = None
                frq_val = frq_entry[0]
            else:
                frq_chr = frq_entry[0]
                try:
                    _ = int(frq_entry[1])  # check if it is SNP id or SNP pos
                    frq_pos = frq_entry[1]
                    frq_snp = None
                except ValueError:  # not an integer, hence it is a SNP id
                    frq_snp = frq_entry[1]
                    frq_pos = None
                frq_val = frq_entry[4]

            # Read the mapping details:
            #
            if map_file is not None:
                map_entry = frq_map.readline()
                map_entry = map_entry.split()  # decompose the line
                if is_pos:
                    map_chr = map_entry[0]
                    map_snp = None
                    map_pos = map_entry[1]
                elif is_map:
                    map_chr = map_entry[0]
                    map_snp = map_entry[1]
                    map_pos = map_entry[3]
                else:
                    msg = "Unknown format for position/map file '{}'".format(map_file)

                    # Close the opened files:
                    #
                    vcf_in.close()
                    vcf_out.close()
                    frq.close()

                    if map_file is not None:
                        frq_map.close()

                    __restore_vcf(vcf_file)  # restore the original file

                    raise ValueError(msg)
            else:
                map_chr = None
                map_snp = None
                map_pos = None

            # Check consistency with the entries:
            #
            if vcf_snp == ".":
                vcf_snp = None

            consistent = True
            msg = None
            if (frq_chr is not None and not vcf_chr == frq_chr) or (map_file is not None and not vcf_chr == map_chr):
                msg = "The VCF, FRQ and MAP/POS files are not consistent.\nFRQ CHR: {}, VCF CHR: {}, MAP CHR: {}\n" \
                      "{}: {}".format(frq_chr, vcf_chr, map_chr, entry_line, line)
                consistent = False
            elif (frq_snp is not None and
                  vcf_snp is not None and
                  not vcf_snp == frq_snp) or\
                    (map_snp is not None and
                     vcf_snp is not None and
                     not vcf_snp == map_snp):
                msg = "The VCF, FRQ and MAP/POS files are not consistent.\nFRQ SNP: {}, VCF SNP: {}, MAP SNP: {}\n" \
                      "{}: {}".format(frq_snp, vcf_snp, map_snp, entry_line, line)
                consistent = False
            elif (map_file is not None and not vcf_pos == map_pos) or\
                    (frq_pos is not None and not vcf_pos == frq_pos) or\
                    (map_file is not None and frq_pos is not None and not map_pos == frq_pos):
                msg = "The VCF, FRQ and MAP/POS files are not consistent.\nVCF POS: {}, MAP POS: {}, FRQ POS: {}\n" \
                      "{}: {}".format(vcf_pos, map_pos, frq_pos, entry_line, line)
                consistent = False
            if not consistent:
                # Close the opened files:
                #
                vcf_in.close()
                vcf_out.close()
                frq.close()

                if map_file is not None:
                    frq_map.close()

                __restore_vcf(vcf_file)  # restore the original file

                raise ValueError(msg)

            if prv_value == ".":  # if empty just insert the TAG value
                entry[info_idx] = "AFngsrelate={}".format(frq_val)
            elif prv_value[-1] == ";":  # if not empty attach the TAG at the end
                entry[info_idx] = entry[info_idx] + "AFngsrelate={}".format(frq_val)
            else:  # if not empty attach the TAG at the end
                entry[info_idx] = entry[info_idx] + ";AFngsrelate={}".format(frq_val)

            # Create the new line and write it to the output file:
            #
            new_line = "\t".join(entry)
            new_line = new_line + "\n"
            vcf_out.write(new_line)  # write on the output file

    # Close the opened files:
    #
    vcf_in.close()
    vcf_out.close()
    frq.close()

    if map_file is not None:
        frq_map.close()


def split_snp(snp: str) -> [str, str]:
    """
    Given a snp in string format, it separates the two strands.

    :param str, snp : The SNP to be divided.

    :return: [str, str] : The two separated strands.
    """

    return snp.split(snp_sep(snp))


def snp_sep(snp: str) -> str:
    """
    Identify the separator of the two strands of the SNP.

    :param str, snp : The SNP to be considered.

    :return: str : The separator
    """

    if "|" in snp:  # identify the separator character
        div_snp = "|"
    elif "/" in snp:
        div_snp = "/"
    else:
        msg = "Unknown separator was found (snp = {}). Expected '|' or '/'".format(snp)
        raise ValueError(msg)

    return div_snp


def select_snps(vcf_file: str, pos_file: str) -> [int, int, int]:
    """
    Given an input file containing the list of accepted SNPs, defined by a chromosome column (the first column) and
    by a positional column (the second column), selects and retains from a given VCF file only the listed SNPs.

    :param str vcf_file : The input VCF file to be filtered.
    :param str pos_file : The file listing the SNPs to be retained (with the first column identifying the chromosome
    number and the second column identifying the position of the SNP).

    :return: [int, int, int] : Number of selected SNPs, Number of SNPs in vcf_file, Number of SNPs in pos_file.
    """

    old_vcf_file = vcf_file + ".raw"  # backup/old file name
    shutil.copy(vcf_file, old_vcf_file)  # copy the original file (so it is not lost)

    old_pos_file = pos_file + ".raw"  # backup/old file name
    shutil.copy(pos_file, old_pos_file)  # copy the original file (so it is not lost)

    vcf = open(old_vcf_file, "r")
    tot_vcf = 0
    read_vcf = True

    pos = open(old_pos_file, "r")
    tot_pos = 0
    read_pos = True

    out_vcf = open(vcf_file, "w")
    out_pos = open(pos_file, "w")
    write_out = 0

    pos_end = False
    vcf_end = False

    is_header = True
    vcf_chr = None
    pos_chr = None
    vcf_pos = None
    pos_pos = None
    vcf_line = None
    pos_line = None
    while not pos_end and not vcf_end:
        if read_pos:
            pos_line = pos.readline()
            while is_header:
                if pos_line.startswith("#"):
                    is_header = True
                else:
                    pos_entry = pos_line.split()
                    try:
                        _ = int(pos_entry[0])
                        is_header = False
                    except ValueError:  # an header without the #, read and split the next line
                        is_header = True

                if is_header:
                    out_pos.write(pos_line)
                    pos_line = pos.readline()

            if pos_line == "":
                pos_end = True
            else:
                tot_pos = tot_pos + 1
                pos_entry = pos_line.split()
                pos_chr = int(pos_entry[0])
                pos_pos = int(pos_entry[1])
            read_pos = False

        if read_vcf:
            vcf_line = vcf.readline()
            while vcf_line.startswith("#"):
                out_vcf.write(vcf_line)
                vcf_line = vcf.readline()

            if vcf_line == "":
                vcf_end = True
            else:
                tot_vcf = tot_vcf + 1
                vcf_entry = vcf_line.split()
                vcf_chr = int(vcf_entry[0])
                vcf_pos = int(vcf_entry[1])
            read_vcf = False

        if vcf_chr == pos_chr and vcf_pos == pos_pos:  # retain the SNP, i.e., write onto output files
            out_vcf.write(vcf_line)
            out_pos.write(pos_line)
            read_pos = True
            read_vcf = True
            write_out = write_out + 1
        else:
            if vcf_chr == pos_chr:
                if vcf_pos < pos_pos:
                    read_vcf = True
                else:
                    read_pos = True
            elif vcf_chr < pos_chr:
                read_vcf = True
            else:
                read_pos = True

    while not vcf_end:
        vcf_line = vcf.readline()
        if vcf_line == "":
            vcf_end = True
        else:
            tot_vcf = tot_vcf + 1

    while not pos_end:
        pos_line = pos.readline()
        if pos_line == "":
            pos_end = True
        else:
            tot_pos = tot_pos + 1

    vcf.close()
    pos.close()
    out_vcf.close()
    out_pos.close()

    return [write_out, tot_vcf, tot_pos]


def idx2int(idx: list) -> list:
    """
    Convert lists of indices which are stored as strings into lists of integers.

    :param list idx : The lists of indices stored as strings.

    :return: list : The lists of indices converted to integers.
    """

    out_idx = []
    for val in idx:
        out_idx.append([int(i) for i in val])

    return out_idx


def idx2str(idx: list) -> list:
    """
    Convert lists of indices which are stored as integers into lists of strings.

    :param list idx : The lists of indices stored as integers.

    :return: list : The lists of indices converted to strings.
    """

    out_idx = []
    for val in idx:
        out_idx.append([str(i) for i in val])

    return out_idx


def __fix_snp(s: str) -> str:
    """
    Fix the syntax of the SNP strand by removing additional information which is not used.

    :param str, s : One strand of a given SNP.

    :return: str : The strand following the removal of additional information not relevant to the simulation.
    """

    valid = ["0", "1", "."]  # accepted values
    if len(s) == 1 and s in valid:
        snp = s
    else:
        spl = s.split(":")
        if len(spl) > 1:
            snp = __fix_snp(spl[0])
        else:
            snp = "-1"  # i.e. to be removed

    return snp


def __check_haploidized(h1: [int], h2: [int], mask: [bool]) -> [bool]:
    """
    Given two lists of haploidized samples, it defines a mask that identifies the common positions with accepted values.

    :param [int], h1 : The first haploidized sample.
    :param [int], h2 : The second haploidized sample.
    :param [bool], mask : The mask identifying the SNPs to be considered.

    :return: [bool] :  The mask of accepted SNPs values updated by considering the haploidized values.
    """

    hap_mask = [True] * len(mask)
    idx = 0
    while idx < len(hap_mask):
        if mask[idx]:
            if h1[idx] == -1 or h2[idx] == -1:
                hap_mask[idx] = False
        else:
            hap_mask[idx] = False

        idx = idx + 1

    return hap_mask


def __parse_data(population: [Individual], freq: [float], feedback=True) -> [bool]:
    """
    Parse all SNPs and associated frequency values to format the data to maintain compatibility
    with the allele sharing coefficient function. It flags also the SNPs which should be removed
    either because the format is incompatible or the frequency value is not acceptable.

    The function modifies the SNPs format within the individuals if necessary and flag as False the
    SNP if it remains in an incompatible status.

    :param [Individual] population : The individual to be studied.
    :param [float] freq : The allele frequency values.
    :param bool, optional feedback : If the flag is set to True it will provide a visual feedback of the ongoing
    process, otherwise it will run silently with only minimal output.

    :return: [bool] : A list of booleans that flag as False the SNPs which are not compatible with
    the allele sharing coefficient function.
    """

    snps = [True] * len(freq)  # at the beginning we assume all SNPs will be retained
    for idx_ind, ind in enumerate(population):  # for each individual in the population
        if feedback:
            print("Parsing individual: {}".format(ind.id))
        upd8_chromosomes = []  # update chromosomes for the individual following the parsing
        idx_freq = 0
        for idx_chr, c in enumerate(ind.chromosomes):  # for each chromosome of the individual
            upd8_chr = []  # update the current chromosome
            for idx_snp, snp in enumerate(c):  # for each SNP in the chromosome
                tmp = snp
                # Parse the SNP:
                #
                div_snp = snp_sep(snp)  # identify the separator character
                spl_snp = split_snp(snp)  # separate the two strands of the SNP

                if len(spl_snp) == 2:  # it is a recognized format

                    # Parse now the two strands:
                    #
                    s1 = __fix_snp(spl_snp[0])
                    s2 = __fix_snp(spl_snp[1])

                    # one of the two strands is in an unknown/unaccepted format or a freq value is not valid
                    if s1 == "-1" or s2 == "-1" or freq[idx_freq] == 0 or freq[idx_freq] == -1:
                        if snps[idx_freq]:
                            print("snp: {} => freq = {}".format(tmp, freq[idx_freq]))
                        snps[idx_freq] = False  # discard the SNP

                    upd8_chr.append("{}{}{}".format(s1, div_snp, s2))
                else:
                    msg = "Unknown SNP format (snp = {}). Expected 'val1{}val2'".format(snp, div_snp)
                    raise ValueError(msg)

                idx_freq = idx_freq + 1
            upd8_chromosomes.append(upd8_chr)
        ind.set_chromosomes(upd8_chromosomes)

    return snps


def __load_data(vcf_file: str, frq_file: str, feedback=True) -> [[Individual], [float]]:
    """
    Import population and frequency values.

    :param str vcf_file : The file name from which the population is imported.
    :param str frq_file: The file name from which the frequency values are loaded.
    :param bool, optional feedback : If the flag is set to True it will provide a visual feedback of the ongoing
    process, otherwise it will run silently with only minimal output.

    :return: [[Individual], [float]] : The population as list of Individual instances and the list of frequency values.
    """

    pop = load_population(vcf_file, feedback=feedback)
    frq = import_freq(frq_file, feedback=False)

    return [pop, frq]


def __write_report(vals, file):
    """
    Convert the result values into text lines to be written in 'file'.

    :param vals: The list of list (containing string and float) which need to be written to the file.
    :param file: The file handler.
    """
    for val in vals:
        line = ""
        first = True
        for entry in val:
            if first:
                line = "{}".format(entry)
                first = False
            else:
                line = line + "\t{}".format(entry)
        line = line + "\n"
        file.write(line)
    file.close()


def __load_haploidized(hap_file: str, feedback=True) -> [[Individual],
                                                         [float],
                                                         [int],
                                                         [bool]]:
    """
    Load a VCF file that contains haploidized samples. It returns the list of samples, the haploidized version,
    the frequency values and the mask of SNPs validity (True for a valid SNP, False otherwise).

    :param str hap_file : The haploidized file.
    :param bool, optional feedback : If the flag is set to True it will provide a visual feedback of the ongoing
    process, otherwise it will run silently with only minimal output.

    :return: [[Individual], [float], [int], [bool]] : list of samples, frequency values, haploidized version of samples
    and mask of valid SNPs.
    """

    # Load the VCF file with haploidized data
    #
    if feedback:
        print("Load haploidized data from VCF file: {}".format(hap_file))
    [population, freq] = __load_data(hap_file, hap_file, feedback)
    mask = [True] * len(freq)
    h = []
    idx_ind = 0
    for ind in population:
        idx_ind = idx_ind + 1
        if feedback:
            print("Extract haploidized data from '{}' ({}/{})".format(ind.id, idx_ind, len(population)))
        idx_freq = 0
        ind_h = []
        tot_snps = 0
        valid_snps = 0
        for chromosome in ind.chromosomes:
            tot_snps = tot_snps + len(chromosome)
            for snp in chromosome:
                if len(snp) > 1:
                    div_snp = snp_sep(snp)  # identify the separator character
                    spl_snp = split_snp(snp)  # separate the two strands of the SNP

                    if len(spl_snp) == 2:  # it is a recognized format

                        # Parse now the two strands:
                        #
                        s1 = __fix_snp(spl_snp[0])
                        s2 = __fix_snp(spl_snp[1])

                        if s1 == s2:
                            curr_snp = s1
                        else:
                            msg = "Unexpected haploidized SNP (snp = {}). Expected 'val1{}val1'".format(snp, div_snp)
                            raise ValueError(msg)
                    else:
                        msg = "Unknown SNP format (snp = {}). Expected 'val1{}val2'".format(snp, div_snp)
                        raise ValueError(msg)
                else:
                    curr_snp = snp

                try:
                    val = int(curr_snp)
                    ind_h.append(val)
                    valid_snps = valid_snps + 1
                except ValueError:
                    ind_h.append(-1)

                if curr_snp not in ["0", "1", "."] or freq[idx_freq] <= 0 or freq[idx_freq] > 1:
                    mask[idx_freq] = False

                idx_freq = idx_freq + 1
        h.append(ind_h)
        if feedback:
            print("  - Found {} valid SNPs. With a total number of checked SNPs of {}".format(valid_snps, tot_snps))

    return population, freq, h, mask


def __run_haploidized(population, freq: [float], mask: [bool], n: int, suffix="_haploid", min_maf=0, feedback=True):
    """
    Compute the allele sharing coefficient for Individual instances that need to be haploidized.
    If population is passed as list of instances of Individual then the freq and mask parameters are expected.
    If population is passed as a string identifying a reference set of samples, the suffix and n are used to
    identify the files containing haploidized versions of the reference file (and the attributes freq and mask
    are ignored).

    :param [Individual] or str population : List of individuals that need to be haploidized prior computing the allele
    sharing coefficient or, alternatively a string representing a VCF file of a reference population that has been
    haploidized.
    Ex. : population = "path/population.vcf"
          suffix = "_haploid"
          n = 3
          Files to be loaded containing haploidized versions of the population:
          "path/population_haploid1.vcf"
          "path/population_haploid2.vcf"
          "path/population_haploid3.vcf"
    :param [float] freq : The allele frequencies.
    :param [bool] mask : A list of booleans identifying which samples should be considered (True) and which one should
    be ignored (False).
    :param int n : The number of repetitions.
    :param str, optional suffix : If population is a reference file, the suffix is used to reconstruct the name of the
    haploidized versions of it. Default suffix is '_haploid'.
    Ex. : suffix = "_haploid"
          population = "path/population.vcf"
          n = 3
          Files to be loaded containing haploidized versions of the population:
          "path/population_haploid1.vcf"
          "path/population_haploid2.vcf"
          "path/population_haploid3.vcf"
    :param float, optional min_maf : Minimum frequency value that is retained (default, all values > 0)
    :param bool, optional feedback : If the flag is set to True it will provide a visual feedback of the ongoing
    process, otherwise it will run silently with only minimal output.

    :return: The results of the analysis as list of list containing column information in string format and float.
    """

    res = []
    for idx_run in range(n):
        # Haploidize the data or load the file:
        #
        if type(population) is str:
            file_name, file_extension = os.path.splitext(population)
            hap_file = file_name + "{}{}".format(suffix, idx_run + 1) + file_extension
            [pop, freq, h, mask] = __load_haploidized(hap_file=hap_file, feedback=feedback)
        else:
            pop = population
            h = []
            idx_h = 0
            for ind in population:
                idx_h = idx_h + 1
                if feedback:
                    msg = "Run {}/{}: haploidize the data, sample {}/{} ".format(idx_run + 1, n, idx_h, len(population))
                    with Spinner(msg):
                        h.append(ind.haploidize())
                    sys.stdout.write("[OK]\n")
                    sys.stdout.flush()
                else:
                    h.append(ind.haploidize())

        # Estimate allele sharing coefficient for all couples in the population:
        #
        idx = 0
        idx_1 = 0
        while idx_1 < len(h):
            idx_2 = idx_1 + 1
            while idx_2 < len(h):
                if feedback:
                    msg = "Run {}/{}: estimate allele sharing coefficient for {} and {} ".format(idx_run + 1, n,
                                                                                                 pop[idx_1].id,
                                                                                                 pop[idx_2].id)
                    with Spinner(msg):
                        hap_mask = __check_haploidized(h[idx_1], h[idx_2], mask)
                        [asc, pos] = allele_sharing_coeff(ind1=h[idx_1], ind2=h[idx_2],
                                                          freq=freq, min_maf=min_maf, mask=hap_mask)
                    msg = "[{} ({})]\n".format(asc, pos)
                    sys.stdout.write(msg)
                    sys.stdout.flush()
                else:
                    hap_mask = __check_haploidized(h[idx_1], h[idx_2], mask)
                    [asc, pos] = allele_sharing_coeff(ind1=h[idx_1], ind2=h[idx_2],
                                                      freq=freq, min_maf=min_maf, mask=hap_mask)

                if idx_run == 0:  # init the structure
                    res.append([idx_1, idx_2, pop[idx_1].id, pop[idx_2].id, pos])
                    if n > 1:  # more than one run so we compute mean value and standard deviation too
                        res[idx].append(0)  # mean ASC
                        res[idx].append(0)  # std. dev. ASC
                res[idx].append(asc)  # append the coefficient for the current run
                idx = idx + 1  # move to the next couple of individuals
                idx_2 = idx_2 + 1  # update index for the second individual
            idx_1 = idx_1 + 1  # update index for the first individual

    if n > 1:  # for more than one run compute mean value and standard deviation (for each SNP)
        for row in res:
            row[5] = statistics.mean(row[7:])
            row[6] = statistics.stdev(row[7:])

    return res


def __read_vcf(vcf_file: str):
    """
    Read the population data from a VCF file.

    :param str vcf_file : The file from which the data are extracted.

    :return: The IDs of the individuals, the chromosomes IDs and the raw GT info of all samples and loci.
    """

    gt_array = []  # holds GT info of all samples for all loci, like a matrix
    chr_id = []  # retains the chromosome id for each row
    ids = []  # list of sample/individual IDs

    in_file = open(vcf_file, "r")

    for line in in_file:  # read GT data
        if line.startswith("#CHR"):  # heather with column identifiers
            line_cols = line.split()
            ids = line_cols[9:]
        elif not line.startswith("##"):  # not a comment and not heather, save the data
            line_cols = line.split()
            chr_id.append(line_cols[0])
            gt_array.append(line_cols[9:])
    in_file.close()

    return [ids, chr_id, gt_array]


def __extract_chromosomes(ids: [str], chr_id: [str], gt_array, individual) -> [[str]]:
    """
    Given a matrix containing GT data, extracts the sequence of chromosomes pertaining to a specific individual.

    :param [str] ids : The list of individual IDs.
    :param [str] chr_id : The list of chromosomes IDs.
    :param gt_array : the GT data.
    :param str, int individual : The individual's ID (as string) or as column index (int) with 0 as the column
    of the first individual.

    :return: [[str]] : The sequence of chromosomes.
    """

    if isinstance(individual, str):
        id_idx = ids.index(individual)  # identify column numbers of the individual
    elif isinstance(individual, int):
        id_idx = check_data("individual", individual, int, 0, len(ids))
    else:
        raise ValueError("Unsupported type for an individual. Either ID (as str) or index (as int)")

    # define the chromosomes of the individual (GT over all locations)
    chromosomes = []
    chr_idx = 0  # index of the chromosome (N.B. Not the ID)
    chr_seq = []  # will retain the sequence of SNPs for a given chromosome
    for val in gt_array:

        # if there is a change to a new chromosome, store the current sequence and initialize a new empty one
        if chr_idx > 0 and not (chr_id[chr_idx] == chr_id[chr_idx - 1]):
            chromosomes.append(chr_seq)
            chr_seq = []

        chr_seq.append(val[id_idx])
        chr_idx = chr_idx + 1
    chromosomes.append(chr_seq)  # append the last sequence too

    return chromosomes


def __restore_vcf(vcf_file: str, suffix=".old"):
    """
    Restore the previous version of the VCF file (if any).

    :param str vcf_file :  The original name (i.e., without the .old suffix) of the file that needs to be restored.
    :param str, optional suffix : The suffix extension attached to the file.
    """

    old_file = vcf_file + suffix  # name of the backup/old file
    old_path = Path(old_file)
    if old_path.is_file():  # there is a file to be restored
        vcf_path = Path(vcf_file)
        if vcf_path.is_file():  # there is a file that need to be removed
            os.unlink(vcf_file)  # remove the file
        shutil.move(old_file, vcf_file)  # restore the previous file
    else:
        msg = "The VCF file '{}' has no previous version.".format(vcf_file)
        raise ValueError(msg)
