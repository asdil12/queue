queue
=====

This tool allows you to queue shell commands.
To add a command to the queue simply type:

```sh
queue wget http://foo.de/bar.iso
```

To start working on the queue, launch a runner with:
```sh
queue -r
Running cmd: wget http://foo.de/bar.iso
…
wget returned 0
```

It will run a command from the queue and then
wait for the next command.
You can start multiple runners for the same queue.

To see what is going on, simply type `queue` without any arguments.

Commands that returned an exit code != 0 will appear in red in the list.

Orphaned running commands that actually died because the runner died too
will also appear in red. These will be rescheduled automatically by
the next available runner if this is not disabled via the config file.

For more information see `queue -h`:
```
usage: queue [-h] [-E] [-e ENV_VAR] [-q QUEUE] [-l] [-L] [-m FROM TO] [-d ENTRY] [-D QUEUE] [-r] [-R] [-f] [-a] ...

positional arguments:
  cmd         Add command to queue

options:
  -h, --help  show this help message and exit
  -E          include full env
  -e ENV_VAR  env vars to include (can be repeatedly specified)
  -q QUEUE    queue to use (defaults to "default")
  -l          list queued commands
  -L          list queues
  -m FROM TO  move queue entry
  -d ENTRY    delete queue entry
  -D QUEUE    delete queue
  -r          run commands from queue
  -R          show currently running commands
  -f          show finished commands
  -a          show cmd runtime as absolute time ranges
```

Also there is a config file at `~/.config/queue/config.toml`.
```toml
[env]
# include all ENV vars for all commands (same as -E)
include_full_all = false

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
```
