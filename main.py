# FileDialog to enter path to csv
# Button to plot
# Plot the graph in frame

from matplotlib.widgets import Cursor
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from tkinter import * 
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,  
NavigationToolbar2Tk)
from tkinter import filedialog as fd
#import sourceInformation

#Initialize certain variables
inpFile = ""        #Catalogue file name selected by user
ra = ""             #Self-explanatory
dec = ""            #Self-explanatory
hmxb = ""           #Placeholder name for dataframe corresponding to selected catalogue
epsilon = 0.1       #Tolerance for checking correspondance between catalogue and astro source coordinates
ra_unwrapped = ""   #Unwrapped Ra values
dec_unwrapped = ""  #Unwrapped Dec values
astroIndex = ""     #Index of source in astro table that corresponds to source selected from catalogue
path_to_astro_file = "AstroSat_final_table1.csv" #Path to final astro table csv
import tkinter as tk

#bigWindow = tk.Tk()
window = tk.Tk()
window.title("Visualizer")

l2 = tk.Label(window, text="Equatorial Chart")
l2.pack()
def onclick(event):
    print (event.x, event.y)

def onpick(event):
    
    sourceSelected.config(text="Source Selected: " + hoverSource["text"])
    print (event.ind)
    
# the figure that will contain the plot 
fig = Figure(figsize = (5, 5), 
                 dpi = 100) 
  
  
# adding the subplot 
#plot1 = fig.add_subplot(111, projection="mollweide") 
plot1 = fig.add_subplot(111, projection=None)
plot1.grid()
plot1.set_xlabel('Right Ascension (rad)')
plot1.set_ylabel('Declination (rad)')

# plotting the graph

def checkNoProb():
    global inpFile, hmxb, ra, dec, ra_unwrapped, dec_unwrapped
    try:
        ra_unwrapped, dec_unwrapped = [], []
        hmxb = pd.read_csv(inpFile)
        #print (hmxb.Name.head())
        ra = hmxb['RAJ2000'].str.split(' ').tolist()
        dec = hmxb['DEJ2000'].str.split(' ').tolist()

        # Converting RA and DEC values to radian
        for i in range(len(ra)):
          a = ra[i]
          ra[i] = float(a[0])*2*np.pi/24 + float(a[1])*2*np.pi/(60*24) + float(a[2])*2*np.pi/(60*60*24)
          ra_unwrapped.append(ra[i])
          if ra[i] > np.pi:
            ra[i] = np.pi- ra[i]

          b = dec[i]
          dec[i] = float(b[0])*np.pi/180 + float(b[1])*np.pi/(60*180) + float(b[2])*np.pi/(180*3600)
          dec_unwrapped.append(dec[i])

        return True
    except Exception as e:
        print (e)
        errorDialog = tk.Toplevel(window)
        errorDialog.title('Error')
        errorMessage = tk.Label(errorDialog, text="Please select an appropriate catalogue file")
        errorMessage.pack()


def plot():
    flag = checkNoProb()
    if flag:
        global plottedPoints, sourceSelected, canvas, fig, window
        #canvas = FigureCanvasTkAgg(fig, 
        #                   master = window)
        sourceSelected['text'] = "<No source selected>"
        plottedPoints = plot1.scatter(ra, dec, s = 5, picker=True)
        #plot1.grid()
        canvas.mpl_connect('pick_event', onpick)
        canvas.mpl_connect('motion_notify_event', on_plot_hover)
        canvas.draw()
     
canvas = FigureCanvasTkAgg(fig, 
                           master = window)   
canvas.draw() 
  
# creating the Matplotlib toolbar 
toolbar = NavigationToolbar2Tk(canvas, 
                               window) 
toolbar.update() 
#canvas.mpl_connect('button_press_event', onclick)
canvas.mpl_connect('pick_event', onpick)
cursor = Cursor(plot1, useblit=True, color='red', linewidth=2)
# placing the toolbar on the Tkinter window 
canvas.get_tk_widget().pack()

frame1 = tk.Frame(window)
frame2 = tk.Frame(window)


hoverSource = tk.Label(frame1, text = "  ")
hoverSource.pack()
def on_plot_hover(event):
    global plottedPoints
    if event.inaxes == plot1:
        #print ("Hey")
        cont, ind = plottedPoints.contains(event)
        if cont:            
            #print ("Hovered", ind)
            hoverSource.config(text="{}".format(hmxb.Name[int(ind['ind'][0])]))
        else:
            hoverSource.config(text="  ")
    else:
        hoverSource.config(text="  ")

