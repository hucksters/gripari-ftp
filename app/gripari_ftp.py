#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse


def main():
    parser = argparse.ArgumentParser(prog="Gripari-FTP",
                                     description="Download from ftp server")

    # CLI arguments for connetcting to FTP
    parser.add_argument("--host",
                        type=str,
                        required=True,
                        dest="host",
                        help="FTP server hostname")
    parser.add_arguemnt("--port",
                        type=int,
                        required=False,
                        dest="port",
                        default=21,
                        help="FTP server port number")
    parser.add_argument(
        "--login",
        type=str,
        required=False,
        dest="login",
        default="",
        help="user login for connecting to FTP server. Aunonymus by default.")
    parser.add_argument(
        "--password",
        type=str,
        required=False,
        dest="pwd",
        default="",
        help="password for login in FTP server. Empty by default.")

    # CLI arguments for connecting to database
    parser.add_argument("--sqlitestring",
                        type=str,
                        required=False,
                        dest="sqlite",
                        help="Path to SQLite data base. :memory: by default.",
                        default=":memory:")

    args = parser.parse_args()


if __name__ == "__main__":
    main()
