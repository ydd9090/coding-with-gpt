from .extensions import db
from datetime import datetime
from app.internallib.clients.bytest_client import BytestClient
from app.internallib.clients.account_manage_client import AccountManageClient

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone_num = db.Column(db.String(11), unique=True, index=True)
    phone_code = db.Column(db.String(4))
    session_id = db.Column(db.String(256))
    create_at = db.Column(db.DateTime, default=datetime.now)
    modify_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    uid = db.Column(db.String(36))
    userid_type = db.Column(db.Integer)

    def __init__(self,*args,**kwargs) -> None:
        super().__init__(*args,**kwargs)
        self._api_client = AccountManageClient()

    def set_session_id(self):
        raise NotImplementedError

    def save(self):
        db.session.add(self)
        db.session.commit()

    def get_uid(self):
        if not self.uid:
            resp = self.apiclient.get_uid(self.phone_num)
            self.uid = str(resp.json().get('data').get(self.phone_num))
        return self.uid

    def get_sec_uuid(self):
        raise NotImplementedError
    
    @property
    def apiclient(self):
        return self._api_client
    
class BytestTemplate(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    bytest_template_id = db.Column(db.Integer)
    name = db.Column(db.String(100))
    platform = db.Column(db.String(20))
    url= db.Column(db.String(200))
    biz = db.Column(db.Integer)
    creator = db.Column(db.String(100))
    create_at = db.Column(db.DateTime,default=datetime.utcnow)
    tasks = db.relationship("Task",back_populates="bytest_template")

    def __init__(self,*args,**kwargs) -> None:
        super().__init__(*args,**kwargs)
        self.bytest_client = BytestClient()

    @classmethod
    def init_bytest_template(cls):
        pass

    def make_url(self,):
        if self.biz is None or self.bytest_template_id is None:
            raise ValueError("biz or bytest_template_id should not be None")
        self.url = "https://bytest.bytedance.net/next/projects/{}/tests/{}/tasks".format(self.biz,self.bytest_template_id)
        return self.url

    def get_task_list(self):
        resp = self.bytest_client.task_list(self.bytest_template_id,self.biz)
        task_total_num = resp.json().get("total")
        task_data_list = resp.json().get("data")("contents")
        task_list = []
        for task_data in task_data_list:
            resp = self.bytest_client.get_task_detail(task_data["id"])
            task_detail_data = resp.json().get("data")
            task_list.append(Task(bytest_task_id=task_detail_data.get("id"),))

    

class Task(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    bytest_task_id = db.Column(db.Integer)      #urlize
    bytest_task_url = db.Column(db.String(200))
    cases_num = db.Column(db.Integer)
    failed_cases_num = db.Column(db.Integer)
    bytest_template_id = db.Column(db.Integer,db.ForeignKey("bytest_template.id"))
    bytest_template = db.relationship("BytestTemplate",back_populates="tasks")
    run_time = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime,default=datetime.utcnow)
    cases = db.relationship("Case",back_populates="task")
    is_failed = db.Column(db.Boolean,default=False)
    failed_cases_num = db.Column(db.Integer)



class Case(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    case_tags = db.Column(db.String(60))
    case_name = db.Column(db.String(100))
    case_class_name = db.Column(db.String(100))
    last_task_id = db.Column(db.Integer)
    task_id = db.Column(db.Integer,db.ForeignKey("task.id"))
    task = db.relationship("Task",back_populates="cases")
    requests = db.relationship("Request",back_populates="case")
    is_failed = db.Column(db.Boolean,default=False)

class Request(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    url_path = db.Column(db.String(200),index=True)
    logid = db.Column(db.String(128))
    http_code = db.Column(db.Integer)
    status_code = db.Column(db.Integer)
    request_data = db.Column(db.String)
    response_data = db.Column(db.String)
    case_id = db.Column(db.Integer,db.ForeignKey("case.id"))
    case = db.relationship("Case",back_populates="requests")
    

