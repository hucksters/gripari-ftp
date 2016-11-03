#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import ThreadedFTPServer


def main():
    # create simple FTP servers
    # see how here http://pythonhosted.org/pyftpdlib/tutorial.html
    authorizer = DummyAuthorizer()

    authorizer.add_user("user", "12345", '.', perm="elradfmwM")

    handler = FTPHandler
    handler.authorizer = authorizer

    handler.banner = "pyftpdlib based ftpd ready."

    address = ('', 2121)
    server = ThreadedFTPServer(address, handler)

    server.max_cons = 256
    server.max_cons_per_ip = 5

    server.serve_forever()


if __name__ == "__main__":
    main()
