__author__ = 'Umesh'

import os, sys
from tkinter import *
from tkinter import filedialog

import volume_manager

class App:
    def __init__(self, master):

        self.score = {}
        self.testScore = {}
        self.master = master
        self.curveLength = 3
        self.frame = Frame(self.master)
        self.frame.pack()

        self.rowN = 0
        # input keyword file to update:
        self.loadInput = Button(self.frame, text="load_input", command=self.openFile)
        self.loadInput.grid(row=self.rowN, column=0)

        self.inputk = Entry(self.frame, width = 50)
        self.inputk.grid(row=self.rowN, column=2)
        self.rowN += 1

        self.matInput = Button(self.frame, text="mat_input", command=self.openFile2)
        self.matInput.grid(row=self.rowN, column=0)

        self.mat_inputk = Entry(self.frame, width = 50)
        self.mat_inputk.grid(row=self.rowN, column=2)

        self.rowN += 1
        # Load Curve details:
        loadCurveSize = Label(self.frame, text="LoadCurve_len")
        loadCurveSize.grid(row=self.rowN, column=0)
        # self.createConf()
        self.rowNo = Entry(self.frame, width=10)
        self.rowNo.grid(row=self.rowN, column=1)
        self.rowNo.insert(0, "2")
        self.createButton("Add_table", self.addTable, self.rowN, 2)
        # self.rowN = self.rowN+1
        print(self.rowN)

        # Load Type drop-down

        # Create a Tkinter variable for configuration selections
        self.loadType = "Topload"
        self.LoadingType = StringVar(self.frame)
        self.LoadingTypeList = set(sorted({'Topload', 'Sideclamp', 'Drop', 'Vibration'}))
        self.LoadingType.set('Topload')
        self.rowN = self.rowN+4
        popupMenu = OptionMenu(self.frame, self.LoadingType, *self.LoadingTypeList, command=self.getloadType)
        popupMenu.grid(row = self.rowN, column =1)
        self.LoadingType.trace('w', self.change_dropdown)

        # Update Material properties
        # E1, E2, GAB, GBC, xc, yc, xt, yt
        self.packageType = "Primary"
        self.packagingType = StringVar(self.frame)
        self.packagingTypeList = set(sorted({'Primary', 'Secondary', 'Tertiary'}))
        self.packagingType.set('Primary')

        # self.materialProp = set(sorted({'Primary', 'Secondary', 'Tertiary'}))



        self.rowN = self.rowN+4
        popupMenu = OptionMenu(self.frame, self.packagingType, *self.packagingTypeList, command=self.getPackagingType)
        popupMenu.grid(row = self.rowN, column =1)
        self.packagingType.trace('w', self.change_dropdown)
        self.createButton("Add_data", self.addData, self.rowN, 3)
        self.createButton("UpdateMaterial", self.update_material, self.rowN, 2)

        # Run Model
        self.rowN = self.rowN+4
        print(self.rowN)
        self.createButton("runModel", self.runModel, self.rowN, 1)
        # Quit
        self.rowN = self.rowN+1
        self.createButton("Quit", self.frame.quit, self.rowN, 1)

    def update_material(self, material_prop):
        """

        :return:
        """
        print("In material update function :")
        print(self.packageType)
        print(self.loadType)
        outlines = []
        mat_kfilepath = self.mat_inputk.get()
        out_filepath = os.path.join(os.path.split(mat_kfilepath)[0], "out_mat.k")
        partIds_ = range(1, 4+1)
        if self.packageType == "Primary":
            partIds = partIds_
        else:
            partIds = []
            pass

        with open(mat_kfilepath, 'r') as inFile:
            inlines = inFile.readlines()

        inMatBlock = False
        inNameBlock = False
        inIdBlock = False
        inMatPropBlock = False
        inOtherPropBlock = False
        inOtherBlock = False
        count = 0
        for line in inlines:
            if line.__contains__("*MAT"):
                # print("In Define block : \n", line)
                outlines.append(line)
                inMatBlock = True
                inNameBlock = True
                inOtherBlock = False
                continue
            if line.__contains__("*"):
                # print("In other block Title: \n", line)
                outlines.append(line)
                inMatBlock = False
                inOtherBlock = True
                continue
            if inOtherBlock:
                # print("In other block : \n", line)
                outlines.append(line)
                continue
            if inMatBlock:
                # print("### ----------------- ------------ In define curve block: \n", line)
                if line.startswith("$"):
                    outlines.append(line)
                    # inIdBlock = True
                    continue
                # else:
                if inNameBlock:
                    outlines.append(line)
                    # print(line)
                    inIdBlock = True
                    inNameBlock = False
                    continue
                if inIdBlock:
                    id_value = int(line[:10].strip())
                    print(id_value)
                    count += 1
                    inIdBlock = False
                    # print(partIds)
                    if id_value in partIds:
                        print(id_value)
                        print(line)
                        new_line = line[:20] + material_prop['E1'].rjust(10) + material_prop['E2'].rjust(10) + material_prop['E1'].rjust(10) + line[50:]
                        print(new_line)
                        outlines.append(new_line)
                        inMatPropBlock = True
                    else:
                        outlines.append(line)
                        inMatPropBlock = False
                        inOtherPropBlock = True
                    continue
                if inMatPropBlock:
                    print("in mat properties update block: ")
                    count += 1
                    print(count)
                    # if count == 2:
                    #     print(line)
                    #     new_line = line[:20] + material_prop['E1'].rjust(10) + material_prop['E2'].rjust(10) + material_prop['E1'].rjust(10) + line[50:]
                    #     print(new_line)
                    #     outlines.append(new_line)
                    if count == 2:
                        print(line)
                        new_line = material_prop['GAB'].rjust(10) + material_prop['GBC'].rjust(10) + material_prop['GAB'].rjust(10) + line[30:]
                        print(new_line)
                        outlines.append(new_line)
                        continue
                    if count == 6:
                        print(line)
                        new_line = material_prop['xc'].rjust(10) + material_prop['xt'].rjust(10) + material_prop['yc'].rjust(10) + material_prop['yt'].rjust(10) + line[40:]
                        print(new_line)
                        outlines.append(new_line)
                        count = 0
                        continue
                    else:
                        outlines.append(line)
                        continue
                if inOtherPropBlock:
                    outlines.append(line)
                    continue


        with open(out_filepath, 'w') as outFile:
            outFile.writelines(outlines)

    def change_dropdown(self, *args):
        self.loadType = self.LoadingType.get()
        self.packageType = self.LoadingType.get()

    def getloadType(self, loadType):
        """
        :return:
        """
        self.loadType = loadType
        print(self.loadType)

    def getPackagingType(self, packageType):
        """
        :return:
        """
        self.packageType = packageType
        print(self.packageType)

    def openFile(self):
        # fName = filedialog.askdirectory()
        fName = filedialog.askopenfilename()
        self.inputk.insert(0,fName)
        print("Tkinter is easy to use!")

    def openFile2(self):
        # fName = filedialog.askdirectory()
        fName = filedialog.askopenfilename()
        self.mat_inputk.insert(0,fName)
        print("Tkinter is easy to use!")

    def addTable(self):
        """

        :return:
        """
        rowN = 0
        self.window = Toplevel(self.frame)
        self.entry_list1 = []
        self.entry_list2 = []
        self.curveLength = int(self.rowNo.get())
        # entry1 = Entry(window, width=10)
        # entry1.grid(row=rowN, column=0)
        # entry1.insert(0, "3")

        for i in range(self.curveLength):
            rowN = i + 1
            print(rowN)
            self.entry_list1.append(Entry(self.window, width=10))
            self.entry_list1[i].grid(row=rowN, column=0)
            self.entry_list1[i].insert(0,0)

            self.entry_list2.append(Entry(self.window, width=10))
            self.entry_list2[i].grid(row=rowN, column=1)
            self.entry_list2[i].insert(0,0)

        rowN = rowN + 1
        print(rowN)
        button_ = Button(self.window, text="Save", command=self.save_data)
        button_.grid(row=rowN, column=1)

    def addData(self):
        """

        :return:
        """
        rowN = 0
        self.window2 = Toplevel(self.frame)
        self.entry_list1 = []
        self.entry_list2 = []

        self.materialProp = ['E1', 'E2', 'GAB', 'GBC', 'xc', 'xt', 'yc', 'yt']
        self.entry_list = []
        self.label_list = []
        for i in range(len(self.materialProp)):
            rowN = i + 1
            print(rowN)
            self.entry_list.append(Entry(self.window2, width=50))
            self.entry_list[i].grid(row=rowN, column=2)
            self.entry_list[i].insert(0,0)

            self.label_list.append(Label(self.window2, text=self.materialProp[i], width=20))
            self.label_list[i].grid(row=rowN, column=0)

        rowN = rowN + 1
        print(rowN)
        button_ = Button(self.window2, text="Save", command=self.save_data2)
        button_.grid(row=rowN, column=1)

    def save_data2(self):
        """

        :return:
        """
        print("In the save data method !")
        self.properties = {}
        for i in range(len(self.materialProp)):
            self.properties.update({self.materialProp[i]: self.entry_list[i].get()})

        print(self.properties)
        self.window2.destroy()
        kfilepath = self.mat_inputk.get()
        self.update_material(self.properties)

    def save_data(self):
        """

        :return:
        """
        print("In the save data method !")
        self.loads = []
        self.times = []
        for i in range(self.curveLength):
            self.loads.append(self.entry_list1[i].get())
            self.times.append(self.entry_list2[i].get())

        print(self.loads)
        print(self.times)
        self.window.destroy()
        kfilepath = self.inputk.get()
        self.update_load_curve(kfilepath, self.loads, self.times)

    def runModel(self):
        """

        :return:
        """
        print("In run model method")

    def createButton(self, buttonName, buttonMethod, rowN, colN):
        """

        :return:
        """
        button_ = Button(self.frame, text=buttonName, command=buttonMethod)
        button_.grid(row=rowN, column=colN)

    def createLabel(self, labelName, rowN, colN):
        """

        :return:
        """
        label_ = Label(self.frame, text=labelName)
        label_.grid(row=rowN, column=colN)

    def createEntry(self, value_, widthV, rowN, colN):
        """

        :return:
        """

        entry_ = Entry(self.frame, width=widthV)
        entry_.grid(row=rowN, column=colN)
        entry_.insert(0, value_)

        return entry_

    def update_load_curve(self, filepath, loadvalues = [], timevalues = []):
        """

        :param filepath:
        :param loadvalues:
        :param timevalues:
        :return:
        """
        import os

        print(filepath)
        out_filepath = os.path.join(os.path.split(filepath)[0], "out_control_cards.k")
        with open(filepath, 'r') as inFile:
            inlines = inFile.readlines()

        outlines = []
        print(filepath)
        inDefineCurveBlock = False
        inOtherBlock = False
        inCurveIdBlock = False
        inCurveValueBlock = False
        count = 0
        for line in inlines:
            if line.__contains__("*DEFINE"):
                # print("In Define block : \n", line)
                outlines.append(line)
                inDefineCurveBlock = True
                inOtherBlock = False
                continue
            if line.__contains__("*"):
                # print("In other block Title: \n", line)
                outlines.append(line)
                inDefineCurveBlock = False
                inOtherBlock = True
                continue
            if inOtherBlock:
                # print("In other block : \n", line)
                outlines.append(line)
                continue
            if inDefineCurveBlock:
                # print("### ----------------- ------------ In define curve block: \n", line)
                if line.startswith("$"):
                    outlines.append(line)
                    inCurveIdBlock = True
                    continue
                # else:
                if inCurveIdBlock:
                    outlines.append(line)
                    # print(line)
                    inCurveValueBlock = True
                    inCurveIdBlock = False
                    continue
                if inCurveValueBlock:
                    print(line)
                    load = self.loads[count]
                    time = self.times[count]
                    new_line = str(load).rjust(20) + str(time).rjust(20) + "\n"
                    print(new_line)
                    outlines.append(new_line)
                    count += 1
                    continue

        with open(out_filepath, 'w') as outFile:
            outFile.writelines(outlines)
        print(loadvalues)
        print(timevalues)


if __name__ == '__main__':

    root = Tk()
    app = App(root)
    root.mainloop()

