import requests
from .accs import print_failure, save_cookies, load_cookies, get_conn_data_from_file


class Profile:
    def __init__(self, data):
        self.ID = data.get('ID')
        self.FirstName = str(data.get('FirstName') or '')
        self.OtherName = str(data.get('OtherName') or '')
        self.Surname = str(data.get('Surname') or '')
        self.BirthDate = str(data.get('BirthDate') or '')
        self.JobTitle = str(data.get('JobTitle') or '')
        self.JobUnit = int(data.get('JobUnit') or 0)
        self.Boss = int(data.get('Boss') or 0)
        self.Contacts = data.get('Contacts')
        self.UserRole = int(data.get('UserRole') or 0)
        self.UserLock = int(data.get('UserLock') or 0)
        self.UserConfig = data.get('UserConfig')
        self.Login = str(data.get('Login') or '')
        self.Passwd = str(data.get('Passwd') or '')

    def login(self, url, cdict={}, save=False):
        authform = {
            "loginName": self.Login,
            "loginPasswd": self.Passwd,
            "loginButton": "Log+in"
        }
        if save:
            load_cookies(cdict)
        text_to_understand_not_logged_in = "Please, enter your login and password"
        r = requests.get(url, cookies=cdict)
        if r.status_code >= 400:
            return r.status_code
        if text_to_understand_not_logged_in in r.text:
            with requests.Session() as s:
                r = s.post(url+'/login', data=authform)
                cdict.clear()
                cdict.update(requests.utils.dict_from_cookiejar(s.cookies))
                if save:
                    save_cookies(cdict)
                if r.status_code >= 400:
                    return r.status_code
                return r.text
        else:
            return r.text

    def logout(self, url, cdict={}, save=False):
        if save:
            load_cookies(cdict)
        text_to_understand_not_logged_in = "Please, enter your login and password"
        r = requests.get(url+'/logout', cookies=cdict)
        if text_to_understand_not_logged_in in r.text:
            cdict.clear()
        if save:
            save_cookies(cdict)
        if r.status_code >= 400:
            return r.status_code
        return r.text

    def load_default_and_login(self, save=False):
        conndata = get_conn_data_from_file()
        cdict = {'sessionid': ''}
        self.Login = conndata['loginName']
        self.Passwd = conndata['loginPasswd']
        self.login(conndata['url'], cdict, save)
        return conndata['url'], cdict

    def formdata(self):
        return {
            "firstName": self.FirstName,
            "otherName": self.OtherName,
            "surname": self.Surname,
            "telOffice": self.Contacts.get('TelOffice'),
            "telMobile":  self.Contacts.get('TelMobile'),
            "email":  self.Contacts.get('Email'),
            "otherContacts": self.Contacts.get('OtherContacts'),
            "birthDate": self.BirthDate,
            "jobTitle": self.JobTitle,
            "jobUnit": self.JobUnit,
            "boss": self.Boss,
        }

    def find_on_page_by_name(self, page_json):
        if page_json.get("Team"):
            for profile in page_json.get("Team"):
                if profile["FirstName"] == self.FirstName and profile["Surname"] == self.Surname:
                    self.ID = profile["ID"]
                    return True, self.ID
        return False, 0

    def create(self, url, cdict):
        formdata = self.formdata()
        formdata["login"] = self.Login,
        formdata["passwd"] = self.Passwd
        formdata["notifyCreatedUser"] = "false"
        formdata["loginSameEmail"] = "false"
        formdata["createButton"] = "Create"
        formdata["api"] = "json"
        r = requests.post(url+'/team/profile/new',
                          cookies=cdict, data=formdata)
        if r.status_code >= 400:
            return r.status_code
        res = r.json()
        found, ID = self.find_on_page_by_name(res)
        if found:
            return ID
        print_failure(res, "User not created.")
        return 0

    def update(self):
        formdata = self.formdata()
        formdata["updateButton"] = "Save"
        formdata["api"] = "json"
        pass

    def delete_by_name(self, url, cdict):
        r = requests.get(
            url+f'/team/?searchText={self.FirstName}&searchButton=Search&api=json', cookies=cdict)
        if r.status_code >= 400:
            return r.status_code
        res = r.json()
        found, _ = self.find_on_page_by_name(res)
        if found:
            formdata = {'ids': self.ID, 'deleteButton': "Delete+selected"}
            r = requests.post(url+'/team/?searchText={self.FirstName}&searchButton=Search&api=json',
                              cookies=cdict, data=formdata)
            if r.status_code >= 400:
                return r.status_code
            res = r.json()
            found, _ = self.find_on_page_by_name(res)
            if found:
                print_failure(res, "User not deleted.")
                return 0
            return res.get('RemovedNum')
