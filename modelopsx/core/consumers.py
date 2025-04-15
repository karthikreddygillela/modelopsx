from channels.generic.websocket import AsyncWebsocketConsumer
import json
import asyncio
import paramiko
import io

class InteractiveSSHConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.ssh_client = None
        self.chan = None

    async def disconnect(self, code):
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
            pem = data.get("pem")

            self.ssh_client = paramiko.SSHClient()
            self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            if pem:
                key = paramiko.RSAKey.from_private_key(io.StringIO(pem))
                self.ssh_client.connect(ip, username=username, pkey=key)
            else:
                self.ssh_client.connect(ip, username=username, password=password)

            self.chan = self.ssh_client.invoke_shell()
            asyncio.create_task(self.forward_output())

        except Exception as e:
            await self.send(text_data=json.dumps({"error": str(e)}))

    async def forward_output(self):
        while True:
            try:
                if self.chan.recv_ready():
                    output = self.chan.recv(1024).decode()
                    await self.send(text_data=json.dumps({"output": output}))
                await asyncio.sleep(0.1)
            except Exception:
                break
