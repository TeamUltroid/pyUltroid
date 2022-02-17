from psutil import Process
from asyncio import create_subprocess_shell, subprocess


class Terminal:
    """Hurrr"""
    def __init__(self):
        self._processes = {}

    @staticmethod
    def to_str(data):
        return data.decode("utf-8").strip()

    async def run(self, cmd):
        process = await create_subprocess_exec(cmd.split(" "), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        pid = process.pid
        self._processes[pid] = process
        return pid

    def terminate(self, pid):
        try:
            self._processes.pop(pid)
            return self._processes[pid].kill()
        except KeyError:
            return None

    async def output(self, pid):
        return self.to_str(await self._processes[pid].stdout.readline())

    async def error(self, pid):
        return self.to_str(await self._processes[pid].stderr.readline())

    async def _auto_remove_processes(self):
        while len(self._processes) != 0:
            for proc in self._processes.keys():
                if proc.returncode != None: # process is still running
                    try:
                        self._processes.pop(proc)
                    except KeyError:
                        pass


class Executor:
    pass
