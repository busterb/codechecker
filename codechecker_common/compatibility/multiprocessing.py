# -------------------------------------------------------------------------
#
#  Part of the CodeChecker project, under the Apache License v2.0 with
#  LLVM Exceptions. See LICENSE for license information.
#  SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
#
# -------------------------------------------------------------------------
"""
Multiprocessing compatibility module.
"""
import sys

# pylint: disable=no-name-in-module
# pylint: disable=unused-import
if sys.platform in ["darwin", "win32"]:
    from multiprocess import \
        Pipe, Pool, Process, \
        Queue, \
        Value, \
        cpu_count
    from multiprocess.managers import SyncManager
else:
    import multiprocessing as _mp
    from concurrent.futures import ProcessPoolExecutor as Pool

    # Python 3.14+ changed the default multiprocessing start method on Linux
    # from "fork" to "forkserver". The "forkserver" method requires all
    # objects passed to child processes to be picklable, which fails for
    # objects containing SQLAlchemy engines/sessions with unpicklable
    # closures. Explicitly use the "fork" context to maintain compatibility.
    _ctx = _mp.get_context("fork")
    Pipe = _ctx.Pipe
    Process = _ctx.Process
    Queue = _ctx.Queue
    Value = _ctx.Value
    cpu_count = _mp.cpu_count
    from multiprocessing.managers import SyncManager
