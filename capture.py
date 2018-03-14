from tkinter import *
import cv2
import time
import os
import sys

directory = "training-images"
numberOfPictures = 20
numberOfWarmupPics = 4
hackathonRole = [
            "Default",
            "Judges",
            "Mentors",
            "Developer",
            "Designer",
            "Audio/Video",
            "Business",
            "Domain Expert",
            "Storyteller",
            "Visual Artist",
            "2D Artist",
            "3DArtist",
            "Audio Designer",
            "Soundscape Artist",
            "Scriptwrite/Writer",
            "Game Designer",
            "Architect/Space Designer",
            "Other"
            ]
userDataLicence = [
    "Default",
    "Public Domain",
    "Seth and his Team"
    ]


class MainGUI:
    def __init__(self, master):
        self.master = master
        master.title("idKnowU - Capture")

        self.label = Label(master, text="Getting to know you \n You may leave fields blank.", height=2, width=60)
        self.label.pack()

        
        self.close_button = Button(master, text="Exit for next user", command=self.shutdown)
        self.close_button.pack()
        self.close_button.pack(side=BOTTOM)
        
        self.bottomSpace = Label(master, text="     ", height=2, width=60)
        self.bottomSpace.pack(side=BOTTOM)

        self.greet_button = Button(master, text="Save", command=self.save, height=3, width=30)
        self.greet_button.pack()
        self.greet_button.pack(side=BOTTOM)

        self.bottomSpaceTwo = Label(master, text="     ", height=2, width=60)
        self.bottomSpaceTwo.pack(side=BOTTOM)
        
        self.capture_button = Button(master, text="Capture Picture", command=self.capturePicture)
        self.capture_button.pack(side=BOTTOM)

        

        self.uName = Entry(master)
        self.uName.pack()
        self.uName.delete(0, END)
        self.uName.insert(0, "Name")

        self.socialMedia = Entry(master)
        self.socialMedia.pack()
        self.socialMedia.delete(0, END)
        self.socialMedia.insert(0, "Social Media")

        self.funFact = Entry(master)
        self.funFact.pack()
        self.funFact.delete(0, END)
        self.funFact.insert(0, "Fun Fact")

        self.email = Entry(master)
        self.email.pack()
        self.email.delete(0, END)
        self.email.insert(0, "Email (optional)")

                
        self.bottomSpaceTwo = Label(master, text="My role:", height=2, width=30)
        self.bottomSpaceTwo.pack()
        self.listbox = Listbox(master, height=18, exportselection=0)
        self.listbox.pack()
        #####THIS USESS THE GLOBAL "hackathonRole"####
        for item in hackathonRole:
            if item != "Default":
                self.listbox.insert(END, item)
        self.listbox.pack()

        self.bottomSpaceTwo = Label(master, text="I submit my data to:", height=2, width=30)
        self.bottomSpaceTwo.pack()
        self.licencebox = Listbox(master, height=3, exportselection=0)
        self.licencebox.pack()
        #####THIS USESS THE GLOBAL "userDataLicence"####
        for item in userDataLicence:
            if item != "Default":
                self.licencebox.insert(END, item)
        self.licencebox.pack()

        self.disclaimer = Label(master, text="By submitting I agree that the above information/pictures\n" +
                                            " will be owned by Seth Persigehl and his team.\n \n"
                                            "Emails will be kept confidential and only used \n " +
                                            "if we need to contact you directly.", height=6, width=60)
        self.disclaimer.pack()
        self.disclaimer.pack(side=BOTTOM)

    def save(self):
        nameDIR = self.uName.get().replace(" ", "")
        nameDIR = nameDIR.lower()
        photoDIR = directory + '/' + nameDIR
        
        if not os.path.exists(photoDIR):
            os.makedirs(photoDIR)
        f = open(photoDIR + '/' + nameDIR + '.txt','w')

        try:
            self.item = self.listbox.curselection()[0] + 1 # the +1 is required to skip 'default'
        except:
            self.item = 0
            print("Error with listbox. Selected the default 'Default'")

        try:
            self.userL = self.licencebox.curselection()[0] + 1 # the +1 is required to skip 'default'
        except:
            self.userL = 0
            print("Error with licencebox. Selected the default 'Default'")
        
        f.write(str(self.uName.get()) + '\n')
        f.write(str(self.socialMedia.get()) + '\n')
        f.write(str(hackathonRole[self.item]) + '\n')
        f.write(str(self.funFact.get()) + '\n')
        f.write(str(self.email.get()) + '\n')
        f.write(str(userDataLicence[self.userL]) + '\n')
        print('Written to disk')

    


    def shutdown(self):
        try:
            cap.release()
        except:
            pass
        cv2.destroyAllWindows()
        os._exit(1)
        quit()
        sys.exit()
        

    def capturePicture(self):
        
        nameDIR = self.uName.get().replace(" ", "")
        nameDIR = nameDIR.lower()
        photoDIR = directory + '/' + nameDIR
        
        if not os.path.exists(photoDIR):
            os.makedirs(photoDIR)

        try:
            cap = cv2.VideoCapture(0)
            time.sleep(0.5)
            for i in range(0,numberOfPictures + numberOfWarmupPics):
                ret, frame = cap.read()
                time.sleep(0.1)
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
                time.sleep(0.1)
                cv2.imshow('frame', rgb)
                if (i >= numberOfWarmupPics):
                    out = cv2.imwrite(photoDIR + '/' + nameDIR + '-' + str(i - numberOfWarmupPics) + '.jpg', frame)
                time.sleep(0.1)
            print('Pictures captured for ' + nameDIR)
        except:
            print("A capture error occured. Trying again!")
            time.sleep(0.1)
            self.capturePicture()
            
        cap.release()
        cv2.destroyAllWindows()
        time.sleep(0.1)
             

time.sleep(0.1)
root = Tk()
my_gui = MainGUI(root)
root.mainloop()
