from .team import Profile
from .accs import get_conn_data_from_file


def bruteforce_nonblock(url, wrong_user, user):
    res = None
    cdict = {}
    for _ in range(10):
        res = wrong_user.login(url, cdict)
    res = user.login(url, cdict)
    user.logout(url, cdict)
    return res


def bruteforce_block(url, wrong_user):
    ALLOWED_LOGIN_ATTEMPTS = 100
    res = None
    cdict = {}
    for _ in range(ALLOWED_LOGIN_ATTEMPTS + 1):
        res = wrong_user.login(url, cdict)
    return res


def test_xbrutforce():
    # url, loginName, and loginPasswd from connect.txt
    conndata = get_conn_data_from_file()
    user = Profile(
        {'Login': conndata['loginName'], 'Passwd': conndata['loginPasswd']})
    wrong_user = Profile({'Login': 'wrong_login', 'Passwd': 'wrong_passwd'})

    res = bruteforce_nonblock(conndata['url'], wrong_user, user)
    assert type(res) == str
    assert '<div id="headmenu">' in res

    res = bruteforce_block(conndata['url'], wrong_user)
    assert type(res) == str
    assert 'System Bruteforce Attack Shield' in res
