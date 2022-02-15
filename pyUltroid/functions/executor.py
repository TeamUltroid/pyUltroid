from psutil import Process
from asyncio import create_subprocess_shell, subprocess


class Terminal:
    """Hurrr"""
    def __init__(self):
        self._processes = {}

    @staticmethod
    def to_str(data):
        return data.decode("utf-8")

    async def run(self, cmd):
        process = await create_subprocess_shell(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        pid = process.pid
        self._processes[pid] = process
        return pid

    async def terminate(self, pid):
        try:
            self._processes.pop(pid)
            return await self._processes[pid].kill()
        except KeyError:
            return None

    async def output(self, pid):
        return self.to_str(await self._processes[pid].stdout.read())

    async def error(self, pid):
        return self.to_str(await self._processes[pid].stderr.read())


class Executor:
    pass
