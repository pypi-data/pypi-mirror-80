"""
Kinship simulation, Individual class:
Maintains the relevant (autosome and/or sex) chromosomes details of the individual as well as references to its parents,
offsprings and gender details. It has an associated ID and it may contain additional information pertaining to the
recombination process from which the individual was generated.
"""

__version__ = '2020.8'
__author__ = 'Team Neogene'

import random
import time
import string
import logging
from kinshipsim import lib


class Individual:

    _chromosomes: [[str]]  # the chromosomes of the individual.
    _x_chromosome: [str]  # the x chromosome of the individual
    _gender: int  # the gender of the individual
    _parents: list  # the parents of the individual (empty list if the individual is a founder's parent).
    _offsprings: list  # the list of offsprings
    _crossover: dict  # dictionary containing the lists of crossover points (one for each parent).
    _strand: dict  # dictionary containing the lists of selected strands for each segment (one for each parent).
    _x_crossover: [int, int, int]  # the three points from which the x chromosome from the mother is segmented
    _x_strand: [int, int, int, int]  # the selection of the strand for each segment
    _id: str  # the id of the individual.

    def __init__(self, ind_id=None, chromosomes=None, parents=None):
        """
        Create a new individual by defining its chromosomes (and no parents, i.e., a founder's parent)
        or by passing the two parents (as two Individual instances). The gender and x chromosome are not initialized
        and therefore are set to None. To set them use the 'set_gender' and 'set_x_chromosome' methods or by calling the
        'x_chromosome_reproduction' method by specifying the gender and the x chromosome of both father and mother.

        :param str, optional ind_id : The ID of the individual. If not defined it is automatically generated.
        :param [[str]], optional chromosomes : The chromosomes associated with the individual.
        :param [Individual, Individual], optional parents : The parents of the individual.
        """

        if parents is not None:
            if chromosomes is not None:
                msg = "The individual must be defined by either two parents or by its chromosomes, not by both."
                logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
                logging.info(msg)

            #  individual generated from the parents
            res = self.chromosomes_reproduction(parents[0].chromosomes, parents[1].chromosomes)
            self._chromosomes = res.get("chromosomes")
            self._crossover = res.get("crossover")
            self._strand = res.get("strand")
            self._parents = parents
        elif chromosomes is None:  # "empty" individual
            self._chromosomes = []
            self._parents = []
            self._crossover = {}
            self._strand = {}
        else:  # individual defined by the passed chromosomes
            self._chromosomes = self.check_chromosomes(chromosomes)
            self._parents = []
            self._crossover = {}
            self._strand = {}

        self._offsprings = []

        if ind_id is None:  # automatically generate an ID
            if not self._parents:
                self._id = "Founder_{}".format(Individual.auto_id())
            else:
                self._id = "Offspring_{}".format(Individual.auto_id())
        else:
            self._id = ind_id

        self._gender = -1
        self._x_chromosome = []
        self._x_crossover = []
        self._x_strand = []

    @property
    def chromosomes(self) -> [[str]]:
        """
        The chromosomes of the individual.

        :return: [[str]] : The chromosomes.
        """

        return self._chromosomes

    @property
    def x_chromosome(self) -> [str]:
        """
        The x chromosomes of the individual.

        :return: [str] : The x chromosome.
        """

        return self._x_chromosome

    @property
    def gender(self) -> int:
        """
        The gender of the individual (0=female, 1=male).

        :return: int : The gender.
        """

        return self._gender

    @property
    def parents(self) -> list:
        """
        The parents of the individual.

        :return: [Individual, Individual] : The parents.
        """

        return self._parents

    @property
    def offsprings(self) -> list:
        """
        The offsprings of the individual.

        :return: [Individual] : The offsprings.
        """

        return self._offsprings

    @property
    def id(self) -> str:
        """
        The ID of the individual.

        :return: str : The ID.
        """

        return self._id

    @property
    def x_crossover(self) -> [int, int, int]:
        """
        The three crossover points that were selected during the creation of the x chromosome of the individual.

        :return: str : The three crossover points.
        """

        return self._x_crossover

    @property
    def x_strand(self) -> [int, int, int, int]:
        """
        The selected strands, for each of the four segments, during the creation of the x chromosome of the individual.

        :return: str : The selected strands.
        """

        return self._x_strand

    def set_chromosomes(self, chrs: [[str]]):
        """
        Assign a new sequence of chromosomes to the individual.

        :param [[str]] chrs : The new sequence of chromosomes.
        """

        self._chromosomes = chrs

    def crossover(self, idx: int) -> [[int]]:
        """
        Returns the crossover points for a specific parent.

        :param int idx : select the parent (0 or 1).

        :return: [[int]] : The crossover points pertaining to the specified parent.
        """

        # evaluate consistency of the parameters
        idx = lib.check_data("parent idx", idx, int, set_val=[0, 1])

        parent = ["parent1", "parent2"]

        crs = []
        if self._crossover:
            crs = self._crossover[parent[idx]]

        return crs

    def set_crossover(self, parent1: [[int]], parent2: [[int]]):
        """
        Assign the given crossover points to the individual.

        :param [[int]] parent1: Crossover points from the first parent.
        :param [[int]] parent2: Crossover points from the second parent.
        """

        self._crossover = {"parent1": parent1, "parent2": parent2}

    def strand(self, idx: int) -> [[int]]:
        """
        Returns the selected strand for each segment of the chromosomes given a specific parent.

        :param int idx : identify the parent (0 or 1).

        :return: [[int]] : The selected strands for each segment of the chromosomes.
        """

        # evaluate consistency of the parameters
        idx = lib.check_data("parent idx", idx, int, set_val=[0, 1])

        parent = ["parent1", "parent2"]

        strand = []
        if self._strand:
            strand = self._strand[parent[idx]]

        return strand

    def set_strand(self, parent1: [[int]], parent2: [[int]]):
        """
        Assign the given selected strands to the individual.

        :param [[int]] parent1: Selected strand from the first parent.
        :param [[int]] parent2: Selected strand from the second parent.
        """

        self._strand = {"parent1": parent1, "parent2": parent2}

    def set_gender(self, gender: int):
        """
        Set the gender of the individual as male (1) or female (0).
        """

        gender = lib.check_data("gender", gender, int, set_val=[0, 1])
        self._gender = gender

    def set_x_chromosome(self, x_chromosome: [str]):
        """
        Set the x chromosome of the individual.
        """

        self._x_chromosome = x_chromosome

    def set_x_crossover(self, x_crossover: [int, int, int]):
        """
        Set the crossover points for the x chromosome.

        :param x_crossover: The crossover points.
        """

        self._x_crossover = x_crossover

    def set_x_strand(self, x_strand: [int, int, int, int]):
        """
        Set the selected strands for the x chromosome.

        :param x_strand: The selected strands.
        """

        self._x_strand = x_strand

    def set_parents(self, parents: list):
        """
        Allows to specify the parents of the individual.

        :param [Individual] parents : The parents of the individual.
        """

        for parent in parents:
            _ = lib.check_data("parent", parent, Individual)
        self._parents = parents

    def set_offsprings(self, offsprings: list):
        """
        Allows to specify the offsprings of the individual.

        :param [Individual] offsprings : The offsprings of the individual.
        """

        for offspring in offsprings:
            _ = lib.check_data("offspring", offspring, Individual)
        self._offsprings = offsprings

    @staticmethod
    def check_chromosomes(chromosomes: [[str]], old_div_snp='/', new_div_snp='|') -> [[str]]:
        """
        SNPs may use two different separators ('|', '/') thus any loaded chromosomes sequence need to be using a common
        format.

        :param [[str]] chromosomes : The chromosomes to be checked for consistency of the separator.
        :param str, optional old_div_snp : The separator of the strands that needs to be replaced.
        :param str, optional new_div_snp : The new separator of the strands.

        :return: [[str]] : The chromosomes sequence using the standard separator '|'.
        """

        fix_chromosomes = []
        for chromosome in chromosomes:
            fix_chromosome = []
            for snp in chromosome:
                fix_chromosome.append(snp.replace(old_div_snp, new_div_snp))
            fix_chromosomes.append(fix_chromosome)

        return fix_chromosomes

    @staticmethod
    def auto_id() -> str:
        """
        Automatically generate an ID for an individual as a random label plus a timestamp.

        :return: str : the ID
        """

        time_id = time.strftime("%Y%m%d%H%M")
        letters = string.ascii_lowercase
        label_id = ""
        for idx in range(len(time_id)):
            label_id = label_id + random.choice(letters)

        return "{}_{}".format(label_id, time_id)

    @staticmethod
    def x_chromosome_reproduction(gender: int, x_father: [str], x_mother: [str], div_snp="|") -> dict:
        """
        Generate the x chromosome of the individual given the x chromosomes of the father and the mother.

        :param int gender : The gender of the individual.
        :param [str] x_father : The x chromosome of the father.
        :param [str] x_mother : The x chromosome of the mother.
        :param str, optional div_snp : The separator of the strands.

        :return: dict : A dictionary with the generated x chromosome, the crossover points and selected strands.
        """

        output = {}

        chr_length = len(x_father)  # length of the chromosome
        if not chr_length == len(x_mother):  # lengths not equal
            msg = "Individuals have different number of SNPs (Found {} and {}).".format(
                chr_length, len(x_mother))
            raise ValueError(msg)

        # define the homologue chromosomes for the mother and father
        mother_homo1 = []
        mother_homo2 = []
        for val in x_mother:
            mother_homo1.append(val.split(div_snp)[0])
            mother_homo2.append(val.split(div_snp)[1])

        father_homo = []
        for val in x_father:
            father_homo.append(val.split(div_snp)[0])

        # range(1, chr_length) generate random values between 1 and chr_length-1
        mother_rec_pts = sorted(random.sample(range(1, chr_length), 3))

        output["x_crossover"] = mother_rec_pts  # returned parameter

        # split the homologue chromosomes according to recombination points
        mother_homo1 = [mother_homo1[i: j] for i, j in
                        zip([0] + mother_rec_pts, mother_rec_pts + [None])]
        mother_homo2 = [mother_homo2[i: j] for i, j in
                        zip([0] + mother_rec_pts, mother_rec_pts + [None])]

        mother_homos = [mother_homo1, mother_homo2]  # merge the two strands of the mother

        # choose one homologue randomly from each segment
        mother_segs = random.choices([0, 1], k=4)

        output["x_strand"] = mother_segs

        # assemble the selected segments together to form gametes
        mother_gamete = []
        father_gamete = father_homo
        for i in range(4):
            mother_gamete = mother_gamete + mother_homos[mother_segs[i]][i]

        # join the gametes to form the offspring chromosome
        single_chr = []
        for i in range(len(mother_gamete)):
            if gender == 0:  # offspring is female (not recombined father | recombined mother)
                offspring_gt = str(father_gamete[i]) + div_snp + str(mother_gamete[i])
            else:  # offspring is male (recombined mother only)
                offspring_gt = str(mother_gamete[i]) + div_snp + str(mother_gamete[i])
            single_chr.append(offspring_gt)

        output["x_chromosome"] = single_chr

        return output

    @staticmethod
    def chromosomes_reproduction(chromosomes1: [[str]], chromosomes2: [[str]], div_snp="|") -> dict:
        """
        Generate the chromosomes of an offspring given the chromosomes of the parents.

        :param [[str]] chromosomes1 : The chromosomes of the first parent.
        :param [[str]] chromosomes2 : The chromosomes of the second parent.
        :param str, optional div_snp : The separator of the strands.

        :return: A dictionary containing the chromosomes of the offspring (chromosomes) the crossover points from each
            parent (crossover["parent1"], crossover["parent2"]) and the selected segments (strand["parent1"],
            strand["parent2"]).
        """

        output = {}

        n_chr = len(chromosomes1)  # number of chromosomes
        if not n_chr == len(chromosomes2):
            msg = "Individuals have different number of chromosomes (Found {} and {}).".format(
                n_chr, len(chromosomes2))
            raise ValueError(msg)

        offspring_chromosome = [[]] * n_chr  # initialize the sequence of the chromosomes
        offspring_crossover = {"parent1": [[0, 0, 0]] * n_chr, "parent2": [[0, 0, 0]] * n_chr}
        offspring_strand = {"parent1": [[0, 0, 0]] * n_chr, "parent2": [[0, 0, 0]] * n_chr}
        for idx_chromosome in range(len(offspring_chromosome)):

            # the considered chromosome (from each parent)
            chr1 = chromosomes1[idx_chromosome]
            chr2 = chromosomes2[idx_chromosome]

            chr_length = len(chr1)
            if not(chr_length == len(chr2)):
                msg = "Individuals have different chromosome length (Found {} and {} for index {}).".format(
                    chr_length, len(chr2), idx_chromosome)
                raise ValueError(msg)

            # evaluate consistency of the length
            chr_length = lib.check_data("chromosome length (idx = {})".format(idx_chromosome),
                                        chr_length, int, min_val=4)

            # define the homologue chromosomes for parent1
            chr1_homo1 = []
            chr1_homo2 = []
            for val in chr1:
                chr1_homo1.append(val.split(div_snp)[0])
                chr1_homo2.append(val.split(div_snp)[1])

            # define the homologue chromosomes for parent2
            chr2_homo1 = []
            chr2_homo2 = []
            for val in chr2:
                chr2_homo1.append(val.split(div_snp)[0])
                chr2_homo2.append(val.split(div_snp)[1])

            # first segment: [0, chr1_rec_pts[0])
            # second segment: [chr1_rec_pts[0], chr1_rec_pts[1])
            # third segment: [chr1_rec_pts[1], chr1_rec_pts[2])
            # third segment: [chr1_rec_pts[2], end]
            #
            # range(1, chr_length) generate random values between 1 and chr_length-1
            chr1_rec_pts = sorted(random.sample(range(1, chr_length), 3))
            chr2_rec_pts = sorted(random.sample(range(1, chr_length), 3))

            offspring_crossover["parent1"][idx_chromosome] = chr1_rec_pts
            offspring_crossover["parent2"][idx_chromosome] = chr2_rec_pts

            # split the homologue chromosomes according to recombination points
            chr1_homo1 = [chr1_homo1[i: j] for i, j in
                          zip([0] + chr1_rec_pts, chr1_rec_pts + [None])]
            chr1_homo2 = [chr1_homo2[i: j] for i, j in
                          zip([0] + chr1_rec_pts, chr1_rec_pts + [None])]
            chr2_homo1 = [chr2_homo1[i: j] for i, j in
                          zip([0] + chr2_rec_pts, chr2_rec_pts + [None])]
            chr2_homo2 = [chr2_homo2[i: j] for i, j in
                          zip([0] + chr2_rec_pts, chr2_rec_pts + [None])]

            chrs1_homos = [chr1_homo1, chr1_homo2]  # merge the two strands of parent 1
            chrs2_homos = [chr2_homo1, chr2_homo2]  # merge the two strands of parent 2

            # choose one homologue randomly from each segment
            chr1_segs = random.choices([0, 1], k=4)
            chr2_segs = random.choices([0, 1], k=4)

            offspring_strand["parent1"][idx_chromosome] = chr1_segs
            offspring_strand["parent2"][idx_chromosome] = chr2_segs

            # assemble the selected segments together to form gametes
            chr1_gamete = []
            chr2_gamete = []
            for i in range(4):
                chr1_gamete = chr1_gamete + chrs1_homos[chr1_segs[i]][i]
                chr2_gamete = chr2_gamete + chrs2_homos[chr2_segs[i]][i]

            # join the gametes to form the offspring chromosome
            single_chr = []
            for i in range(len(chr1_gamete)):
                offspring_gt = str(chr1_gamete[i]) + div_snp + str(chr2_gamete[i])
                single_chr.append(offspring_gt)

            offspring_chromosome[idx_chromosome] = single_chr

        output["chromosomes"] = offspring_chromosome
        output["crossover"] = offspring_crossover
        output["strand"] = offspring_strand

        return output

    def x_breed(self):
        """
        Simulate the x chromosome for the current individual by considering the x chromosomes of the parents.
        If the gender of the current individual is not defined yet, the sex is randomly assigned.
        """

        if self._parents and \
                self._parents[0].x_chromosome and self.parents[1].x_chromosome:  # we should consider the x chromosome

            msg = None
            if self._parents[0].gender == -1 or self._parents[0].gender == -1:
                msg = "Gender of the parents is unknown."
            elif self.parents[0].gender == self.parents[1].gender:
                msg = "Cannot generate x chromosome for the offspring as parents are of the same sex."

            if msg is not None:
                raise ValueError(msg)

            # determine gender if not already assigned
            if self._gender == -1:
                self._gender = random.choice([0, 1])

            if self._parents[0].gender == 0:  # first parent is the mother
                x_father = self._parents[1].x_chromosome
                x_mother = self._parents[0].x_chromosome
            else:  # first parent is the father
                x_father = self._parents[0].x_chromosome
                x_mother = self._parents[1].x_chromosome

            # generate x chromosome for the individual
            x = self.x_chromosome_reproduction(gender=self._gender, x_father=x_father, x_mother=x_mother)

            # store x chromosome, crossover points and strand selection
            self._x_chromosome = x["x_chromosome"]
            self._x_crossover = x["x_crossover"]
            self._x_strand = x["x_strand"]

    def breed(self, mate, n=1, offspring_gender=None, offspring_id=None):
        """
        Given a mate Individual, a new offspring Individual is created.

        :param Individual mate : The partner with whom the offspring is generated.
        :param int, optional n : The number of offsprings that will be generated.
        :param [int], optional offspring_gender : The gender for the offsprings to be generated.
        :param str or [str], optional offspring_id : The ID(s) of the offspring(s).

        :return: Individual : A single Individual if n=1 or a list of Individual for n>1
        """

        # verify consistency of the parameters
        n = lib.check_data("n", n, int, min_val=1)

        if n == 1:
            if type(offspring_id) is str:
                tmp_id = offspring_id
            else:
                tmp_id = None
            offspring = Individual(ind_id=tmp_id, parents=[self, mate])

            if offspring_gender is not None:
                offspring.set_gender(offspring_gender)
            offspring.x_breed()

            # add the offspring to the list of each parent
            self._offsprings.append(offspring)
            mate._offsprings.append(offspring)
        else:
            offspring = []
            for idx in range(n):
                if offspring_id is not None and type(offspring_id) is list:
                    tmp_id = offspring_id[idx]
                else:
                    tmp_id = None

                if offspring_gender is None:
                    tmp_gender = None
                else:
                    tmp_gender = offspring_gender[idx]

                offspring.append(self.breed(mate=mate, offspring_gender=tmp_gender, offspring_id=tmp_id))

        return offspring

    def haploidize(self, accepted=None) -> [int]:
        """
        Haploidize individual's SNPs. If the SNP contains values which are not present in the accepted list,
        the haploidization process will return a missing value, i.e. -1.

        :param: [str], optional accepted : The list of accepted values.

        :return: [int] The haploidized sequence.
        """

        if accepted is None:
            accepted = ["0", "1"]

        h = []  # haploidized output

        for chromosome in self._chromosomes:  # go through each chromosome
            for snp in chromosome:  # go through each SNP of the current chromosome

                # remove additional information which is not of interest here (if any)
                if "|" in snp:  # identify the separator character
                    div_snp = "|"
                elif "/" in snp:
                    div_snp = "/"
                else:
                    msg = "Unknown separator was found (snp = {}). Expected '|' or '/'".format(snp)
                    raise ValueError(msg)

                spl_snp = snp.split(div_snp)
                if spl_snp[0] in accepted:
                    r_snp = spl_snp[1].split(":")
                    if len(r_snp) == 2:
                        snp = spl_snp[0] + div_snp + r_snp[0]

                    # split the SNP and randomly select its value to haploidize it
                    spl_snp = snp.split(div_snp)

                    if spl_snp[1] in accepted:
                        sel = spl_snp[random.getrandbits(1)]
                    else:
                        sel = "-1"
                else:
                    sel = "-1"
                h.append(int(sel))

        return h

    def has_parents(self) -> bool:
        """
        Returns True if the Individual has parents.

        :return: bool : True if the Individual has parents.
        """

        has_parents = True
        if not self._parents:
            has_parents = False

        return has_parents

    def is_founder(self) -> bool:
        """
        Returns True if the current Individual is a founder.

        :return: bool : True if the Individual is a founder.
        """

        # the Individual is a founder if it has no parents
        return not(self.has_parents())

    def is_sibling(self, individual) -> bool:
        """
        Return True if the passed individual is a sibling, False otherwise.

        :param Individual individual : The individual to be verified as sibling.

        :return: bool : True if the individual is a sibling, False otherwise.
        """

        sibling = False
        if self.has_parents() and individual.has_parents():  # both individuals must have parents
            individual = lib.check_data("individual", individual, Individual)  # check correctness of the parameter
            parent_ids = [self._parents[0].id, self._parents[1].id]  # list of parent IDs

            # both parents are shared
            if individual.parents[0].id in parent_ids and individual.parents[1].id in parent_ids:
                sibling = True

        return sibling

    def is_parent(self, offspring) -> bool:
        """
        Return True if the passed individual is an offspring of the current instance, False otherwise.

        :param Individual offspring : The individual to be verified as offspring of the current instance.

        :return: bool : True if the given individual is an offspring of the current instance, False otherwise.
        """

        parent = False
        if offspring.has_parents() and (self._id == offspring.parents[0].id or self._id == offspring.parents[1].id):
            parent = True

        return parent

    def is_offspring(self, parent) -> bool:
        """
        Return True if the passed individual is a parent of the current instance, False otherwise.

        :param Individual parent : The individual to be verified as parent of the current instance.

        :return: bool : True if the given individual is a parent of the current instance, False otherwise.
        """

        offspring = False
        if self.has_parents() and (parent.id == self._parents[0].id or parent.id == self._parents[1].id):
            offspring = True

        return offspring
