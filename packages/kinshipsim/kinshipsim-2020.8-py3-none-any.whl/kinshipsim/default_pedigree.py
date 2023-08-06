"""
Kinship simulation, Default Pedigree class:
Define the pedigree structure together with indices and labels of interest.
"""

__version__ = '2020.8'
__author__ = 'Team Neogene'

from kinshipsim.individual import Individual
from kinshipsim.pedigree import Pedigree
from kinshipsim import lib


class DefaultPedigree(Pedigree):

    ids = ["Founder1", "Founder2", "Founder3", "Founder4", "Founder5", "Founder6", "Founder7", "Founder8",
           "Offspring1", "Offspring2", "Offspring3", "Offspring4", "Offspring5", "Offspring6", "Offspring7",
           "Offspring8", "Offspring9", "Offspring10", "Offspring11", "Offspring12", "Offspring13", "Offspring14",
           "Offspring15", "Offspring16", "Offspring17"]
    gender = [1, 0, 0, 1, 0, 1, 0, 1, 1, 0, -1, 0, 1, 0, 1, -1, 0, 0, 1, 0, 1, 0, 1, 1, -1]
    parents_ids = [[None, None], [None, None], [None, None], [None, None], [None, None], [None, None], [None, None],
                   [None, None], ["Founder1", "Founder2"], ["Founder1", "Founder2"], ["Offspring1", "Offspring2"],
                   ["Founder3", "Offspring1"], ["Founder3", "Offspring1"], ["Founder4", "Offspring2"],
                   ["Founder4", "Offspring2"], ["Offspring5", "Offspring6"], ["Founder5", "Founder6"],
                   ["Founder5", "Founder6"], ["Founder6", "Offspring4"], ["Founder6", "Offspring4"],
                   ["Founder7", "Offspring7"], ["Founder7", "Offspring7"], ["Founder7", "Founder8"],
                   ["Founder7", "Founder8"], ["Offspring12", "Offspring13"]]
    x_chr_1st_group_01 = {"txt": "Mother-Daughter",
                          "val": [["Founder2", "Offspring2"], ["Founder3", "Offspring4"],
                                  ["Founder5", "Offspring9"], ["Founder5", "Offspring10"],
                                  ["Founder7", "Offspring14"], ["Offspring2", "Offspring6"],
                                  ["Offspring4", "Offspring12"]]
                          }
    x_chr_1st_group_02 = {"txt": "Mother-Son",
                          "val": [["Founder2", "Offspring1"], ["Founder3", "Offspring5"],
                                  ["Founder7", "Offspring13"], ["Founder7", "Offspring15"],
                                  ["Founder7", "Offspring16"], ["Offspring2", "Offspring7"],
                                  ["Offspring4", "Offspring11"]]
                          }
    x_chr_1st_group_03 = {"txt": "Father-Daughter",
                          "val": [["Founder1", "Offspring2"], ["Founder4", "Offspring6"],
                                  ["Founder6", "Offspring9"], ["Founder6", "Offspring10"],
                                  ["Founder6", "Offspring12"], ["Offspring1", "Offspring4"],
                                  ["Offspring7", "Offspring14"]]
                          }
    x_chr_1st_group_04 = {"txt": "Father-Son",
                          "val": [["Founder1", "Offspring1"], ["Founder4", "Offspring7"],
                                  ["Founder6", "Offspring11"], ["Founder8", "Offspring15"],
                                  ["Founder8", "Offspring16"], ["Offspring1", "Offspring5"],
                                  ["Offspring7", "Offspring13"]]
                          }
    x_chr_1st_group_05 = {"txt": "Sisters",
                          "val": [["Offspring9", "Offspring10"]]
                          }
    x_chr_1st_group_06 = {"txt": "Brothers",
                          "val": [["Offspring15", "Offspring16"]]
                          }
    x_chr_1st_group_07 = {"txt": "Sister-Brother",
                          "val": [["Offspring1", "Offspring2"], ["Offspring4", "Offspring5"],
                                  ["Offspring6", "Offspring7"], ["Offspring11", "Offspring12"],
                                  ["Offspring13", "Offspring14"]]
                          }
    x_chr_2nd_group_01 = {"txt": "Half-Brothers",
                          "val": [["Offspring13", "Offspring15"], ["Offspring13", "Offspring16"]]
                          }
    x_chr_2nd_group_02 = {"txt": "Uncle-Nephew",
                          "val": [["Offspring1", "Offspring7"]]
                          }
    chr_1st_group_01 = {"txt": "Parent-Offspring",
                        "val": [["Founder1", "Offspring1"], ["Founder1", "Offspring2"],
                                ["Founder2", "Offspring1"], ["Founder2", "Offspring2"],
                                ["Founder3", "Offspring4"], ["Founder3", "Offspring5"],
                                ["Founder4", "Offspring6"], ["Founder4", "Offspring7"],
                                ["Founder5", "Offspring9"], ["Founder5", "Offspring10"],
                                ["Founder6", "Offspring9"], ["Founder6", "Offspring10"],
                                ["Founder6", "Offspring11"], ["Founder6", "Offspring12"],
                                ["Founder7", "Offspring13"], ["Founder7", "Offspring14"],
                                ["Founder7", "Offspring15"], ["Founder7", "Offspring16"],
                                ["Founder8", "Offspring15"], ["Founder8", "Offspring16"],
                                ["Offspring1", "Offspring4"], ["Offspring1", "Offspring5"],
                                ["Offspring2", "Offspring6"], ["Offspring2", "Offspring7"],
                                ["Offspring4", "Offspring11"], ["Offspring4", "Offspring12"],
                                ["Offspring7", "Offspring13"], ["Offspring7", "Offspring14"]]
                        }
    chr_1st_group_02 = {"txt": "Siblings",
                        "val": [["Offspring1", "Offspring2"], ["Offspring4", "Offspring5"],
                                ["Offspring6", "Offspring7"], ["Offspring9", "Offspring10"],
                                ["Offspring11", "Offspring12"], ["Offspring13", "Offspring14"],
                                ["Offspring15", "Offspring16"]]
                        }
    chr_1st_group_03 = {"txt": "Parent-Offspring (1st degree inbred, siblings inbreeding)",
                        "val": [["Offspring1", "Offspring3"], ["Offspring2", "Offspring3"]]
                        }
    chr_1st_group_04 = {"txt": "Parent-Offspring (1st cousins inbreeding, 3rd degree inbred)",
                        "val": [["Offspring5", "Offspring8"], ["Offspring6", "Offspring8"]]
                        }
    chr_1st_group_05 = {"txt": "Parent-Offspring (2nd cousins inbreeding, 5th degree inbred)",
                        "val": [["Offspring12", "Offspring17"],
                                ["Offspring13", "Offspring17"]]
                        }
    chr_2nd_group_01 = {"txt": "Grandparent-Grandchild",
                        "val": [["Founder1", "Offspring4"], ["Founder1", "Offspring5"],
                                ["Founder1", "Offspring6"], ["Founder1", "Offspring7"],
                                ["Founder2", "Offspring4"], ["Founder2", "Offspring5"],
                                ["Founder2", "Offspring6"], ["Founder2", "Offspring7"],
                                ["Founder3", "Offspring11"], ["Founder3", "Offspring12"],
                                ["Founder4", "Offspring13"], ["Founder4", "Offspring14"],
                                ["Offspring1", "Offspring11"], ["Offspring1", "Offspring12"],
                                ["Offspring2", "Offspring13"], ["Offspring2", "Offspring14"]]
                        }
    chr_2nd_group_02 = {"txt": "Grandparent-Grandchild (1st degree inbred, siblings inbreeding)",
                        "val": [["Founder1", "Offspring3"],
                                ["Founder2", "Offspring3"]]
                        }
    chr_2nd_group_03 = {"txt": "Grandparent-Grandchild (3rd degree, 1st cousins inbreeding)",
                        "val": [["Founder3", "Offspring8"], ["Founder4", "Offspring8"],
                                ["Offspring1", "Offspring8"], ["Offspring2", "Offspring8"]]
                        }
    chr_2nd_group_04 = {"txt": "Grandparent-Grandchild (5th degree relatives, 2nd cousins inbreeding)",
                        "val": [["Founder6", "Offspring17"], ["Founder7", "Offspring17"],
                                ["Offspring4", "Offspring17"], ["Offspring7", "Offspring17"]]
                        }
    chr_2nd_group_05 = {"txt": "Aunt|Uncle-Niece|Nephew",
                        "val": [["Offspring1", "Offspring6"], ["Offspring1", "Offspring7"],
                                ["Offspring2", "Offspring4"], ["Offspring2", "Offspring5"],
                                ["Offspring5", "Offspring11"], ["Offspring5", "Offspring12"],
                                ["Offspring6", "Offspring13"], ["Offspring6", "Offspring14"]]
                        }
    chr_2nd_group_06 = {"txt": "Aunt|Uncle-Niece|Nephew (1st cousins inbreeding, 3rd degree inbred)",
                        "val": [["Offspring4", "Offspring8"], ["Offspring7", "Offspring8"]]
                        }
    chr_2nd_group_07 = {"txt": "Aunt|Uncle-Niece|Nephew (2nd cousins inbreeding, 5th degree inbred)",
                        "val": [["Offspring11", "Offspring17"], ["Offspring14", "Offspring17"]]
                        }
    chr_2nd_group_08 = {"txt": "Half-sibling",
                        "val": [["Offspring9", "Offspring11"], ["Offspring9", "Offspring12"],
                                ["Offspring10", "Offspring11"], ["Offspring10", "Offspring12"],
                                ["Offspring13", "Offspring15"], ["Offspring13", "Offspring16"],
                                ["Offspring14", "Offspring15"], ["Offspring14", "Offspring16"]]
                        }
    chr_2nd_group_09 = {"txt": "Half-sibling (1st degree inbred)",
                        "val": [["Offspring3", "Offspring4"], ["Offspring3", "Offspring5"],
                                ["Offspring3", "Offspring6"], ["Offspring3", "Offspring7"]]
                        }
    chr_3rd_group_01 = {"txt": "Great Grandparent-Great Grandchild",
                        "val": [["Founder1", "Offspring11"], ["Founder1", "Offspring12"],
                                ["Founder1", "Offspring13"], ["Founder1", "Offspring14"],
                                ["Founder2", "Offspring11"], ["Founder2", "Offspring12"],
                                ["Founder2", "Offspring13"], ["Founder2", "Offspring14"]]
                        }
    chr_3rd_group_02 = {"txt": "Great Grandparent-Great Grandchild (1st cousins inbreeding, 3rd degree inbred)",
                        "val": [["Founder1", "Offspring8"], ["Founder2", "Offspring8"]]
                        }
    chr_3rd_group_03 = {"txt": "Great Grandparent-Great Grandchild (2nd cousins inbreeding, 5th degree inbred)",
                        "val": [["Founder3", "Offspring17"], ["Founder4", "Offspring17"],
                                ["Offspring1", "Offspring17"], ["Offspring2", "Offspring17"]]
                        }
    chr_3rd_group_04 = {"txt": "Great Aunt|Great Uncle-Grandniece|Grandnephew",
                        "val": [["Offspring1", "Offspring13"], ["Offspring1", "Offspring14"],
                                ["Offspring2", "Offspring11"], ["Offspring2", "Offspring12"]]
                        }
    chr_3rd_group_05 = {"txt": "Great Aunt|Great Uncle-Grandniece|Grandnephew (2nd cousins inbreeding, 5th degree "
                               "inbred, Group 05)",
                        "val": [["Founder3", "Offspring17"], ["Founder4", "Offspring17"],
                                ["Offspring1", "Offspring17"], ["Offspring2", "Offspring17"]]
                        }
    chr_3rd_group_06 = {"txt": "Half-aunt|Half-uncle-Half-",
                        "val": [["Offspring3", "Offspring11"], ["Offspring3", "Offspring12"],
                                ["Offspring3", "Offspring13"], ["Offspring3", "Offspring14"]]
                        }

    chr_3rd_group_07 = {"txt": "Half-aunt|Half-uncle-Half-inbred",
                        "val": [["Offspring3", "Offspring8"]]
                        }
    chr_3rd_group_08 = {"txt": "First Cousins",
                        "val": [["Offspring4", "Offspring6"], ["Offspring4", "Offspring7"],
                                ["Offspring5", "Offspring6"], ["Offspring5", "Offspring7"]]
                        }
    chr_3rd_group_09 = {"txt": "Great Aunt|Great Uncle-Grandniece|Grandnephew (2nd cousins inbreeding, 5th degree "
                               "inbred, Group 09)",
                        "val": [["Offspring5", "Offspring17"], ["Offspring6", "Offspring17"]]
                        }
    chr_3rd_group_10 = {"txt": "First Cousins (2nd cousins inbreeding, 5th degree inbred)",
                        "val": [["Offspring8", "Offspring11"], ["Offspring8", "Offspring12"],
                                ["Offspring8", "Offspring13"], ["Offspring8", "Offspring14"]]
                        }
    chr_unr_group_01 = {"txt": "Unrelated",
                        "val": [["Founder1", "Founder2"], ["Founder1", "Founder3"], ["Founder1", "Founder4"],
                                ["Founder1", "Founder5"], ["Founder1", "Founder6"], ["Founder1", "Founder7"],
                                ["Founder1", "Founder8"], ["Founder1", "Offspring9"], ["Founder1", "Offspring10"],
                                ["Founder1", "Offspring15"], ["Founder1", "Offspring16"], ["Founder2", "Founder3"],
                                ["Founder2", "Founder4"], ["Founder2", "Founder5"], ["Founder2", "Founder6"],
                                ["Founder2", "Founder7"], ["Founder2", "Founder8"], ["Founder2", "Offspring9"],
                                ["Founder2", "Offspring10"], ["Founder2", "Offspring15"], ["Founder2", "Offspring16"],
                                ["Founder3", "Founder4"], ["Founder3", "Founder5"], ["Founder3", "Founder6"],
                                ["Founder3", "Founder7"], ["Founder3", "Founder8"], ["Founder3", "Offspring1"],
                                ["Founder3", "Offspring2"], ["Founder3", "Offspring3"], ["Founder3", "Offspring6"],
                                ["Founder3", "Offspring7"], ["Founder3", "Offspring9"], ["Founder3", "Offspring10"],
                                ["Founder3", "Offspring13"], ["Founder3", "Offspring14"], ["Founder3", "Offspring15"],
                                ["Founder3", "Offspring16"], ["Founder4", "Founder5"], ["Founder4", "Founder6"],
                                ["Founder4", "Founder7"], ["Founder4", "Founder8"], ["Founder4", "Offspring1"],
                                ["Founder4", "Offspring2"], ["Founder4", "Offspring3"], ["Founder4", "Offspring4"],
                                ["Founder4", "Offspring5"], ["Founder4", "Offspring9"], ["Founder4", "Offspring10"],
                                ["Founder4", "Offspring11"], ["Founder4", "Offspring12"], ["Founder4", "Offspring15"],
                                ["Founder4", "Offspring16"], ["Founder5", "Founder6"], ["Founder5", "Founder7"],
                                ["Founder5", "Founder8"], ["Founder5", "Offspring1"], ["Founder5", "Offspring2"],
                                ["Founder5", "Offspring3"], ["Founder5", "Offspring4"], ["Founder5", "Offspring5"],
                                ["Founder5", "Offspring6"], ["Founder5", "Offspring7"], ["Founder5", "Offspring8"],
                                ["Founder5", "Offspring11"], ["Founder5", "Offspring12"], ["Founder5", "Offspring13"],
                                ["Founder5", "Offspring14"], ["Founder5", "Offspring15"], ["Founder5", "Offspring16"],
                                ["Founder5", "Offspring17"], ["Founder6", "Founder7"], ["Founder6", "Founder8"],
                                ["Founder6", "Offspring1"], ["Founder6", "Offspring2"], ["Founder6", "Offspring3"],
                                ["Founder6", "Offspring4"], ["Founder6", "Offspring5"], ["Founder6", "Offspring6"],
                                ["Founder6", "Offspring7"], ["Founder6", "Offspring8"], ["Founder6", "Offspring13"],
                                ["Founder6", "Offspring14"], ["Founder6", "Offspring15"], ["Founder6", "Offspring16"],
                                ["Founder7", "Founder8"], ["Founder7", "Offspring1"], ["Founder7", "Offspring2"],
                                ["Founder7", "Offspring3"], ["Founder7", "Offspring4"], ["Founder7", "Offspring5"],
                                ["Founder7", "Offspring6"], ["Founder7", "Offspring7"], ["Founder7", "Offspring8"],
                                ["Founder7", "Offspring9"], ["Founder7", "Offspring10"], ["Founder7", "Offspring11"],
                                ["Founder7", "Offspring12"], ["Founder8", "Offspring1"], ["Founder8", "Offspring2"],
                                ["Founder8", "Offspring3"], ["Founder8", "Offspring4"], ["Founder8", "Offspring5"],
                                ["Founder8", "Offspring6"], ["Founder8", "Offspring7"], ["Founder8", "Offspring8"],
                                ["Founder8", "Offspring9"], ["Founder8", "Offspring10"], ["Founder8", "Offspring11"],
                                ["Founder8", "Offspring12"], ["Founder8", "Offspring13"], ["Founder8", "Offspring14"],
                                ["Founder8", "Offspring17"], ["Offspring1", "Offspring9"],
                                ["Offspring1", "Offspring10"], ["Offspring1", "Offspring15"],
                                ["Offspring1", "Offspring16"], ["Offspring2", "Offspring9"],
                                ["Offspring2", "Offspring10"], ["Offspring2", "Offspring15"],
                                ["Offspring2", "Offspring16"], ["Offspring3", "Offspring9"],
                                ["Offspring3", "Offspring10"], ["Offspring3", "Offspring15"],
                                ["Offspring3", "Offspring16"], ["Offspring4", "Offspring9"],
                                ["Offspring4", "Offspring10"], ["Offspring4", "Offspring15"],
                                ["Offspring4", "Offspring16"], ["Offspring5", "Offspring9"],
                                ["Offspring5", "Offspring10"], ["Offspring5", "Offspring15"],
                                ["Offspring5", "Offspring16"], ["Offspring6", "Offspring9"],
                                ["Offspring6", "Offspring10"], ["Offspring6", "Offspring15"],
                                ["Offspring6", "Offspring16"], ["Offspring7", "Offspring9"],
                                ["Offspring7", "Offspring10"], ["Offspring7", "Offspring15"],
                                ["Offspring7", "Offspring16"], ["Offspring8", "Offspring9"],
                                ["Offspring8", "Offspring10"], ["Offspring8", "Offspring15"],
                                ["Offspring8", "Offspring16"], ["Offspring9", "Offspring13"],
                                ["Offspring9", "Offspring14"], ["Offspring9", "Offspring15"],
                                ["Offspring9", "Offspring16"], ["Offspring10", "Offspring13"],
                                ["Offspring10", "Offspring14"], ["Offspring10", "Offspring15"],
                                ["Offspring10", "Offspring16"], ["Offspring11", "Offspring15"],
                                ["Offspring11", "Offspring16"], ["Offspring12", "Offspring15"],
                                ["Offspring12", "Offspring16"]]
                        }

    def get_pedigree_gender(self) -> [int]:
        """
        Return the gender assigned to each individual in the pedigree.
        If the individual has a dynamic gender assignment (i.e., assigned at the time of instantiation of the pedigree),
        the gender value returned is -1 (i.e., unknown). Otherwise, 0s (females) and 1s (males) are returned.

        :return: [int] The gender codes of the pedigree.
        """

        return self.gender

    def get_parents_ids(self) -> [[str, str]]:
        """
        Returns the IDs of the parents for each individual of the default pedigree.

        :return: [[str, str]] The list of parent IDs for each individual.
        """

        return self.parents_ids

    def get_pedigree_ids(self) -> [str]:
        """
        Return the list of individual IDs for the standard pedigree.

        :return: [str] The IDs of the pedigree.
        """

        return self.ids

    def get_pedigree(self, vcf_file: str, founder: [str]) -> [Individual]:
        """
        Given a list of 8 founders and the source VCF file, generates a 'four-generations' pedigree.
        The pedigree is returned as a list of Individual instances and can be explored by following
        the parents and offsprings attributes defined for each individual.

        :param str vcf_file : Input VCF file from which the founders are imported.
        :param [str] founder : The list of founders' ID to be loaded from the VCF file.

        :return: The pedigree as a list of Individual instances.
        """

        # First add all the founders to the list:
        #
        pedigree = [Individual(ind_id=self.ids[0], chromosomes=lib.extract_chromosomes(vcf_file, founder[0])),
                    Individual(ind_id=self.ids[1], chromosomes=lib.extract_chromosomes(vcf_file, founder[1])),
                    Individual(ind_id=self.ids[2], chromosomes=lib.extract_chromosomes(vcf_file, founder[2])),
                    Individual(ind_id=self.ids[3], chromosomes=lib.extract_chromosomes(vcf_file, founder[3])),
                    Individual(ind_id=self.ids[4], chromosomes=lib.extract_chromosomes(vcf_file, founder[4])),
                    Individual(ind_id=self.ids[5], chromosomes=lib.extract_chromosomes(vcf_file, founder[5])),
                    Individual(ind_id=self.ids[6], chromosomes=lib.extract_chromosomes(vcf_file, founder[6])),
                    Individual(ind_id=self.ids[7], chromosomes=lib.extract_chromosomes(vcf_file, founder[7]))]

        # Start generating the pedigree by breeding the founders and later on other offsprings:
        #
        pedigree = pedigree + lib.get_individual(pedigree, self.ids[0]).breed(
            mate=lib.get_individual(pedigree, self.ids[1]),
            n=2, offspring_id=[self.ids[8], self.ids[9]])

        pedigree = pedigree + [lib.get_individual(pedigree, self.ids[8]).breed(
            mate=lib.get_individual(pedigree, self.ids[9]),
            offspring_id=self.ids[10])]

        pedigree = pedigree + lib.get_individual(pedigree, self.ids[2]).breed(
            mate=lib.get_individual(pedigree, self.ids[8]),
            n=2, offspring_id=[self.ids[11], self.ids[12]])

        pedigree = pedigree + lib.get_individual(pedigree, self.ids[3]).breed(
            mate=lib.get_individual(pedigree, self.ids[9]),
            n=2, offspring_id=[self.ids[13], self.ids[14]])

        pedigree = pedigree + [lib.get_individual(pedigree, self.ids[12]).breed(
            mate=lib.get_individual(pedigree, self.ids[13]),
            offspring_id=self.ids[15])]

        pedigree = pedigree + lib.get_individual(pedigree, self.ids[4]).breed(
            mate=lib.get_individual(pedigree, self.ids[5]),
            n=2, offspring_id=[self.ids[16], self.ids[17]])

        pedigree = pedigree + lib.get_individual(pedigree, self.ids[5]).breed(
            mate=lib.get_individual(pedigree, self.ids[11]),
            n=2, offspring_id=[self.ids[18], self.ids[19]])

        pedigree = pedigree + lib.get_individual(pedigree, self.ids[6]).breed(
            mate=lib.get_individual(pedigree, self.ids[14]),
            n=2, offspring_id=[self.ids[20], self.ids[21]])

        pedigree = pedigree + lib.get_individual(pedigree, self.ids[6]).breed(
            mate=lib.get_individual(pedigree, self.ids[7]),
            n=2, offspring_id=[self.ids[22], self.ids[23]])

        pedigree = pedigree + [lib.get_individual(pedigree, self.ids[19]).breed(
            mate=lib.get_individual(pedigree, self.ids[20]),
            offspring_id=self.ids[24])]

        return pedigree

    def x_groups(self, n: int) -> dict:
        """
        Returns couples of IDs identifying the individuals in the pedigree having the desired relationship.
        This method refers to relationships defined by the X chromosome, such as mother-son, mother-daughter,
        father-son, father-daughter, ...

        :param int n : The degree of the relation.

        :return: dict : A dictionary with the couples of IDs identifying the individuals in the pedigree with the
        desired degree. Within the dictionary there are distinct groups, based on the specificity of the relations.
        """

        if n == 1:
            groups = {"group_01": self.x_chr_1st_group_01, "group_02": self.x_chr_1st_group_02,
                      "group_03": self.x_chr_1st_group_03, "group_04": self.x_chr_1st_group_04,
                      "group_05": self.x_chr_1st_group_05, "group_06": self.x_chr_1st_group_06,
                      "group_07": self.x_chr_1st_group_07}
        elif n == 2:
            groups = {"group_01": self.x_chr_2nd_group_01,
                      "group_02": self.x_chr_2nd_group_02
                      }
        else:  # unknown n-th degree relationships
            groups = {}

        return self.__get_indices(groups)

    def aut_groups(self, n: int) -> dict:
        """
        Return couples of IDs identifying the individuals in the pedigree having the desired relationship degree.
        The couples are also grouped according to the specificity of the relation (e.g., parent-offspring, siblings).

        :param int n : The degree of the relation.

        :return: dict : A dictionary with the couples of IDs identifying the individuals in the pedigree with the
        desired degree. Within the dictionary there are distinct groups, based on the specificity of the relations.
        """

        if n == 1:  # first degree relationships
            groups = {"group_01": self.chr_1st_group_01,
                      "group_02": self.chr_1st_group_02,
                      "group_03": self.chr_1st_group_03,
                      "group_04": self.chr_1st_group_04,
                      "group_05": self.chr_1st_group_05
                      }
        elif n == 2:  # second degree relationships
            groups = {"group_01": self.chr_2nd_group_01,
                      "group_02": self.chr_2nd_group_02,
                      "group_03": self.chr_2nd_group_03,
                      "group_04": self.chr_2nd_group_04,
                      "group_05": self.chr_2nd_group_05,
                      "group_06": self.chr_2nd_group_06,
                      "group_07": self.chr_2nd_group_07,
                      "group_08": self.chr_2nd_group_08,
                      "group_09": self.chr_2nd_group_09
                      }
        elif n == 3:  # third degree relationships
            groups = {"group_01": self.chr_3rd_group_01,
                      "group_02": self.chr_3rd_group_02,
                      "group_03": self.chr_3rd_group_03,
                      "group_04": self.chr_3rd_group_04,
                      "group_05": self.chr_3rd_group_05,
                      "group_06": self.chr_3rd_group_06,
                      "group_07": self.chr_3rd_group_07,
                      "group_08": self.chr_3rd_group_08,
                      "group_09": self.chr_3rd_group_09,
                      "group_10": self.chr_3rd_group_10
                      }
        elif n == -1:  # unrelated couples
            groups = {"group_01": self.chr_unr_group_01
                      }
        else:  # unknown n-th degree relationships
            groups = {}

        return self.__get_indices(groups)

    def __get_indices(self, groups: dict) -> dict:
        """
        Update the dictionary with the indices of each id.

        :param dict groups : The dictionary containing the couples of IDs.

        :return: dict : The dictionary updated with the indices of all IDs.
        """

        for key, value in groups.items():
            value["idx"] = []
            for ids in value["val"]:
                id1 = lib.id2index(ids[0], self.ids)
                if id1 == -1:
                    msg = "Individual '{}' was not found.".format(ids[0])
                    raise ValueError(msg)
                id2 = lib.id2index(ids[1], self.ids)
                if id2 == -1:
                    msg = "Individual '{}' was not found.".format(ids[1])
                    raise ValueError(msg)
                value["idx"].append([str(id1), str(id2)])

        return groups