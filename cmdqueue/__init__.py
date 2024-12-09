import os
import toml
import tomlkit
import textwrap

config_dir = os.path.expanduser('~/.config/queue')
config_file = os.path.join(config_dir, 'config.toml')
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


def ensure_existing_files(queue: str):
    os.makedirs(queues_dir, exist_ok=True)
    if not os.path.exists(config_file):
        default_config = textwrap.dedent("""
            [env]
            # include all ENV vars for all commands (same as -E)
            include_all = false

            # list of ENV vars to include (same as -e)
            # e.g. include = ["SHELL", "SSH_AUTH_SOCK"]
            include = []

            [env.static]
            # additional statically configured ENV vars
            # FOO = "bar"

            [running]
            # When the queue runner is stopped during cmd execution
            # this leaves the cmd orphaned that was executed at that time.
            # If reschedule_orphaned_cmds is enabled this cmd will get rescheduled.
            reschedule_orphaned_cmds = true
        """)
        with open(config_file, 'w') as f:
            f.write(default_config)

def load_config() -> dict:
    with open(config_file, 'r') as f:
        return toml.load(f)
