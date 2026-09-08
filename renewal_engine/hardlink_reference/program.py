def link(source, target):
    from pathlib import Path
    s = Path(source)
    t = Path(target)
    s.link_to(t)
