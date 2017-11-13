__author__ = 'Umesh'

import os, sys
import json

class MaterialCards:

    def __init__(self):
        """
            It contains various material cards
        :return:
        """
        self.baseDir = os.path.dirname(sys.argv[0])
        self.template_path = os.path.join(self.baseDir, "Template")
        self.json_file = os.path.join(self.template_path, "material_cards.json")
        self.sectionCards_json = os.path.join(self.template_path, "section_cards.json")
        self.eosCards_json = os.path.join(self.template_path, "eos_cards.json")

        self.material_cards_type = []
        self.map_material_cards_type_title = {}

        self.section_cards_type = []
        self.map_section_cards_type_title = {}

        self.eos_cards_type = []
        self.map_eos_cards_type_title = {}

        self.get_info()

    def get_info(self):
        """

        :return:
        """
        # Material Cards
        with open(self.json_file) as readIn:
            self.material_cards = json.load(readIn)

        for key in self.material_cards.keys():
            self.material_cards_type.append(key)
            self.map_material_cards_type_title.update({self.material_cards[key]["Card_Title"][0]:key})

        # Section Cards
        with open(self.sectionCards_json) as readIn:
            self.section_cards = json.load(readIn)

        for key in self.section_cards.keys():
            self.section_cards_type.append(key)
            self.map_section_cards_type_title.update({self.section_cards[key]["Card_Title"][0]:key})

        # EOS Cards
        with open(self.eosCards_json) as readIn:
            self.eos_cards = json.load(readIn)

        for key in self.eos_cards.keys():
            self.eos_cards_type.append(key)
            self.map_eos_cards_type_title.update({self.eos_cards[key]["Card_Title"][0]:key})

if __name__ == '__main__':

    material_card = MaterialCards()
    print(material_card.material_cards_type)