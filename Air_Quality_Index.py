from tkinter import *
from PIL import Image,ImageTk
from tkinter import messagebox
import requests
import json
import pandas as pd
from tkinter import ttk

df = pd.read_excel("Country_Code.xlsx")

root =Tk()
root.title('Air Quality Application')
root.iconbitmap('logo1.ico')
root.geometry("1000x630+180+0")

list1 = []
for i in range(len(df)):
     temp = str(df.iloc[i,0].split(',')[0])
     keys = temp
     list1.append(keys)
     

title = Label(root,text="AIR QUALITY INDEX",anchor=CENTER,font=("Rockwell",20,"bold","italic"),fg="white",bg='skyblue',bd=25,relief=RIDGE,)
title.pack(side=TOP,fill=X)

instruction = Label(root,text="1: Select Option(zipcode-country/lon-lat/city-country)    2: Fill Following Information   3: Click On Submit Button",font=("Rockwell",13,"bold","italic"),fg="red",pady=10)
instruction.pack()

m = StringVar()
m.set('lonLan')

#--------------------------MAIN FRAME--------------------------#

mainFrame = LabelFrame(root,bd=20,relief=RIDGE)
mainFrame.place(x=0,y=130,width=1000,height=500)


#----------------------------RIGHT FRAME--------------------------------------------#
rightFrame = LabelFrame(mainFrame,text="Air Quality Info",bd=5,relief=RIDGE,padx=10,font=("Rockwell",12,"bold","italic"))
rightFrame.place(x=480,y=5,width=480,height=450)

#------------------------------------x---------------------------------#
#EXCECUTE FUNCTION
def execute():

    global api_request
    global country_display
    display_clear()
    option_get = m.get()    
    if option_get == 'zipcode':
        zip= zipcode_entry.get()
    
        country1 = s.split('-')[1]
        country_display = s.split('-')[0]
        if zip.isdigit() and len(country1) !=0 :
            api_request = requests.get("https://api.weatherbit.io/v2.0/current/airquality?postal_code="+zip+"&country="+country1+"&key=07fe8a7265f84c5faf4fc46b0416247d")
            display()        
        else:
            error = messagebox.showerror("Error","Please Enter Valid Data..")
    
    elif option_get == 'lonLan':
        
        lon = long_entry.get()
        lan = lat_entry.get()
        if len(lon) !=0 or len(lan) !=0:
            lon = float(lon)
            lan = float(lan)

            if isinstance(lon,float) and isinstance(lan,float):
                print(lon,lan)
                api_request = requests.get("https://api.weatherbit.io/v2.0/current/airquality?lat="+str(lan)+"&lon="+str(lon)+"&key=07fe8a7265f84c5faf4fc46b0416247d")
                display()
            else:
                error = messagebox.showerror("Error","Enter Proper Digits Only..")
        
        else:
            error = messagebox.showerror("Error","Invalid Data..")   
    
    elif option_get == 'city':

        city = city_entry.get()
        country1 = s.split('-')[1]
        country_display = s.split('-')[0] 
        if len(city) !=0 or len(country1) !=0:
            api_request = requests.get("https://api.weatherbit.io/v2.0/current/airquality?city="+city+"&country="+country1+"&key=07fe8a7265f84c5faf4fc46b0416247d")  
            display()
        else:
            error = messagebox.showerror("Error","Invalid Data..")

