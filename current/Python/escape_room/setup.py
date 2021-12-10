#!/usr/bin/env python3.9
import cx_Freeze

executables = [cx_Freeze.Executable("main.py")]

cx_Freeze.setup(
    name="Escape Room",
    options={"build_exe": {"packages":["pygame", "games"],
                           "include_files":["./assets"],
                            "optimize": 2}
             },
    executables = executables
    )