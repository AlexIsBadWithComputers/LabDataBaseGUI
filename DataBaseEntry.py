from Tkinter import * 
import tkFileDialog
import glob
from DropDownValues import *
from DataExtract import * 
from DataBaseEnterer import *
from MySQLdb import IntegrityError, OperationalError
from Commands import DataCommands, ErrorCommands

class RootWindow(Frame):
	
	"""This makes a convenient GUI for committing things to our data base"""


	def __init__(self, parent):
		Frame.__init__(self, parent)

		# Create a canvas for the scrollbar of option menu widgets
		self.canvas = Canvas(parent, borderwidth=10)
		self.frame = Frame(self.canvas)
		self.vsb = Scrollbar(parent, orient="vertical", command=self.canvas.yview)

		self.canvas.configure(yscrollcommand=self.vsb.set)
		self.canvas.configure(width=730, height=400)

		self.frame2 = Frame(parent, background = "#ffffff")
		self.TextBox = Text(self.frame2, wrap=NONE)

		self.TextScrollY = Scrollbar(self.frame2)
		self.TextScrollX = Scrollbar(self.frame2, orient=HORIZONTAL)
		self.TextScrollY.config(command=self.TextBox.yview)
		self.TextScrollX.config(command=self.TextBox.xview)
		self.TextBox.config(yscrollcommand=self.TextScrollY.set)
		self.TextBox.config(xscrollcommand=self.TextScrollX.set)
		
		self.TextScrollY.pack(side="right",fill="y")
		self.TextScrollX.pack(side="bottom",fill="x")
		self.TextBox.pack(side="bottom",fill="both", expand=True)
		self.frame2.pack(side="bottom",fill='both')
		
		self.vsb.pack(side="right", fill="y")
		self.canvas.pack(side="top", fill='both', anchor=NW)
		
		self.canvas.create_window((4,4), window=self.frame, tags=self.frame, anchor='nw')
		self.frame.bind("<Configure>", self.onFrameConfigure)

		self.labels = ["FileName","Element","Machine","Spike","Tech","Contract","Type"]
		self.parent = parent

		self.initUI()


	def initUI(self):
		"""
		Layout the default window options
		"""

		self.parent.title("Database Commit")
		self.pack(fill=BOTH, expand = 1)

		menubar = Menu(self.parent)
		self.parent.config(menu=menubar)

		fileMenu = Menu(menubar)
		fileMenu.add_command(label="Open", command = self.onOpen)
		menubar.add_cascade(label="Directory", menu=fileMenu)

		commitMenu = Menu(menubar)
		commitMenu.add_command(label="Current Formatting", command=self.MenuRead)
		commitMenu.add_command(label="Remove Data", command=self.DataDelete)
		menubar.add_cascade(label="Commit", menu=commitMenu)

		var1 = StringVar()
		var2 = StringVar()
		var3 = StringVar()
		var4 = StringVar()
		var5 = StringVar()
		var6 = StringVar()
		# Create autofill button and the menus from which to auto fill

		self.button = Button(self.frame, text = "Autofill with -->", 
			 				 fg='green', 
			 				 command = lambda: self.Filler(var1,var2,var3,var4,var5,var6))
		self.button.configure(width=10)
		self.button.grid(row=1,column=0)
		
		self.ElementMenu2 = OptionMenu(self.frame, var1 ,*list(Element))
		self.SpikeMenu = OptionMenu(self.frame, var2, *list(Spike))
		self.TechMenu = OptionMenu(self.frame, var3, *list(Tech))
		self.ContractMenu = OptionMenu(self.frame, var4, *list(Contract))
		self.TypeMenu = OptionMenu(self.frame, var5, *list(Type))
		self.MachineMenu = OptionMenu(self.frame,var6,*list(Machine))

		self.ElementMenu2.configure(width=2, fg='green')
		self.ElementMenu2.grid(column=1, row=1)

		self.MachineMenu.configure(width=8, fg='green')
		self.MachineMenu.grid(column=2, row=1)

		self.SpikeMenu.configure(width=8, fg='green')
		self.SpikeMenu.grid(column=3, row=1)

		self.TechMenu.configure(width=10, fg='green')
		self.TechMenu.grid(column=4, row=1)

		self.ContractMenu.configure(width=10, fg='green')
		self.ContractMenu.grid(column=5, row=1)

		self.TypeMenu.configure(width=8, fg='green')
		self.TypeMenu.grid(column=6, row=1)

		#create label headers

		for i in range(len(self.labels)):
			Label(self.frame, text=self.labels[i]).grid(column=i, row = 0)

	def Filler(self,var1,var2,var3,var4,var5,var6):

		"""
		This function is used to autofill the option menu widgets on the push
		of a button. the vars are simply the choice of the "master option menus"
		"""

		try:
		
			for i in range(len(self.element_menu_list)):
			
				self.element_var[i].set(var1.get())
				self.spike_var[i].set(var2.get())
				self.tech_var[i].set(var3.get())
				self.contract_var[i].set(var4.get())
				self.type_var[i].set(var5.get())
				self.machine_var[i].set(var6.get())

		#if you push the button with nothing to do... it doens't do anything
		except AttributeError:
			self.TextBox.insert(END, "No values to fill.... \n")
			pass

	def onFrameConfigure(self,event):
		self.canvas.configure(scrollregion=self.canvas.bbox("all"))

	
	def onOpen(self):
		"""
		This function is uest to select the directory and read
		the ASCII grid exports from thermo software.
		"""

		ftype = [ ('Data Exports','*.exp'),('All Files','*')]
		self.dlg = tkFileDialog.askdirectory()

		if self.dlg != '':
			text = self.readFiles(self.dlg)


	def readFiles(self,directoryname):
		"""
		Reads the number of files and defines the drop down menus that we'll be using
		to select options of the data base commit
		"""

		# Get rid of old widgets. 
		listy = self.frame.grid_slaves()
		for l in listy:
			if int(l.grid_info()["row"]) > 1:
				l.grid_forget()
		
		# Allocate arrays of widgets and values to the correct number
		count = 0
		for files in glob.iglob(directoryname + '/*.exp'):
			count += 1
		for i in range(count):

			self.element_menu_list = [i for i in range(count)]
			self.element_var = [StringVar() for i in range(count)]
			
			self.spike_menu_list = [i for i in range(count)]
			self.spike_var = [StringVar()  for i in range(count)]

			self.tech_menu_list = [i for i in range(count)]
			self.tech_var = [StringVar()  for i in range(count)]

			self.contract_menu_list =[i for i in range(count)]
			self.contract_var = [StringVar()  for i in range(count)]
			
			self.type_menu_list =[i for i in range(count)]
			self.type_var = [StringVar()  for i in range(count)]

			self.machine_menu_list = [i for i in range(count)]
			self.machine_var = [StringVar() for i in range(count)]

			self.Butt = [i for i in range(count)]

		# Create the widgets we need.
		for i, files in enumerate(glob.iglob(directoryname + '/*.exp')):

			self.Butt[i] = Button(self.frame, text=files.split('/')[-1].strip(".exp"),
				   command= lambda file=files: self.PreviewFile(file), wraplength=80,width=10)
			self.Butt[i].configure(width=10)
			self.Butt[i].grid(column = 0, row = i+3,sticky = W)
			
			self.element_menu_list[i] = OptionMenu(self.frame, 
												   self.element_var[i], 
												   *list(Element))
			self.element_menu_list[i].configure(width=2)
			self.element_menu_list[i].grid(column=1, row=i+3)

			self.machine_menu_list[i] = OptionMenu(self.frame, 
												   self.machine_var[i], 
												   *list(Machine))
			self.machine_menu_list[i].configure(width=8)
			self.machine_menu_list[i].grid(column=2, row=i+3)
			
			self.spike_menu_list[i] = OptionMenu(self.frame, 
												 self.spike_var[i], 
												 *list(Spike))
			self.spike_menu_list[i].configure(width=8)
			self.spike_menu_list[i].grid(column=3, row=i+3)
			
			self.tech_menu_list[i] = OptionMenu(self.frame, 
												self.tech_var[i], 
												*list(Tech))
			self.tech_menu_list[i].configure(width=10)
			self.tech_menu_list[i].grid(column=4, row=i+3)
			
			self.contract_menu_list[i] = OptionMenu(self.frame, 
													self.contract_var[i], 
													*list(Contract))
			self.contract_menu_list[i].configure(width=10)
			self.contract_menu_list[i].grid(column=5, row=i+3)
			
			self.type_menu_list[i] = OptionMenu(self.frame, 
												self.type_var[i], 
												*list(Type))
			self.type_menu_list[i].configure(width=8)
			self.type_menu_list[i].grid(column=6, row=i+3)


	def PreviewFile(self,file):
		"""
		This function reads a ASCII grid export from Thermo software
		and displays it in this progrom. This is so you can
		tell how to label data before database commitment
		"""

		f = open(file, 'r')
		self.TextBox.delete("1.0",END)
		
		for lines in f:
			self.TextBox.insert(END,lines)
		
		f.close()

	def MenuRead(self):
		"""
		This function reads the arguments of all the created OptionMenu
		widgets and uses them to commit these data to the database.
		"""

		# TODO LOOK FOR None IN DATA AND ERROR IN ORDER TO CATCH BAD FORMATTING.
		
		noprint = False

		# Encryption is for cowards.
		
		CorrectPassword = 'a'


		# Prompt for password before commit. 
		self.password = None
		self.TextBox.delete("1.0",END)
		self.GetPassword()
		if self.password != CorrectPassword:
			self.TextBox.delete("1.0",END)
			self.TextBox.insert(END, "I can't let you do that Dave. That is not the correct password.")
			return
		else: 
			self.TextBox.delete("1.0",END)
			self.TextBox.insert("1.0", "Password accepted. \n")

		db = Database()

		try:
			
			for i in range(len(self.spike_var)):
				# Make sure that all the data has been filled out!
				if self.element_var[i].get() == '':
					self.TextBox.delete("1.0",END)
					self.TextBox.insert(END, "You have not indicated an Element for every file. \n")
					return

				if self.machine_var[i].get() == '':
					self.TextBox.delete("1.0",END)
					self.TextBox.insert(END, "You have not indicated the Machine for every file. \n")
					return
				
				if self.spike_var[i].get() == '':
					self.TextBox.delete("1.0",END)
					self.TextBox.insert(END, "You have not indicated a Spike for every file. \n")
					return
				
				if self.tech_var[i].get() == '':
					self.TextBox.delete("1.0",END)
					self.TextBox.insert(END, 'You have not indicated a Tech for every file. \n')
					return
				if self.contract_var[i].get() == '':
					self.TextBox.delete("1.0",END)
					self.TextBox.insert(END,'You have not indicated a Contract for every file. \n')
					return

				if self.type_var[i].get() == '':
					self.TextBox.delete("1.0",END)
					self.TextBox.insert(END, 'You have not indicated a Type for every file. \n')
					return
				
			query1 =("INSERT INTO MainTable "
						"(SampleName, Element, Instrument, Spike, Technician, Contract, SampleType, calander, FilePath)"
						"VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)")
			self.TextBox.delete("1.0",END)
			for i, files in enumerate(glob.iglob(self.dlg + '/*.exp')):
				#First load up the god damn main table cause this will work no matter what.
			
				
				p
				data, errors, date = IsotopeData(self.element_var[i].get()).GrabData(files)

				dataquery1 =  [files.split('/')[-1].strip(".exp"), self.element_var[i].get(), self.machine_var[i].get(),
								 self.spike_var[i].get(), self.tech_var[i].get(), self.contract_var[i].get(),
								 self.type_var[i].get(), date, files]
				
				query2 = DataCommands[self.element_var[i].get()]
				query3 = ErrorCommands[self.element_var[i].get()]
				
				nulls = 0
				for elements in data:
					if elements ==None:
						nulls +=1

				if nulls > 1:
					self.TextBox.insert(END, '\n\n The file \n')
					self.TextBox.insert(END, files)
					self.TextBox.insert(END, "\nhas ")
					self.TextBox.insert(END, nulls)
					self.TextBox.insert(END, " NULL values for ratio/voltage "
						                     "table, the file is either not formatted correctly or\n" 
						                     "the wrong element was chosen \n\n")
					noprint = True

				print(data)
				DataToBase = tuple([str(files)] + data)
				ErrDataToBase = tuple([str(files)] + errors)
			
				try:
					db.insert(query1, dataquery1)
					db.insert(query2, DataToBase)
					db.insert(query3,ErrDataToBase)
					if noprint == False:
						self.TextBox.insert(END, "File: ")
						self.TextBox.insert(END, str(files))
						self.TextBox.insert(END,"\nhas been successfully added to the database. \n")
				except IntegrityError as e:
					db.rollypolly()
					noprint = True
					self.TextBox.insert(END, "File: ")
					self.TextBox.insert(END, str(files))
					self.TextBox.insert(END,"\nis already in the database.")
					self.TextBox.insert(END," If you want to update these values you must first"
												" remove it with \n Commit-> Remove Data. \n \n")
					pass
				except OperationalError as e:
					date = date.split("-")
					date = str(date[0]) + "-" +str(date[2]) + "-" + str(date[1])
					dataquery1 =  [files.split('/')[-1].strip(".exp"), self.element_var[i].get(), self.machine_var[i].get(),
								 self.spike_var[i].get(), self.tech_var[i].get(), self.contract_var[i].get(),
								 self.type_var[i].get(), date, files]
					db.insert(query1, dataquery1)
					db.insert(query2, DataToBase)
					db.insert(query3,ErrDataToBase)
					self.TextBox.insert(END, "File: ")
					self.TextBox.insert(END, str(files))
					self.TextBox.insert(END,"\nhas been successfully added to the database. \n")
			
			if noprint == False:
				#self.TextBox.delete("1.0",END)
				self.TextBox.insert(END, "\nCurrent directory: ")
				self.TextBox.insert(END, str(self.dlg))
				self.TextBox.insert(END, " \n has successfully been added to the database. \n")
			
		
		except AttributeError:
			self.TextBox.insert(END, "You haven't selected any directories to commit \n")
			pass
	
	def DataDelete(self):
		"""
		This deletes files from the database if, for example, you screwed up entering it 
		the first time. Academic sabotage is also an option.
		"""

		# Encryption is for cowards.y

		CorrectPassword = 'a'
		self.password = None
		self.TextBox.delete("1.0",END)
		self.GetPassword()
		if self.password != CorrectPassword:
			self.TextBox.delete("1.0",END)
			self.TextBox.insert(END, "I can't let you do that Dave. That is not the correct password. \n")
			return
		else:
			self.TextBox.delete("1.0",END)
			self.TextBox.insert(END, "Password accepted \n")
		db = Database()

		try:
			directory = self.dlg
		except AttributeError:
			self.TextBox.delete("1.0",END)
			self.TextBox.insert(END, "No directory selected, cannot update database\n")
			return
		
		for i, files in enumerate(glob.iglob(directory + '/*.exp')):
			
			DataTable = str(self.element_var[i].get()) + "Table"
			ErrorTable = str(self.element_var[i].get()) + "Error"
			
			command1 = "DELETE FROM `MainTable` WHERE FilePath = '%s' " % str(files)
		
			db.deleteinsert(command1)
			self.TextBox.insert(END, "The file: ")
			self.TextBox.insert(END, str(files))
			self.TextBox.insert(END, "\nhas been removed from the data base. \n")


	def GetPassword(self):
		self.wait_window(PasswordDialog(self))
		return self.password
	#	return self.password
		
class PasswordDialog(Toplevel):
    def __init__(self, parent2):
        Toplevel.__init__(self)
        self.parent2 = parent2
        self.label = Label(self,text="Please Enter Password")
        self.label.pack()
        self.entry = Entry(self, show='*')
        self.entry.bind("<KeyRelease-Return>", self.StorePassEvent)
        self.entry.pack()
        self.button = Button(self)
        self.button["text"] = "Submit"
        self.button["command"] = self.StorePass
        self.button.pack()


    def StorePassEvent(self, event):
        self.StorePass()

    def StorePass(self):
        self.parent2.password = self.entry.get()
        self.destroy()
        print("Password was", self.parent2.password)
        return self.parent2.password


        #print(self.parent.password)
        
        


		
def main():
	root = Tk()
	ex = RootWindow(root)
	#root.geometry("1200x450")
	root.mainloop()

if __name__ == '__main__':
	main()
