import os
import random
from datetime import date
from .team import Profile
from .docs import Document
from .accs import get_conn_data_from_file, make_test_file


def test_create_document():
    random.seed()
    admin = Profile({})
    url, cdict = admin.load_default_and_login()
    doc = Document({
        "RegNo": f'{random.randint(1000, 9999)}-{random.randint(10, 99)}',
        "RegDate": date.today(),
        # TODO: other fields
        "FileList": ["upload1.txt", "upload2.txt"]
    })
    for fname in doc.FileList:
        make_test_file(fname)
    ID = doc.create(url, cdict)
    for fname in doc.FileList:
        os.remove(fname)
    assert ID != 0
    admin.logout(url, cdict)

    
