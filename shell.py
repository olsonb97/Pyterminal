import subprocess
import os

initial_dir = os.getcwd()

def new_session():
    return initial_dir

def run_command(session, command):
    try:
        new_session = session
        output = ""
        if command.startswith('cd'):
            new_session, output = change_directory(session, command)
        else:
            output = subprocess.check_output(command, cwd=session, stderr=subprocess.STDOUT, shell=True, text=True).rstrip()
    except subprocess.SubprocessError as e:
        output = f"Command execution error: {e}"
    except Exception as e:
        output = f"Unexpected error: {e}"
    return new_session, output

def change_directory(session, command):
    path = command.split('cd', 1)[1].strip()
    new_path = os.path.join(session, path)
    normalized_path = os.path.normpath(new_path)

    if os.path.isdir(normalized_path) and os.path.exists(normalized_path):
        session = normalized_path
        output = f"Changed directory to {session}"
    else:
        output = "Invalid directory"
    return session, output
