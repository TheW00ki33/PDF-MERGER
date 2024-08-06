###################################################
##### MergeMyPdfs GUI (according to PyPDF4) #######
#### GUI-Version 1.0.1 - DEV for Python 3.9.7 #####
###################################################

# Version 1.0.0 edited before Release

#import some libaries
from tkinter import *
from tkinter import filedialog
import tkinter as tk
import os
import shutil
from PyPDF4 import PdfFileReader, PdfFileWriter
 
root = Tk()
 
# create the GUI-functon
def openGUI():

    # create basic window
    root.title('MergeMyPdfs')
    root.geometry("375x200")
    #root.configure(background='white') --> for example the simple function
    root.config(bg='#A7A7B3')
    root.resizable(False, False)
    #root.iconbitmap('icon_cc.ico') #(r'C:\Users\...\mergeMyPdfs.ico') if not in same dir
    #root.iconphoto(False, PhotoImage(file='icon_cc.png')) #replace False with Waise to insert icon on all upcoming windows

    # create input description
    inpFldTitle = Label(root, text="Insert destination Filename:")
    inpFldTitle.config(bg='#A7A7B3')
    inpFldTitle.pack(side=TOP)

    # create status section
    statFldTitle = Label(root, text="Status:")
    statFldTitle.config(bg='#A7A7B3')
    statFldTitle.place(x=168, y=160, height=20, width=50)

    # first status
    changeBtn("Welcome, lets merge! [Mode: idle]", "black")

    # create input box
    name_input = Entry(root, bd=2) #frame depth --> bd=[value]
    name_input.pack(side=TOP)

    # bool declaration for checkbox
    global chckVal
    chckVal = tk.BooleanVar()
    chckVal.set(True)

    # create checkbox
    chckBox = tk.Checkbutton(root, text='Save in specific path', var = chckVal) #you could add -->, onvalue="True Val", offvalue="False Val"<-- for specific callback
    chckBox.config(bg='#A7A7B3')
    chckBox.place(x=125, y=65, height=20, width=130)

    # .pdf info on right side of ENTRY
    statFldTitle = Label(root, text=".pdf")
    statFldTitle.config(bg='#A7A7B3')
    statFldTitle.place(x=252, y=22, height=20, width=30)

    # create button for start merging && save-func
    b = Button(root, command=lambda: mergePdfs(name_input.get() + ".pdf"), height=1, width=20, text="Choose PDFs", bg="#10C3DA", activebackground="#10A8DA")
    b.place(x=114, y=110)
    #b.pack(pady=2) --> if you want to pack it center, pady is the y-value

    root.mainloop()

# merge algor
def mergePdfs(resultKey):
    try:
        # error action (stop func) for no-name
        if resultKey == ".pdf":
            changeBtn("Please insert a filename!", "red")
            return
        
        if chckVal.get() == 1:
            ##root.withdraw()
            firstWdir = os.getcwd() #CURRENT WORKDIR
            root.folder_selected = filedialog.askdirectory(parent=root, title="Select the Directory where you want to save the new File") #SAVE PATH IN OTHER VAR
            if root.folder_selected == "":
                changeBtn("No valid path!", "red")
                return

        writerPdf = PdfFileWriter()
        files = filedialog.askopenfilenames(parent=root, title="Select the PDFs you want to merge")
 
        for file in root.tk.splitlist(files):
            readerPdf = PdfFileReader(file)
            for page in range(readerPdf.getNumPages()):
                writerPdf.addPage(readerPdf.getPage(page))
 
        with open(resultKey, 'wb') as tempPdf:
            if readerPdf.getNumPages() != 0:
                if chckVal.get() == 1:
                    changeBtn("Successfully saved in choosen directory!", "green") # the .get()-Function returns boolean as bin-value {0=False / 1=True}

                else:
                    changeBtn("Successfully merged to " + resultKey + "!", "green") # merge info
                
            else:
                changeBtn("No files selected to merge!", "red")
            writerPdf.write(tempPdf)
    except:
        changeBtn("Choosen files is no PDF!", "red")
        os.remove(resultKey) # deletes pdf after an error occoured, bcs pdf is empty

    if chckVal.get() == 1 and readerPdf.getNumPages() != 0: #MAYBE ERROR OCOURRES, CHECK!!!!
        os.chdir(root.folder_selected)
        curDir = os.getcwd()
        srcDir = r'' + firstWdir + '\\' + resultKey
        destiMve = r'' + curDir + '\\' + resultKey
        shutil.move(srcDir, destiMve)

# Output-Info (just a empty button)
output = Label(root, text="", fg="white")

def changeBtn(output_text, colour):
    output['text'] = output_text
    output['fg'] = colour
    output['bg'] = '#A7A7B3'
    output.pack(side=BOTTOM)
 
openGUI()