#---------------------------------------------------X-----------------------------------------------------------------------------#
#Display Function
def display():

    try:
        api = json.loads(api_request.content)
         
        country_code = api['country_code']  
        city =api['city_name']
        
        for i in api['data']:
            quality= i['aqi']
                    
          
        if quality >=0 and quality<=50:
            category = "Good"
        elif quality >=51 and quality<=100:
            category = "Moderate"
        elif quality >=101 and quality<=150:
            category = "Unhealthy for Sensitive Groups"
        elif quality >=151 and quality<=200:
            category = "Unhealthy"
        elif quality >=201 and quality<=300:
            category = "Very Unhealthy"
        elif quality >=301 and quality<=500:
            category = "Hazardous"
                    
        
        if category == "Good":
            color = "#00E400"
        elif category == "Moderate":
            color = "#ffff00"
        elif category == "Unhealthy for Sensitive Groups":
            color = "#ff7e00"
        elif category == "Unhealthy":
            color = "#ff0000"
        elif category == "Very Unhealthy":
            color = "#99004c"
        elif category == "Hazardous":
            color = "#7e0023"

        city_name_label = Label(rightFrame,text="City",font=("Rockwell",15,"bold"),padx=2,pady=13,background=color)
        city_name_label.grid(row=0,column=0,sticky=W)
        city_name = Label(rightFrame,text=city,font=("Rockwell",15,"bold"),padx=2,pady=13,background=color)
        city_name.grid(row=0,column=1)

        air_quality_label = Label(rightFrame,text="Air Quality",font=("Rockwell",15,"bold"),padx=2,pady=13,background=color)
        air_quality_label.grid(row=1,column=0,sticky=W)
        air_quality = Label(rightFrame,text=quality,font=("Rockwell",15,"bold"),padx=2,pady=13,background=color)
        air_quality.grid(row=1,column=1)
    
        category_label = Label(rightFrame,text="Category",font=("Rockwell",15,"bold"),padx=2,pady=13,background=color)
        category_label.grid(row=2,column=0,sticky=W)
        category_air = Label(rightFrame,text=category,font=("Rockwell",15,"bold"),padx=2,pady=13,background=color)
        category_air.grid(row=2,column=1)

        country_name_label = Label(rightFrame,text="Country",font=("Rockwell",15,"bold"),padx=2,pady=13,background=color)
        country_name_label.grid(row=3,column=0,sticky=W)
        country_name = Label(rightFrame,text=country_display,font=("Rockwell",15,"bold"),padx=2,pady=13,background=color)
        country_name.grid(row=3,column=1)
        rightFrame.configure(background=color)                
    except Exception as e:
        api = error = messagebox.showerror("Error","Please Enter Valid Zipcode or Co-ordinates or City and Country.. ")

#----------------------------------x-------------------------------------#
#Clear Display
def display_clear():
       
    for w in rightFrame.winfo_children():
        w.destroy()

#-----------------------------------x-----------------------------------------#
#Get ComboBox Value (country_entry)
def onChange(event):
    global s
    s = country_entry.get()
    if len(s) == 0:
        error = messagebox.showerror("Error","Please Enter Valid Data..")
#-------------------------------------------x----------------------------#
#Clear All Fields
def clear_field():
    
    display_clear()
    zipcode_entry.delete(0,END)
    long_entry.delete(0,END)
    lat_entry.delete(0,END)
    city_entry.delete(0,END)
    country_entry.delete(0,END)
    rightFrame.configure(background="SystemButtonFace")

#----------------------x----------------------------------------------------#
#----------------------------LEFT FRAME---------------------------------------#
leftFrame = LabelFrame(mainFrame,text="Fill Info",bd=5,relief=RIDGE,padx=10,font=("Rockwell",12,"bold","italic"))
leftFrame.place(x=0,y=5,width=470,height=450)

#----------------------------------------x------------------------------------#
#Check Option
def Check(val):
    rightFrame.configure(background="SystemButtonFace")
    #my_label.destroy()
    display_clear()
    if val == 'zipcode':
        zipcode_entry.configure(state=NORMAL)
        country_entry['state'] = 'readonly'
    else:
        zipcode_entry.delete(0,END)
        zipcode_entry.configure(state=DISABLED)
        country_entry['state'] = DISABLED

    if val == 'lonLan':
        long_entry.configure(state=NORMAL)
        lat_entry.configure(state=NORMAL)
    else:
        long_entry.delete(0,END)
        lat_entry.delete(0,END)
        long_entry.configure(state=DISABLED)
        lat_entry.configure(state=DISABLED)
    
    if val == 'city':
        city_entry.configure(state=NORMAL)
        country_entry['state'] = 'readonly'
    else:
        city_entry.delete(0,END)
        country_entry.delete(0,END)
        city_entry.configure(state=DISABLED)
        #country_entry['state'] = DISABLED
    
