# ------------------------------------------------------------------------------
#  Created by Tyler Stegmaier
#  Copyright (c) 2020.
#
# ------------------------------------------------------------------------------

from .Widgets import _BaseTkinterWidget_, tk




__all__ = ['DebugWidget']

def DebugWidget(w: _BaseTkinterWidget_, *, root: tk.Tk or tk.Toplevel, Message: str):
    assert (isinstance(w, _BaseTkinterWidget_) and isinstance(w, tk.BaseWidget))
    from pprint import PrettyPrinter
    pp = PrettyPrinter(indent=4)
    print(f'---------------- {Message} < {w.__class__.__name__} > ----------------')
    pp.pprint({
            'root.children':                  root.children,
            'Type':                           w.__class__,
            'Widget':                         w,
            'PI (position info)':             w.pi,
            'w.master.children':              w.master.children,
            'w.children':                     w.children,
            'w.winfo_id()':                   w.winfo_id(),
            'w.winfo_name()':                 w.winfo_name(),
            'w.winfo_parent()':               w.winfo_parent(),
            'w.winfo_manager()':              w.winfo_manager(),
            'w.winfo_ismapped()':             w.winfo_ismapped(),
            'w.winfo_children()':             w.winfo_children(),
            'w.winfo_pathname(w.winfo_id())': w.winfo_pathname(w.winfo_id()),
            })
    print()
    print()
