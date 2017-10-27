__author__ = 'Umesh'

import os, sys

class CreateInput:
    def __init__(self):
        """

        :return:
        """
        self.Kfile = "input.k"
        self.loadType = "Topload"

    def initKfile(self):
        """
        write k file with *KEYWORD heading and any other
        lines that may be needed at the top
        :return:
        """
        with open(self.Kfile,"w") as f:
            f.write("*KEYWORD\n")

    def endKfile(self):
        """
        write k file with *END keyword at the end
        :return:
        """
        with open(self.Kfile,"a") as f:
            f.write("*END\n")

    def writeKfile(self, text=""):
        """
        Appends the text provided to .k file
        :param text:  the text to be added in the .k file
        :return:
        """
        if text is None: return
        with open(self.Kfile,"a") as f:
            f.write(text)

    def getTitleBlock(self,title=""):
        """

        :param title: return the *TITLE block containing the title specified
        :return:
        """

        return "*TITLE\n%s\n"%title

    def addIncludeBlock(self,fileNames=[]):
        """

        :param fileName: add fileName to the master input deck using INCLUDE syntax
        :return:
        """
        if fileNames == []: return

        with open(self.Kfile,"a") as f:
            f.write("*INCLUDE\n%s\n"%'\n'.join(fileNames))

    def addIncludePathBlock(self,pathNames=""):
        """

        :param pathNames: add pathNames to the master input deck using INCLUDE_PATH syntax
         pathNames can be either a string or a list containing multiple paths
        :return:
        """
        if pathNames is "" or []: return
        if type(pathNames) == list:
            pathNames = "\n".join(pathNames)


        with open(self.Kfile,"a") as f:
            f.write("*INCLUDE_PATH\n%s\n"%pathNames)

    def addIncludeRelPathBlock(self,relative_path=""):
        """

        :param relative_path: add a relative path to the master input deck using INCLUDE_RELATIVE_PATH
         syntax. relative_path can be either a string or a list containing multiple paths
        :return:
        """
        if relative_path is "" or []: return
        if type(relative_path) == list:
            relative_path = "\n".join(relative_path)

        with open(self.Kfile,"a") as f:
            f.write("*INCLUDE_PATH_RELATIVE\n%s\n"%relative_path)

    def create_input_k(self, destPath = ""):
        """

        :return:
        """
        self.Kfile = os.path.join(destPath, "input.k")
        self.initKfile()
        title = self.getTitleBlock(self.loadType.upper())
        self.writeKfile(title)
        self.addIncludeRelPathBlock("Output")
        self.addIncludeBlock(["mesh.k", "mat.k","control_cards.k"])
        self.endKfile()

if __name__ == '__main__':

    dest_path = r"D:\Umesh\AxiomProject\VEOL_GUI\TestCase2"
    input1 = CreateInput()
    input1.create_input_k(dest_path)
