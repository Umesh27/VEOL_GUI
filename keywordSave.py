__author__ = 'Administrator'

import os, sys


def saveKey(filName):

    str1 = r"C:\LSTC\LS-PrePost\4.3-x64\lsprepost4.3_x64.exe", "k=%s -nographics"%filName
    str1 = r"C:\LSTC\LS-PrePost\4.3-x64\lsprepost4.3_x64.exe", "k=%s -nographics"%filName

def createSCL(fileName, keyIn, keyOut):

    print(fileName)
    with open(fileName, "r") as inFile:
        tmp_str = "".join(inFile.readlines())

    mat_path = os.path.join(os.path.split(keyIn)[0], "mat.k")
    control_path = os.path.join(os.path.split(keyIn)[0], "control_cards.k")
    mesh_path = os.path.join(os.path.split(keyIn)[0], "mesh.k")

    final_str = tmp_str.replace("$keyPath$", keyIn)
    final_str = final_str.replace("$keyPath1$", mat_path)
    final_str = final_str.replace("$keyPath2$", control_path)
    final_str = final_str.replace("$keyPath3$", mesh_path)
    final_str = final_str.replace("$outPath$", keyOut)

    outPath = os.path.join(os.path.split(keyIn)[0], "openSaveKey.scl")
    #print(outPath)
    outPathCfile = os.path.join(os.path.split(keyIn)[0], "openSaveKey.cfile")
    #print(outPathCfile)
    #print(final_str)
    with open(outPath, 'w') as outFile:
        outFile.write(final_str)

    str1 = "runscript %s"%outPath
    # str1 = "runscript %s \n exit"%outPath
    #print(str1)
    with open(outPathCfile, 'w') as outCfile:
        outCfile.write(str1)

    # lsppCommand = r"C:\LSTC\LS-PrePost\4.3-x64\lsprepost4.3_x64.exe c=%s -nographics"%outPathCfile
    lsppCommand = r"C:\LSTC\LS-PrePost\4.3-x64\lsprepost4.3_x64.exe c=%s "%outPathCfile
    #print(lsppCommand)

    os.system(lsppCommand)

if __name__ == '__main__':
    tmp_path = r"D:\Umesh\VEOL\project\Veol\templates\open_save_key.tmp"
    #keyInPath = r"D:\Umesh\LSPP\Testing\2May\156\case1\SEQ2\input.k"
    #keyOutPath = r"D:\Umesh\LSPP\Testing\2May\156\case1\SEQ2\input1.k"
    #keyInPath = r"D:\Umesh\LSPP\Testing\2May\172\Test1\input.k"
    #keyInPath = r"D:\Umesh\VEOL\\tmp\Veol_input_files\Test_Assembly\115\case1\SEQ2\Top_Bottom\input.k"
    #keyOutPath = r"D:\Umesh\VEOL\\tmp\Veol_input_files\Test_Assembly\115\case1\SEQ2\Top_Bottom\input1.k"
    #createSCL(tmp_path, keyInPath, keyOutPath)

    #parent_dir = r"D:\Umesh\VEOL\\tmp\Veol_input_files\Test_Assembly"
    parent_dir = r"D:\Test_App"
    dirs = ['118']#os.listdir(parent_dir)
    for dir in dirs:
        if os.path.isdir(os.path.join(parent_dir,dir)):
            dirPath = os.path.join(parent_dir,dir)

            caseDirs = os.listdir(dirPath)
            for _casedir in caseDirs:
                if os.path.isdir(os.path.join(dirPath,_casedir)):
                    casenum = _casedir.split("case")[-1]
                    try:
                        keyInPath = os.path.join(dirPath,_casedir,"SEQ2","Front_Back","input.k")
                        keyOutPath = os.path.join(dirPath,_casedir,"SEQ2","Front_Back","input1.k")
                        createSCL(tmp_path, keyInPath, keyOutPath)
                        print(keyOutPath)
                    except Exception as ex:
                        print("file not found !", ex)
                        pass
