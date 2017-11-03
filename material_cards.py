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

        self.get_info()

    def get_info(self):
        """

        :return:
        """
        with open(self.json_file) as readIn:
            self.material_cards = json.load(readIn)

        self.material_cards_type = []
        self.map_material_cards_type_title = {}
        for key in self.material_cards.keys():
            self.material_cards_type.append(key)
            self.map_material_cards_type_title.update({self.material_cards[key]["Card_Title"][0]:key})

if __name__ == '__main__':

    material_card = MaterialCards()
    print(material_card.material_cards_type)