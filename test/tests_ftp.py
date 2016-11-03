#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time
import pytest
import random
import string
import tempfile
from ftplib import FTP
import subprocess

import gripari_ftp.ftp as ftp


@pytest.fixture(scope="module")
def ftp_server(request):
    server = subprocess.Popen([sys.executable, os.path.join(
        os.path.split(os.path.abspath(__file__))[0], "local_ftp_server.py")])

    time.sleep(2)

    yield server
    server.terminate()


def test_last_modified_files(ftp_server):
    def upload_files_to_ftp(number=10):
        def name_generator():
            return ''.join(random.choice(string.ascii_lowercase)
                           for _ in range(10))

        with FTP() as local_ftp_client:
            local_ftp_client.connect(host="localhost", port=2121)
            local_ftp_client.login(user="user", passwd="12345")

            for _ in range(number):
                with tempfile.TemporaryFile() as fp:
                    fp.write(b"<testxml></testxml>")
                    fp.seek(0)
                    local_ftp_client.storlines(
                        "STOR {}.xml".format(name_generator()), fp)

    ftp_client = ftp.initialize("0.0.0.0", 2121, "user", "12345")

    number_of_uploaded_files = 1

    upload_files_to_ftp(number_of_uploaded_files)
    load_from_ftp = ftp.last_modified_files(ftp_client)
    assert load_from_ftp != []

    for filename in load_from_ftp:
        ftp.download(ftp_client, filename, lambda x: None)

    upload_files_to_ftp(number_of_uploaded_files)
    another_load_from_ftp = ftp.last_modified_files(ftp_client)

    assert another_load_from_ftp != []
    assert len(another_load_from_ftp) == number_of_uploaded_files
    assert set(another_load_from_ftp).intersection(set(load_from_ftp)) == set()

    ftp.finalize(ftp_client)
