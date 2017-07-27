class PasswordDialog(Toplevel):
    """Prompts for password in separate window"""
    
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
