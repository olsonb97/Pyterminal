import tkinter as tk
import os
import shell

class Terminal:

    def __init__(self):

        # Initialize the application
        self.initial_dir = os.getcwd()
        self.session = self.initial_dir
        self.session_type = "Shell"
        self.initialize_ui()

    def initialize_ui(self):

        self.root = tk.Tk()
        self.root.title("Pyterminal")

        # Create the menu bar
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        # Create the "File" menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)

        # Add "New Session" command to the "Session" menu
        self.file_menu.add_command(label="New Session", command=self.new_session)

        # Create a frame to hold all widgets
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Configure grid weights
        self.main_frame.columnconfigure(0, weight=0)
        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.rowconfigure(0, weight=1)

        # Create a text box for command output
        self.text_box = tk.Text(self.main_frame, height=20, width=70, bg="black", fg="white", state='disabled')
        self.text_box.grid(row=0, column=0, columnspan=3, sticky="nsew")

        # Session label
        self.session_label = tk.Label(self.main_frame, text=self.session_type, anchor="w")
        self.session_label.grid(row=1, column=0, sticky='w')

        # Command entry box
        self.command_box = tk.Entry(self.main_frame, borderwidth=3, relief="sunken")
        self.command_box.grid(row=1, column=1, sticky='ew')
        self.command_box.bind('<Return>', self.execute_command)

        # Send button
        self.command_button = tk.Button(self.main_frame, text="Send", borderwidth=3, relief="raised", command=self.execute_command)
        self.command_button.grid(row=1, column=2, sticky='ew')

    def new_session(self):
        new_session_window = tk.Toplevel(self.root)
        new_session_window.title("New Session")

        session_type_var = tk.StringVar(new_session_window)
        session_type_var.set("Shell")  # default value

        def update_session_type(*args):
            session_type = session_type_var.get()
            if session_type == "SSH":
                ssh_options_frame.pack()
            else:
                ssh_options_frame.forget()

        # Use trace_add instead of trace
        session_type_var.trace_add("write", update_session_type)

        session_type_dropdown = tk.OptionMenu(new_session_window, session_type_var, "Shell", "SSH")
        session_type_dropdown.pack(padx=10, pady=10)

        ssh_options_frame = tk.Frame(new_session_window)
        ssh_username_label = tk.Label(ssh_options_frame, text="Username:")
        ssh_username_entry = tk.Entry(ssh_options_frame)
        ssh_ip_label = tk.Label(ssh_options_frame, text="IP Address:")
        ssh_ip_entry = tk.Entry(ssh_options_frame)

        ssh_username_label.grid(row=0, column=0, sticky="e", padx=10, pady=10)
        ssh_username_entry.grid(row=0, column=1, padx=10, pady=10)
        ssh_ip_label.grid(row=1, column=0, sticky="e", padx=10, pady=10)
        ssh_ip_entry.grid(row=1, column=1, padx=10, pady=10)

        def on_ok():
            if session_type_var.get() == "SSH":
                username = ssh_username_entry.get()
                ip_address = ssh_ip_entry.get()
                # Logic for SSH session
            else:
                self.session = self.initial_dir
            new_session_window.destroy()

        ok_button = tk.Button(new_session_window, text="OK", command=on_ok)
        ok_button.pack(padx=10, pady=10)

    def execute_command(self, event=None):
        command = self.command_box.get().strip()
        output = ""
        if self.session_type == "Shell":
            session, output = shell.run_shell_command(self.session, command)
            self.session = session
        self.update_text_box(f"> {command}\n"+(f"{output}\n" if output else ""))
        self.command_box.delete(0, tk.END)

    def update_text_box(self, output):
        self.text_box.config(state='normal')
        self.text_box.insert(tk.END, output)
        self.text_box.see(tk.END)
        self.text_box.config(state='disabled')
        self.update_session_label()

    def update_session_label(self):
        self.session_label.config(text=self.session_type)

    def run(self):
        self.root.mainloop()

obj = Terminal()
obj.run()