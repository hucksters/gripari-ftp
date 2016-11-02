#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import pytest
import string
import random
import gripari_ftp.db as db


@pytest.fixture(scope="module")
def sqlitedb(request):
    sdb = db.initialize(":memory:")

    yield sdb

    db.finalize(sdb)


def test_find_nonexists(sqlitedb):
    def name_generator():
        return ''.join(random.choice(string.ascii_lowercase)
                       for _ in range(10))

    documents = [(int(time.time()), "{}.xml".format(name_generator()))
                 for _ in range(100)]

    train_docs = documents[:90]
    with sqlitedb:
        sqlitedb.executemany("INSERT INTO documents VALUES (?, ?)", train_docs)
    test_docs = documents[80:]

    assert sorted(db.nonexists(sqlitedb, [x[1] for x in test_docs])) == sorted(
        [x[1] for x in documents[90:]])
