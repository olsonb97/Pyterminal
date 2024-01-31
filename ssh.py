import paramiko

# create new ssh Client
def new_session(username, hostname, password, port=22):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname, port, username, password)
    return ssh

# execute command
def run_command(session, command):

    stdin, stdout, stderr = session.exec_command(command)

    stdout.channel.recv_exit_status()
    output = stdout.read().decode()
    
    error = stderr.read().decode() if stderr else ''
    if error:
        output += error
    
    return session, output