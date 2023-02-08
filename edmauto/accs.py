import os


def print_failure(res, desc):
    print(f'Fail Description: {desc} Result output:')
    if res.get("message"):
        print(res['message'])
    print(res)


def save_cookies(cdict):
    try:
        with open('cookie.txt', 'w') as f:
            for k in cdict:
                f.write(k + '=' + cdict[k] + '\n')
    except Exception as e:
        print("saveCookies: unable to save cookies file" + "\n" + str(e))


def load_cookies(cdict):
    cdict.clear()
    try:
        with open('cookie.txt', 'r') as f:
            for s in f:
                if s == "":
                    continue
                arr = s.rstrip().split('=', 1)
                cdict[arr[0]] = arr[1]
    except Exception as e:
        print("loadCookies: unable to open cookies file" + "\n" + str(e))


def get_conn_data_from_file():
    defaultConnFile = "url = http://127.0.0.1:8090\nloginName = admin\nloginPasswd = "
    if not os.path.exists('connect.txt'):
        with open('connect.txt', 'w') as f:
            f.write(defaultConnFile)
    conndata = {}
    with open('connect.txt', 'r') as f:
        for line in f:
            if line.startswith('#') or line == "":
                continue
            arr = line.split('=', 1)
            conndata[arr[0].strip()] = arr[1].strip()
    return conndata


def make_test_file(fname):
    fileData = fname + "\nTest file content.\nTest file data."
    if not os.path.exists(fname):
        with open(fname, 'w') as f:
            f.write(fileData)


def view_version():
    pass


def view_manual():
    pass


def object_nonexistent():
    pass
