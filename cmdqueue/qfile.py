#!/usr/bin/python3

import os
import tomlkit
import fcntl

def encode_line(cmd: list, env: dict, **kwargs) -> str:
    """
    Encode a line entry like this:
    cmd = ["echo", "123", "456"], env = {PWD = "/foo", FOO = "bar", BAZ = "abc"}
    """
    line = tomlkit.inline_table()
    cmd_args = tomlkit.array()
    cmd_args.extend(cmd)
    line.add('cmd', cmd_args)
    env_vars = tomlkit.inline_table()
    env = env.copy()
    # ensure PWD is first
    env_vars.add('PWD', env['PWD'])
    del env['PWD']
    env_vars.update(env)
    line.add('env', env_vars)
    line.update(kwargs)
    return tomlkit.dumps(line).strip().replace("\n", ", ")


def decode_line(line: str) -> dict:
    return dict(tomlkit.loads('toml = {%s}' % line)['toml']) # type: ignore


def encode(cmds: list) -> str:
    return "\n".join((encode_line(**cmd) for cmd in cmds))+"\n"


def decode(qstr: str) -> list:
    return [decode_line(l) for l in filter(lambda l: l, qstr.strip().split("\n"))]


lockfds = {}
def lock_file(file: str):
    global lockfds
    touch(file)
    if not lockfds.get(file):
        lockfds[file] = open(file)
    fcntl.flock(lockfds[file], fcntl.LOCK_EX)


def unlock_file(file: str):
    if f := lockfds.get(file):
        fcntl.flock(f, fcntl.LOCK_UN)


def load(file: str, unlock=True) -> list:
    touch(file)
    with open(file) as f:
        lock_file(file)
        s = f.read()
        if unlock:
            unlock_file(file)
        return decode(s)


def dump(cmds: list, file: str, unlock=True):
    with open(file, 'w') as f:
        s = encode(cmds)
        lock_file(file)
        f.write(s)
        if unlock:
            unlock_file(file)


def touch(file):
    if not os.path.exists(file):
        open(file, 'a').close()
