__author__ = 'Umesh'

import os, sys, csv
from tkinter import *
from tkinter import filedialog
import material_prop as mat_prop
import create_input as create_input
from tkinter import messagebox
import json
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
        self.projectPath = r"D:\Umesh\AxiomProject\VEOL_GUI\Rakesh_Project\Test1"#self.case_path
        self.ProjectPathEntry.insert(0, self.projectPath)
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
        self.materialProp1 = []
        self.materialProp = []
        self.matTypeList = []
        self.json_file = r"D:\Umesh\AxiomProject\VEOL_GUI\Rakesh_Project\Test1\file.json"
        with open(self.json_file) as readIn:
            self.prop_mat = json.load(readIn)

        for key in self.prop_mat.keys():
            self.matTypeList.append(key)

        self.matType = StringVar(self.frame)
        self.materialType = "MAT_54"
        # self.matTypeList = set(sorted({'MAT_54', 'MAT_55', 'MAT_20', 'MAT_24'}))
        self.matTypeList = set(sorted(self.matTypeList))
        self.matType.set('MAT_54')
        self.mat55_template = os.path.join(self.template_path, "mat55.k")
        self.mat24_template = os.path.join(self.template_path, "mat24.k")
        self.rigid_template = os.path.join(self.template_path, "rigid.k")
        self.mapMat = {'MAT_54':self.mat55_template, 'MAT_55':self.mat55_template, 'MAT_20':self.rigid_template, 'MAT_24':self.mat24_template}
        popupMenu = OptionMenu(self.frame, self.matType, *self.matTypeList, command=self.getMatType)
        popupMenu.grid(row = self.rowN, column=1)
        self.matType.trace('w', self.change_dropdown)

        self.addNewMat = Button(self.frame, text="AddNewMaterial", command=self.add_new_material)
        self.addNewMat.grid(row=self.rowN, column=2)
        self.createButton("Add_data", self.add_materialInfo, self.rowN, 3)
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
        self.createButton("Add_data", self.add_controlCards, self.rowN, 3)

        # Open Input
        self.rowN += 1
        self.createButton("Open Input", self.open_input, self.rowN, 1, fg='red')

        # Run Input
        # self.rowN += 1
        self.createButton("Run", self.run_info, self.rowN, 2, fg='red')

        # Exit
        # self.rowN += 1
        self.createButton("Exit", self.frame.quit, self.rowN, 3, fg='red')

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

    def add_new_material(self):
        """

        :return:
        """
        self.window_newMat = Toplevel(self.frame)

        rowN = 0
        self.matTitle = Label(self.window_newMat, text="MAT_Title", width=20)
        self.matTitle.grid(row=rowN, column=0)
        self.matTitle_entry= Entry(self.window_newMat, width=20)
        self.matTitle_entry.grid(row=rowN, column=1)
        self.matTitle_entry.insert(0,"MAT_Title")

        rowN += 1
        self.partTitle = Label(self.window_newMat, text="Part_Title", width=20)
        self.partTitle.grid(row=rowN, column=0)
        self.partTitle_entry= Entry(self.window_newMat, width=20)
        self.partTitle_entry.grid(row=rowN, column=1)
        self.partTitle_entry.insert(0,"Part_Title")
        self.partTitle_entry_freq= Entry(self.window_newMat, width=5, fg='blue')
        self.partTitle_entry_freq.grid(row=rowN, column=2)
        self.partTitle_entry_freq.insert(0,"y")

        rowN += 1
        self.cardTitle = Label(self.window_newMat, text="Card_Title", width=20)
        self.cardTitle.grid(row=rowN, column=0)
        self.cardTitle_entry= Entry(self.window_newMat, width=20)
        self.cardTitle_entry.grid(row=rowN, column=1)
        self.cardTitle_entry.insert(0,"Card_Title")
        self.cardTitle_entry_freq= Entry(self.window_newMat, width=5, fg='blue')
        self.cardTitle_entry_freq.grid(row=rowN, column=2)
        self.cardTitle_entry_freq.insert(0,"y")

        rowN += 1
        self.cardInfo = Label(self.window_newMat, text="Card_Info", width=20)
        self.cardInfo.grid(row=rowN, column=0)
        self.cardInfoText=Button(self.window_newMat, text="+", width=5, command=self.add_entry)
        self.cardInfoText.grid(row=rowN, column=1)
        self.cardInfoSave=Button(self.window_newMat, text="save", width=5, command=self.save_newMatInfo)
        self.cardInfoSave.grid(row=rowN, column=2)

        rowN += 1
        self.cardInfo_label = Label(self.window_newMat, text="Parameter_Label", width=20)
        self.cardInfo_label.grid(row=rowN, column=0)
        self.cardInfo_default = Label(self.window_newMat, text="Defaults", width=20)
        self.cardInfo_default.grid(row=rowN, column=1)
        self.cardInfo_freq = Label(self.window_newMat, text="Frequency", width=20)
        self.cardInfo_freq.grid(row=rowN, column=2)

        self.matRow = rowN
        self.newMatInfo_label = []
        self.newMatInfo = []
        self.newMatInfo_default = []
        self.newMatInfo_freq = []
        self.newMatInfo_all = []

    def add_entry(self):
        """

        :return:
        """
        self.matRow += 1
        self.mat_label = Entry(self.window_newMat, text="", width=10)
        self.mat_label.grid(row=self.matRow, column=0)
        self.mat_default = Entry(self.window_newMat, text="", width=10)
        self.mat_default.grid(row=self.matRow, column=1)
        self.mat_freq = Entry(self.window_newMat, text="", width=10)
        self.mat_freq.grid(row=self.matRow, column=2)

        self.newMatInfo_label.append([self.mat_label, self.mat_default, self.mat_freq])

    def save_newMatInfo(self):
        """

        :return:
        """

        print(self.newMatInfo_label, len(self.newMatInfo_label))

        for item in self.newMatInfo_label:
            self.newMatInfo.append(item[0].get())
            self.newMatInfo_default.append(item[1].get())
            self.newMatInfo_freq.append(item[2].get())


        newMatInfo = ",".join(self.newMatInfo)
        newMatInfo_default = ",".join(self.newMatInfo_default)
        newMatInfo_freq = ",".join(self.newMatInfo_freq)

        self.prop_mat.update({self.matTitle_entry.get():
                                  {"Part_Title":[self.partTitle_entry.get(), self.partTitle_entry_freq.get()],
                                   "Card_Title":[self.cardTitle_entry.get(), self.cardTitle_entry_freq.get()],
                                   "Mat_Parameters":[newMatInfo, newMatInfo_default, newMatInfo_freq]}})

        with open(self.json_file, 'w') as outFile:
            json.dump(self.prop_mat, outFile)

    def add_materialInfo(self):
        """

        :return:
        """

        self.window2 = Toplevel(self.frame)
        self.material1 = mat_prop.MaterialProp()
        # self.mat54_prop = ["MAT_54", "Title", "*MAT_ENHANCED_COMPOSITE_DAMAGE", "mid,ro,ea,eb,(ec),prba,(prca),(prcb),"
        #                                          "gab,gbc,gca,(kf),aopt,2way,,"
        #                                          "xp,yp,zp,a1,a2,a3,mangle,,"
        #                                          "v1,v2,v3,d1,d2,d3,dfailm,dfails,"
        #                                          "tfail,alph,soft,fbrt,ycfac,dfailt,dfailc,efs,"
        #                                          "xc,xt,yc,yt,sc,crit,beta,,"
        #                                          "pel,epsf,epsr,tsmd,soft2,,"
        #                                          "slimt1,slimc1,slimt2,slimc2,slims,ncyred,softg,,"
        #                                          "lcxc, lcxt, lcyc, lcyt, lcsc, dt"]
        #
        # self.mat55_prop = ["MAT_55", "Title", "*MAT_ENHANCED_COMPOSITE_DAMAGE", "mid,ro,ea,eb,(ec),prba,(prca),(prcb),"
        #                                          "gab,gbc,gca,(kf),aopt,2way,,"
        #                                          "xp,yp,zp,a1,a2,a3,mangle,,"
        #                                          "v1,v2,v3,d1,d2,d3,dfailm,dfails,"
        #                                          "tfail,alph,soft,fbrt,ycfac,dfailt,dfailc,efs,"
        #                                          "xc,xt,yc,yt,sc,crit,beta,,"
        #                                          "pel,epsf,epsr,tsmd,soft2,,"
        #                                          "slimt1,slimc1,slimt2,slimc2,slims,ncyred,softg,,"]
        #
        # self.mat24_prop = ["MAT_24", "Title", "*MAT_PIECEWISE_LINEAR_PLASTICITY", "mid,ro,e,pr,sigy,etan,fail,tdel,"
        #                                       "c,p,lcss,lcsr,vp,lcf,,"
        #                                       "eps1,eps2,eps3,eps4,eps5,eps6,eps7,eps8,"
        #                                       "es1,es2,es3,es4,es5,es6,es7,es8"]
        #
        # self.mat20_prop = ["MAT_20", "Title", "*MAT_RIGID", "mid,ro,e,pr,n,couple,m,alias,"
        #                                          "cmo,con1,con2,,"
        #                                          "lco or a1,a2,a3,v1,v2,v3,,"]



        self.entry_list = []
        self.label_list = []
        colN = 0
        rowN = 0
        count = 0
        # for i in range(len(self.materialProp)):
        #     if self.materialProp[i][0] == self.materialType:
        try:
            crit_fail = float(self.materialType.split("_")[-1])
        except Exception as Ex:
            crit_fail = 0.0
            print(Ex)
            pass
        self.material1.material_prop['crit'] = str(crit_fail)
        self.materialProp_curr = self.prop_mat[self.materialType]["Mat_Parameters"][0].split(',')
        self.materialProp_curr_default = self.prop_mat[self.materialType]["Mat_Parameters"][1].split(',')
        self.materialProp_curr_freq = self.prop_mat[self.materialType]["Mat_Parameters"][2].split(',')

        for j in range(len(self.materialProp_curr)):
            if count == 8:
                rowN += 2
                colN = 0
                count = 0

            if self.materialProp_curr[j] == "":
                self.label_list.append(Label(self.window2, text=self.materialProp_curr[j], width=10))
                self.entry_list.append(Entry(self.window2, width=10))
                rowN += 2
                colN = 0
                count = 0
                continue

            if self.materialProp_curr_freq[j].strip() == "y":
                self.label_list.append(Label(self.window2, text=self.materialProp_curr[j].upper(), width=10, fg="blue"))
                self.entry_list.append(Entry(self.window2, width=10, fg="blue"))
            else:
                self.label_list.append(Label(self.window2, text=self.materialProp_curr[j].upper(), width=10))
                self.entry_list.append(Entry(self.window2, width=10))
            self.label_list[j].grid(row=rowN, column=colN)

            self.entry_list[j].grid(row=rowN+1, column=colN)
            # self.entry_list[j].insert(0,self.material1.material_prop.get(self.materialProp_curr[j].strip(), 0.0))
            self.entry_list[j].insert(0,self.materialProp_curr_default[j])
            count += 1
            colN += 1

        rowN += 3
        # print(rowN)
        add_button = Button(self.window2, text="Add", command=self.add_new)
        add_button.grid(row=rowN, column=0)
        button_ = Button(self.window2, text="Save", command=self.save_data2)
        button_.grid(row=rowN, column=1)
        Exitbutton_ = Button(self.window2, text="Exit", command=self.close_window)
        Exitbutton_.grid(row=rowN, column=2)

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
        # print("##############################################################")
        outlines = []
        colN = 0
        rowN = 0
        count = 0
        newline = []
        index = 0
        outlines.append("\n")
        outlines.append(self.prop_mat[self.materialType]["Card_Title"][0])
        for j in range(len(self.materialProp_curr)):
            print("[{}] {}: {}".format(index, self.materialProp_curr[j], self.entry_list[index].get()))
            tmp_prop = self.entry_list[index].get()
            newline.append(tmp_prop.rjust(10))

            if count == 8 or j == (len(self.materialProp_curr)-1):
                rowN += 2
                colN = 0
                count = 0
                line1 = "\n" + "".join(newline)# + "\n"
                outlines.append(line1)
                newline = []

            if self.materialProp_curr[j] == "":
                rowN += 2
                colN = 0
                count = 0
                line1 = "\n" + "".join(newline) #+ "\n"
                outlines.append(line1)
                newline = []
                index += 1
                continue

            count += 1
            colN += 1
            index += 1

        with open(self.mat_out, 'a') as outFile:
            outFile.writelines(outlines)

    def add_materialInfo_orig(self):
        """

        :return:
        """

        print(self.template.get())
        template_path = self.template.get()
        with open(template_path, 'r') as inFile:
            self.template_lines = inFile.readlines()

        self.window2 = Toplevel(self.frame)
        self.material1 = mat_prop.MaterialProp()
        self.mat54_prop = ['Title', 'Id', 'Density', 'E1', 'E2', 'E3', 'PR', 'GAB', 'GBC', 'FBRT', 'YCFAC', 'XC', 'XT', 'YC', 'YT']#, 'SECTION']
        self.mat20_prop = ['Title', 'Id', 'Density', 'E1', 'PR', 'CMO', 'CON1', 'CON2']#, 'SECTION']
        self.mat24_prop = ['Title', 'Id', 'Density', 'E1', 'PR', 'SIGY', 'ETAN', 'FAIL', 'LCSS']#, 'SECTION']

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
        colN = 0
        rowN = 0
        for i in range(len(self.materialProp)):
            # print(self.materialProp[i], rowN, colN)

            if self.materialProp[i] == 'PR':
                self.label_list.append(Label(self.window2, text=self.materialProp[i], width=10))
                self.label_list[i].grid(row=rowN, column=colN)

                self.entry_list.append(Entry(self.window2, width=10))
                self.entry_list[i].grid(row=rowN+1, column=colN)
                self.entry_list[i].insert(0,self.material1.material_prop[self.materialProp[i]])
                rowN += 2
                colN = 0
                continue

            if self.materialProp[i] == 'XC':
                rowN += 2
                colN = 0
                self.label_list.append(Label(self.window2, text=self.materialProp[i], width=10))
                self.label_list[i].grid(row=rowN, column=colN)

                self.entry_list.append(Entry(self.window2, width=10))
                self.entry_list[i].grid(row=rowN+1, column=colN)
                self.entry_list[i].insert(0,self.material1.material_prop[self.materialProp[i]])
                colN += 1
                continue

            self.label_list.append(Label(self.window2, text=self.materialProp[i], width=10))
            self.label_list[i].grid(row=rowN, column=colN)

            self.entry_list.append(Entry(self.window2, width=10))
            self.entry_list[i].grid(row=rowN+1, column=colN)
            self.entry_list[i].insert(0,self.material1.material_prop[self.materialProp[i]])

            colN += 1

        rowN += 3
        # print(rowN)
        add_button = Button(self.window2, text="Add", command=self.add_new)
        add_button.grid(row=rowN, column=0)
        button_ = Button(self.window2, text="Save", command=self.save_data2)
        button_.grid(row=rowN, column=1)
        Exitbutton_ = Button(self.window2, text="Exit", command=self.close_window)
        Exitbutton_.grid(row=rowN, column=2)

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

    def add_controlCards(self):
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
                import_table = Button(self.window_CC, text="Import Table", command=self.import_table)
                import_table.grid(row=rowN, column=2)#, sticky=W)
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
        button_ = Button(self.window_CC, text="Save", command=self.save_data_CC, fg='red')
        button_.grid(row=rowN, column=2, sticky=W)

        button_ = Button(self.window_CC, text="Exit", command=self.close_window_CC, fg='red')
        button_.grid(row=rowN, column=2)#, sticky=W)

        # rowN = rowN + 1
        # showButton_ = Button(self.window_CC, text="Show", command=self.show_curve_info)
        # showButton_.grid(row=rowN, column=2)#, sticky=W)

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

    def import_table(self):
        """

        :return:
        """

        rowN = 0
        # self.noOfCurve = int(self.entry_list_CC[6].get())

        self.entry_list_all = []

        # for i in range(self.noOfCurve):
        # self.curveNo = i+1
        self.window_CC3 = Toplevel(self.frame)

        self.curveTitle = Label(self.window_CC3, text="Title")
        self.curveTitle.grid(row=rowN, column=0)
        self.curveTitle_entry = Entry(self.window_CC3, width=10)
        self.curveTitle_entry.grid(row=rowN, column=1)
        self.curveTitle_entry.insert(0, "Title")

        rowN += 1
        self.curveId = Label(self.window_CC3, text="ID")
        self.curveId.grid(row=rowN, column=0)
        self.curveId_entry = Entry(self.window_CC3, width=10)
        self.curveId_entry.grid(row=rowN, column=1)
        self.curveId_entry.insert(0, 1)

        rowN += 1
        self.import_data = Button(self.window_CC3, text="Import Data", command=self.getData)
        self.import_data.grid(row=rowN, column=0)
        # self.curveLength_entry = Entry(self.window_CC3, width=10)
        # self.curveLength_entry.grid(row=rowN, column=1)
        # self.curveLength_entry.insert(0, 1)

        # rowN += 1
        # self.createTable = Button(self.window_CC3, text="addData", command=self.create_table)
        # self.createTable.grid(row=rowN, column=1)
        rowN = rowN + 1
        self.save_tableData1 = Button(self.window_CC3, text="Save", command=self.save_tableData)
        self.save_tableData1.grid(row=rowN, column=1)
        rowN = rowN + 1
        self.clear_entry1 = Button(self.window_CC3, text="clearEntry", command=self.clear_entry)
        self.clear_entry1.grid(row=rowN, column=1)

    def getData(self):
        """

        :return:
        """
        import csv
        fName = filedialog.askopenfilename()
        # self.ProjectPathEntry.delete(0,'end')
        # self.getCSVPath.insert(0,fName)

        # csvPath = self.getCSVPath.get()
        print(fName)
        col1 = []
        col2 = []
        with open(fName, 'r') as csvFile:
            csv_reader = csv.reader(csvFile)
            print(csv_reader)
            for row in csv_reader:
                col1.append(row[0])
                col2.append(row[1])
                print(row[0], row[1])

        self.curveLength = len(col1)
        self.entry_list_CC21 = []
        self.entry_list_CC22 = []
        rowN = 4
        # self.curveLength = int(self.entry_list_CC[6].get())
        for i in range(self.curveLength):
            rowN += i + 1
            # print(rowN)
            self.entry_list_CC21.append(Entry(self.window_CC3, width=10))
            self.entry_list_CC21[i].grid(row=rowN, column=0)
            self.entry_list_CC21[i].insert(0,col1[i])

            self.entry_list_CC22.append(Entry(self.window_CC3, width=10))
            self.entry_list_CC22[i].grid(row=rowN, column=1)
            self.entry_list_CC22[i].insert(0,col2[i])

        # rowN = rowN + 1
        # # print(rowN)
        # self.createTable.forget()
        # self.createTable.grid(row=rowN, column=1)
        rowN = rowN + 1
        self.save_tableData1.forget()
        self.save_tableData1.grid(row=rowN, column=1)
        rowN = rowN + 1
        self.clear_entry1.forget()
        self.clear_entry1.grid(row=rowN, column=1)

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
        # self.template.delete(0, 'end')
        # self.template.insert(0, self.mapMat[self.materialType])

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

