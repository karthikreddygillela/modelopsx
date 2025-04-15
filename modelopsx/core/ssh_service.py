import paramiko
from io import StringIO

def ssh_to_jumpbox(jumpbox_data, command):
    try:
        # Step 1: Connect to JumpBox
        jump_client = paramiko.SSHClient()
        jump_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        if jumpbox_data['auth_type'] == 'pem':
            pkey = paramiko.RSAKey.from_private_key(StringIO(jumpbox_data['pem_file']))
            jump_client.connect(
                hostname=jumpbox_data['ip'],
                username=jumpbox_data['username'],
                pkey=pkey
            )
        else:
            jump_client.connect(
                hostname=jumpbox_data['ip'],
                username=jumpbox_data['username'],
                password=jumpbox_data['password']
            )

        # Optional: run a command if provided
        if command:
            stdin, stdout, stderr = jump_client.exec_command(command)
            result = stdout.read().decode()
            error = stderr.read().decode()
            jump_client.close()
            return result if result else error
        else:
            # You can return the open shell for interactive use
            chan = jump_client.invoke_shell()
            return chan  # For interactive WebSocket shells

    except Exception as e:
        return f"[Error] {str(e)}"
