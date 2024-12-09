import os
import tomlkit

config_dir = os.path.expanduser('~/.config/queue')
queues_dir = os.path.join(config_dir, 'queues')
running_file = os.path.join(config_dir, 'running')
finished_file = os.path.join(config_dir, 'finished')

def queue_file_path(queue_name: str) -> str:
    return os.path.join(queues_dir, queue_name)

def ls_queues() -> list:
    queues = os.listdir(queues_dir)
    if 'default' in queues:
        queues.remove('default')
        queues.insert(0, 'default')
    return queues

def cmdfmt(entry: dict) -> str:
    return ' '.join(entry['cmd'])

def envpwdfmt(entry: dict) -> tuple[str, str]:
    """pop PWD from entry"""
    env = entry['env'].copy()
    pwd = entry['env']['PWD']
    del env['PWD']
    envf = tomlkit.inline_table()
    envf.update(env)
    return pwd, tomlkit.dumps(env).strip().replace("\n", ", ")
