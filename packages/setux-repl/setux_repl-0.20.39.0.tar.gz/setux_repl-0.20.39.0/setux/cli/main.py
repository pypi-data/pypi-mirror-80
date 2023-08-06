from os import environ
from os.path import expanduser
from sys import argv

from setux.targets import Local, SSH
from setux.logger import debug
from setux.repl import commands
from setux.repl.repl import repl, help
from .usage import usage


def get_target(name=None, dest=None):
    name = name or environ.get('setux_target')
    dest = dest or environ.get('setux_outdir', expanduser('~/setux'))
    if name:
        target = SSH(name=name, host=name, outdir=dest)
    else:
        target = Local(outdir=dest)
    return target


def main():

    if len(argv)==1:
        target = get_target()
        debug(f'repl {target}')
        repl(target)

    elif len(argv)==2:
        name = argv[1]
        if name=='help':
            help()
            return
        target = get_target()
        cmd = commands.get(name)
        if name in target.modules.items:
            target.deploy(name)
        elif cmd:
            cmd(target, None)
        else:
            try:
                target = get_target(name)
            except:
                target = None
            if target and target.cnx:
                repl(target)
            else:
                return usage()

    elif len(argv)==3:
        name, t = argv[1:]
        try:
            target = get_target(t)
        except:
            target = None
        if not (target and target.cnx):
            return usage()
        cmd = commands.get(name)
        if name in target.modules.items:
            target.deploy(name)
        elif cmd:
            cmd(target, None)
        else:
            print(f' unkown ! {name} !')
            return usage()

