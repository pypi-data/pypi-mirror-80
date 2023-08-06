"""
Kinship simulation, Pedigree abstract class:
Define the main pedigree methods and structures upon which defining concrete pedigree implementations.
"""

__version__ = '2020.8'
__author__ = 'Team Neogene'

from abc import ABC, abstractmethod
from kinshipsim.individual import Individual
from kinshipsim import lib


class Pedigree(ABC):
    FEMALE = 0
    MALE = 1

    def __init__(self):
        super(Pedigree, self).__init__()

    @abstractmethod
    def get_pedigree_gender(self) -> [int]:
        """
        Return the gender list assigned to each individual of the pedigree.
        If the individual has a dynamic gender assignment (i.e., assigned at the time of instantiation of the pedigree),
        the gender value returned should be -1 (i.e., unknown). Otherwise, 0s (females) and 1s (males) are returned.

        :return: [int] The gender codes of the pedigree.
        """
        pass

    @abstractmethod
    def get_parents_ids(self) -> [[str, str]]:
        """
        Returns the IDs of the parents for each individual of the default pedigree.

        :return: [[str, str]] The list of parent IDs for each individual.
        """
        pass

    @abstractmethod
    def get_pedigree_ids(self) -> [str]:
        """
        Return the list IDs of the individuals of the pedigree.

        :return: [str] The IDs of the pedigree.
        """
        pass

    @abstractmethod
    def x_groups(self, n: int) -> dict:
        """
        Returns couples of IDs identifying the individuals in the pedigree having the n-th degree relationships.
        This method refers to relationships defined by the X chromosome, such as mother-son, mother-daughter,
        father-son, father-daughter, ...

        :param int n : The degree of the relation.

        :return: dict : A dictionary with the couples of IDs identifying the individuals in the population with the
        desired degree. Within the dictionary there may be distinct groups, based on the specificity of the relations.
        """

        pass

    @abstractmethod
    def aut_groups(self, n: int) -> dict:
        """
        Returns couples of IDs identifying the individuals in the pedigree having the desired relationship degree.
        The couples are also grouped according to the specificity of the relation (e.g., parent-offspring, siblings) for
        the autosome chromosomes. With n = -1 it should return unrelated couples.

        :param int n : The degree of the relation.

        :return: dict : A dictionary with the couples of IDs identifying the individuals in the population with the
        desired degree. Within the dictionary there may be distinct groups, based on the specificity of the relations.
        """

        pass

    @abstractmethod
    def get_pedigree(self, vcf_file: str, founder: [str]) -> [Individual]:
        """
        Given a list of founders and the source VCF file, generates a pedigree.
        The pedigree is returned as a list of Individual instances and can be explored by following
        the parents and offsprings attributes defined for each individual.

        :param str vcf_file : Input VCF file from which the founders are imported.
        :param [str] founder : The list of founders' ID to be loaded from the VCF file.

        :return: The pedigree as a list of Individual instances.
        """

        pass

    def get_x_chr_groups(self, n: int, population=None) -> dict:
        """
        Returns couples of IDs and optionally indices identifying the individuals in the population having the
        n-th degree relationships. This method refers to relationships defined by the X chromosome, such as
        mother-son, mother-daughter, father-son, father-daughter, ...

        :param int n : The degree of the relation.
        :param [Individual] or [str], optional population : The population defining the pedigree.
        If it is set to None, the IDs are returned, otherwise the indices from the population are also included.
        The population can also be represented by a list of strings as IDs of individuals.

        :return: dict : A dictionary with the couples of IDs (and optionally indices) identifying the individuals
        in the population with the desired degree. Within the dictionary there may be distinct groups, based on
        the specificity of the relations.
        """

        return Pedigree.match_idx(population, self.x_groups(n))

    def get_aut_chr_groups(self, n: int, population=None) -> dict:
        """
        Return couples of IDs and optionally indices identifying the individuals in the population having the desired
        relationship degree. The couples are also grouped according to the specificity of the relation
        (e.g., parent-offspring, siblings) for the autosome chromosomes. With n = -1 it should return unrelated couples.

        :param int n : The degree of the relation.
        :param [Individual] or [str], optional population : The population defining the pedigree.
        If it is set to None, the IDs are returned, otherwise the indices from the population.
        The population can also be represented by a list of strings defining the individuals' ID.

        :return: dict : A dictionary with the couples of IDs (and optionally indices) identifying the individuals
        in the population with the desired degree. Within the dictionary there are distinct groups, based on
        the specificity of the relations.
        """

        return Pedigree.match_idx(population, self.aut_groups(n))

    @staticmethod
    def match_idx(population: [Individual], in_groups: dict) -> dict:
        """
        It matches each individual ID found in the dictionary with the respective index of the given population.

        :param [Individual] population : The reference population.
        :param dict in_groups : The dictionary containing the relationships among individuals.

        :return: dict : An updated copy of the given dictionary which includes the indices.
        """

        if population is not None:  # if a population is given add also the indices associated with each ID
            out_groups = in_groups.copy()
            if type(population[0]) is not str:  # a list of Individual instances
                for key, value in out_groups.items():
                    value["idx"] = []
                    for ids in value["val"]:
                        ind1 = lib.get_individual(population, ids[0])
                        if ind1 is None:
                            msg = "Individual '{}' was not found.".format(ids[0])
                            raise ValueError(msg)
                        ind2 = lib.get_individual(population, ids[1])
                        if ind2 is None:
                            msg = "Individual '{}' was not found.".format(ids[1])
                            raise ValueError(msg)
                        value["idx"].append([str(lib.ind2index(ind1, population)),
                                             str(lib.ind2index(ind2, population))])
            else:  # a list of IDs
                for key, value in out_groups.items():
                    value["idx"] = []
                    for ids in value["val"]:
                        id1 = lib.id2index(ids[0], population)
                        if id1 == -1:
                            msg = "Individual '{}' was not found.".format(ids[0])
                            raise ValueError(msg)
                        id2 = lib.id2index(ids[1], population)
                        if id2 == -1:
                            msg = "Individual '{}' was not found.".format(ids[1])
                            raise ValueError(msg)
                        value["idx"].append([str(id1), str(id2)])
        else:
            out_groups = in_groups

        return out_groups
