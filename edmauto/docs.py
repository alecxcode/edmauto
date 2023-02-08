import requests
from .accs import print_failure


class Document:
    def __init__(self, data):
        self.ID = data.get('ID')
        self.RegNo = str(data.get('RegNo') or '')
        self.RegDate = str(data.get('RegDate') or '')
        self.IncNo = str(data.get('IncNo') or '')
        self.IncDate = str(data.get('IncDate') or '')
        self.Category = int(data.get('Category') or 0)
        self.DocType = int(data.get('DocType') or 0)
        self.About = str(data.get('About') or '')
        self.Authors = str(data.get('Authors') or '')
        self.Addressee = str(data.get('Addressee') or '')
        self.DocSum = int(data.get('DocSum') or 0)
        self.Currency = int(data.get('Currency') or 0)
        self.EndDate = str(data.get('EndDate') or '')
        self.Creator = int(data.get('Creator') or 0)
        self.Note = str(data.get('Note') or '')
        self.FileList = data.get('FileList') or []

    def formdata(self):
        return {
            "regNo": self.RegNo,
            "regDate": self.RegDate,
            # TODO: other fields except "fileList"
        }

    def find_on_page_by_regno(self, page_json):
        if page_json.get("Docs"):
            for document in page_json["Docs"]:
                if document["RegNo"] == self.RegNo:
                    self.ID = document["ID"]
                    return True, self.ID
        return False, 0

    def create(self, url, cdict):
        formdata = self.formdata()
        formdata["createButton"] = "Create"
        formdata["api"] = "json"
        uploads = []
        for fname in self.FileList:
            uploads.append(('fileList', (fname, open(fname, 'rb'))))
        r = requests.post(url+'/docs/document/new',
                          cookies=cdict, data=formdata, files=uploads)
        if r.status_code >= 400:
            return r.status_code
        r = requests.get(
            url+f'/docs/?searchText={self.RegNo}&searchButton=Search&api=json', cookies=cdict)
        if r.status_code >= 400:
            return r.status_code
        res = r.json()
        found, ID = self.find_on_page_by_regno(res)
        if found:
            return ID
        print_failure(res, "Document not created.")
        return 0

    def update():
        pass

    def delete():
        pass

    def add_approver():
        pass

    def remove_approver():
        pass

    def save_approval_note():
        pass

    def approve():
        pass

    def reject():
        pass

    def view_approval_list():
        pass
