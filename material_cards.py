__author__ = 'Umesh'

import os, sys
import json

class MaterialCards:

    def __init__(self):
        """
            It contains various material cards
        :return:
        """
        self.material_cards_read = {}
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
            self.material_cards_jsonObj = json.load(readIn)

        for key in self.material_cards_jsonObj.keys():
            self.material_cards_type.append(key)
            self.map_material_cards_type_title.update({self.material_cards_jsonObj[key]["Card_Title"][0]:key})

        # Section Cards
        with open(self.sectionCards_json) as readIn:
            self.section_cards_jsonObj = json.load(readIn)

        for key in self.section_cards_jsonObj.keys():
            self.section_cards_type.append(key)
            self.map_section_cards_type_title.update({self.section_cards_jsonObj[key]["Card_Title"][0]:key})

        # EOS Cards
        with open(self.eosCards_json) as readIn:
            self.eos_cards_jsonObj = json.load(readIn)

        for key in self.eos_cards_jsonObj.keys():
            self.eos_cards_type.append(key)
            self.map_eos_cards_type_title.update({self.eos_cards_jsonObj[key]["Card_Title"][0]:key})

    def read_mat_file(self):
        """
            Reading material file and collecting all cards in the file
        :return:
        """

        # self.read_mat_file = filedialog.askopenfilename(initialdir=r"D:\Umesh\AxiomProject\VEOL_GUI\Rakesh_Project\Test1")
        self.read_mat_file_path = r""
        self.read_mat_file_in = os.path.join(os.path.split(self.read_mat_file_path)[0], "mat.k")
        self.read_mat_file_out = os.path.join(os.path.split(self.read_mat_file_path)[0], "mat_edit.k")
        with open(self.read_mat_file_out, 'w') as outFile:
            outFile.write("")
        with open(self.read_mat_file_in, 'r') as readFile:
            inlines = readFile.readlines()

        card_title_list = []
        section_card_title_list = []
        count = 0
        self.read_material_cards_type_list = []
        self.read_material_parameters = {}
        self.read_material_parameters_tmp = []

        self.read_section_cards_type_list = []
        self.read_section_parameters = {}
        self.read_section_parameters_tmp = []

        inSectionBlock = False
        inMatBlock = False
        print(self.map_material_cards_type_title)
        print(self.map_section_cards_type_title)
        for line in inlines:
            if line.startswith("*"):
                if line.startswith("*SECTION"):
                    inSectionBlock = True
                    inMatBlock = False
                    section_card_title = line.strip()
                    section_card_title_list.append(section_card_title)
                    count = 1
                    if not self.read_section_parameters_tmp == []:
                        self.read_section_parameters.update({section_tmp_line:self.read_section_parameters_tmp})
                        self.read_section_parameters_tmp = []
                    continue

                if line.startswith("*MAT"):
                    inSectionBlock = False
                    inMatBlock = True
                    card_title = line.strip()
                    card_title_list.append(card_title)
                    count = 1
                    if card_title == "*MAT_ENHANCED_COMPOSITE_DAMAGE":
                        if not self.read_material_parameters_tmp == []:
                            self.read_material_parameters.update({tmp_line:self.read_material_parameters_tmp})
                            self.read_material_parameters_tmp = []
                    else:
                        if not self.read_material_parameters_tmp == []:
                            self.read_material_parameters.update({tmp_line:self.read_material_parameters_tmp})
                            self.read_material_parameters_tmp = []
                    continue

            if inSectionBlock:
                print(line)
                if line.startswith("$"):
                    continue
                if count == 1:
                    section_id = int(line[:10].strip())
                    print(section_card_title, str(self.map_section_cards_type_title[section_card_title]))
                    section_tmp_line = ",".join([str(self.map_section_cards_type_title[section_card_title]), str(section_id)])
                    self.read_section_cards_type_list.append(section_tmp_line)
                list1 = re.findall('.{%d}'%10, line)
                if len(list1) < 9:
                    self.read_section_parameters_tmp.extend(list1)
                else:
                    list1.pop()
                    self.read_section_parameters_tmp.extend(list1)
                count += 1
                continue

            if inMatBlock:
                if line.startswith("$"):
                    continue
                if count == 1:
                    mat_id = int(line[:10].strip())
                    if not card_title == "*MAT_ENHANCED_COMPOSITE_DAMAGE":
                        matType = str(self.map_material_cards_type_title[card_title])
                        tmp_line = ",".join([str(self.map_material_cards_type_title[card_title]), str(mat_id)])
                        self.read_material_cards_type_list.append(tmp_line)

                if count == 6:
                    crit_fail = int(float(line[51:60].strip()))
                    if crit_fail == 54:
                        matType = "MAT_54"
                        tmp_line = ",".join([matType, str(mat_id)])
                        self.read_material_cards_type_list.append(tmp_line)
                    else:
                        matType = "MAT_55"
                        tmp_line = ",".join([matType, str(mat_id)])
                        self.read_material_cards_type_list.append(tmp_line)

                list1 = re.findall('.{%d}'%10, line)
                if len(list1) < 9:
                    self.read_material_parameters_tmp.extend(list1)
                else:
                    list1.pop()
                    self.read_material_parameters_tmp.extend(list1)
                count += 1

        self.read_material_parameters.update({self.read_material_cards_type_list[-1]:self.read_material_parameters_tmp})
        self.read_section_parameters.update({self.read_section_cards_type_list[-1]:self.read_section_parameters_tmp})
        # print(self.read_material_cards_type_list)
        # self.rowN += 3
        self.read_material_card = self.read_material_cards_type_list[0]
        # self.read_material_card_set = StringVar(self.frame)
        # popupMenu = OptionMenu(self.frame, self.read_material_card_set, *self.read_material_cards_type_list, command=self.get_read_material_type)
        # popupMenu.grid(row = self.rowN, column=1)
        # self.read_material_card_set.set(self.read_material_cards_type_list[0])
        # self.read_material_card_set.trace('w', self.read_material_dropdown)
        # self.editMatData = self.createButton(self.frame, "Show", self.show_material, self.rowN, 2, sticky_=W)

        # self.rowN += 3
        self.read_section_card = self.read_section_cards_type_list[0]
        # self.read_section_card_set = StringVar(self.frame)
        # popupMenu = OptionMenu(self.frame, self.read_section_card_set, *self.read_section_cards_type_list, command=self.get_read_section_type)
        # popupMenu.grid(row = self.rowN, column=1)
        # self.read_section_card_set.set(self.read_section_card)
        # self.read_section_card_set.trace('w', self.read_section_dropdown)
        # self.editSectionData = self.createButton(self.frame, "Show", self.show_section, self.rowN, 2, sticky_=W)



if __name__ == '__main__':

    material_card = MaterialCards()
    print(material_card.material_cards_type)