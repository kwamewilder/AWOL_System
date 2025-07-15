import tkinter as tk
from tkinter import ttk
import json

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AWOL Management System")
        self.geometry("800x600")

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        # Menu
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="New Entry", command=self.new_entry)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        # Toolbar
        toolbar = ttk.Frame(self, padding="5")
        toolbar.pack(side="top", fill="x")

        ttk.Button(toolbar, text="New Entry", command=self.new_entry).pack(side="left")
        ttk.Button(toolbar, text="Add AWOL/Rejab", command=self.add_awol_rejab).pack(side="left")

        self.search_var = tk.StringVar()
        self.search_var.trace("w", self.search)
        ttk.Label(toolbar, text="Search:").pack(side="left", padx=(10, 5))
        ttk.Entry(toolbar, textvariable=self.search_var).pack(side="left", fill="x", expand=True)

        # Main content area
        self.main_content = ttk.Frame(self, padding="5")
        self.main_content.pack(side="top", fill="both", expand=True)

        self.entries = []
        self.create_entry_list()

    def create_entry_list(self):
        columns = ("Svc Number", "Rank", "Name", "Unit")
        self.tree = ttk.Treeview(self.main_content, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.show_details)

        # Details view
        self.details_view = tk.Text(self.main_content, height=10)
        self.details_view.pack(fill="x")

    def show_details(self, event):
        selected_item = self.tree.focus()
        if selected_item:
            item = self.tree.item(selected_item)
            svc_number = item["values"][0]
            for entry in self.entries:
                if entry["Svc Number"] == svc_number:
                    self.details_view.delete("1.0", "end")
                    self.details_view.insert("end", f"AWOL/Rejab History for {entry['Name']}\n\n")
                    for awol_rejab in entry["AWOL/Rejab"]:
                        self.details_view.insert("end", f"AWOL Date: {awol_rejab['AWOL Date']}\n")
                        self.details_view.insert("end", f"Rejab Date: {awol_rejab['Rejab Date']}\n")
                        self.details_view.insert("end", f"Remarks: {awol_rejab['Remarks']}\n\n")
                    break

    def search(self, *args):
        search_term = self.search_var.get().lower()
        for i in self.tree.get_children():
            self.tree.delete(i)
        for entry in self.entries:
            if search_term in entry["Svc Number"].lower() or search_term in entry["Name"].lower():
                self.tree.insert("", "end", values=(entry["Svc Number"], entry["Rank"], entry["Name"], entry["Unit"]))

    def add_entry(self, entry):
        entry_dict = {
            "Svc Number": entry[0],
            "Rank": entry[1],
            "Name": entry[2],
            "Unit": entry[3],
            "AWOL/Rejab": []
        }
        self.entries.append(entry_dict)
        self.tree.insert("", "end", values=entry)

    def new_entry(self):
        NewEntryWindow(self)

    def add_awol_rejab(self):
        selected_item = self.tree.focus()
        if selected_item:
            item = self.tree.item(selected_item)
            svc_number = item["values"][0]
            for entry in self.entries:
                if entry["Svc Number"] == svc_number:
                    AddAwolRejabWindow(self, entry)
                    break

class AddAwolRejabWindow(tk.Toplevel):
    def __init__(self, master, entry):
        super().__init__(master)
        self.master = master
        self.entry = entry
        self.title(f"Add AWOL/Rejab for {entry['Name']}")
        self.geometry("400x300")

        self.create_widgets()

    def create_widgets(self):
        # Form fields
        labels = ["AWOL Date:", "Rejab Date:", "Remarks:"]
        self.entries = {}
        for i, label_text in enumerate(labels):
            ttk.Label(self, text=label_text).grid(row=i, column=0, padx=5, pady=5, sticky="w")
            entry = ttk.Entry(self)
            entry.grid(row=i, column=1, padx=5, pady=5, sticky="ew")
            self.entries[label_text[:-1]] = entry

        # Buttons
        button_frame = ttk.Frame(self)
        button_frame.grid(row=len(labels), column=0, columnspan=2, pady=10)
        ttk.Button(button_frame, text="Save", command=self.save_awol_rejab).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Cancel", command=self.destroy).pack(side="left", padx=5)

    def save_awol_rejab(self):
        awol_rejab_data = {
            "AWOL Date": self.entries["AWOL Date"].get(),
            "Rejab Date": self.entries["Rejab Date"].get(),
            "Remarks": self.entries["Remarks"].get()
        }
        self.entry["AWOL/Rejab"].append(awol_rejab_data)
        self.destroy()

class NewEntryWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.title("New Entry")
        self.geometry("400x300")

        self.create_widgets()

    def create_widgets(self):
        # Form fields
        self.entries = {}
        labels = ["Svc Number:", "Rank:", "Name:", "Unit:"]
        for i, label_text in enumerate(labels):
            ttk.Label(self, text=label_text).grid(row=i, column=0, padx=5, pady=5, sticky="w")
            entry = ttk.Entry(self)
            entry.grid(row=i, column=1, padx=5, pady=5, sticky="ew")
            self.entries[label_text[:-1]] = entry

        # Buttons
        button_frame = ttk.Frame(self)
        button_frame.grid(row=len(labels), column=0, columnspan=2, pady=10)
        ttk.Button(button_frame, text="Save", command=self.save_entry).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Cancel", command=self.destroy).pack(side="left", padx=5)

    def save_entry(self):
        entry_data = (
            self.entries["Svc Number"].get(),
            self.entries["Rank"].get(),
            self.entries["Name"].get(),
            self.entries["Unit"].get(),
        )
        self.master.add_entry(entry_data)
        self.destroy()

    def on_closing(self):
        self.save_data()
        self.destroy()

    def load_data(self):
        try:
            with open("data.json", "r") as f:
                self.entries = json.load(f)
                for entry in self.entries:
                    self.tree.insert("", "end", values=(entry["Svc Number"], entry["Rank"], entry["Name"], entry["Unit"]))
        except FileNotFoundError:
            pass

    def save_data(self):
        with open("data.json", "w") as f:
            json.dump(self.entries, f, indent=4)

if __name__ == "__main__":
    app = App()
    app.mainloop()
