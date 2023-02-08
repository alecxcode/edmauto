from .team import Profile
from .accs import get_conn_data_from_file


def test_login():
    conndata = get_conn_data_from_file()
    # Cookie dict
    cdict = {}
    user = Profile(
        {'Login': conndata['loginName'], 'Passwd': conndata['loginPasswd']})
    res = user.login(conndata['url'], cdict)
    assert type(res) == str
    assert '<div id="headmenu">' in res


def test_logout():
    conndata = get_conn_data_from_file()
    # Cookie dict
    cdict = {}
    user = Profile(
        {'Login': conndata['loginName'], 'Passwd': conndata['loginPasswd']})
    res = user.logout(conndata['url'], cdict)
    text_to_understand_not_logged_in = "Please, enter your login and password"
    assert type(res) == str
    assert text_to_understand_not_logged_in in res


def test_create_user():
    admin = Profile({})
    url, cdict = admin.load_default_and_login()
    user = Profile({
        "FirstName": "John",
        "OtherName": "A.",
        "Surname": "Anderson",
        "Contacts": {
            "TelOffice": "355",
            "TelMobile": "+123423423",
            "Email": "test@example.org",
            "OtherContacts": "some_messenger"
        },
        "BirthDate": "2000-01-01",
        "JobTitle": "System Testing User",
        "JobUnit": "0",
        "Boss": "1",
        "Login": "testuser",
        "Passwd": "123123",
        "CreateButton": "Create"
    })
    ID = user.create(url, cdict)
    assert ID != 0
    admin.logout(url, cdict, False)


def test_create_user_nonadmin_deny():
    conndata = get_conn_data_from_file()
    cdict = {'sessionid': ''}
    profile = Profile({'Login': "testuser", 'Passwd': "123123"})
    profile.login(conndata['url'], cdict)
    user = Profile({
        "FirstName": "Tester",
        "Contacts": {},
        "CreateButton": "Create"
    })
    err = user.create(conndata['url'], cdict)
    assert err == 403  # should be forbidden
    user.logout(conndata['url'], cdict)


def test_delete_user():
    admin = Profile({})
    url, cdict = admin.load_default_and_login()
    user = Profile({
        "FirstName": "John",
        "OtherName": "A.",
        "Surname": "Anderson",
        "Contacts": {},
    })
    deletedNum = user.delete_by_name(url, cdict)
    assert deletedNum == 1
    admin.logout(url, cdict)
