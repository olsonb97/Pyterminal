import tkinter as tk
import shell
import ssh

class Terminal:

    def __init__(self):

        # Initialize the application
        self.session = shell.initialize_session()
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

        # Create widgets
        self.text_box = tk.Text(self.main_frame, height=20, width=70, bg="black", fg="white", state='disabled')
        self.session_label = tk.Label(self.main_frame, text=self.session_type, anchor="w")
        self.command_box = tk.Entry(self.main_frame, borderwidth=3, relief="sunken")
        self.command_button = tk.Button(self.main_frame, text="Send", borderwidth=3, relief="raised", command=self.execute_command)

        # Pack widgets
        self.text_box.grid(row=0, column=0, columnspan=3, sticky="nsew")
        self.session_label.grid(row=1, column=0, sticky='w')
        self.command_box.grid(row=1, column=1, sticky='ew')
        self.command_button.grid(row=1, column=2, sticky='ew')

        # Bind enter to command box
        self.command_box.bind('<Return>', self.execute_command)

    def new_session(self):

        # Create Window for New Session
        new_session_window = tk.Toplevel(self.root)
        new_session_window.title("New Session")

        # Create variable for the selected dropdown option
        session_type_var = tk.StringVar(new_session_window, "Shell")  # Default value set to "Shell"

        # Create Dropdown menu in the window
        session_type_dropdown = tk.OptionMenu(new_session_window, session_type_var, "Shell", "SSH")
        session_type_dropdown.pack(padx=10, pady=10)

        # Create frame for SSH widgets
        ssh_options_frame = tk.Frame(new_session_window)

        # Pack and unpack options window based on selection
        def update_session_type(*args):
            if session_type_var.get() == "SSH":
                ssh_options_frame.pack()
            else:
                ssh_options_frame.forget()
        
        # Update GUI whenever the var is written ( changed )
        session_type_var.trace_add("write", update_session_type)

        # Create widgets for the SSH Frame
        ssh_password_label = tk.Label(ssh_options_frame, text="Password:")
        ssh_password_entry = tk.Entry(ssh_options_frame, show="*")
        ssh_username_label = tk.Label(ssh_options_frame, text="Username:")
        ssh_username_entry = tk.Entry(ssh_options_frame)
        ssh_hostname_label = tk.Label(ssh_options_frame, text="Hostname:")
        ssh_hostname_entry = tk.Entry(ssh_options_frame)
        ssh_port_label = tk.Label(ssh_options_frame, text="Port:")
        ssh_port_entry = tk.Entry(ssh_options_frame)
        ssh_port_entry.insert(0, "22")

        # Pack the SSH widgets to the SSH Frame
        ssh_hostname_label.grid(row=0, column=0, sticky="e", padx=10, pady=10)
        ssh_hostname_entry.grid(row=0, column=1, padx=10, pady=10)
        ssh_username_label.grid(row=0, column=2, sticky="e", padx=10, pady=10)
        ssh_username_entry.grid(row=0, column=3, padx=10, pady=10)
        ssh_password_label.grid(row=1, column=2, sticky="e", padx=10, pady=10)
        ssh_password_entry.grid(row=1, column=3, padx=10, pady=10)
        ssh_port_label.grid(row=1, column=0, sticky="e", padx=10, pady=10)
        ssh_port_entry.grid(row=1, column=1, padx=10, pady=10)

        # Change Session type on clicking OK button
        def on_ok():
            try:
                if session_type_var.get() == "SSH":
                    username = ssh_username_entry.get()
                    hostname = ssh_hostname_entry.get()
                    password = ssh_password_entry.get()
                    port = ssh_port_entry.get()
                    new_session = ssh.initialize_session(username, hostname, password, port)
                elif session_type_var.get() == "Shell":
                    new_session = shell.initialize_session

                self.initialize_session(new_session)

            except Exception as e:
                error_window = tk.Toplevel(self.root)
                error_window.title("Error")
                error_message = tk.Label(error_window, text=str(e), wraplength=400)
                error_message.pack(pady=10, padx=10)
                close_button = tk.Button(error_window, text="Close", command=error_window.destroy)
                close_button.pack(pady=5)
            finally:
                new_session_window.destroy()

        # Create OK button
        ok_button = tk.Button(new_session_window, text="OK", command=on_ok)
        ok_button.pack(padx=10, pady=10)

    def get_command_entry(self):
        command = self.command_box.get().strip()
        self.command_box.delete(0, tk.END)
        return command

    def execute_command(self, event=None):
        command = self.get_command_entry()
        try:
            if self.session_type == "Shell":
                session, output = shell.run_shell_command(self.session, command)
                self.session = session
            self.update_text_box(f"> {command}\n"+(f"{output}\n" if output else ""))
        except Exception as e:
            output = f"Error executing command: {e}"
    
    def initialize_session(self, session):
        self.session = session
        self.session_type = "Shell"
        self.update_text_box(f"New Shell Started: {self.session}")
        self.update_session_label()

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