__author__ = 'Umesh'

import os, sys, csv, re
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import json
import subprocess

# Import local modules
import material_cards
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

        self.rowN = 0
        self.project_path_button = self.createButton(self.frame, "ProjectPath", self.open_projectPath, self.rowN, 1)
        self.project_path = r"D:\Umesh\AxiomProject\VEOL_GUI\Rakesh_Project\Test1"
        self.project_path_entry = self.createEntry(self.frame, self.project_path, self.rowN, 2, widthV=50)
        self.createButton(self.frame, "Create_Input", self.create_input, self.rowN, 3, fg_='brown')

        self.rowN += 1
        # Material Cards Info
        self.MaterialCards = material_cards.MaterialCards()
        self.material_cards_type = StringVar(self.frame)
        self.material_card = self.MaterialCards.material_cards_type[0]
        self.material_cards_type_list = set(sorted(self.MaterialCards.material_cards_type))
        self.material_cards_type.set(self.material_card)

        popupMenu = OptionMenu(self.frame, self.material_cards_type, *self.material_cards_type_list, command=self.get_material_type)
        popupMenu.grid(row = self.rowN, column=1)
        self.material_cards_type.trace('w', self.material_dropdown)

        self.add_new_material_card_button = Button(self.frame, text="AddNewMaterial", command=self.add_new_material_card)
        self.add_new_material_card_button.grid(row=self.rowN, column=2, sticky=W)

        self.read_material_button = Button(self.frame, text="ReadMaterial", command=self.read_material)
        self.read_material_button.grid(row=self.rowN, column=2)#, sticky=W)

        self.add_material_info_button = Button(self.frame, text="AddMaterialPara", command=self.add_material_info)
        self.add_material_info_button.grid(row=self.rowN, column=3, sticky=W)


        self.rowN += 1
        # Open Input
        self.createButton(self.frame, "Open Input", self.open_input, self.rowN, 1, fg_='red')
        # Run Input
        self.createButton(self.frame, "Run", self.run_info, self.rowN, 2, fg_='red')
        # Exit
        self.createButton(self.frame, "Exit", self.frame.quit, self.rowN, 3, fg_='red')

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

        self.material_out_file_name = "Mat_out.k"
        self.material_out_file = os.path.join(self.project_path, self.material_out_file_name)
        with open(self.material_out_file, 'w') as outFile:
            outFile.write("")

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

        # v0 = StringVar()
        # e0 = Entry(root, textvariable = v0, state = 'readonly')
        # v0.set('Select')

        parameter_label = StringVar()
        parameter_label_entry = Entry(self.window_newMat, textvariable=parameter_label, state='readonly')
        parameter_label.set('PARAMETER_LABEL')
        parameter_label_entry.grid(row=rowN, column=0)
        # self.createLabel(self.window_newMat, "PARAMETER_LABEL", rowN, 0, width=20)
        parameter_defaults = StringVar()
        parameter_defaults_entry = Entry(self.window_newMat, textvariable=parameter_defaults, state='readonly')
        parameter_defaults.set('DEFAULTS')
        parameter_defaults_entry.grid(row=rowN, column=1)
        # self.createLabel(self.window_newMat, "DEFAULTS", rowN, 1, width=20)
        parameter_freq = StringVar()
        parameter_freq_entry = Entry(self.window_newMat, textvariable=parameter_freq, state='readonly')
        parameter_freq.set('FREQUENCY')
        parameter_freq_entry.grid(row=rowN, column=2)
        # self.createLabel(self.window_newMat, "FREQUENCY", rowN, 2, width=20)
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
        count = 0
        self.read_material_cards_type_list = []
        self.read_material_parameters = {}
        self.read_material_parameters_tmp = []

        for line in inlines:
            if line.startswith("*"):
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
        print(self.read_material_cards_type_list)
        self.rowN += 3
        self.read_material_card = self.read_material_cards_type_list[0]
        self.read_material_card_set = StringVar(self.frame)
        popupMenu = OptionMenu(self.frame, self.read_material_card_set, *self.read_material_cards_type_list, command=self.get_read_material_type)
        popupMenu.grid(row = self.rowN, column=1)
        self.read_material_card_set.set(self.read_material_cards_type_list[0])
        self.read_material_card_set.trace('w', self.read_material_dropdown)
        self.editMatData = self.createButton(self.frame, "Show", self.show_material, self.rowN, 2, sticky_=W)

    def get_read_material_type(self, material_card_type):
        """
        :return:
        """
        self.read_material_card = material_card_type

    def read_material_dropdown(self):
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
        for j in range(len(self.curr_material_parameters)):
            if count == 8:# or j == (len(self.curr_material_parameters)):
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
                line1 = "\n" + "".join(newline)# + "\n"
                outlines.append(line1)

            count += 1
            colN += 1
            index += 1

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

    def open_input(self):
        """

        :return:
        """

    def run_info(self):
        """

        :return:
        """

    def createButton(self, frame_, buttonName, buttonMethod, rowN, colN, fg_='black', sticky_=N):
        """

        :return:
        """
        # print(buttonName, sticky_)
        button_ = Button(frame_, text=buttonName, command=buttonMethod, fg=fg_)
        button_.grid(row=rowN, column=colN, sticky=sticky_)

    def createLabel(self, frame_, labelName, rowN, colN, width=10, fg_='black'):
        """

        :return:
        """
        label_ = Label(frame_, text=labelName, width=width, fg=fg_)
        label_.grid(row=rowN, column=colN)

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
