__author__ = 'Umesh'
import os, sys
import json

class ControlCards:

    def __init__(self):
        """
            Consist of control cards
        :return:
        """
        self.baseDir = os.path.dirname(sys.argv[0])
        self.template_path = os.path.join(self.baseDir, "Template")
        self.control_cards_json_file = os.path.join(self.template_path, "control_cards.json")

        self.control_cards_type = []
        self.map_control_cards_type_title = {}

        self.define_json_file = os.path.join(self.template_path, "define_cards.json")
        self.define_cards_type = []
        self.map_define_cards_type_title = {}

        self.get_info()

    def get_info(self):
        """
        :return:
        """

        with open(self.control_cards_json_file) as readIn:
            self.control_cards = json.load(readIn)

        for key in self.control_cards.keys():
            self.control_cards_type.append(key)
            self.map_control_cards_type_title.update({self.control_cards[key]["Card_Title"][0]:key})

        with open(self.define_json_file) as readIn_define:
            self.define_cards = json.load(readIn_define)

        for key in self.define_cards.keys():
            self.define_cards_type.append(key)
            self.map_define_cards_type_title.update({self.define_cards[key]["Card_Title"][0]:key})


if __name__ == '__main__':

    control_cards = ControlCards()
