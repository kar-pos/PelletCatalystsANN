import customtkinter
import torch
import numpy as np
from CTkMessagebox import CTkMessagebox
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

#%% Functions definitions
def _quit():
    root.quit()
    root.destroy()
    
def addlabels(x,y):
    for i in range(len(x)):
        plt.text(i, round(y[0,i],2),round(y[0,i],2), ha = 'center',
                 bbox = dict(facecolor = '#343638', alpha =.8))
    
def combobox_callback(choice):
    state1 = combobox1.get()
    state2 = combobox2.get()
    if state1=="Custom":
        try:
            feedstock = pd.read_excel('Custom_feedstock.xlsx',skiprows = 1)
            feedstock = feedstock.to_numpy(dtype=float)
            label1h.configure(text="Custom feedstock loaded",text_color=("green"))
        except:
            label1h.configure(text="Custom feedstock load filed!",text_color=("red"))
    else:
        label1h.configure(text="Reference feedstock",text_color=("white"))
    if state2!="None":
        textbox.configure(state="normal")
    else:
        textbox.delete("0.0", "end")  # delete all text
        textbox.insert("0.0", "0.0")
        textbox.configure(state="disabled")
        
#Collecting data and calculatin ANN results
def calculate_callback():
    state1 = combobox1.get()
    state2 = combobox2.get()
    #Results
    if state1 == "Wood pellets":
        feedstock=ref_wood
    elif state1 == "Straw pellets":
        feedstock=ref_straw
    elif state1 == "Hemp pellets":
        feedstock=ref_hemp
    else:
        try:
            feedstock = pd.read_excel('Custom_feedstock.xlsx',skiprows = 1)
            feedstock = feedstock.to_numpy(dtype=float)
        except:
            label1h.configure(text="Custom feedstock load filed!",text_color=("red"))
            CTkMessagebox(title="Incorrect feedstock data!", message="Calculation aborted! Check inputs.",
                  icon="warning", option_1="Cancel")
            return
    if state2 == "None":
        catalyst_type=0
    elif state2 == "Pt":
        catalyst_type=1
    elif state2 == "TiO2":
        catalyst_type=2
    elif state2 == "CuO":
        catalyst_type=3
    else:
        catalyst_type=4
    try:
        catalyst_amount=textbox.get("0.0", "end")
        catalyst_amount=float(catalyst_amount)
    except:
        CTkMessagebox(title="Incorrect catalyst data!", message="Calculation aborted! Check inputs.",
                  icon="warning", option_1="Cancel")
        return
    catalyst_adblue=checkbox.get();
            
    input_array=np.append(feedstock, [catalyst_amount,catalyst_adblue,catalyst_type])
    model_out=model(torch.tensor(input_array.reshape(1, -1), dtype=torch.float32)).detach().numpy()
    row=0
    for key, value in data_plot.items():
        data_plot[key]=model_out[0,row]
        row=row+1
    figure.clf()
    parameters=data_plot.keys()
    model_values=data_plot.values()
    axes = figure.add_subplot()
    axes.bar(parameters, model_values)
    axes.tick_params(axis='x', labelrotation = 20)
    axes.set_title('Model output parameters')
    axes.set_ylabel('Value')
    addlabels(parameters, model_out)
    canvas.draw()
    root.update()
    button2.configure(state="normal")

def copy_callback():
    root.clipboard_clear()
    root.clipboard_append(data_plot)
#%% Constants preparing
#Loading ANN model
model=torch.jit.load('ANN_model_deployed.pth');

#Reference feedstocks
ref_wood=[0.08, 48, 5.7, 0.017, 43.2, 8.65, 1.88679, 75.15, 627, 693, 258, 369, 66, 435, 18.5116, 1.77966]
ref_straw=[0.58, 44, 6.2, 0.068, 41.3, 9.71, 2.83019, 71.42, 400, 476, 77.6, 322.4, 76, 398.4, 15.9694, 1.94444]
ref_hemp=[4.9, 46, 6.8, 0.267, 42.7, 9.83, 7.61905, 66.16, 324, 362, 148, 176, 38, 214, 17.011, 1.875]

#Catalyst and AdBlue settings
catalyst_amount=0
catalyst_type=0
catalyst_adblue=0

