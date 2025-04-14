from channels.generic.websocket import AsyncWebsocketConsumer
import json
import paramiko
import asyncio
import io

class InteractiveSSHConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.ssh_client = None
        self.chan = None

    async def disconnect(self, close_code):
        if self.chan:
            self.chan.close()
        if self.ssh_client:
            self.ssh_client.close()

    async def receive(self, text_data):
        data = json.loads(text_data)

        if data.get("action") == "connect":
            await self.start_ssh(data)
        elif self.chan:
            self.chan.send(data.get("command"))

    async def start_ssh(self, data):
        try:
            ip = data.get("ip")
            username = data.get("username")
            password = data.get("password")
            pem_content = data.get("pem")

            self.ssh_client = paramiko.SSHClient()
            self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            if pem_content:
                pkey = paramiko.RSAKey.from_private_key(io.StringIO(pem_content))
                self.ssh_client.connect(ip, username=username, pkey=pkey)
            else:
                self.ssh_client.connect(ip, username=username, password=password)

            self.chan = self.ssh_client.invoke_shell()
            asyncio.create_task(self.send_shell_output())

        except Exception as e:
            await self.send(text_data=json.dumps({"error": str(e)}))

    async def send_shell_output(self):
        while True:
            try:
                if self.chan.recv_ready():
                    data = self.chan.recv(1024).decode()
                    await self.send(text_data=json.dumps({"output": data}))
                await asyncio.sleep(0.1)
            except Exception:
                break
