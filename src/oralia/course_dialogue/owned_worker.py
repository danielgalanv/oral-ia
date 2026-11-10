"""Identity-bound cleanup for the explicitly spawned local worker tree."""

import psutil


class OwnedWorkerTree:
    def __init__(self, pid):
        self.root = psutil.Process(pid)
        self.born = self.root.create_time()
        self.owned = {pid: (self.root, self.born)}

    @staticmethod
    def alive(process, born):
        try:
            return process.create_time() == born and process.is_running()
        except psutil.NoSuchProcess:
            return False

    def capture(self):
        if self.alive(self.root, self.born):
            try:
                for child in self.root.children(recursive=True):
                    self.owned.setdefault(child.pid, (child, child.create_time()))
            except psutil.NoSuchProcess:
                pass

    def terminate(self):
        self.capture()
        # Stop descendants first; PID reuse never grants ownership.
        for process, born in reversed(list(self.owned.values())):
            if self.alive(process, born):
                try:
                    process.terminate()
                except psutil.NoSuchProcess:
                    pass

    def finish(self):
        self.terminate()
        for process, born in reversed(list(self.owned.values())):
            if self.alive(process, born):
                try:
                    process.wait(timeout=5)
                except psutil.TimeoutExpired:
                    if self.alive(process, born):
                        process.kill()
                        process.wait(timeout=5)
                except psutil.NoSuchProcess:
                    pass
        return [
            {"pid": process.pid, "created": born, "stopped": not self.alive(process, born)}
            for process, born in self.owned.values()
        ]
