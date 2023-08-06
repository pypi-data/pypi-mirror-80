# OLIB - object library
#
#

__version__ = 11

import importlib
import ol
import os
import time
import threading

starttime = time.time()

class Kernel(ol.hdl.Handler):

    def __init__(self):
        super().__init__()
        self.ready = threading.Event()
        self.stopped = False
        self.cfg = ol.Cfg()
        kernels.append(self)

    def announce(self, txt):
        pass

    def cmd(self, txt):
        if not txt:
            return None
        e = ol.hdl.Event()
        e.txt = txt
        ol.prs.parse(e, e.txt)
        self.dispatch(e)
        return e

    def init(self, mns):
        mods = []
        thrs = []
        for mn in ol.utl.spl(mns):
            ms = ""
            for pn in self.packages:
                n = "%s.%s" % (pn, mn)
                spec = importlib.util.find_spec(n)
                if spec:
                    ms = n
                    break
            print(ms)
            if not ms:
                continue
            try:
                mod = self.load_mod(ms)
            except (ModuleNotFoundError, ValueError):
                try:
                    mod = self.load_mod(mn)
                except (ModuleNotFoundError, ValueError) as ex:
                    if mn in str(ex):
                        continue
                    print(ol.utl.get_exception())
                    continue
            mods.append(mod)
            func = getattr(mod, "init", None)
            if func:
                thrs.append(ol.tsk.launch(func, self, name=ol.get_name(func)))
        for thr in thrs:
            thr.join()
        return mods

    def scandir(self, path):
        mods = []
        ol.utl.cdir(path + os.sep + "")
        for fn in os.listdir(path):
            if fn.startswith("_") or not fn.endswith(".py"):
                continue
            mn = "bmod.%s" % fn[:-3]
            try:
                module = self.load_mod(mn)
            except Exception as ex:
                print(ol.utl.get_exception())
                continue
            mods.append(module)
        return mods

    def say(self, channel, txt):
        print(txt)

    def start(self):
        assert ol.wd
        super().start()

    def stop(self):
        self.stopped = True
        self.queue.put(None)

    def wait(self):
        while not self.stopped:
            time.sleep(60.0)

kernels = []

def boot(name, wd, md=""):
    cfg = ol.prs.parse_cli()
    k = get_kernel()
    ol.update(k.cfg, cfg)
    ol.wd = k.cfg.wd = wd
    k.cfg.md = md or os.path.join(ol.wd, "bmod", "")
    return k

def get_kernel():
    if kernels:
        return kernels[0]
    return Kernel()
