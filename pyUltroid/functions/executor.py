from asyncio import create_subprocess_shell, subprocess


class Terminal:
    """
    Class for running terminal commands asynchronously.

    Methods:
        run(commands: str)
            commands: Terminal Commands.
            Returns Process id (int)
        terminate(pid: int)
            pid: Process id returned in `run` method.
            Returns True if terminated else False (bool?
        output(pid: int)
            pid: Process id returned in `run` method.
            Returns Output of process (str)
        error(pid: int)
            pid: Process id returned in `run` method.
            Returns Error of process (str)
    """
    def __init__(self) -> None:
        self._processes = {}

    @staticmethod
    def _to_str(data: bytes) -> str:
        return data.decode("utf-8").strip()

    async def run(self, cmd: str) -> int:
        process = await create_subprocess_exec(cmd.split(" "), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        pid = process.pid
        self._processes[pid] = process
        return pid

    def terminate(self, pid: int) -> bool:
        try:
            self._processes.pop(pid)
            self._processes[pid].kill()
            return True
        except KeyError:
            return False

    async def output(self, pid: int) -> str:
        return self._to_str(await self._processes[pid].stdout.readline())

    async def error(self, pid: int) -> str:
        return self._to_str(await self._processes[pid].stderr.readline())

    @property
    async def _auto_remove_processes(self) -> None:
        while len(self._processes) != 0:
            for proc in self._processes.keys():
                if proc.returncode != None: # process is still running
                    try:
                        self._processes.pop(proc)
                    except KeyError:
                        pass


class Executor:
    pass