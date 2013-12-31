# SQL GUI
import Tkinter as tk
from sql_interpreter import SqlBox


class SqlGUI():
    IN_STR = "in<<"
    OUT_STR = "out>>"
    END = "\n"

    def __init__(self, master):
        #- DECLARE VARIABLES -#
        self.command_entry_var = tk.StringVar()
        self.in_query = False # INDACES INRTO QUESTION
        self.database = None
        # -- FRAME DESIGN -- #
        # *  - CREATE FRAME -  * #
        self.frame = tk.Frame(master,bg = 'red',)
        self.frame.grid()
        #- MENU -#
            #- CREATE SCROLLBAR -#
        self.scrollbar = tk.Scrollbar(self.frame)
        self.scrollbar.grid(column = 1, row = 0, sticky= tk.N + tk.S)
            #- CREATE TEXTBOX -#
        self.text_box = tk.Text(self.frame, padx=5,pady=5, width=100)
        self.text_box.grid(column = 0, row = 0, padx=2, pady=2)
            # ATTACH SCROLLBAR #
        self.text_box.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.text_box.yview)
            #- COMMAND CREATE ENTRY -#
        self.command_entry = tk.Entry(self.frame,
                                      textvariable=self.command_entry_var,
                                      width=100)
        self.command_entry.grid(padx=2,pady=2)
        #---- BINDINGS ----#
        self.command_entry.bind("<Return>", self.on_enter)
        # --- ON CREATION --- #
        self.text_box.insert(tk.END,"DATABASE NAME?: ")
        self.in_query = True
    
    #---- EVENTS ----#
    def on_enter(self,*args):
        text = self.command_entry_var.get()
        print text
        self.command_entry_var.set('')
        
        if self.in_query:
            # IF INTRO QUESTIOJN
            self.database = SqlBox(text)
            self.text_box.insert(tk.END, text+SqlGUI.END) 
            self.in_query = False
        else:
            # IF TYPICAL INPUT
            response = self.database.in_(text)            
            self.text_box.insert(tk.END,SqlGUI.IN_STR+text+SqlGUI.END)
            
            # IF RESPONSE:
            if type(response) == list:
                for line in response:
                    line_string = str(line)
                    self.text_box.insert(tk.END, (SqlGUI.OUT_STR+line_string+'\n\n'))
            elif type(response) == str:
                self.text_box.insert(tk.END, SqlGUI.OUT_STR+response+SqlGUI.END)
            else:
                self.text_box.insert(tk.END, str(response)+SqlGUI.END)
                self.text_box.see(tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("SQL INTERPRETER")
    app = SqlGUI(root)
    root.mainloop()
    try:
        root.destroy()
    except:
        pass