#canvas.mpl_connect('motion_notify_event', on_plot_hover) 



def fileChooser():
    global inpFile
    fileName = fd.askopenfilename()
    fileChosen.config(text=fileName)
    inpFile = fileName
    print (inpFile)


def downloadNow():
    global astroIndex, path_to_astro_file
    fileName = fd.asksaveasfilename(defaultextension='.csv')
    if fileName != '':
        try:
            df = hmxb
            sourceName = sourceSelected["text"]
            ind = df.index[df['Name'] == sourceName[17:]].tolist()[0]
            astroTable = pd.read_csv(path_to_astro_file)
            if astroIndex == "":
                df.iloc[ind].replace(np.nan, 'NaN', regex=True).to_csv(fileName)
            else:
                pd.concat([df.iloc[ind].replace(np.nan, 'NaN', regex=True), astroTable.iloc[astroIndex]]).to_csv(fileName)
        except:
            errorDialog = tk.Toplevel()
            errorDialog.title('Error')
            errorMessage = tk.Label(errorDialog, text='Something went wrong')
            errorMessage.pack()
    

def viewInfo():
    global epsilon, ra, dec, ra_unwrapped, dec_unwrapped, astroIndex, path_to_astro_file
    #import sourceInformation
    #print ("You've chosen to display info of the selected source")
    #sourceInformation.displayInfo(hmxb, sourceSelected['text'])
    df = hmxb
    if sourceSelected["text"] != "<No source selected>":
        master = tk.Toplevel(window)
        master.title('Source Information')
        heading = tk.Label(master, text = "Source Information: ")
        heading.pack()
        nested = tk.Frame(master)
        nested.pack(side=tk.LEFT)
        multiList = tk.Listbox(nested, width=100, height = 20)
        multiList.pack(side="left", fill=tk.BOTH)

        scrollbar = Scrollbar(nested, orient="vertical")
        scrollbar.config(command=multiList.yview)
        scrollbar.pack(side="right", fill="y")

        multiList.config(yscrollcommand=scrollbar.set)

        
        sourceName = sourceSelected["text"]
        ind = df.index[df['Name'] == sourceName[17:]].tolist()[0]
        #for i in range(len(df.columns)):
        #   lab = tk.Label(master, text=df.columns[i] + ": " + str(df.iloc[ind][df.columns[i]]))
        #   lab.pack()

        for i in range(len(df.columns)-1):
            multiList.insert(tk.END, df.columns[i] + ": " + str(df.iloc[ind][df.columns[i]]))

        downloadButton = tk.Button(master, text="Save Source Information", command=downloadNow)
        downloadButton.pack(side=tk.LEFT)

        ### Check if it is present in AstroSat
        #astro = pd.read_csv("C:\\Users\\ADP\Downloads\\AstroSat_final_table1.csv")
        astro = pd.read_csv(path_to_astro_file)
        flag = False
        for i in range(len(astro)):
            if (float(astro.iloc[i]['CR1']) - ra_unwrapped[ind]*180/np.pi)**2 <= epsilon**2:
                if (float(astro.iloc[i]['CR2']) - dec_unwrapped[ind]*180/np.pi)**2 <= epsilon**2:
                    flag = True
                    heading['text'] = 'Selected source has been observed by AstroSat'
                    astroIndex = i
                    break

        if flag == False:
            heading['text'] = 'Selected source has not been observed by AstroSat'
    

fileButton = tk.Button(frame1, text="Select Catalogue", command=fileChooser)
fileButton.pack(fill=tk.X)
plotButton = tk.Button(frame1, text="Plot", command=plot)
plotButton.pack(fill=tk.X)



viewInfoButton = tk.Button(frame1, text="View Info for Selected Source", command = viewInfo)
viewInfoButton.pack(fill = tk.X)

emptySpace1 = tk.Label(frame1, text="  ")
emptySpace1.pack()

fileChosen = tk.Label(frame1, text = "<No file chosen>")
fileChosen.pack()

sourceSelected = tk.Label(frame1, text = "<No source selected>")
sourceSelected.pack()
frame1.pack()
window.mainloop()
