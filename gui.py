import json
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

def load_json():
    with open('data.json', 'r') as f:
        return json.load(f)

def save_json(data):
    with open('data.json', 'w') as f:
        json.dump(data, f, indent=4)

def update_treeview():
    for item in tree.get_children():
        tree.delete(item)
    for i, model in enumerate(data):
        tree.insert("", "end", iid=i, values=(
            model["Name"], model["Part Number"], model["Colors"],
            model["RAM"], model["Price"], model["Storage"]
            ))

def save_edits():
    selected_item = tree.selection()[0]
    for i, field in enumerate(fields):
        data[int(selected_item)][field] = entries[i].get()
    save_json(data)
    update_treeview()
    messagebox.showinfo("Info", "Changes saved successfully")

def on_item_selected(event):
    selected_item = tree.selection()[0]
    model = data[int(selected_item)]
    for i, field in enumerate(fields):
        entries[i].delete(0, END)
        entries[i].insert(0, model[field])

data = load_json()

root = Tk()
root.title("Phone Models")
root.geometry("1200x600")

columns = ["Name", "Part Number", "Colors", "RAM", "Price", "Storage"]
tree = ttk.Treeview(root, columns=columns, show='headings')

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=150)

tree.pack(fill=BOTH, expand=True)

scrollbar = Scrollbar(tree, orient="vertical", command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.pack(side=RIGHT, fill=Y)

update_treeview()

tree.bind('<<TreeviewSelect>>', on_item_selected)

edit_frame = Frame(root)
edit_frame.pack(pady=10)

fields = ["Name", "Part Number", "Colors", "RAM", "Price", "Storage"]
entries = []

for field in fields:
    frame = Frame(edit_frame)
    frame.pack(fill=X, padx=5, pady=5)
    label = Label(frame, text=field, width=15)
    label.pack(side=LEFT)
    entry = Entry(frame)
    entry.pack(side=RIGHT, fill=X, expand=True)
    entries.append(entry)

save_button = Button(root, text="Save", command=save_edits)
save_button.pack(pady=10)

root.mainloop()
