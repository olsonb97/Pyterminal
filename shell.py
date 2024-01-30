import subprocess
import shlex
import os

def run_shell_command(session, command):
    try:
        shlex_command = shlex.split(command)
        new_session = session
        if command.startswith('cd'):
            new_session, output = change_directory(session, command)
        else:
            output = subprocess.check_output(shlex_command, cwd=session, stderr=subprocess.STDOUT, shell=False, text=True).rstrip()
    except subprocess.CalledProcessError as e:
        output = e.output.rstrip()
    return new_session, output

def initialize_shell():
    return os.getcwd()

def change_directory(session, command):
    path = command.split('cd', 1)[1].strip()
    try:
        os.chdir(os.path.join(session, path))
        session = os.getcwd()
        output = f"Changed directory to {session}"
    except OSError as e:
        output = f"Error: {e.strerror}"
    return session, output 