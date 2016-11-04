#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ftplib
import time
from typing import NamedTuple, List, Text, Callable, Any

import gripari_ftp.db as db

Reader = NamedTuple("FTPReader", [("ftp", ftplib.FTP), ("db", db.Connection)])


def initialize(host: str="",
               port: int=21,
               user: str="anonymous",
               pwd: str="") -> Reader:
    """
    Initialize ftp client.
    """
    client = ftplib.FTP()
    client.connect(host=host, port=port)
    client.login(user=user, passwd=pwd)

    sdb = db.initialize("persistent.sqlite3")

    return Reader(client, sdb)


def finalize(client: Reader):
    """
    Close connection to FTP server
    """
    db.finalize(client.db)
    client.ftp.quit()


def last_modified_files(client: Reader) -> List[str]:
    """
    Return list of files which we didn't meet before on FTP.
    We call them last modified (created).
    """
    return db.nonexists(client.db,
                        [res[0]
                         for res in client.ftp.mlsd(facts=["type"])
                         if res[1]["type"] == "file"])


def download(client: Reader, candidate: Text, callback:
             Callable[[bytes], Any]):
    """
    Download from FTP server file with name candidate and call callback
    for every line from file
    """
    client.ftp.retrbinary("RETR {}".format(candidate), callback)

    with client.db:
        client.db.execute("INSERT INTO documents VALUES (?, ?)",
                          (int(time.time()), candidate))