#------------------------------------------x-----------------------------------------#
#Create Options For Input
option1 = Radiobutton(leftFrame,text="Zipcode and Country",variable=m,value="zipcode",font=("Rockwell",12,"bold"),padx=2,pady=6,command=lambda: Check(m.get()))
option1.grid(row=0,column=0,sticky=W)

option2 = Radiobutton(leftFrame,text="Longitude and Latitude",variable=m,value="lonLan",font=("Rockwell",12,"bold"),padx=2,pady=6,command=lambda: Check(m.get()))
option2.grid(row=1,column=0,sticky=W)

option3 = Radiobutton(leftFrame,text="City and Country",variable=m,value="city",font=("Rockwell",12,"bold"),padx=2,pady=6,command=lambda: Check(m.get()))
option3.grid(row=2,column=0,sticky=W)

#----------------------------------------------x-------------------------------------#
#Create Labels and Entry Boxes
#For Zipcode
zipcode_label = Label(leftFrame, text="Enter Zipcode",font=("Rockwell",12,"bold"),padx=2,pady=10)
zipcode_label.grid(row=3,column=0,sticky=W)
zipcode_entry = Entry(leftFrame,width=20,font=("Rockwell",12,"bold"),state=DISABLED)
zipcode_entry.grid(row=3,column=1)
#------------------x---------------------------------------------#
#For City And Country
city_label = Label(leftFrame, text="Enter City",font=("Rockwell",12,"bold"),padx=2,pady=10)
city_label.grid(row=4,column=0,sticky=W)
city_entry = Entry(leftFrame,width=20,font=("Rockwell",12,"bold"),state=DISABLED)
city_entry.grid(row=4,column=1)

country_label = Label(leftFrame, text="Enter Country",font=("Rockwell",12,"bold"),padx=2,pady=10)
country_label.grid(row=5,column=0,sticky=W)

text_font = ("Rockwell",12,"bold")
country_entry = ttk.Combobox(leftFrame,value = list1,width=18,state=DISABLED,font=text_font)
country_entry.current(0)
country_entry.bind("<<ComboboxSelected>>",onChange)
country_entry.grid(row=5,column=1)

#----------------------------x-----------------------------------#
# For Longitude and Latitude
lat_label = Label(leftFrame, text="Enter Latitude",font=("Rockwell",12,"bold"),padx=2,pady=10)
lat_label.grid(row=6,column=0,sticky=W)
lat_entry = Entry(leftFrame,width=20,font=("Rockwell",12,"bold"))
lat_entry.grid(row=6,column=1)

long_label = Label(leftFrame, text="Enter Longitude",font=("Rockwell",12,"bold"),padx=2,pady=10)
long_label.grid(row=7,column=0,sticky=W)
long_entry = Entry(leftFrame,width=20,font=("Rockwell",12,"bold"))
long_entry.grid(row=7,column=1)
#----------------------------------------------x---------------------------------#

#Create Buttons
submit_btn = Button(leftFrame,text="Submit",font=("Rockwell",12,"bold"),padx=50,pady=10,command=execute)
submit_btn.grid(row=8,column=0,sticky=W)

clear_field_btn = Button(leftFrame,text="Clear Fields",font=("Rockwell",12,"bold"),padx=50,pady=10,command=clear_field)
clear_field_btn.grid(row=8,column=1,sticky=W)
#-----------------------------------------------------x------------------------------#
root.mainloop()
