__author__ = 'Umesh'

import os, sys
from tkinter import *
from tkinter import filedialog
import material_prop as mat_prop
import create_input as create_input
from tkinter import messagebox
import subprocess


class App:
    def __init__(self, master):


        self.partInfo = {}
        self.curveInfo = {}
        self.BPM = ""
        self.curveTitleList = []
        self.curveIdList = []
        self.curveValList = []
        self.master = master
        self.curveLength = 2
        self.frame = Frame(self.master)
        self.frame.pack()
        self.rowN = 0
        self.curveLines = []
        self.sectionLines = []
        self.curveNo = 0
        self.inShellSection = False
        self.inSolidSection = False
        self.inMat54 = False
        self.inMat24 = False
        self.inRigid = False
        self.memory = "400M"
        self.ncpu = "12"
        # self.projectPath = r"D:\Umesh\AxiomProject\VEOL_GUI\TestCase2"
        baseDir = os.path.dirname(sys.argv[0])

        # print()
        self.template_path = os.path.join(baseDir, "Template")
        self.case_path = os.path.join(baseDir, "Rakesh_Project", "Output")
        # Create a Tkinter variable for configuration selections


        # create input keyword
        self.rowN += 1
        self.ProjectPath = Button(self.frame, text="ProjectPath", command=self.openFolder)
        self.ProjectPath.grid(row=self.rowN, column=1)
        self.ProjectPathEntry = Entry(self.frame, width = 70)
        self.ProjectPathEntry.grid(row=self.rowN, column=2)
        self.ProjectPathEntry.insert(0, self.case_path)
        self.projectPath = self.case_path
        self.createButton("Create Input", self.create_input_keyword, self.rowN, 3)
        self.rowN += 1

        # Read Input Mesh
        self.InputMeshPath = Button(self.frame, text="MeshPath", command=self.openFile)
        self.InputMeshPath.grid(row=self.rowN, column=1)
        self.InputMeshPathEntry = Entry(self.frame, width = 70)
        self.InputMeshPathEntry.grid(row=self.rowN, column=2)
        self.createButton("Show Info", self.show_info, self.rowN, 3)
        self.rowN += 1

        # Material Properties
        self.matType = StringVar(self.frame)
        self.materialType = "MAT54/55"
        self.matTypeList = set(sorted({'MAT54/55', 'RIGID', 'MAT24'}))
        self.matType.set('MAT54/55')
        self.mat55_template = os.path.join(self.template_path, "mat55.k")
        self.mat24_template = os.path.join(self.template_path, "mat24.k")
        self.rigid_template = os.path.join(self.template_path, "rigid.k")
        self.mapMat = {'MAT54/55':self.mat55_template, 'RIGID':self.rigid_template, 'MAT24':self.mat24_template}
        popupMenu = OptionMenu(self.frame, self.matType, *self.matTypeList, command=self.getMatType)
        popupMenu.grid(row = self.rowN, column=1)
        self.matType.trace('w', self.change_dropdown)

        self.template = Entry(self.frame, width = 70)
        self.template.grid(row=self.rowN, column=2)
        self.template.insert(0, self.mat55_template)
        self.createButton("Add_data", self.addData, self.rowN, 3)
        self.rowN += 1

        self.section_label = Label(self.frame, text="Section", width=20, fg='red')
        self.section_label.grid(row=self.rowN, column=1, sticky=W)

        self.shell_button = Button(self.frame, text="Shell", command=self.shell_button_click)
        self.shell_button.grid(row=self.rowN, column=2, sticky=W)
        self.solid_button = Button(self.frame, text="Solid", command=self.solid_button_click)
        self.solid_button.grid(row=self.rowN, column=2)#, sticky="nsew")

        self.rowN += 1

        # Control cards

        self.loadType = StringVar(self.frame)
        self.loadingType = "Topload"
        self.loadTypeList = set(sorted({'Topload', 'Sideclamp', 'Vibration', 'Drop'}))
        self.loadType.set('Topload')
        self.controlCards_template = os.path.join(self.template_path, "control_cards.k")
        self.controlCards_topload_template = os.path.join(self.template_path, "control_cards_topload.k")
        self.mapControlCards = {'Topload':self.controlCards_topload_template, 'Sideclamp':self.controlCards_template, 'Vibration':self.controlCards_template, 'Drop':self.controlCards_template}
        popupMenu = OptionMenu(self.frame, self.loadType, *self.loadTypeList, command=self.getLoadType)
        popupMenu.grid(row = self.rowN, column=1)
        self.loadType.trace('w', self.change_dropdown)
        self.template_controlcards = Entry(self.frame, width = 70)
        self.template_controlcards.grid(row=self.rowN, column=2)
        self.template_controlcards.insert(0, self.mapControlCards[self.loadingType])# self.controlCards_template)
        self.createButton("Add_data", self.addData_controlCards, self.rowN, 3)

        # Open Input
        self.rowN += 1
        self.createButton("Open Input", self.open_input, self.rowN, 1, fg='red')

        # Run Input
        # self.rowN += 1
        self.createButton("Run", self.run_input, self.rowN, 2, fg='red')

        # Exit
        # self.rowN += 1
        self.createButton("Exit", self.frame.quit, self.rowN, 3, fg='red')

    def run_input(self):
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
        self.shell_button = Button(self.window_run, text="Run", command=self.run_input2, fg='red')
        self.shell_button.grid(row=rowN, column=0)

    def run_input2(self):
        """

        :return:
        """
        tmpFile = os.path.join(self.template_path,"run_windows.tmp")
        with open(tmpFile,"r") as f:
            s = f.read()

        s = s.replace("$INPUTFILEPATH$", self.input1.Kfile)
        s = s.replace("$NCPU$", self.ncpu_entry.get())
        s = s.replace("$MEMORY$", self.memory_entry.get())
        runFile = os.path.join(self.projectPath,"run.bat")
        with open(runFile,"w") as f:
            f.write(s)

        p = subprocess.Popen("run.bat", cwd=self.projectPath, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        out,err = p.communicate()


    def create_input_keyword(self):
        """

        :return:
        """
        self.projectPath = self.ProjectPathEntry.get()
        self.input1 = create_input.CreateInput()
        self.input1.create_input_k(self.projectPath)

        print(self.projectPath)
        self.mat_out = os.path.join(self.projectPath, "mat.k")
        with open(self.mat_out, 'w') as outFile:
            outFile.write("")


        # def generateRunScript_new(self):
        # """
        #
        # :return:
        # """

    def open_input(self):
        """

        :return:
        """
        print("Opening Input file !")
        import keywordSave
        temp_path = os.path.join(self.template_path, "open_save_key.tmp")
        input_path = os.path.abspath(self.input1.Kfile)
        self.Kfile_new = os.path.join(os.path.split(input_path)[0], "out_key.k")
        print(self.Kfile_new)
        keywordSave.createSCL(temp_path, keyIn=input_path, keyOut=self.Kfile_new)

    def openFolder(self):
        fName = filedialog.askdirectory()
        self.ProjectPathEntry.delete(0,'end')
        self.ProjectPathEntry.insert(0,fName)

    def openFile(self):
        fName = filedialog.askopenfilename()
        self.InputMeshPathEntry.delete(0,'end')
        self.InputMeshPathEntry.insert(0,fName)

    def show_info(self):
        """

        :return:
        """
        self.meshFile = self.InputMeshPathEntry.get()

        with open(self.meshFile) as readFile:
            readlines = readFile.readlines()

        inOtherBlock = False
        inPartBlock = False
        inTitleBlock = False
        inPartIdBlock = False
        for line in readlines:
            count = 0
            if line.startswith("*PART"):
                inPartBlock = True
                inTitleBlock = True
                inOtherBlock = False
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
                    inPartIdBlock = False
                    inTitleBlock = True
                    continue
            if inOtherBlock:
                continue
        print(self.partInfo)

    def addData(self):
        """

        :return:
        """

        print(self.template.get())
        template_path = self.template.get()
        with open(template_path, 'r') as inFile:
            self.template_lines = inFile.readlines()

        rowN = 0
        self.window2 = Toplevel(self.frame)
        self.material1 = mat_prop.MaterialProp()
        self.mat54_prop = ['Title', 'Id', 'Density', 'E1', 'E2', 'Mu', 'GAB', 'GBC', 'FBRT', 'YCFAC', 'XC', 'XT', 'YC', 'YT']#, 'SECTION']
        self.mat20_prop = ['Title', 'Id', 'Density', 'E1', 'Mu', 'CMO', 'CON1', 'CON2']#, 'SECTION']
        self.mat24_prop = ['Title', 'Id', 'Density', 'E1', 'Mu', 'SIGY', 'ETAN', 'FAIL', 'LCSS']#, 'SECTION']

        # 'MAT54/55', 'RIGID'

        if self.materialType == "MAT54/55":
            self.inMat54 = True
            self.inMat24 = False
            self.inRigid = False
            self.materialProp = self.mat54_prop
        elif self.materialType == "RIGID":
            self.inMat54 = False
            self.inMat24 = False
            self.inRigid = True
            self.materialProp = self.mat20_prop
        elif self.materialType == "MAT24":
            self.inMat54 = False
            self.inMat24 = True
            self.inRigid = False
            self.materialProp = self.mat24_prop
        else:
            messagebox.showerror("Error", "Select correct Material Card :")
        self.entry_list = []
        self.label_list = []
        for i in range(len(self.materialProp)):
            rowN = i + 1
            # print(rowN)

            # if self.materialProp[i] == 'SECTION':
            #     self.label_list.append(Label(self.window2, text=self.materialProp[i], width=20))
            #     self.label_list[i].grid(row=rowN, column=0)
            #
            #     self.shell_button = Button(self.window2, text="Shell", command=self.shell_button_click)
            #     self.shell_button.grid(row=rowN, column=1)
            #     self.solid_button = Button(self.window2, text="Solid", command=self.solid_button_click)
            #     self.solid_button.grid(row=rowN, column=2)
            #     continue
            #
            self.entry_list.append(Entry(self.window2, width=50))
            self.entry_list[i].grid(row=rowN, column=2)
            self.entry_list[i].insert(0,self.material1.material_prop[self.materialProp[i]])

            self.label_list.append(Label(self.window2, text=self.materialProp[i], width=20))
            self.label_list[i].grid(row=rowN, column=0)

        rowN = rowN + 1
        # print(rowN)
        add_button = Button(self.window2, text="Add", command=self.add_new)
        add_button.grid(row=rowN, column=1)
        button_ = Button(self.window2, text="Save", command=self.save_data2)
        button_.grid(row=rowN, column=2)
        Exitbutton_ = Button(self.window2, text="Exit", command=self.close_window)
        Exitbutton_.grid(row=rowN, column=3)

    def shell_button_click(self):
        """

        :return:
        """
        self.inShellSection = True
        self.inSolidSection = False
        rowN = 0
        self.window2_shell = Toplevel(self.frame)

        self.shell_section_prop = ['TITLE', 'SECID', 'ELFORM', 'SHRF', 'NIP', 'PROPT', 'QR/IRID', 'ICOMP', 'SETYP', 'T1', 'NLOC']

        self.shell_entry_list = []
        self.shell_label_list = []
        for i in range(len(self.shell_section_prop)):
            rowN = i + 1
            # print(rowN)
            self.shell_label_list.append(Label(self.window2_shell, text=self.shell_section_prop[i], width=20))
            self.shell_label_list[i].grid(row=rowN, column=0)

            self.shell_entry_list.append(Entry(self.window2_shell, width=50))
            self.shell_entry_list[i].grid(row=rowN, column=2)
            self.shell_entry_list[i].insert(0,0)

        rowN = rowN + 1
        # print(rowN)
        add_button = Button(self.window2_shell, text="Add", command=self.section_add_new)
        add_button.grid(row=rowN, column=1)
        button_ = Button(self.window2_shell, text="Save", command=self.section_save_data)
        button_.grid(row=rowN, column=2)
        Exitbutton_ = Button(self.window2_shell, text="Exit", command=self.section_close_window)
        Exitbutton_.grid(row=rowN, column=3)

    def solid_button_click(self):
        """

        :return:
        """
        self.inSolidSection = True
        self.inShellSection = False
        rowN = 0
        self.window2_solid = Toplevel(self.frame)

        self.solid_section_prop = ['TITLE', 'SECID', 'ELFORM', 'AET']

        self.solid_entry_list = []
        self.solid_label_list = []
        for i in range(len(self.solid_section_prop)):
            rowN = i + 1
            # print(rowN)
            self.solid_label_list.append(Label(self.window2_solid, text=self.solid_section_prop[i], width=20))
            self.solid_label_list[i].grid(row=rowN, column=0)

            self.solid_entry_list.append(Entry(self.window2_solid, width=50))
            self.solid_entry_list[i].grid(row=rowN, column=2)
            self.solid_entry_list[i].insert(0,0)

        rowN = rowN + 1
        # print(rowN)
        add_button = Button(self.window2_solid, text="Add", command=self.section_add_new)
        add_button.grid(row=rowN, column=1)
        button_ = Button(self.window2_solid, text="Save", command=self.section_save_data)
        button_.grid(row=rowN, column=2)
        Exitbutton_ = Button(self.window2_solid, text="Exit", command=self.section_close_window)
        Exitbutton_.grid(row=rowN, column=3)

    def section_add_new(self):
        """
                        *SECTION_SHELL
                        $HMNAME PROPERTIES         3thk
                                 3        16       1.0         2
                               3.1       3.1       3.1       3.1
                        *SECTION_SOLID
                        $HMNAME PROPERTIES         2sld
                                 2         2
        :return:
        """
        # ['TITLE', 'SECID', 'ELFORM', 'SHRF', 'NIP', 'PROPT', 'QR/IRID', 'ICOMP', 'SETYP', 'T1', 'NLOC']

        if self.inShellSection:
            self.sectionTitle = self.shell_entry_list[0].get()
            self.sectId = self.shell_entry_list[1].get()
            self.elform = self.shell_entry_list[2].get()
            self.shrf = self.shell_entry_list[3].get()
            self.nip = self.shell_entry_list[4].get()
            self.propt = self.shell_entry_list[5].get()
            self.qr = self.shell_entry_list[6].get()
            self.icomp = self.shell_entry_list[7].get()
            self.setyp = self.shell_entry_list[8].get()
            self.thk = self.shell_entry_list[9].get()
            self.nloc = self.shell_entry_list[10].get()

            tmp_section_lines = "*SECTION_SHELL\n" \
                                "$HMNAME PROPERTIES         3%s\n" \
                                "%s%s%s%s\n" \
                                "%s%s%s%s%s\n"%(str(self.sectionTitle).rjust(10), self.sectId.rjust(10), self.elform.rjust(10), self.shrf.rjust(10), self.nip.rjust(10),
                                                self.thk.rjust(10), self.thk.rjust(10), self.thk.rjust(10), self.thk.rjust(10), self.nloc.rjust(10))
            # print(tmp_section_lines)

            self.sectionLines.append(tmp_section_lines)

        elif self.inSolidSection:
            # self.solid_section_prop = ['TITLE', 'SECID', 'ELFORM', 'AET']
            self.sectionTitle = self.solid_entry_list[0]
            self.sectId = self.solid_entry_list[1]
            self.elform = self.solid_entry_list[2]
            self.aet = self.solid_entry_list[3]

            tmp_section_lines = "*SECTION_SOLID\n" \
                                "$HMNAME PROPERTIES         3%s\n" \
                                "%s%s%s\n"%(str(self.sectionTitle).rjust(10), self.sectId.rjust(10), self.elform.rjust(10), self.aet.rjust(10))
            # print(tmp_section_lines)

            self.sectionLines.append(tmp_section_lines)

        else:
            messagebox.showerror("ERROR", "Not selected section type :")


    def section_save_data(self):
        """

        :return:
        """
        # ['TITLE', 'SECID', 'ELFORM', 'SHRF', 'NIP', 'PROPT', 'QR/IRID', 'ICOMP', 'SETYP', 'T1']

        if self.inShellSection:
            self.sectionTitle = self.shell_entry_list[0].get()
            self.sectId = self.shell_entry_list[1].get()
            self.elform = self.shell_entry_list[2].get()
            self.shrf = self.shell_entry_list[3].get()
            self.nip = self.shell_entry_list[4].get()
            self.propt = self.shell_entry_list[5].get()
            self.qr = self.shell_entry_list[6].get()
            self.icomp = self.shell_entry_list[7].get()
            self.setyp = self.shell_entry_list[8].get()
            self.thk = self.shell_entry_list[9].get()
            self.nloc = self.shell_entry_list[10].get()
            tmp_section_lines = "*SECTION_SHELL\n" \
                                "$HMNAME PROPERTIES         3%s\n" \
                                "%s%s%s%s\n" \
                                "%s%s%s%s%s\n"%(str(self.sectionTitle).rjust(10), self.sectId.rjust(10), self.elform.rjust(10), self.shrf.rjust(10), self.nip.rjust(10),
                                                self.thk.rjust(10), self.thk.rjust(10), self.thk.rjust(10), self.thk.rjust(10), self.nloc.rjust(10))
            # print(tmp_section_lines)

            self.sectionLines.append(tmp_section_lines)
            self.window2_shell.destroy()
            with open(self.mat_out, 'a') as outFile:
                outFile.writelines(tmp_section_lines)

        elif self.inSolidSection:
            # self.solid_section_prop = ['TITLE', 'SECID', 'ELFORM', 'AET']
            self.sectionTitle = self.solid_entry_list[0].get()
            self.sectId = self.solid_entry_list[1].get()
            self.elform = self.solid_entry_list[2].get()
            self.aet = self.solid_entry_list[3].get()

            tmp_section_lines = "*SECTION_SOLID\n" \
                                "$HMNAME PROPERTIES         3%s\n" \
                                "%s%s%s\n"%(str(self.sectionTitle).rjust(10), self.sectId.rjust(10), self.elform.rjust(10), self.aet.rjust(10))
            # print(tmp_section_lines)

            self.sectionLines.append(tmp_section_lines)
            self.window2_solid.destroy()
            with open(self.mat_out, 'a') as outFile:
                outFile.writelines(tmp_section_lines)
        else:
            messagebox.showerror("ERROR", "Not selected section type :")

    def section_close_window(self):
        """

        :return:
        """

        if self.inShellSection:
            self.window2_shell.destroy()
        elif self.inSolidSection:
            self.window2_solid.destroy()


    def close_window(self):
        """

        :return:
        """
        self.window2.destroy()

    def close_window_CC(self):
        """

        :return:
        """
        self.window_CC.destroy()


    def addData_controlCards(self):
        """

        :return:
        """

        print(self.template_controlcards.get())
        template_path = self.template_controlcards.get()
        with open(template_path, 'r') as inFile:
            self.template_lines_control_cards = inFile.readlines()

        self.control_cards_out = os.path.join(self.projectPath, "control_cards.k")
        with open(self.control_cards_out, 'w') as outFile:
            outFile.write("")

        rowN = 0
        self.window_CC = Toplevel(self.frame)

        if self.loadingType == "Topload":
            self.label_CC = ['EndTime', 'DT', 'DefineCurve', 'BoundaryPrescribedMotion', 'LoadBodyY', 'LoadBodyParts']#]
        else:
            self.label_CC = ['EndTime', 'TimeStepScaleFact', 'DT2MS', 'TiedProj', 'DT', 'D3Dump', 'DefineCurve',
                         'BoundaryPrescribedMotion', 'LoadBodyY', 'LoadBodyParts']#]

        self.label_CC_val = [60, 0.9, 1e-3, 1, 0.60, 6000, 2]
        self.entry_list_CC = []
        self.label_list_CC = []
        for i in range(len(self.label_CC)):
            rowN = i + 1
            # print(rowN)
            self.label_list_CC.append(Label(self.window_CC, text=self.label_CC[i], width=20))
            self.label_list_CC[i].grid(row=rowN, column=0)

            if self.label_CC[i] == 'DefineCurve':
                # print("row id at define curve :", rowN)
                add_table = Button(self.window_CC, text="Add Table", command=self.add_table)
                add_table.grid(row=rowN, column=2, sticky=W)
                show_table = Button(self.window_CC, text="Show Curve", command=self.show_curve)
                show_table.grid(row=rowN, column=3, sticky=W)
                continue

            if self.label_CC[i] == "BoundaryPrescribedMotion":
                # print()
                add_BPM = Button(self.window_CC, text="Add BPM", command=self.add_BPM)
                add_BPM.grid(row=rowN, column=2, sticky=W)
                continue

            if self.label_CC[i] == "LoadBodyY":
                # print()
                add_BPM = Button(self.window_CC, text="Add", command=self.add_loadBodyY)
                add_BPM.grid(row=rowN, column=2, sticky=W)
                continue

            if self.label_CC[i] == "LoadBodyParts":
                # print()
                add_BPM = Button(self.window_CC, text="Add", command=self.add_loadBodyParts)
                add_BPM.grid(row=rowN, column=2, sticky=W)
                continue


            self.entry_list_CC.append(Entry(self.window_CC, width=50))
            self.entry_list_CC[i].grid(row=rowN, column=2)
            self.entry_list_CC[i].insert(0,self.label_CC_val[i])


        rowN = rowN + 1
        # print(rowN)
        button_ = Button(self.window_CC, text="Save", command=self.save_data_CC)
        button_.grid(row=rowN, column=2, sticky=W)

        button_ = Button(self.window_CC, text="Exit", command=self.close_window_CC)
        button_.grid(row=rowN, column=2)#, sticky=W)

        rowN = rowN + 1
        showButton_ = Button(self.window_CC, text="Show", command=self.show_curve_info)
        showButton_.grid(row=rowN, column=2)#, sticky=W)

    def add_loadBodyY(self):
        """

        :return:
        """
        rowN = 0
        self.LBY_prop = {'Title':"Title", 'LCID':1, 'SF':1.0}
        self.window_LBY = Toplevel(self.frame)
        self.entry_list_LBY = []
        self.label_list_LBY = []
        self.partInfoList = StringVar(self.frame)
        self.curveInfoList = StringVar(self.frame)
        for key,value in self.LBY_prop.items():#range(len(self.BPM_prop)):
            # print(rowN)
            self.label_list_LBY.append(Label(self.window_LBY, text=key, width=20))
            self.label_list_LBY[rowN].grid(row=rowN, column=0)

            if key == "LCID":
                popupMenu = OptionMenu(self.window_LBY, self.curveInfoList, *self.curveInfo.keys(), command=self.getCurveId)
                popupMenu.grid(row = rowN, column=2)
                self.curveInfoList.set(list(self.curveInfo.keys())[0])
                self.curveInfoList.trace('w', self.change_dropdown2)
                self.entry_list_LBY.append(Entry(self.window_LBY, width=50))
                # print(rowN)
                rowN += 1
                continue

            # print(rowN)
            self.entry_list_LBY.append(Entry(self.window_LBY, width=50))
            self.entry_list_LBY[rowN].grid(row=rowN, column=2)
            self.entry_list_LBY[rowN].insert(0,value)
            rowN += 1

        rowN = rowN + 1
        button_ = Button(self.window_LBY, text="Save", command=self.save_LBY)
        button_.grid(row=rowN, column=1)
        rowN = rowN + 1
        clearEntry = Button(self.window_LBY, text="Exit", command=self.exit_LBY)
        clearEntry.grid(row=rowN, column=1)

    def save_LBY(self):
        """
            *LOAD_BODY_Y
            $HMNAME LOADCOLS       1$TITLE$
            $HWCOLOR LOADCOLS       1      11
            $#    lcid        sf    lciddr        xc        yc        zc       cid
            $LCID$$SF$         0       0.0       0.0       0.0         0

        :return:
        """

        print("In save BPM function: ")
        # print(self.partInfo[self.partInfo_Id])
        print(self.curveInfo[self.curveInfo_Id])
        # part_id = self.partInfo[self.partInfo_Id]
        curve_id = self.curveInfo[self.curveInfo_Id]

        self.LBY = "*LOAD_BODY_Y\n" \
                   "$HMNAME LOADCOLS       1%s\n" \
                   "$HWCOLOR LOADCOLS       2       4\n" \
                   "%s%s         0       0.0       0.0       0.0         0"%(self.entry_list_LBY[0].get().rjust(10),
                                                                               curve_id.rjust(10),
                                                                               self.entry_list_LBY[2].get().rjust(10),
                                                                               )
        # print(self.LBY)

    def exit_LBY(self):
        """

        :return:
        """

        self.window_LBY.destroy()

    def add_loadBodyParts(self):
        """
        :return:
        """

        rowN = 0
        self.LBP_prop = {'Title':"Title", 'PSID':1}
        self.window_LBP = Toplevel(self.frame)
        self.entry_list_LBP = []
        self.label_list_LBP = []
        self.partInfoList = StringVar(self.frame)
        self.curveInfoList = StringVar(self.frame)
        for key,value in self.LBP_prop.items():#range(len(self.BPM_prop)):
            # print(rowN)
            self.label_list_LBP.append(Label(self.window_LBP, text=key, width=20))
            self.label_list_LBP[rowN].grid(row=rowN, column=0)
            # print(rowN)
            self.entry_list_LBP.append(Entry(self.window_LBP, width=50))
            self.entry_list_LBP[rowN].grid(row=rowN, column=2)
            self.entry_list_LBP[rowN].insert(0,value)
            rowN += 1

        rowN = rowN + 1
        button_ = Button(self.window_LBP, text="Save", command=self.save_LBP)
        button_.grid(row=rowN, column=1)
        rowN = rowN + 1
        clearEntry = Button(self.window_LBP, text="Exit", command=self.exit_LBP)
        clearEntry.grid(row=rowN, column=1)

    def save_LBP(self):
        """
            *LOAD_BODY_PARTS
            $HMNAME LOADCOLS       1$TITLE$
            $HWCOLOR LOADCOLS       1      11
            $#    psid
            $PSID$

        :return:
        """

        print("In save Load Body Parts function: ")

        self.LBP = "*LOAD_BODY_PARTS\n" \
                   "$HMNAME LOADCOLS       1%s\n" \
                   "$HWCOLOR LOADCOLS       2       4\n" \
                   "%s         0       0.0       0.0       0.0         0"%(self.entry_list_LBP[0].get().rjust(10),
                                                                             self.entry_list_LBP[1].get().rjust(10)
                                                                            )

    def exit_LBP(self):
        """

        :return:
        """

        self.window_LBP.destroy()

    def show_curve(self):
        """

        :return:
        """

        self.window_CC3 = Toplevel(self.frame)
        text_ = Text(self.window_CC3)

        tmp_lines = []
        for i in range(len(self.curveTitleList)):
            tmpV = ""
            for j in range(len(self.curveValList[i][0])):
                tmpV += "\t".join([self.curveValList[i][0][j], self.curveValList[i][1][j]]) + '\n'
            newLine = "Title %s\n" \
                      "ID    %s\n" \
                      "Value \n" \
                      "%s"%(self.curveTitleList[i], self.curveIdList[i], tmpV)
            # print("#######################################################################")
            # print(newLine)
            text_.insert(END, newLine + '\n')
        text_.pack()

    def add_BPM(self):
        """

        :return:
        """


        rowN = 0
        self.BPM_prop = {'Title':"Title", 'PID':2, 'DOF':2, 'VAD':0, 'LCID':1}
        self.window_BPM = Toplevel(self.frame)
        self.entry_list_BPM = []
        self.label_list_BPM = []
        self.partInfoList = StringVar(self.frame)
        self.curveInfoList = StringVar(self.frame)
        for key,value in self.BPM_prop.items():#range(len(self.BPM_prop)):
            # print(rowN)
            self.label_list_BPM.append(Label(self.window_BPM, text=key, width=20))
            self.label_list_BPM[rowN].grid(row=rowN, column=0)

            if key == "PID":
                popupMenu = OptionMenu(self.window_BPM, self.partInfoList, *self.partInfo.keys(), command=self.getPartId)
                popupMenu.grid(row = rowN, column=2)
                self.partInfoList.set(list(self.partInfo.keys())[0])
                self.partInfoList.trace('w', self.change_dropdown1)
                self.entry_list_BPM.append(Entry(self.window_BPM, width=50))
                # self.entry_list_BPM[rowN].grid(row=rowN, column=2)
                # self.entry_list_BPM[rowN].insert(0,value)
                # print(rowN)
                rowN += 1
                continue

            if key == "LCID":
                popupMenu = OptionMenu(self.window_BPM, self.curveInfoList, *self.curveInfo.keys(), command=self.getCurveId)
                popupMenu.grid(row = rowN, column=2)
                self.curveInfoList.set(list(self.curveInfo.keys())[0])
                self.curveInfoList.trace('w', self.change_dropdown2)
                self.entry_list_BPM.append(Entry(self.window_BPM, width=50))
                # self.entry_list_BPM[rowN].grid(row=rowN, column=2)
                # self.entry_list_BPM[rowN].insert(0,value)
                # print(rowN)
                rowN += 1
                continue

            # print(rowN)
            self.entry_list_BPM.append(Entry(self.window_BPM, width=50))
            self.entry_list_BPM[rowN].grid(row=rowN, column=2)
            self.entry_list_BPM[rowN].insert(0,value)
            rowN += 1

        rowN = rowN + 1
        button_ = Button(self.window_BPM, text="Save", command=self.save_BPM)
        button_.grid(row=rowN, column=1)
        rowN = rowN + 1
        clearEntry = Button(self.window_BPM, text="Exit", command=self.exit_BPM)
        clearEntry.grid(row=rowN, column=1)

    def save_BPM(self):
        """
                *BOUNDARY_PRESCRIBED_MOTION_RIGID
                $HMNAME LOADCOLS       2disp
                $HWCOLOR LOADCOLS       2       4
                         2         2         2         2       1.0
        :return:
        """
        print("In save BPM function: ")
        # print(self.partInfo[self.partInfo_Id])
        # print(self.curveInfo[self.curveInfo_Id])
        part_id = self.partInfo[self.partInfo_Id]
        curve_id = self.curveInfo[self.curveInfo_Id]

        self.BPM = "*BOUNDARY_PRESCRIBED_MOTION_RIGID\n" \
                   "$HMNAME LOADCOLS%s%s\n" \
                   "$HWCOLOR LOADCOLS       2       4\n" \
                   "%s%s%s%s       1.0"%(part_id.rjust(10),  self.entry_list_BPM[0].get().rjust(10), part_id.rjust(10),
                                           self.entry_list_BPM[2].get().rjust(10), self.entry_list_BPM[3].get().rjust(10), curve_id.rjust(10))

    def exit_BPM(self):
        """

        :return:
        """

        self.window_BPM.destroy()

    def show_curve_info(self):
        """

        :return:
        """
        # print("\n".join(self.curveLines))

    def add_table(self):
        """

        :return:
        """
        rowN = 0
        # self.noOfCurve = int(self.entry_list_CC[6].get())

        self.entry_list_all = []

        # for i in range(self.noOfCurve):
        # self.curveNo = i+1
        self.window_CC2 = Toplevel(self.frame)

        self.curveTitle = Label(self.window_CC2, text="Title")
        self.curveTitle.grid(row=rowN, column=0)
        self.curveTitle_entry = Entry(self.window_CC2, width=10)
        self.curveTitle_entry.grid(row=rowN, column=1)
        self.curveTitle_entry.insert(0, "Title")

        rowN += 1
        self.curveId = Label(self.window_CC2, text="ID")
        self.curveId.grid(row=rowN, column=0)
        self.curveId_entry = Entry(self.window_CC2, width=10)
        self.curveId_entry.grid(row=rowN, column=1)
        self.curveId_entry.insert(0, 1)

        rowN += 1
        self.curveLength_ = Label(self.window_CC2, text="Length")
        self.curveLength_.grid(row=rowN, column=0)
        self.curveLength_entry = Entry(self.window_CC2, width=10)
        self.curveLength_entry.grid(row=rowN, column=1)
        self.curveLength_entry.insert(0, 1)

        rowN += 1
        self.createTable = Button(self.window_CC2, text="addData", command=self.create_table)
        self.createTable.grid(row=rowN, column=1)
        rowN = rowN + 1
        self.save_tableData = Button(self.window_CC2, text="Save", command=self.save_tableData)
        self.save_tableData.grid(row=rowN, column=1)
        rowN = rowN + 1
        self.clear_entry = Button(self.window_CC2, text="clearEntry", command=self.clear_entry)
        self.clear_entry.grid(row=rowN, column=1)

    def create_table(self):
        """
            create table by counting the number of rows
        :return:
        """
        self.curveLength = int(self.curveLength_entry.get())
        self.entry_list_CC21 = []
        self.entry_list_CC22 = []
        rowN = 4
        # self.curveLength = int(self.entry_list_CC[6].get())
        for i in range(self.curveLength):
            rowN += i + 1
            # print(rowN)
            self.entry_list_CC21.append(Entry(self.window_CC2, width=10))
            self.entry_list_CC21[i].grid(row=rowN, column=0)
            self.entry_list_CC21[i].insert(0,0)

            self.entry_list_CC22.append(Entry(self.window_CC2, width=10))
            self.entry_list_CC22[i].grid(row=rowN, column=1)
            self.entry_list_CC22[i].insert(0,0)

        rowN = rowN + 1
        # print(rowN)
        self.createTable.forget()
        self.createTable.grid(row=rowN, column=1)
        rowN = rowN + 1
        self.save_tableData.forget()
        self.save_tableData.grid(row=rowN, column=1)
        rowN = rowN + 1
        self.clear_entry.forget()
        self.clear_entry.grid(row=rowN, column=1)

    def clear_entry(self):
        """

        :return:
        """
        for i in range(len(self.entry_list_CC21)):
            # print(i)
            self.entry_list_CC21[i].destroy()
            self.entry_list_CC22[i].destroy()
        # self.save_tableData.destroy()
        # self.clear_entry.destroy()

    def save_tableData(self):
        """
                *DEFINE_CURVE
                $HMNAME CURVES       1$TITLE$
                $HWCOLOR CURVES       1      11
                $HMCURVE     1    2 $TITLE$
                $CURVEID$         0       1.0       1.0       0.0       0.0         0
                $A$$O$
        :return:
        """
        print("In the save data method !")

        self.curveTitle_ = self.curveTitle_entry.get()
        self.curveTitleList.append(self.curveTitle_)
        self.curveId_ = self.curveId_entry.get()
        self.curveIdList.append(self.curveId_)
        self.curveInfo.update({self.curveTitle_:self.curveId_})
        entry_list_CC21 = []
        entry_list_CC22 = []

        # self.loads_CC2 = []
        # self.times_CC2 = []
        self.curve = "*DEFINE_CURVE\n" \
                     "$HMNAME CURVES       1%s\n" \
                     "$HWCOLOR CURVES       1      11\n" \
                     "$HMCURVE     1    2 %s\n" \
                     "%s         0       1.0       1.0       0.0       0.0         0\n"%(str(self.curveTitle_).rjust(10), str(self.curveTitle_).rjust(10), str(self.curveId_).rjust(10))
        for i in range(self.curveLength):
            if i == (self.curveLength - 1):
                self.curve += str(self.entry_list_CC21[i].get()).rjust(20) + str(self.entry_list_CC22[i].get()).rjust(20)
                entry_list_CC21.append(self.entry_list_CC21[i].get())
                entry_list_CC22.append(self.entry_list_CC22[i].get())
            else:
                self.curve += str(self.entry_list_CC21[i].get()).rjust(20) + str(self.entry_list_CC22[i].get()).rjust(20) + '\n'
                entry_list_CC21.append(self.entry_list_CC21[i].get())
                entry_list_CC22.append(self.entry_list_CC22[i].get())
                # self.loads_CC2.append(self.entry_list_CC21[i].get())
                # self.times_CC2.append(self.entry_list_CC22[i].get())

        # print(self.loads_CC2)
        self.curveValList.append([entry_list_CC21, entry_list_CC22])
        # print(self.times_CC2)
        # print(self.curve)
        self.curveLines.append(self.curve)
        # self.curveInfo.update({self.curveNo:[self.curveTitle_, self.curveId_, self.curve]})
        # self.window_CC2.destroy()

    def add_new(self):
        """

        :return:
        """
        self.save_data2()
        # for i in range(len(self.materialProp)):
        #     self.entry_list[i].delete(0,'end')

    def save_data2(self):
        """

        :return:
        """
        # final_section_lines = '\n'.join(self.sectionLines)
        # print(final_section_lines)

        outlines = []

        if self.inMat54:
            # print(self.entry_list)
            # self.materialProp = ['Title', 'Id', 'Density', 'E1', 'E2', 'Mu', 'GAB', 'GBC', 'FBRT', 'YCFAC', 'xc', 'xt', 'yc', 'yt']
            for line in self.template_lines:
                # print(line)
                line = line.replace("$TITLE$", self.entry_list[0].get())
                line = line.replace("$ID$", self.entry_list[1].get().rjust(10))
                line = line.replace("$DENSITY$", self.entry_list[2].get().rjust(10))
                line = line.replace("$E1$", self.entry_list[3].get().rjust(10))
                line = line.replace("$E2$", self.entry_list[4].get().rjust(10))
                line = line.replace("$MU$", self.entry_list[5].get().rjust(10))
                line = line.replace("$GAB$", self.entry_list[6].get().rjust(10))
                line = line.replace("$GBC$", self.entry_list[7].get().rjust(10))
                line = line.replace("$DEFINE$", ("-" + self.entry_list[1].get()).rjust(10))
                line = line.replace("$FBRT$", self.entry_list[8].get().rjust(10))
                line = line.replace("$YCFAC$", self.entry_list[9].get().rjust(10))
                line = line.replace("$XC$", self.entry_list[10].get().rjust(10))
                line = line.replace("$XT$", self.entry_list[11].get().rjust(10))
                line = line.replace("$YC$", self.entry_list[12].get().rjust(10))
                line = line.replace("$YT$", self.entry_list[13].get().rjust(10))
                # line = line.replace("$SECTION$", final_section_lines)
                outlines.append(line)
                continue
        if self.inMat24:
            # self.mat24_prop = ['Title', 'Id', 'Density', 'E1', 'Mu', 'SIGY', 'ETAN', 'FAIL', 'LCSS', 'SECTION']
            # print(self.entry_list)
            for line in self.template_lines:
                # print(line)
                line = line.replace("$TITLE$", self.entry_list[0].get())
                line = line.replace("$ID$", self.entry_list[1].get().rjust(10))
                line = line.replace("$DENSITY$", self.entry_list[2].get().rjust(10))
                line = line.replace("$E1$", self.entry_list[3].get().rjust(10))
                line = line.replace("$MU$", self.entry_list[4].get().rjust(10))
                line = line.replace("$SIGY$", self.entry_list[5].get().rjust(10))
                line = line.replace("$ETAN$", self.entry_list[6].get().rjust(10))
                line = line.replace("$FAIL$", self.entry_list[7].get().rjust(10))
                line = line.replace("$LCSS$", self.entry_list[8].get().rjust(10))
                # line = line.replace("$SECTION$", final_section_lines)
                outlines.append(line)
        if self.inRigid:
            # self.mat20_prop = ['Title', 'Id', 'Density', 'E1', 'Mu', 'CMO', 'CON1', 'CON2', 'SECTION']
            # print(self.entry_list)
            for line in self.template_lines:
                # print(line)
                line = line.replace("$TITLE$", self.entry_list[0].get())
                line = line.replace("$ID$", self.entry_list[1].get().rjust(10))
                line = line.replace("$DENSITY$", self.entry_list[2].get().rjust(10))
                line = line.replace("$E1$", self.entry_list[3].get().rjust(10))
                line = line.replace("$MU$", self.entry_list[4].get().rjust(10))
                line = line.replace("$CMO$", self.entry_list[5].get().rjust(10))
                line = line.replace("$CON1$", self.entry_list[6].get().rjust(10))
                line = line.replace("$CON2$", self.entry_list[7].get().rjust(10))
                # line = line.replace("$SECTION$", final_section_lines)
                outlines.append(line)

        # print(self.mat_out)
        with open(self.mat_out, 'a') as outFile:
            outFile.writelines(outlines)

    def save_data_CC(self):
        """

        :return:
        """
        # self.label_CC = ['EndTime', 'TimeStepScaleFact', 'DT2MS', 'TiedProj', 'DT', 'D3Dump', 'CurveId', 'DefineCurve_Title']
        # self.add_table()
        # self.save_tableData()
        try:
            outlines = []
            final_curve = "\n".join(self.curveLines)

            for line in self.template_lines_control_cards:
                # print(line)
                if self.loadingType == "Topload":
                    line = line.replace("$ENDTIM$", self.entry_list_CC[0].get().rjust(10))
                    line = line.replace("$DT$", self.entry_list_CC[1].get().rjust(10))
                    line = line.replace("$DEFINE_CURVE$", final_curve)
                    line = line.replace("$BPM$", self.BPM)
                    line = line.replace("$LBY$", self.LBY)
                    line = line.replace("$LBP$", self.LBP)
                    outlines.append(line)
                else:
                    line = line.replace("$ENDTIM$", self.entry_list_CC[0].get().rjust(10))
                    line = line.replace("$TIMESTSC$", self.entry_list_CC[1].get().rjust(10))
                    line = line.replace("$DT2MS$", self.entry_list_CC[2].get().rjust(10))
                    line = line.replace("$TIEDPRJ$", self.entry_list_CC[3].get().rjust(10))
                    line = line.replace("$DT$", self.entry_list_CC[4].get().rjust(10))
                    line = line.replace("$D3DUMP$", self.entry_list_CC[5].get().rjust(10))
                    line = line.replace("$DEFINE_CURVE$", final_curve)
                    line = line.replace("$BPM$", self.BPM)
                    line = line.replace("$LBY$", self.LBY)
                    line = line.replace("$LBP$", self.LBP)
                    outlines.append(line)

            with open(self.control_cards_out, 'a') as outFile:
                outFile.writelines(outlines)
        except Exception as ex:

            messagebox.showerror("ERROR", "Define Curve Info OR %s"%ex)

    def change_dropdown(self, *args):

        # Material
        self.materialType = self.matType.get()
        # print(self.materialType)
        self.template.delete(0, 'end')
        self.template.insert(0, self.mapMat[self.materialType])

        # Control Cards
        self.template_controlcards.delete(0, 'end')
        self.loadingType = self.loadType.get()
        self.template_controlcards.insert(0, self.mapControlCards[self.loadingType])

    def change_dropdown1(self, *args):
        """

        :param args:
        :return:
        """
        # Part ID
        self.partInfo_Id = self.partInfoList.get()
        print(self.partInfo_Id)


    def change_dropdown2(self, *args):
        """

        :param args:
        :return:
        """
        # Curve ID
        self.curveInfo_Id = self.curveInfoList.get()
        print(self.curveInfo_Id)

    def getCurveId(self, curveId):
        """
        :return:
        """
        self.curveId = curveId
        print(self.curveId)

    def getPartId(self, partId):
        """
        :return:
        """
        self.partId = partId
        print(self.partId)

    def getLoadType(self, loadingType):
        """
        :return:
        """
        self.loadingType = loadingType
        # print(self.loadingType)

    def getMatType(self, materialType):
        """
        :return:
        """
        self.materialType = materialType
        # print(self.materialType)

    def createButton(self, buttonName, buttonMethod, rowN, colN, fg='black'):
        """

        :return:
        """
        button_ = Button(self.frame, text=buttonName, command=buttonMethod, fg=fg)
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


if __name__ == '__main__':

    root = Tk()
    app = App(root)
    root.mainloop()

