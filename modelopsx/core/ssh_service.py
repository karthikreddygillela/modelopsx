import paramiko
from io import StringIO

def ssh_to_target(jumpbox_data, target_data, command):
    try:
        # Step 1: Connect to JumpBox
        jump_client = paramiko.SSHClient()
        jump_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        if jumpbox_data['auth_type'] == 'pem':
            pkey = paramiko.RSAKey.from_private_key(jumpbox_data['pem_file'])
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

        # Step 2: Connect to Target via JumpBox
        jump_transport = jump_client.get_transport()
        dest_addr = (target_data['ip'], 22)
        local_addr = ('', 0)
        channel = jump_transport.open_channel("direct-tcpip", dest_addr, local_addr)

        target_client = paramiko.SSHClient()
        target_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        if target_data['auth_type'] == 'pem':
            pkey = paramiko.RSAKey.from_private_key(target_data['pem_file'])
            target_client.connect(
                hostname=target_data['ip'],
                username=target_data['username'],
                pkey=pkey,
                sock=channel
            )
        else:
            target_client.connect(
                hostname=target_data['ip'],
                username=target_data['username'],
                password=target_data['password'],
                sock=channel
            )

        stdin, stdout, stderr = target_client.exec_command(command)
        result = stdout.read().decode()
        error = stderr.read().decode()

        target_client.close()
        jump_client.close()

        return result if result else error

    except Exception as e:
        return f"[Error] {str(e)}"