#preparing data holder
data_plot={'CO [ppm]': 0,
    'NOx [ppm]': 0,
    'CO2 [%]': 0,
    'O2 [%]': 0,
    'Dust [g/m3]': 0,
    'VOC [ug/30dm3]': 0,
    'PAH [ug/30dm3]': 0,
    'Temperature [C]': 0,
    'Scc [%]': 0,
    'Scfa[%]': 0,
    'F [kg/h]': 0}

#%% GUI settings
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

root = customtkinter.CTk()

frame = customtkinter.CTkFrame(master=root)
frame.pack(pady=20, padx=30, fill="both", expand=True)

label1 = customtkinter.CTkLabel(master=frame, text="ANN for catalytic pellets combustion modeling", font=("Roboto",24))
label1.pack(pady=12,padx=10)

label1 = customtkinter.CTkLabel(master=frame, text="Set feedstock", font=("Roboto",14))
label1.pack(pady=0,padx=10)

combobox1 = customtkinter.CTkComboBox(frame, values=["Wood pellets", "Straw pellets","Hemp pellets","Custom"], command=combobox_callback)
combobox1.set("Wood pellets")
combobox1.pack(pady=0,padx=10)
label1h = customtkinter.CTkLabel(master=frame, text="Reference feedstock", font=("Roboto",10))
label1h.pack(pady=0,padx=10)

label2 = customtkinter.CTkLabel(master=frame, text="Set Catalyst", font=("Roboto",14))
label2.pack(pady=0,padx=10)

combobox2 = customtkinter.CTkComboBox(frame, values=["None", "Pt","TiO_2","CuO","MnO_2"], command=combobox_callback)
combobox2.set("None")
combobox2.pack(pady=0,padx=10)
frame_in = customtkinter.CTkFrame(master=frame)
frame_in.pack()
label2h = customtkinter.CTkLabel(master=frame_in, text="Amount [g/m2]")
textbox = customtkinter.CTkTextbox(master=frame_in, height=20, width=70)
textbox.insert("0.0", "0.0")
textbox.configure(state="disabled")
checkbox = customtkinter.CTkCheckBox(master=frame_in, text="AdBlue",
                                     onvalue=1, offvalue=0)
label2h.pack(side=customtkinter.LEFT, padx=10)
textbox.pack(side=customtkinter.LEFT, padx=10)
checkbox.pack(side=customtkinter.LEFT)

frame_in2 = customtkinter.CTkFrame(master=frame,fg_color="transparent")
frame_in2.pack(pady=10)
button = customtkinter.CTkButton(master=frame_in2, text="Calculate", command=calculate_callback)
button2 = customtkinter.CTkButton(master=frame_in2, text="Copy to clipboard", state="disabled", command=copy_callback)
button.pack(side=customtkinter.LEFT, padx=10)
button2.pack(side=customtkinter.LEFT, padx=10)

# figure, axes = Figure(figsize=(11, 7), dpi=100)
# figure.set_facecolor('#212121')
figure, axes = plt.subplots()
figure.set_facecolor('#212121')
figure.set_figwidth(17)
figure.set_figheight(8)
figure.text(0.3, 0.7, 
         'Calculate to see results', 
         style = 'italic', 
         fontsize = 30, 
         bbox ={'facecolor':'#1f538d', 
                'alpha':0.6, 
                'pad':10}) 
mpl.rcParams['text.color']="#d6d6d6"
mpl.rcParams['axes.labelcolor'] = "#d6d6d6"
mpl.rcParams['xtick.color'] = "#d6d6d6"
mpl.rcParams['ytick.color'] = "#d6d6d6"
canvas = FigureCanvasTkAgg(figure, master=frame)
canvas.get_tk_widget().pack()
# canvas = customtkinter.CTkCanvas(master=frame, width =800, height=210, bg="white")
# canvas.pack()

w = 950 # width for the Tk root
h = 750 # height for the Tk root
# get screen width and height
ws = root.winfo_screenwidth() # width of the screen
hs = root.winfo_screenheight() # height of the screen
# calculate x and y coordinates for the Tk root window
x = (ws/2) - (w/2)
y = (hs/2) - (h/2)
# set the dimensions of the screen 
# and where it is placed
root.title("ANN combustion v 1.0")
root.geometry('%dx%d+%d+%d' % (w, h, x, y))
root.protocol("WM_DELETE_WINDOW", _quit)
root.mainloop()