
from datetime import datetime

def now() -> str:
    d = datetime.now()
    return str(datetime.now().replace(microsecond=d.microsecond // 1000 * 1000)).strip('0')

def htdiff(end, start, absolute=False) -> str:
    end = datetime.fromisoformat(end)
    start = datetime.fromisoformat(start)
    if absolute:
        if start.date() == end.date():
            end = end.time()
        start = start.replace(microsecond=0)
        end = end.replace(microsecond=0)
        return f"{start} - {end}"
    d = end - start
    hours = d.days * 24
    hours += d.seconds // 3600
    minutes = (d.seconds % 3600) // 60
    seconds = d.seconds % 60
    milliseconds = d.microseconds // 1000
    s = ''
    if hours:
        s += f"{hours}h"
    if minutes:
        if s:
            s += ' '
        s += f"{minutes}m"
    if seconds:
        if s:
            s += ' '
        s += f"{seconds}s"
    if milliseconds and not s:
        s += f"{milliseconds}ms"
    return s
