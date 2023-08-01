import argparse
import tkinter as tk
from tkinter import ttk, messagebox
import basic_templates
import user_templates
from pprint import pformat
from commitment import load_key, load_data, save_data, commit_changes


class DictEditor(ttk.Frame):
    def __init__(self, master=None, args=None):
        super().__init__(master)
        self.master = master
        self.args = args
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.tree = ttk.Treeview(self.master)
        self.tree["columns"]=("key", "value")
        self.tree.column("#0", width=270, minwidth=270, stretch=tk.NO)
        self.tree.column("key", width=150, minwidth=150, stretch=tk.NO)
        self.tree.column("value", width=400, minwidth=200)

        self.tree.heading("#0",text="Parent",anchor=tk.W)
        self.tree.heading("key", text="Key",anchor=tk.W)
        self.tree.heading("value", text="Value/Type",anchor=tk.W)

        self.tree.pack(side="top", fill="both")
        self.add_btn = tk.Button(self.master, text="Add", command=self.add_item)
        self.add_btn.pack(side="left")
        self.del_btn = tk.Button(self.master, text="Delete", command=self.del_item)
        self.del_btn.pack(side="left")
        self.edit_btn = tk.Button(self.master, text="Edit", command=self.edit_item)
        self.edit_btn.pack(side="left")
        self.show_btn = tk.Button(self.master, text="Show dict", command=self.show_dict)
        self.show_btn.pack(side="left")
        # create the buttons
        load_data_button = ttk.Button(self, text="Load data")
        save_data_button = ttk.Button(self, text="Save data")
        commit_button = ttk.Button(self, text="Commit changes")

        # assign commands to the buttons
        load_data_button['command'] = self.load_data
        save_data_button['command'] = self.save_data
        commit_button['command'] = self.get_commit_message

        # place the buttons onto the grid
        load_data_button.grid(row=4, column=0, sticky='w')
        save_data_button.grid(row=4, column=1, sticky='w')
        commit_button.grid(row=4, column=2, sticky='w')

        self.key_var = tk.StringVar()
        self.value_var = tk.StringVar()
        self.key_entry = tk.Entry(self.master, textvariable=self.key_var)
        self.value_entry = tk.Entry(self.master, textvariable=self.value_var)

        self.load_data()

    def load_data(self):
        # assume args.key_file is defined somewhere in your code, or you can set it manually
        key = load_key(args.key_file)
        self.bdb_data = load_data('bdb.jsonc', key)
        #self.tree.delete(*self.tree.get_children())
        #self.add_dict(self.data)

    def save_data(self):
        key = load_key(args.key_file)
        data_to_save = self.show_dict()
        self.bdb_data.append(data_to_save)
        save_data('bdb.jsonc', self.bdb_data, key)

    def commit_changes(self):
        commit_changes('.', 'bdb.jsonc', 'updated data commit message')

    def get_commit_message(self):
        # create a top level window
        top = tk.Toplevel()
        top.title("Commit Message")
        msg_label = ttk.Label(top, text="Enter commit message:")
        msg_label.pack(side="top")

        msg_entry = ttk.Entry(top)
        msg_entry.pack(side="top")

        submit_button = ttk.Button(top, text="Submit",
                                   command=lambda: self.commit_changes(msg_entry.get()))
        submit_button.pack(side="bottom")

    def commit_changes(self, commit_message):
        # args.key_file is defined somewhere in your code or you can set it manually
        key = load_key(args.key_file)
        save_data('bdb.jsonc', self.data, key)
        commit_changes('.', 'bdb.jsonc', commit_message)
        print('Data committed with message:', commit_message)

    def add_item(self):
        selected = self.tree.focus()
        self.key_entry.pack(side="left")
        self.value_entry.pack(side="left")
        self.confirm_btn = tk.Button(self.master, text="Confirm Add", command=lambda: self.confirm_add())
        self.confirm_btn.pack(side="left")
    


    def confirm_add(self, parent):
        key = self.key_var.get()
        value = self.value_var.get()
        if key:
            if parent:
                self.tree.insert(parent, "end", text="Child", values=(key, value))
            else:
                self.tree.insert('', 'end', text="Parent", values=(key, value))
        else:
            messagebox.showerror("Error", "Key cannot be empty")
        self.clear_entry()

    def confirm_add(self):
        selected = self.tree.focus()
        key = self.key_entry.get()
        value = self.value_entry.get()
        if value.startswith('.'):
            templates = {**basic_templates.basic_templates, **user_templates.user_templates}
            if value in templates:
                template = templates[value]
                self.insert_template(template, key, parent=selected)
            else:
                messagebox.showinfo('Invalid Template', f'No template named {value} found.')
        else:
            value_type = self.entry_value_type.get()
            if value_type == ".dict":
                self.tree.insert(selected, "end", text="Child", values=(key, value_type))
            elif value_type == ".array":
                self.tree.insert(selected, "end", text="Child", values=(key, value_type))
            else:
                self.tree.insert(selected, "end", text="Child", values=(key, value))

    def insert_template(self, template, key, parent=""):
        templates = {**basic_templates.basic_templates, **user_templates.user_templates}
        if isinstance(template, dict):
            new_parent = self.tree.insert(parent, "end", text="Child", values=(key, '.dict'))
            for k, v in template.items():
                if isinstance(v, str) and v.startswith('.'):
                    if v in templates:
                        self.insert_template(templates[v], k, parent=new_parent)
                    else:
                        self.tree.insert(new_parent, "end", text="Child", values=(k, v))
                elif isinstance(v, dict):
                    self.insert_template(v, k, parent=new_parent)
                elif isinstance(v, list):
                    self.insert_template(v, k, parent=new_parent)
                else:
                    self.tree.insert(new_parent, "end", text="Child", values=(k, v))
        elif isinstance(template, list):
            new_parent = self.tree.insert(parent, "end", text="Child", values=(key, '.array'))
            for i, v in enumerate(template):
                if isinstance(v, str) and v.startswith('.'):
                    if v in templates:
                        self.insert_template(templates[v], f'index_{i}', parent=new_parent)
                    else:
                        self.tree.insert(new_parent, "end", text="Child", values=(f'index_{i}', v))
                elif isinstance(v, dict):
                    self.insert_template(v, f'index_{i}', parent=new_parent)
                elif isinstance(v, list):
                    self.insert_template(v, f'index_{i}', parent=new_parent)
                else:
                    self.tree.insert(new_parent, "end", text="Child", values=(f'index_{i}', v))
        else:
            self.tree.insert(parent, "end", text="Child", values=(key, template))

    def del_item(self):
        selected = self.tree.focus()
        if selected:
            self.tree.delete(selected)

    def edit_item(self):
        selected = self.tree.focus()
        if selected:
            item = self.tree.item(selected)
            self.key_var.set(item['values'][0])
            self.value_var.set(item['values'][1])
            self.key_entry.pack(side="left")
            self.value_entry.pack(side="left")
            self.confirm_btn = tk.Button(self.master, text="Confirm Edit", command=lambda: self.confirm_edit(selected))
            self.confirm_btn.pack(side="left")

    def confirm_edit(self, item_id):
        key = self.key_var.get()
        value = self.value_var.get()
        if key:
            self.tree.item(item_id, values=(key, value))
        else:
            messagebox.showerror("Error", "Key cannot be empty")
        self.clear_entry()

    def clear_entry(self):
        self.key_var.set("")
        self.value_var.set("")
        self.key_entry.pack_forget()
        self.value_entry.pack_forget()
        self.confirm_btn.pack_forget()

    def show_dict(self):
        root_children = self.tree.get_children('')
        res_dict = self.extract_dict(root_children)
        print(res_dict)
        return res_dict

    def extract_dict(self, children, parent=""):
        res_dict = {}
        for child in children:
            key, value_type = self.tree.item(child)['values']
            new_children = self.tree.get_children(child)
            if new_children:
                if value_type == '.dict':
                    res_dict[key] = self.extract_dict(new_children, child)
                elif value_type == '.array':
                    res_dict[key] = self.extract_list(new_children, child)
            else:
                if value_type not in ['.dict', '.array']:
                    res_dict[key] = value_type
        return res_dict

    def extract_list(self, children, parent=""):
        res_list = []
        for child in children:
            key, value_type = self.tree.item(child)['values']
            new_children = self.tree.get_children(child)
            if new_children:
                if value_type == '.dict':
                    res_list.append(self.extract_dict(new_children, child))
                elif value_type == '.array':
                    res_list.append(self.extract_list(new_children, child))
            else:
                if value_type not in ['.dict', '.array']:
                    res_list.append(value_type)
        return res_list
    def save_template(self):
        selected = self.tree.focus()
        if selected:
            root_children = self.tree.get_children(selected)
            res_dict = self.extract_dict(root_children)
            template_name = simpledialog.askstring("Input", "Enter template name:", parent=self.master)
            if template_name:
                user_templates.user_templates['.' + template_name] = res_dict
                with open('user_templates.py', 'w') as f:
                    f.write(f'user_templates = {pformat(user_templates.user_templates)}')

    def add_template(self):
        selected = self.tree.focus()
        templates = {**basic_templates.basic_templates, **user_templates.user_templates}
        template_name = simpledialog.askstring("Input", "Enter template name:", parent=self.master)
        if template_name and template_name in templates:
            template = templates[template_name]
            self.add_dict(template, parent=selected)

    def add_dict(self, data_dict, parent=""):
        templates = {**basic_templates.basic_templates, **user_templates.user_templates}
        for key, value in data_dict.items():
            if isinstance(value, str) and value.startswith('.'):
                if value in templates:
                    template = templates[value]
                    if isinstance(template, dict):
                        new_parent = self.tree.insert(parent, "end", text="Child", values=(key, '.dict'))
                        self.add_dict(template, new_parent)
                    elif isinstance(template, list):
                        new_parent = self.tree.insert(parent, "end", text="Child", values=(key, '.array'))
                        self.add_list(template, new_parent)
            elif isinstance(value, dict):
                new_parent = self.tree.insert(parent, "end", text="Child", values=(key, '.dict'))
                self.add_dict(value, new_parent)
            elif isinstance(value, list):
                new_parent = self.tree.insert(parent, "end", text="Child", values=(key, '.array'))
                self.add_list(value, new_parent)
            else:
                self.tree.insert(parent, "end", text="Child", values=(key, value))

    def add_list(self, data_list, parent=""):
        templates = {**basic_templates.basic_templates, **user_templates.user_templates}
        for i, value in enumerate(data_list):
            if isinstance(value, str) and value.startswith('.'):
                if value in templates:
                    template = templates[value]
                    if isinstance(template, dict):
                        new_parent = self.tree.insert(parent, "end", text="Child", values=(f'index_{i}', '.dict'))
                        self.add_dict(template, new_parent)
                    elif isinstance(template, list):
                        new_parent = self.tree.insert(parent, "end", text="Child", values=(f'index_{i}', '.array'))
                        self.add_list(template, new_parent)
            elif isinstance(value, dict):
                new_parent = self.tree.insert(parent, "end", text="Child", values=(f'index_{i}', '.dict'))
                self.add_dict(value, new_parent)
            elif isinstance(value, list):
                new_parent = self.tree.insert(parent, "end", text="Child", values=(f'index_{i}', '.array'))
                self.add_list(value, new_parent)
            else:
                self.tree.insert(parent, "end", text="Child", values=(f'index_{i}', value))


# Parsing command-line arguments
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--key_file', type=str, help='Path to the file containing the encryption key')
    args = parser.parse_args()

    print(f'key path is {args}')

    root = tk.Tk()
    app = DictEditor(master=root, args=args)
    app.mainloop()
