#!/usr/bin/env python
# This file is part of Xpra.
# Copyright (C) 2011-2014 Antoine Martin <antoine@xpra.org>
# Xpra is released under the terms of the GNU GPL v2, or, at your option, any
# later version. See the file COPYING for details.

import unittest

from xpra.platform import (
    init, clean, threaded_server_init,
    program_context,
    set_default_name,
    #set_name, set_prgname, set_application_name,
    get_prgname,
    get_application_name,
    get_username, 
    command_error, command_info,
    )
from xpra.make_thread import start_thread

class PlatformInfoTest(unittest.TestCase):

    def test_all(self):
        set_default_name("platform info test", "platform-info-test")
        init()
        t = start_thread(threaded_server_init, "server-init")
        t.join()
        with program_context():
            assert get_application_name()=="platform-info-test"
            assert get_prgname()=="platform info test"

        calls = []
        def ccall(*args):
            calls.append(args)
        from xpra.scripts import main as xpra_main
        xpra_main.error = ccall
        xpra_main.info = ccall
        command_error("error")
        command_info("info")
        assert len(calls)==2, "expected 2 messages but got: %s" % (calls,)
        assert get_username()
        clean()


def main():
    unittest.main()

if __name__ == '__main__':
    main()