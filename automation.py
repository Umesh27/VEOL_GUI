__author__ = 'Umesh'

import os, sys, csv, re
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import json
import subprocess

# Import local modules
import material_cards, control_cards
import material_prop as mat_prop
import create_input as create_input

class VIEWER:

    def __init__(self, master):
        """
            It contains of the basic features to automate the pre-processing of design
        :return:
        """

        self.master = master
        self.frame = Frame(self.master)
        self.frame.pack()
        self.baseDir = os.path.dirname(sys.argv[0])
        self.template_path = os.path.join(self.baseDir, "Template")

        self.rowN = 0
        self.project_path_button = self.createButton(self.frame, "ProjectPath", self.open_projectPath, self.rowN, 1, sticky_=EW, bg_='lightyellow')
        self.project_path = r"D:\Umesh\AxiomProject\VEOL_GUI\Rakesh_Project\Test1"
        self.project_path_entry = self.createEntry(self.frame, self.project_path, self.rowN, 2, widthV=50)
        self.createButton(self.frame, "Create_Input", self.create_input, self.rowN, 3, sticky_=EW, bg_='lightyellow')

        # Input Info
        self.rowN += 1
        self.input_path_button = self.createButton(self.frame, "Input_Path", self.open_inputPath, self.rowN, 1, sticky_=EW, bg_='lightyellow')
        self.meshFile = r"D:\Umesh\AxiomProject\VEOL_GUI\Rakesh_Project\Test1\mesh.k"
        self.input_path_entry = self.createEntry(self.frame,self.meshFile, self.rowN, 2, widthV=50)
        self.createButton(self.frame, "Get_Info", self.get_info, self.rowN, 3, sticky_=EW, bg_='lightyellow')
        self.input_parts = []
        self.partInfo = {"":""}
        self.partRowNo = self.rowN
        self.map_part_material = {}
        self.map_part_section = {}
        self.map_part_thickness = {}
        self.partSetIdList = []

        self.parts_info = StringVar(self.frame)
        self.parts_info.set("")
        self.partInfo_list = set(sorted(self.partInfo.keys()))
        self.part_option = OptionMenu(self.frame, self.parts_info, *self.partInfo_list, command=self.get_part_ID)
        self.part_option.config(bg='lightyellow')
        self.part_option.grid(row = self.partRowNo+1, column=2, sticky="N")
        self.parts_info.trace('w', self.part_dropdown)

        self.rowN += 1
        # Material Cards Info
        self.MaterialCards = material_cards.MaterialCards()
        self.material_cards_type = StringVar(self.frame)
        self.material_card = self.MaterialCards.material_cards_type[0]
        self.material_cards_type_list = set(sorted(self.MaterialCards.material_cards_type))
        self.material_cards_type.set(self.material_card)

        popupMenu = OptionMenu(self.frame, self.material_cards_type, *self.material_cards_type_list, command=self.get_material_type)
        popupMenu.config(bg='lightyellow')
        popupMenu.grid(row = self.rowN, column=2, sticky="W", ipadx_=5)
        self.material_cards_type.trace('w', self.material_dropdown)

        self.add_new_material_card_button = Button(self.frame, text="AddNewMaterial", command=self.add_new_material_card, bg='peachpuff')
        self.add_new_material_card_button.grid(row=self.rowN, column=1, sticky=EW)

        self.read_material_button = Button(self.frame, text="ReadMaterial", command=self.read_material, bg='lightblue')
        self.read_material_button.grid(row=self.rowN, column=2, ipadx=15, sticky=E)

        self.add_material_info_button = Button(self.frame, text="AddMaterialPara", command=self.add_material_info, bg='lightyellow')
        self.add_material_info_button.grid(row=self.rowN, column=3, sticky=EW)

        self.rowN += 1
        self.section_cards_type = StringVar(self.frame)
        self.section_type = self.MaterialCards.section_cards_type[0]
        self.section_cards_type.set(self.section_type)
        popupMenu = OptionMenu(self.frame, self.section_cards_type, *self.MaterialCards.section_cards_type, command=self.get_section_type)
        popupMenu.config(bg='lightyellow')
        popupMenu.grid(row = self.rowN, column=2, ipadx=25, sticky=E)
        self.section_cards_type.trace('w', self.section_dropdown)

        self.add_section_button = Button(self.frame, text="Add_Section", command=self.add_section, bg='lightyellow')
        self.add_section_button.grid(row=self.rowN, column=3, sticky=EW)

        # Update Part Info ( partId = MaterialId = SectionId)
        self.rowN += 1
        self.updatePart_button = Button(self.frame, text="UpdatePartInfo", command=self.update_part_info, bg='lightyellow')
        self.updatePart_button.grid(row=self.rowN, column=3, sticky=EW)

        # Control Cards Info
        self.rowN += 1
        # Define Curve
        self.curveTitleList = []
        self.curveIdList = []
        self.curveInfo = {}
        self.curveValList = []
        self.curveLines = []
        self.curveList = []
        self.ControlCards = control_cards.ControlCards()
        self.define_cards_type = StringVar(self.frame)
        self.define_card = self.ControlCards.define_cards_type[0]
        self.define_cards_type_list = set(sorted(self.ControlCards.define_cards_type))
        self.define_cards_type.set(self.define_card)

        self.define_popupMenu = OptionMenu(self.frame, self.define_cards_type, *self.define_cards_type_list, command=self.get_define_type)
        self.define_popupMenu.grid(row = self.rowN, column=2, sticky=E, ipadx=30)
        self.define_popupMenu.config(bg='lightyellow')
        self.define_cards_type.trace('w', self.define_dropdown)

        # self.createLabel(self.frame, "DefineCurve", self.rowN, 2, sticky_=E, bg_='yellow', ipadx_=15)
        self.createButton(self.frame, "Import_Info", self.import_curve_info, self.rowN, 2, ipadx_=40, sticky_=W, bg_='lightblue')
        self.createButton(self.frame, "Add_Info", self.add_define_cards_info, self.rowN, 3, sticky_=EW, bg_='lightyellow')

        self.rowN += 1
        # self.ControlCards = control_cards.ControlCards()
        self.control_cards_type = StringVar(self.frame)
        self.control_card = self.ControlCards.control_cards_type[0]
        self.control_cards_type_list = set(sorted(self.ControlCards.control_cards_type))
        self.control_cards_type.set(self.control_card)

        popupMenu = OptionMenu(self.frame, self.control_cards_type, *self.control_cards_type_list, command=self.get_control_type)
        popupMenu.grid(row = self.rowN, column=2, sticky=E)
        popupMenu.config(bg='lightyellow')
        self.control_cards_type.trace('w', self.control_dropdown)

        self.add_new_control_card_button = Button(self.frame, text="AddNewControlCards", command=self.add_new_control_card, bg='peachpuff')
        self.add_new_control_card_button.grid(row=self.rowN, column=1, sticky=W)

        self.read_control_button = Button(self.frame, text="ReadControlCards", command=self.read_control_card, bg='lightblue')
        self.read_control_button.grid(row=self.rowN, column=2, sticky=W)

        self.add_control_cards_info_button = Button(self.frame, text="AddControlCardsPara", command=self.add_control_cards_info, bg='lightyellow')
        self.add_control_cards_info_button.grid(row=self.rowN, column=3, sticky=W)

        self.rowN += 1
        # Open Input
        self.createButton(self.frame, "Open Input", self.open_input, self.rowN, 1, sticky_=EW, bg_='lightgreen')
        # Review Input
        self.createButton(self.frame, "Review Input", self.review_input, self.rowN, 2, sticky_=W, ipadx_=35, bg_='lightgreen')
        # Run Input
        self.createButton(self.frame, "Run", self.run_info, self.rowN, 2, sticky_=E, ipadx_=55, bg_='lightgreen')
        # Exit
        self.createButton(self.frame, "Exit", self.frame.quit, self.rowN, 3, sticky_=EW, bg_='lightgreen')

    def review_input(self):
        """
        :return:
        """
        row_ = 0

        parameter_label1 = StringVar()
        parameter_label_entry1 = Entry(self.frame, textvariable=parameter_label1, state='readonly', justify=CENTER)
        parameter_label1.set('PartID')
        parameter_label_entry1.grid(row=row_, column=5, sticky=N)

        parameter_label2 = StringVar()
        parameter_label_entry2 = Entry(self.frame, textvariable=parameter_label2, state='readonly', justify=CENTER)
        parameter_label2.set('PartName')
        parameter_label_entry2.grid(row=row_, column=6, sticky=N)

        parameter_label3 = StringVar()
        parameter_label_entry3 = Entry(self.frame, textvariable=parameter_label3, state='readonly', justify=CENTER)
        parameter_label3.set('ID, MaterialType')
        parameter_label_entry3.grid(row=row_, column=7, sticky=N)

        parameter_label4 = StringVar()
        parameter_label_entry4 = Entry(self.frame, textvariable=parameter_label4, state='readonly', justify=CENTER)
        parameter_label4.set('ID, ShellType')
        parameter_label_entry4.grid(row=row_, column=8, sticky=N)

        parameter_label5 = StringVar()
        parameter_label_entry5 = Entry(self.frame, textvariable=parameter_label5, state='readonly', justify=CENTER)
        parameter_label5.set('Thickness')
        parameter_label_entry5.grid(row=row_, column=9, sticky=N)

        # self.createButton(self.frame, "EXIT", self.save_mat_info, row_, 10, fg_='red', sticky_='E')

        print(self.map_part_material)
        print(self.map_part_section)
        self.partID_label = []
        self.partName_label = []
        self.partMat_label = []
        self.partShell_label = []
        self.partThk_label = []

        index = 0
        for key in sorted(self.map_part_material.keys()):
            row_ += 1
            print(index)

            partID_label = StringVar()
            print(key, self.map_part_id_name.get(key, ""), self.map_part_material.get(key, ""), self.map_part_section.get(key, ""), self.map_part_thickness.get(key, ""))
            self.partID_label.append(Entry(self.frame, textvariable=partID_label, width=5, state='readonly'))
            partID_label.set(key)
            self.partID_label[index].grid(row = row_, column=5)
            # self.partID_label[index].insert(0, key)

            partName_label = StringVar()
            self.partName_label.append(Entry(self.frame, textvariable=partName_label, width=15, state='readonly'))
            partName_label.set(self.map_part_id_name.get(key, ""))
            self.partName_label[index].grid(row = row_, column=6)
            # self.partName_label[index].insert(0, self.map_part_id_name[key])

            partMat_label = StringVar()
            self.partMat_label.append(Entry(self.frame, textvariable=partMat_label, width=10, state='readonly'))
            partMat_label.set(self.map_part_material.get(key, ""))
            self.partMat_label[index].grid(row = row_, column=7)
            # self.partMat_label[index].insert(0, self.map_part_material[key])

            partShell_label = StringVar()
            self.partShell_label.append(Entry(self.frame, textvariable=partShell_label, width=10, state='readonly'))
            partShell_label.set(self.map_part_section.get(key, ""))
            self.partShell_label[index].grid(row = row_, column=8)
            # self.partShell_label[index].insert(0, self.map_part_section[key])

            partThk_label = StringVar()
            self.partThk_label.append(Entry(self.frame, textvariable=partThk_label, width=5, state='readonly'))
            partThk_label.set(self.map_part_thickness.get(key, ""))
            self.partThk_label[index].grid(row = row_, column=9)
            # self.partThk_label[index].insert(0, self.map_part_thickness[key])
            index += 1

    def open_inputPath(self):
        """
        :return:
        """
        self.meshFile = filedialog.askopenfilename(initialdir=r"D:\Umesh\AxiomProject\VEOL_GUI\Rakesh_Project\Test1")
        self.input_path_entry.delete(0,'end')
        self.input_path_entry.insert(0,self.meshFile)

    def get_info(self):
        """
                *PART
                *SET_PART_LIST
        :return:
        """
        self.partInfo = {}
        self.map_part_id_name = {}
        with open(self.meshFile) as readFile:
            readlines = readFile.readlines()

        inOtherBlock = False
        inPartBlock = False
        inSetPartListBlock = False
        inTitleBlock = False
        inPartIdBlock = False
        for line in readlines:
            count = 0
            if line.startswith("*PART"):
                inPartBlock = True
                inTitleBlock = True
                inOtherBlock = False
                inSetPartListBlock = False
                # print(line)
                continue
            if line.startswith("*SET_PART_LIST"):
                inPartBlock = False
                inTitleBlock = False
                inOtherBlock = False
                inSetPartListBlock = True
                # print(line)
                continue
            if line.__contains__("*"):
                inOtherBlock = True
                inPartBlock = False
                continue
            if inPartBlock:
                if line.startswith("$"):
                    continue
                if inTitleBlock:
                    # print("In part title Block :")
                    # print(line.strip())
                    partName = line.strip()
                    inTitleBlock = False
                    inPartIdBlock = True
                    continue
                if inPartIdBlock:
                    # print("In partId Block :")
                    # print(line)
                    partId = line[:10].strip()
                    self.partInfo.update({partName:partId})
                    self.map_part_id_name.update({partId:partName})
                    inPartIdBlock = False
                    inTitleBlock = True
                    continue
            if inSetPartListBlock:
                if line.startswith("$"):
                    continue
                self.partSetIdList.append(line[:10].strip())
                inSetPartListBlock = False
            if inOtherBlock:
                continue
        print(self.partInfo)
        print("part_set_id :", self.partSetIdList)

        self.update_option_menu()

    def update_option_menu(self):
        """
        :return:
        """
        self.partInfo_list = set(sorted(self.partInfo.keys()))
        menu = self.part_option['menu']
        menu.delete(0, 'end')
        for string in self.partInfo_list:
            menu.add_command(label=string,
                             command=lambda value=string: self.parts_info.set(value))

    def update_part_info(self):
        """
        :return:
        """
        print(self.partInfo)
        self.window_partInfo = Toplevel(self.frame)
        row_ = 0
        self.createLabel(self.window_partInfo, "PartID", row_, 0, 10)
        self.createLabel(self.window_partInfo, "PartName", row_, 1, 10)
        self.createLabel(self.window_partInfo, "SectionID", row_, 2, 10)
        self.createLabel(self.window_partInfo, "MaterialID", row_, 3, 10)

        self.partInfo_entry = []
        self.partID_label = []
        self.partName_label = []
        self.partMat_label = []
        self.partShell_label = []

        index = 0
        for key in sorted(self.map_part_id_name.keys()):
            row_ += 1
            print(index)

            partID_label = StringVar()
            self.partID_label.append(Entry(self.window_partInfo, textvariable=partID_label, width=5, state='readonly'))
            partID_label.set(key)
            self.partID_label[index].grid(row = row_, column=0)

            partName_label = StringVar()
            self.partName_label.append(Entry(self.window_partInfo, textvariable=partName_label, width=15, state='readonly'))
            partName_label.set(self.map_part_id_name.get(key, ""))
            self.partName_label[index].grid(row = row_, column=1)

            partShell_label = StringVar()
            self.partShell_label.append(Entry(self.window_partInfo, textvariable=partShell_label, width=10))#, state='readonly'))
            partShell_label.set(self.map_part_section.get(key, "").split(',')[0])
            self.partShell_label[index].grid(row = row_, column=2)

            partMat_label = StringVar()
            self.partMat_label.append(Entry(self.window_partInfo, textvariable=partMat_label, width=10))#, state='readonly'))
            partMat_label.set(self.map_part_material.get(key, "").split(',')[0])
            self.partMat_label[index].grid(row = row_, column=3)

            index += 1

        row_ += 2
        self.createButton(self.window_partInfo, "Save", self.update, row_, 2, sticky_=EW)
        self.createButton(self.window_partInfo, "Exit", self.close_window_part_info, row_, 3, sticky_=EW)

    def update(self):
        """
        :return:
        """

        self.map_part_id_mid_sid = {}
        for i in range(len(self.partID_label)):
            self.map_part_id_mid_sid.update({self.partID_label[i].get():[self.partShell_label[i].get(), self.partMat_label[i].get()]})

        with open(self.meshFile) as readFile:
            readlines = readFile.readlines()

        inOtherBlock = False
        inPartBlock = False
        inTitleBlock = False
        inPartIdBlock = False
        outlines = []
        for line in readlines:
            count = 0
            if line.startswith("*PART"):
                outlines.append(line)
                inPartBlock = True
                inTitleBlock = True
                inOtherBlock = False
                continue
            if line.__contains__("*"):
                outlines.append(line)
                inOtherBlock = True
                inPartBlock = False
                continue
            if inPartBlock:
                if line.startswith("$"):
                    outlines.append(line)
                    continue
                if inTitleBlock:
                    outlines.append(line)
                    partName = line.strip()
                    inTitleBlock = False
                    inPartIdBlock = True
                    continue
                if inPartIdBlock:
                    partId = line[:10].strip()
                    sectId = self.map_part_id_mid_sid[partId][0]
                    matId = self.map_part_id_mid_sid[partId][1]
                    line1 = line[:10] + sectId.rjust(10) + matId.rjust(10) + line[31:]
                    self.partInfo.update({partName:partId})
                    self.map_part_id_name.update({partId:partName})
                    inPartIdBlock = False
                    inTitleBlock = True
                    outlines.append(line1)
                    continue
            if inOtherBlock:
                outlines.append(line)
                continue
        print(self.partInfo)

        self.meshFile_out = os.path.join(os.path.split(self.meshFile)[0], "mesh_edit.k")
        with open(self.meshFile_out, 'w') as outFile:
            outFile.writelines(outlines)

    def close_window_part_info(self):
        """
        :return:
        """
        self.window_partInfo.destroy()

    def add_new_control_card(self):
        """
        :return:
        """

    def read_control_card(self):
        """
        :return:
        """

    def get_control_type(self, control_card):
        """
        :return:
        """
        self.control_card = control_card

    def control_dropdown(self, *args):
        """
        :return:
        """
        self.control_card = self.control_cards_type.get()

    def define_dropdown(self, *args):
        """
        :return:
        """
        self.define_card = self.define_cards_type.get()

    def get_define_type(self, define_card):
        """
        :return:
        """
        self.define_card = define_card

    def add_define_cards_info(self):
        """

        :return:
        """
        self.window_defineCardsInfo = Toplevel(self.frame)
        self.entry_list_define_cards = []
        self.label_list_define_cards = []
        colN = 0
        rowN = 0
        count = 0

        self.curr_define_card_parameters = self.ControlCards.define_cards[self.define_card]["Control_Parameters"][0].split(',')
        self.curr_define_card_parameters_default = self.ControlCards.define_cards[self.define_card]["Control_Parameters"][1].split(',')
        self.curr_define_card_parameters_freq = self.ControlCards.define_cards[self.define_card]["Control_Parameters"][2].split(',')

        for j in range(len(self.curr_define_card_parameters)):
            if count == 8:
                rowN += 2
                colN = 0
                count = 0

            if self.curr_define_card_parameters[j] == "":
                self.label_list_define_cards.append(Label(self.window_defineCardsInfo, text=self.curr_define_card_parameters[j], width=10))
                self.entry_list_define_cards.append(Entry(self.window_defineCardsInfo, width=10))
                rowN += 2
                colN = 0
                count = 0
                continue

            if self.curr_define_card_parameters_freq[j].strip().upper() == "Y":
                self.label_list_define_cards.append(Label(self.window_defineCardsInfo, text=self.curr_define_card_parameters[j].upper(), width=10, fg="blue"))
                self.entry_list_define_cards.append(Entry(self.window_defineCardsInfo, width=10, fg="blue"))
            else:
                self.label_list_define_cards.append(Label(self.window_defineCardsInfo, text=self.curr_define_card_parameters[j].upper(), width=10))
                self.entry_list_define_cards.append(Entry(self.window_defineCardsInfo, width=10))

            if self.curr_define_card_parameters[j] == "CURVE":
                self.label_list_define_cards[j].grid(row=rowN, column=colN)
                # self.entry_list_control_cards[j].grid(row=rowN+1, column=colN)
                self.createButton(self.window_defineCardsInfo, "Add_Info", self.add_curve_info, rowN+1, colN, bg_='lightyellow')
                self.createButton(self.window_defineCardsInfo, "Import_Info", self.import_curve_info, rowN+1, colN+1, bg_='lightblue')
                continue

            self.label_list_define_cards[j].grid(row=rowN, column=colN)
            self.entry_list_define_cards[j].grid(row=rowN+1, column=colN)
            self.entry_list_define_cards[j].insert(0,self.curr_define_card_parameters_default[j])

            count += 1
            colN += 1

        rowN += 3
        # print(rowN)
        button_ = Button(self.window_defineCardsInfo, text="Save", command=self.save_define_cards_info)
        button_.grid(row=rowN, column=1)
        Exitbutton_ = Button(self.window_defineCardsInfo, text="Exit", command=self.close_window_define_cards)
        Exitbutton_.grid(row=rowN, column=2)

    def add_curve_info(self):
        """
        :return:
        """
        self.curveRowN = 0
        self.curveInfoList = []
        self.window_defineCurve = Toplevel(self.frame)

        A1 = StringVar()
        A1_entry = Entry(self.window_defineCurve, textvariable=A1, state='readonly')
        A1.set('A1')
        A1_entry.grid(row=self.curveRowN, column=0)

        O1 = StringVar()
        O1_entry = Entry(self.window_defineCurve, textvariable=O1, state='readonly')
        O1.set('O1')
        O1_entry.grid(row=self.curveRowN, column=1)

        self.add_new_entry_button = Button(self.window_defineCurve, text="+", command=self.add_curve_entry, fg='blue')
        self.add_new_entry_button.grid(row=self.curveRowN, column=2)
        self.save_entry_button = Button(self.window_defineCurve, text="Save", command=self.save_curve_entry, fg='blue')
        self.save_entry_button.grid(row=self.curveRowN, column=3)

    def add_curve_entry(self):
        """

        :return:
        """
        self.curveRowN += 1
        self.A1 = self.createEntry(self.window_defineCurve, "", self.curveRowN, 0, widthV=20)
        self.O1 = self.createEntry(self.window_defineCurve, "", self.curveRowN, 1, widthV=20)
        self.curveInfoList.append([self.A1, self.O1])

    def save_curve_entry(self):
        """
        :return:
        """
        self.curveValList_str = ""
        for i in range(len(self.curveInfoList)):
            if i == len(self.curveInfoList)-1:
                self.curveValList_str += self.curveInfoList[i][0].get().rjust(20) + self.curveInfoList[i][1].get().rjust(20)
            else:
                self.curveValList_str += self.curveInfoList[i][0].get().rjust(20) + self.curveInfoList[i][1].get().rjust(20) +'\n'

        print(self.curveValList_str)
        self.window_defineCurve.destroy()

    def import_curve_info(self):
        """
        :return:
        """

    def save_define_cards_info(self):
        """
        :return:
        """
        outlines = []
        colN = 0
        rowN = 0
        count = 0
        newline = []
        index = 0
        outlines.append("\n")
        outlines.append(self.ControlCards.define_cards[self.define_card]["Card_Title"][0])
        header_line = "\n$$"
        for j in range(len(self.curr_define_card_parameters)):
            if count == 8:# or j == (len(self.curr_material_parameters)):
                rowN += 2
                colN = 0
                count = 0
                line1 = "\n" + "".join(newline)# + "\n"
                value_line = header_line + line1
                outlines.append(value_line)
                header_line = "\n$$"
                newline = []

            if self.curr_define_card_parameters[j] == "":
                rowN += 2
                colN = 0
                count = 0
                line1 = "\n" + "".join(newline) #+ "\n"
                value_line = header_line + line1
                outlines.append(value_line)
                header_line = "\n$$"
                newline = []
                index += 1
                continue
            if self.curr_define_card_parameters[j] == "LCID":
                lcid = self.entry_list_define_cards[index].get().strip()

            if self.curr_define_card_parameters[j] == "CURVE":
                if header_line == "\n$$":
                    header_line += self.curr_define_card_parameters[j].rjust(8)
                else:
                    header_line += self.curr_define_card_parameters[j].rjust(10)
                newline.append(self.curveValList_str)
            else:
                if header_line == "\n$$":
                    header_line += self.curr_define_card_parameters[j].rjust(8)
                else:
                    header_line += self.curr_define_card_parameters[j].rjust(10)
                tmp_prop = self.entry_list_define_cards[index].get().strip()
                newline.append(tmp_prop.rjust(10))

            if j == (len(self.curr_define_card_parameters)-1):
                line1 = "\n" + "".join(newline)# + "\n"
                value_line = header_line + line1
                outlines.append(value_line)
                header_line = "\n$$"

            count += 1
            colN += 1
            index += 1
        # line = ",".join([mid, self.material_card])
        # self.map_part_material.update({self.partID:line})
        # print(self.map_part_material)
        self.curveList.append(lcid)
        with open(self.control_card_out_file, 'a') as outFile:
            outFile.writelines(outlines)

    def close_window_define_cards(self):
        """
        :return:
        """
        self.window_defineCardsInfo.destroy()

    def add_control_cards_info(self):
        """

        :return:
        """
        self.window_controlCardsInfo = Toplevel(self.frame)
        self.entry_list_control_cards = []
        self.label_list_control_cards = []
        colN = 0
        rowN = 0
        count = 0

        self.curr_control_card_parameters = self.ControlCards.control_cards[self.control_card]["Control_Parameters"][0].split(',')
        self.curr_control_card_parameters_default = self.ControlCards.control_cards[self.control_card]["Control_Parameters"][1].split(',')
        self.curr_control_card_parameters_freq = self.ControlCards.control_cards[self.control_card]["Control_Parameters"][2].split(',')

        for j in range(len(self.curr_control_card_parameters)):
            if count == 8:
                rowN += 2
                colN = 0
                count = 0

            if self.curr_control_card_parameters[j] == "":
                self.label_list_control_cards.append(Label(self.window_controlCardsInfo, text=self.curr_control_card_parameters[j], width=10))
                self.entry_list_control_cards.append(Entry(self.window_controlCardsInfo, width=10))
                rowN += 2
                colN = 0
                count = 0
                continue

            if self.curr_control_card_parameters_freq[j].strip().upper() == "Y":
                self.label_list_control_cards.append(Label(self.window_controlCardsInfo, text=self.curr_control_card_parameters[j].upper(), width=10, fg="blue"))
                self.entry_list_control_cards.append(Entry(self.window_controlCardsInfo, width=10, fg="blue"))
            else:
                self.label_list_control_cards.append(Label(self.window_controlCardsInfo, text=self.curr_control_card_parameters[j].upper(), width=10))
                self.entry_list_control_cards.append(Entry(self.window_controlCardsInfo, width=10))

            if self.curr_control_card_parameters[j] == "PID":
                self.label_list_control_cards[j].grid(row=rowN, column=colN)
                self.parts_info2 = StringVar(self.window_controlCardsInfo)
                self.parts_info2.set("")
                self.part_option2 = OptionMenu(self.window_controlCardsInfo, self.parts_info2, *self.partInfo_list, command=self.get_part_ID2)
                self.part_option2.config(bg='lightyellow')
                self.part_option2.grid(row = rowN+1, column=colN)
                self.parts_info2.trace('w', self.part_dropdown2)
                count += 1
                colN += 1
                continue
            elif self.curr_control_card_parameters[j] == "LCID":
                self.label_list_control_cards[j].grid(row=rowN, column=colN)
                self.curve_info = StringVar(self.window_controlCardsInfo)
                self.curve_info.set("")
                self.curvePopup = OptionMenu(self.window_controlCardsInfo, self.curve_info, *self.curveList, command=self.get_curve_ID)
                self.curvePopup.config(bg='lightyellow')
                self.curvePopup.grid(row = rowN+1, column=colN)
                self.curve_info.trace('w', self.curve_dropdown)
                count += 1
                colN += 1
                continue
            elif self.curr_control_card_parameters[j] == "PSID":
                self.label_list_control_cards[j].grid(row=rowN, column=colN)
                self.partSetID_info = StringVar(self.window_controlCardsInfo)
                self.partSetID_info.set("")
                self.partSetPopup = OptionMenu(self.window_controlCardsInfo, self.partSetID_info, *self.partSetIdList, command=self.get_partSet_ID)
                self.partSetPopup.config(bg='lightyellow')
                self.partSetPopup.grid(row = rowN+1, column=colN)
                self.partSetID_info.trace('w', self.partSet_dropdown)
                count += 1
                colN += 1
                continue
            else:
                self.label_list_control_cards[j].grid(row=rowN, column=colN)
                self.entry_list_control_cards[j].grid(row=rowN+1, column=colN)
                self.entry_list_control_cards[j].insert(0,self.curr_control_card_parameters_default[j])
                count += 1
                colN += 1

        rowN += 3
        # print(rowN)
        button_ = Button(self.window_controlCardsInfo, text="Save", command=self.save_control_cards_info)
        button_.grid(row=rowN, column=1)
        Exitbutton_ = Button(self.window_controlCardsInfo, text="Exit", command=self.close_window_CC)
        Exitbutton_.grid(row=rowN, column=2)

    def get_partSet_ID(self, partSetID):
        self.partSetID = partSetID

    def partSet_dropdown(self, *args):
        """
        :return:
        """
        self.partSetID = self.partSetID_info.get()

    def get_curve_ID(self, curveID):
        self.curveID = curveID

    def curve_dropdown(self, *args):
        """
        :return:
        """
        self.curveID = self.curve_info.get()

    def save_control_cards_info(self):
        """
        :return:
        """
        outlines = []
        colN = 0
        rowN = 0
        count = 0
        newline = []
        index = 0
        outlines.append("\n")
        outlines.append(self.ControlCards.control_cards[self.control_card]["Card_Title"][0])
        header_line = "\n$$"
        for j in range(len(self.curr_control_card_parameters)):
            if count == 8:# or j == (len(self.curr_material_parameters)):
                rowN += 2
                colN = 0
                count = 0
                line1 = "\n" + "".join(newline)# + "\n"
                value_line = header_line + line1
                outlines.append(value_line)
                header_line = "\n$$"
                newline = []

            if self.curr_control_card_parameters[j] == "":
                rowN += 2
                colN = 0
                count = 0
                line1 = "\n" + "".join(newline) #+ "\n"
                value_line = header_line + line1
                outlines.append(value_line)
                header_line = "\n$$"
                newline = []
                index += 1
                continue

            # print("[{}] {}: {}".format(index, self.curr_material_parameters[j], self.entry_list[index].get()))
            if self.curr_control_card_parameters[j] == "PID":
                tmp_prop = self.partInfo[self.parts_info2.get()]
            elif self.curr_control_card_parameters[j] == "LCID":
                tmp_prop = self.curve_info.get()
            elif self.curr_control_card_parameters[j] == "PSID":
                tmp_prop = self.partSetID_info.get()
            else:
                tmp_prop = self.entry_list_control_cards[index].get().strip()
            if header_line == "\n$$":
                header_line += self.curr_control_card_parameters[j].rjust(8)
            else:
                header_line += self.curr_control_card_parameters[j].rjust(10)
            newline.append(tmp_prop.rjust(10))
            if j == (len(self.curr_control_card_parameters)-1):
                line1 = "\n" + "".join(newline)# + "\n"
                value_line = header_line + line1
                outlines.append(value_line)
                header_line = "\n$$"

            count += 1
            colN += 1
            index += 1

        with open(self.control_card_out_file, 'a') as outFile:
            outFile.writelines(outlines)

    def close_window_CC(self):
        """
        :return:
        """
        self.window_controlCardsInfo.destroy()

    def get_section_type(self, section_type):
        """
        :return:
        """
        self.section_type = section_type

    def section_dropdown(self, *args):
        """
        :return:
        """
        self.section_type = self.section_cards_type.get()

    def add_section(self):
        """
        :return:
        """

        self.window_sectionInfo = Toplevel(self.frame)
        self.entry_list_section = []
        self.label_list_section = []
        colN = 0
        rowN = 0
        count = 0

        self.curr_section_parameters = self.MaterialCards.section_cards[self.section_type]["Section_Parameters"][0].split(',')
        self.curr_section_parameters_default = self.MaterialCards.section_cards[self.section_type]["Section_Parameters"][1].split(',')
        self.curr_section_parameters_freq = self.MaterialCards.section_cards[self.section_type]["Section_Parameters"][2].split(',')

        for j in range(len(self.curr_section_parameters)):
            if count == 8:
                rowN += 2
                colN = 0
                count = 0

            if self.curr_section_parameters[j] == "":
                self.label_list_section.append(Label(self.window_sectionInfo, text=self.curr_section_parameters[j], width=10))
                self.entry_list_section.append(Entry(self.window_sectionInfo, width=10))
                rowN += 2
                colN = 0
                count = 0
                continue

            if self.curr_section_parameters_freq[j].strip().upper() == "Y":
                self.label_list_section.append(Label(self.window_sectionInfo, text=self.curr_section_parameters[j].upper(), width=10, fg="blue"))
                self.entry_list_section.append(Entry(self.window_sectionInfo, width=10, fg="blue"))
            else:
                self.label_list_section.append(Label(self.window_sectionInfo, text=self.curr_section_parameters[j].upper(), width=10))
                self.entry_list_section.append(Entry(self.window_sectionInfo, width=10))
            self.label_list_section[j].grid(row=rowN, column=colN)

            self.entry_list_section[j].grid(row=rowN+1, column=colN)
            self.entry_list_section[j].insert(0,self.curr_section_parameters_default[j])

            count += 1
            colN += 1

        rowN += 3
        # print(rowN)
        save_button_ = Button(self.window_sectionInfo, text="Save", command=self.save_section_)
        save_button_.grid(row=rowN, column=1)
        exit_button_ = Button(self.window_sectionInfo, text="Exit", command=self.close_section_)
        exit_button_.grid(row=rowN, column=2)

    def save_section_(self):
        """
        :return:
        """
        # print("##############################################################")
        outlines = []
        colN = 0
        rowN = 0
        count = 0
        newline = []
        index = 0
        outlines.append("\n")
        outlines.append(self.MaterialCards.section_cards[self.section_type]["Card_Title"][0])
        header_line = "\n$$"
        for j in range(len(self.curr_section_parameters)):
            if count == 8 or j == (len(self.curr_section_parameters)-1):
                rowN += 2
                colN = 0
                count = 0
                line1 = "\n" + "".join(newline)# + "\n"
                value_line = header_line + line1
                outlines.append(value_line)
                header_line = "\n$$"
                newline = []

            if self.curr_section_parameters[j] == "":
                rowN += 2
                colN = 0
                count = 0
                line1 = "\n" + "".join(newline) #+ "\n"
                value_line = header_line + line1
                outlines.append(value_line)
                header_line = "\n$$"
                newline = []
                index += 1
                continue

            if self.curr_section_parameters[j].upper() == 'T1':
                """ """
                thickness = self.entry_list_section[index].get()
                print(self.curr_section_parameters[j].upper(), thickness)
            if self.curr_section_parameters[j].upper() == 'SECID':
                """ """
                mid = self.entry_list_section[index].get()
                print(self.curr_section_parameters[j].upper(), mid)

            # print("[{}] {}: {}".format(index, self.curr_section_parameters[j], self.entry_list_section[index].get()))
            if header_line == "\n$$":
                header_line += self.curr_section_parameters[j].rjust(8)
            else:
                header_line += self.curr_section_parameters[j].rjust(10)
            tmp_prop = self.entry_list_section[index].get().strip()
            newline.append(tmp_prop.rjust(10))
            if j == (len(self.curr_section_parameters)-1):
                line1 = "\n" + "".join(newline)# + "\n"
                value_line = header_line + line1
                outlines.append(value_line)
                header_line = "\n$$"

            count += 1
            colN += 1
            index += 1
        line = ",".join([mid, self.section_type])
        self.map_part_section.update({self.partID:line})
        if self.section_type == "SHELL":
            self.map_part_thickness.update({self.partID:thickness})
        else:
            self.map_part_thickness.update({self.partID:""})

        # print(self.map_part_section)

        with open(self.material_out_file, 'a') as outFile:
            outFile.writelines(outlines)

    def close_section_(self):
        """
        :return:
        """
        self.window_sectionInfo.destroy()

    def open_projectPath(self):
        """

        :return:
        """
        project_path = filedialog.askdirectory(initialdir=r"D:\Umesh\AxiomProject\VEOL_GUI\Rakesh_Project\Test1")
        self.project_path_entry.delete(0,'end')
        self.project_path_entry.insert(0,project_path)

    def create_input(self):
        """

        :return:
        """
        self.project_path = self.project_path_entry.get()
        self.input_keyword = create_input.CreateInput()
        self.input_keyword.create_input_k(self.project_path)
        print(self.input_keyword.Kfile)

        self.material_out_file_name = "mat.k"
        self.material_out_file = os.path.join(self.project_path, self.material_out_file_name)
        with open(self.material_out_file, 'w') as outFile:
            outFile.write("")

        self.control_card_out_file_name = "control_cards.k"
        self.control_card_out_file = os.path.join(self.project_path, self.control_card_out_file_name)
        with open(self.control_card_out_file, 'w') as outFile:
            outFile.write("*KEYWORD")

    def add_new_material_card(self):
        """

        :return:
        """
        self.window_newMat = Toplevel(self.frame)

        rowN = 0
        self.materialTitle = ""
        self.createLabel(self.window_newMat, "MAT_TITLE", rowN, 0, width=20)
        self.mat_title_entry = self.createEntry(self.window_newMat, "MAT_TITLE", rowN, 1, widthV=20)
        rowN += 1
        self.createLabel(self.window_newMat, "PART_TITLE", rowN, 0, width=20, fg_='blue')
        self.part_title_entry = self.createEntry(self.window_newMat, "PART_TITLE", rowN, 1, widthV=20, fg_='blue')
        self.part_title_freq = self.createEntry(self.window_newMat, "Y", rowN, 2, widthV=5, fg_='blue')
        rowN += 1
        self.createLabel(self.window_newMat, "CARD_TITLE", rowN, 0, width=20, fg_='blue')
        self.card_title_entry = self.createEntry(self.window_newMat, "CARD_TITLE", rowN, 1, widthV=20, fg_='blue')
        self.card_title_freq = self.createEntry(self.window_newMat, "Y", rowN, 2, widthV=5, fg_='blue')
        rowN += 1
        self.createLabel(self.window_newMat, "CARD_INFO", rowN, 0, width=20, fg_='blue')
        self.createButton(self.window_newMat, "SAVE", self.save_new_mat_info, rowN, 2, fg_='red')
        rowN += 1

        parameter_label = StringVar()
        parameter_label_entry = Entry(self.window_newMat, textvariable=parameter_label, state='readonly')
        parameter_label.set('PARAMETER_LABEL')
        parameter_label_entry.grid(row=rowN, column=0)

        parameter_defaults = StringVar()
        parameter_defaults_entry = Entry(self.window_newMat, textvariable=parameter_defaults, state='readonly')
        parameter_defaults.set('DEFAULTS')
        parameter_defaults_entry.grid(row=rowN, column=1)

        parameter_freq = StringVar()
        parameter_freq_entry = Entry(self.window_newMat, textvariable=parameter_freq, state='readonly')
        parameter_freq.set('FREQUENCY')
        parameter_freq_entry.grid(row=rowN, column=2)

        select_ = StringVar()
        select_entry = Entry(self.window_newMat, textvariable=select_, state='readonly')
        select_.set('Select_To_Delete')
        select_entry.grid(row=rowN, column=3)

        self.add_new_entry_button = Button(self.window_newMat, text="+", command=self.add_entry, fg='blue')
        self.add_new_entry_button.grid(row=rowN, column=4)

        self.delete_new_entry_button = Button(self.window_newMat, text="-", command=self.delete_entry, fg='red')
        self.delete_new_entry_button.grid(row=rowN, column=5)

        self.matRowN = rowN
        self.material_new_info = []
        self.newMatInfo = []
        self.newMatInfo_defaults = []
        self.newMatInfo_freq = []

    def add_entry(self):
        """

        :return:
        """
        self.matRowN += 1

        var = IntVar()
        self.c = Checkbutton(self.window_newMat, variable = var)
        self.c.val = var
        self.c.grid(row = self.matRowN, column = 3)
        self.material_label = self.createEntry(self.window_newMat, "", self.matRowN, 0, widthV=20)
        self.material_defaults = self.createEntry(self.window_newMat, "", self.matRowN, 1, widthV=20)
        self.material_freq = self.createEntry(self.window_newMat, "", self.matRowN, 2, widthV=20)
        self.material_new_info.append([self.material_label, self.material_defaults, self.material_freq, self.c])

    def delete_entry(self):
        """
            to delete the entries not required
        :return:
        """
        for rowno, row in reversed(list(enumerate(self.material_new_info))):
            if row[3].val.get() == 1:
                for i in row:
                    i.destroy()
                self.material_new_info.pop(rowno)

    def save_new_mat_info(self):
        """
        :return:
        """
        # print(self.material_new_info, len(self.material_new_info))
        for item in self.material_new_info:
            self.newMatInfo.append(item[0].get())
            self.newMatInfo_defaults.append(item[1].get())
            self.newMatInfo_freq.append(item[2].get())


        newMatInfo = ",".join(self.newMatInfo)
        newMatInfo_default = ",".join(self.newMatInfo_defaults)
        newMatInfo_freq = ",".join(self.newMatInfo_freq)

        self.MaterialCards.material_cards.update({self.mat_title_entry.get():
                                  {"Part_Title":[self.part_title_entry.get(), self.part_title_freq.get()],
                                   "Card_Title":[self.card_title_entry.get(), self.card_title_freq.get()],
                                   "Mat_Parameters":[newMatInfo, newMatInfo_default, newMatInfo_freq]}})

        with open(self.MaterialCards.json_file, 'w') as outFile:
            json.dump(self.MaterialCards.material_cards, outFile)

    def read_material(self):
        """

        :return:
        """
        self.read_mat_file = filedialog.askopenfilename(initialdir=r"D:\Umesh\AxiomProject\VEOL_GUI\Rakesh_Project\Test1")
        with open(self.read_mat_file, 'r') as readFile:
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
        print(self.MaterialCards.map_material_cards_type_title)
        print(self.MaterialCards.map_section_cards_type_title)
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
                    print(section_card_title, str(self.MaterialCards.map_section_cards_type_title[section_card_title]))
                    section_tmp_line = ",".join([str(self.MaterialCards.map_section_cards_type_title[section_card_title]), str(section_id)])
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
                        matType = str(self.MaterialCards.map_material_cards_type_title[card_title])
                        tmp_line = ",".join([str(self.MaterialCards.map_material_cards_type_title[card_title]), str(mat_id)])
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
        self.rowN += 3
        self.read_material_card = self.read_material_cards_type_list[0]
        self.read_material_card_set = StringVar(self.frame)
        popupMenu = OptionMenu(self.frame, self.read_material_card_set, *self.read_material_cards_type_list, command=self.get_read_material_type)
        popupMenu.grid(row = self.rowN, column=1)
        self.read_material_card_set.set(self.read_material_cards_type_list[0])
        self.read_material_card_set.trace('w', self.read_material_dropdown)
        self.editMatData = self.createButton(self.frame, "Show", self.show_material, self.rowN, 2, sticky_=W)

        self.rowN += 3
        self.read_section_card = self.read_section_cards_type_list[0]
        self.read_section_card_set = StringVar(self.frame)
        popupMenu = OptionMenu(self.frame, self.read_section_card_set, *self.read_section_cards_type_list, command=self.get_read_section_type)
        popupMenu.grid(row = self.rowN, column=1)
        self.read_section_card_set.set(self.read_section_card)
        self.read_section_card_set.trace('w', self.read_section_dropdown)
        self.editSectionData = self.createButton(self.frame, "Show", self.show_section, self.rowN, 2, sticky_=W)

    def get_read_section_type(self, section_card_type):
        """
        :return:
        """
        self.read_section_card = section_card_type

    def read_section_dropdown(self, *args):
        """
        :return:
        """
        self.read_section_card = self.read_section_card_set.get()

    def show_section(self):
        """
        :return:
        """
        # print("In edit button !")
        rowN = 1
        self.window_sectionInfo_read = Toplevel(self.frame)
        section_card_type = self.read_section_card.split(',')[0]
        self.curr_section_parameters = self.MaterialCards.section_cards[section_card_type]["Section_Parameters"][0].split(',')
        sectionPara_curr_freq = self.MaterialCards.section_cards[section_card_type]["Section_Parameters"][2].split(',')
        count = 0
        colN = 0
        self.label_list_section = []
        self.entry_list_section = []
        index = 0
        for j in range(len(self.curr_section_parameters)):
            if count == 8:
                rowN += 2
                colN = 0
                count = 0

            if self.curr_section_parameters[j] == "":
                self.label_list_section.append(Label(self.window_sectionInfo_read, text=self.curr_section_parameters[j], width=10))
                self.entry_list_section.append(Entry(self.window_sectionInfo_read, width=10))
                rowN += 2
                colN = 0
                count = 0
                continue

            if sectionPara_curr_freq[j].strip().upper() == "Y":
                self.label_list_section.append(Label(self.window_sectionInfo_read, text=self.curr_section_parameters[j].upper(), width=10, fg="blue"))
                self.entry_list_section.append(Entry(self.window_sectionInfo_read, width=10, fg="blue"))
            else:
                self.label_list_section.append(Label(self.window_sectionInfo_read, text=self.curr_section_parameters[j].upper(), width=10))
                self.entry_list_section.append(Entry(self.window_sectionInfo_read, width=10))
            self.label_list_section[j].grid(row=rowN, column=colN)

            self.entry_list_section[j].grid(row=rowN+1, column=colN)

            try:
                self.entry_list_section[j].insert(0,self.read_section_parameters[self.read_section_card][index])
            except Exception as Ex:
                print(Ex, index)
                self.entry_list_section[j].insert(0,"")

            count += 1
            colN += 1
            index += 1

        rowN += 3
        button_ = Button(self.window_sectionInfo_read, text="Save", command=self.update_section)
        button_.grid(row=rowN, column=1)
        Exitbutton_ = Button(self.window_sectionInfo_read, text="Exit", command=self.close_section_window_read)
        Exitbutton_.grid(row=rowN, column=2)

    def update_section(self):
        """
        :return:
        """
        outlines = []
        colN = 0; rowN = 0; count = 0; index = 0
        newline = []
        outlines.append("\n")
        section_card_type = self.read_section_card.split(',')[0]
        outlines.append(self.MaterialCards.section_cards[section_card_type]["Card_Title"][0])
        for j in range(len(self.curr_section_parameters)):
            if count == 8:# or
                rowN += 2
                colN = 0
                count = 0
                line1 = "\n" + "".join(newline)# + "\n"
                outlines.append(line1)
                newline = []

            if self.curr_section_parameters[j] == "":
                rowN += 2
                colN = 0
                count = 0
                line1 = "\n" + "".join(newline) #+ "\n"
                outlines.append(line1)
                newline = []
                index += 1
                continue

            print("[{}] {}: {}".format(index, self.curr_section_parameters[j], self.entry_list_section[index].get()))
            tmp_prop = self.entry_list_section[index].get().strip()
            newline.append(tmp_prop.rjust(10))

            if j == (len(self.curr_section_parameters)-1):
                line1 = "\n" + "".join(newline) #+ "\n"
                outlines.append(line1)

            count += 1
            colN += 1
            index += 1

        # self.mat_out = filedialog.asksaveasfilename()
        self.presentMatFile_out = os.path.join(os.path.split(self.read_mat_file)[0], "mat_edit.k")
        if not os.path.exists(self.presentMatFile_out):
            open(self.presentMatFile_out, 'w').close()

        with open(self.presentMatFile_out, 'a') as outFile:
            outFile.writelines(outlines)

    def close_section_window_read(self):
        """
        :return:
        """
        self.window_sectionInfo_read.destroy()

    def get_read_material_type(self, material_card_type):
        """
        :return:
        """
        self.read_material_card = material_card_type

    def read_material_dropdown(self, *args):
        """
        :return:
        """
        self.read_material_card = self.read_material_card_set.get()

    def show_material(self):
        """
        :return:
        """

        # print("In edit button !")
        rowN = 1
        self.window_matInfo_read = Toplevel(self.frame)
        material_card_type = self.read_material_card.split(',')[0]
        self.curr_material_parameters = self.MaterialCards.material_cards[material_card_type]["Mat_Parameters"][0].split(',')
        materialPara_curr_freq = self.MaterialCards.material_cards[material_card_type]["Mat_Parameters"][2].split(',')
        count = 0
        colN = 0
        crit_fail = str(float(material_card_type.split('_')[-1]))
        self.entry_list = []
        self.label_list = []
        index = 0
        for j in range(len(self.curr_material_parameters)):
            if count == 8:
                rowN += 2
                colN = 0
                count = 0

            if self.curr_material_parameters[j] == "":
                self.label_list.append(Label(self.window_matInfo_read, text=self.curr_material_parameters[j], width=10))
                self.entry_list.append(Entry(self.window_matInfo_read, width=10))
                rowN += 2
                colN = 0
                count = 0
                continue

            if materialPara_curr_freq[j].strip().upper() == "Y":
                self.label_list.append(Label(self.window_matInfo_read, text=self.curr_material_parameters[j].upper(), width=10, fg="blue"))
                self.entry_list.append(Entry(self.window_matInfo_read, width=10, fg="blue"))
            else:
                self.label_list.append(Label(self.window_matInfo_read, text=self.curr_material_parameters[j].upper(), width=10))
                self.entry_list.append(Entry(self.window_matInfo_read, width=10))
            self.label_list[j].grid(row=rowN, column=colN)

            self.entry_list[j].grid(row=rowN+1, column=colN)
            if self.curr_material_parameters[j] == "crit":
                self.entry_list[j].insert(0,str(crit_fail))
            else:
                try:
                    self.entry_list[j].insert(0,self.read_material_parameters[self.read_material_card][index])
                except Exception as Ex:
                    print(Ex, index)
                    self.entry_list[j].insert(0,"")

            count += 1
            colN += 1
            index += 1

        rowN += 3
        button_ = Button(self.window_matInfo_read, text="Save", command=self.update_material)
        button_.grid(row=rowN, column=1)
        Exitbutton_ = Button(self.window_matInfo_read, text="Exit", command=self.close_window_read)
        Exitbutton_.grid(row=rowN, column=2)

    def update_material(self):
        """
        :return:
        """
        outlines = []
        colN = 0
        rowN = 0
        count = 0
        newline = []
        index = 0
        outlines.append("\n")
        material_card_type = self.read_material_card.split(',')[0]
        outlines.append(self.MaterialCards.material_cards[material_card_type]["Card_Title"][0])
        for j in range(len(self.curr_material_parameters)):
            if count == 8:# or
                rowN += 2
                colN = 0
                count = 0
                line1 = "\n" + "".join(newline)# + "\n"
                outlines.append(line1)
                newline = []

            if self.curr_material_parameters[j] == "":
                rowN += 2
                colN = 0
                count = 0
                line1 = "\n" + "".join(newline) #+ "\n"
                outlines.append(line1)
                newline = []
                index += 1
                continue

            print("[{}] {}: {}".format(index, self.curr_material_parameters[j], self.entry_list[index].get()))
            tmp_prop = self.entry_list[index].get().strip()
            newline.append(tmp_prop.rjust(10))

            if j == (len(self.curr_material_parameters)-1):
                line1 = "\n" + "".join(newline) #+ "\n"
                outlines.append(line1)

            count += 1
            colN += 1
            index += 1

        # self.mat_out = filedialog.asksaveasfilename()
        self.presentMatFile_out = os.path.join(os.path.split(self.read_mat_file)[0], "mat_edit.k")
        if not os.path.exists(self.presentMatFile_out):
            open(self.presentMatFile_out, 'w').close()

        with open(self.presentMatFile_out, 'a') as outFile:
            outFile.writelines(outlines)

    def add_material_info(self):
        """

        :return:
        """
        self.window_matInfo = Toplevel(self.frame)
        self.entry_list = []
        self.label_list = []
        colN = 0
        rowN = 0
        count = 0
        try:
            crit_fail = float(self.material_card.split("_")[-1])
        except Exception as Ex:
            crit_fail = 0.0
            print(Ex)
            pass
        self.curr_material_parameters = self.MaterialCards.material_cards[self.material_card]["Mat_Parameters"][0].split(',')
        self.curr_material_parameters_default = self.MaterialCards.material_cards[self.material_card]["Mat_Parameters"][1].split(',')
        self.curr_material_parameters_freq = self.MaterialCards.material_cards[self.material_card]["Mat_Parameters"][2].split(',')

        for j in range(len(self.curr_material_parameters)):
            if count == 8:
                rowN += 2
                colN = 0
                count = 0

            if self.curr_material_parameters[j] == "":
                self.label_list.append(Label(self.window_matInfo, text=self.curr_material_parameters[j], width=10))
                self.entry_list.append(Entry(self.window_matInfo, width=10))
                rowN += 2
                colN = 0
                count = 0
                continue

            if self.curr_material_parameters_freq[j].strip().upper() == "Y":
                self.label_list.append(Label(self.window_matInfo, text=self.curr_material_parameters[j].upper(), width=10, fg="blue"))
                self.entry_list.append(Entry(self.window_matInfo, width=10, fg="blue"))
            else:
                self.label_list.append(Label(self.window_matInfo, text=self.curr_material_parameters[j].upper(), width=10))
                self.entry_list.append(Entry(self.window_matInfo, width=10))
            self.label_list[j].grid(row=rowN, column=colN)

            self.entry_list[j].grid(row=rowN+1, column=colN)
            # self.entry_list[j].insert(0,self.material1.material_prop.get(self.materialProp_curr[j].strip(), 0.0))
            if self.curr_material_parameters[j] == "crit":
                self.entry_list[j].insert(0,str(crit_fail))
            else:
                self.entry_list[j].insert(0,self.curr_material_parameters_default[j])

            count += 1
            colN += 1

        rowN += 3
        # print(rowN)
        button_ = Button(self.window_matInfo, text="Save", command=self.save_mat_info)
        button_.grid(row=rowN, column=1)
        Exitbutton_ = Button(self.window_matInfo, text="Exit", command=self.close_window)
        Exitbutton_.grid(row=rowN, column=2)

    def close_window(self):
        """

        :return:
        """
        self.window_matInfo.destroy()

    def close_window_read(self):
        """

        :return:
        """
        self.window_matInfo_read.destroy()

    def save_mat_info(self):
        """
        :return:
        """
        # print("##############################################################")
        outlines = []
        colN = 0
        rowN = 0
        count = 0
        newline = []
        index = 0
        outlines.append("\n")
        outlines.append(self.MaterialCards.material_cards[self.material_card]["Card_Title"][0])
        header_line = "\n$$"
        for j in range(len(self.curr_material_parameters)):
            if count == 8:# or j == (len(self.curr_material_parameters)):
                rowN += 2
                colN = 0
                count = 0
                line1 = "\n" + "".join(newline)# + "\n"
                value_line = header_line + line1
                outlines.append(value_line)
                header_line = "\n$$"
                newline = []

            if self.curr_material_parameters[j] == "":
                rowN += 2
                colN = 0
                count = 0
                line1 = "\n" + "".join(newline) #+ "\n"
                value_line = header_line + line1
                outlines.append(value_line)
                header_line = "\n$$"
                newline = []
                index += 1
                continue

            # print("[{}] {}: {}".format(index, self.curr_material_parameters[j], self.entry_list[index].get()))
            if self.curr_material_parameters[j] == 'mid':
                mid = self.entry_list[index].get().strip()

            if header_line == "\n$$":
                header_line += self.curr_material_parameters[j].rjust(8)
            else:
                header_line += self.curr_material_parameters[j].rjust(10)

            tmp_prop = self.entry_list[index].get().strip()
            newline.append(tmp_prop.rjust(10))
            if j == (len(self.curr_material_parameters)-1):
                line1 = "\n" + "".join(newline)# + "\n"
                value_line = header_line + line1
                outlines.append(value_line)
                header_line = "\n$$"

            count += 1
            colN += 1
            index += 1
        line = ",".join([mid, self.material_card])
        self.map_part_material.update({self.partID:line})
        # print(self.map_part_material)

        with open(self.material_out_file, 'a') as outFile:
            outFile.writelines(outlines)

    def get_material_type(self, material_type):
        """

        :return:
        """
        self.material_card = material_type
        print(self.material_card)

    def material_dropdown(self, *args):
        """

        :return:
        """
        self.material_card = self.material_cards_type.get()

    def get_part_ID(self, partID):
        self.partID = partID

    def part_dropdown(self, *args):
        """
        :return:
        """
        self.partID = self.partInfo[self.parts_info.get()]
        # self.part_option

    def get_part_ID2(self, partID):
        self.partID2 = partID

    def part_dropdown2(self, *args):
        """
        :return:
        """
        self.partID2 = self.partInfo[self.parts_info2.get()]
        # self.part_option

    def open_input(self):
        """

        :return:
        """
        print("Opening Input file !")
        import keywordSave
        temp_path = os.path.join(self.template_path, "open_save_key.tmp")
        input_path = os.path.abspath(self.input_keyword.Kfile)
        self.Kfile_new = os.path.join(os.path.split(input_path)[0], "out_key.k")
        print(self.Kfile_new)
        keywordSave.createSCL(temp_path, keyIn=input_path, keyOut=self.Kfile_new)

    def run_info(self):
        """
        :return:
        """
        print("Running Input file !")
        rowN = 0
        self.window_run = Toplevel(self.frame)

        self.ncpu_label = Label(self.window_run, text="NCPU", width=20)
        self.ncpu_label.grid(row=rowN, column=0)

        self.ncpu_entry = Entry(self.window_run, width=50)
        self.ncpu_entry.grid(row=rowN, column=1)
        self.ncpu_entry.insert(0,"12")

        rowN += 1
        self.memory_label = Label(self.window_run, text="MEMORY", width=20)
        self.memory_label.grid(row=rowN, column=0)

        self.memory_entry = Entry(self.window_run, width=50)
        self.memory_entry.grid(row=rowN, column=1)
        self.memory_entry.insert(0,"400")

        rowN += 1
        self.shell_button = Button(self.window_run, text="Run", command=self.run_input, fg='red')
        self.shell_button.grid(row=rowN, column=0)

    def run_input(self):
        """
        :return:
        """
        tmpFile = os.path.join(self.template_path,"run_windows.tmp")
        with open(tmpFile,"r") as f:
            s = f.read()

        s = s.replace("$INPUTFILEPATH$", self.input_keyword.Kfile)
        s = s.replace("$NCPU$", self.ncpu_entry.get())
        s = s.replace("$MEMORY$", self.memory_entry.get())
        runFile = os.path.join(self.project_path,"run.bat")
        with open(runFile,"w") as f:
            f.write(s)

        p = subprocess.Popen("run.bat", cwd=self.project_path, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        out,err = p.communicate()
        p.terminate()

    def createButton(self, frame_, buttonName, buttonMethod, rowN, colN, fg_='black', sticky_=N, bg_='lightgray', ipadx_=0):
        """

        :return:
        """
        # print(buttonName, sticky_)
        button_ = Button(frame_, text=buttonName, command=buttonMethod, fg=fg_, bg=bg_)
        button_.grid(row=rowN, column=colN, sticky=sticky_, ipadx=ipadx_)

    def createLabel(self, frame_, labelName, rowN, colN, width=10, fg_='black', sticky_=N, bg_="white", ipadx_=0):
        """

        :return:
        """
        label_ = Label(frame_, text=labelName, width=width, fg=fg_, bg=bg_)
        label_.grid(row=rowN, column=colN, sticky=sticky_, ipadx=ipadx_)

    def createEntry(self, frame_, value_, rowN, colN, widthV, fg_='black'):
        """

        :return:
        """

        entry_ = Entry(frame_, width=widthV, fg=fg_)
        entry_.grid(row=rowN, column=colN)
        entry_.insert(0, value_)

        return entry_

if __name__ == '__main__':

    root = Tk()
    application = VIEWER(root)
    root.mainloop()
