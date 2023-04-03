from flask import Blueprint,render_template,flash,url_for,redirect
from app.internallib.clients.bytest_client import BytestClient
from app.forms import BytestTemplateForm
from app.models import BytestTemplate
from app.extensions import db
from app.models import Task



bytest_bp = Blueprint("bytest",__name__)


@bytest_bp.route("/index",methods=["GET","POST"])
def index():

    form = BytestTemplateForm()
    if form.validate_on_submit():
        template_id = form.bytest_template_id.data
        bytest_client = BytestClient()
        resp = bytest_client.template(template_id)
        if resp.json().get("code") != 0:
            flash("获取模板信息失败:{}".format(resp.json().get("msg")))
            return redirect(url_for("bytest.index"))
        bytest_template = BytestTemplate()
        dict_data = resp.json().get("data")
        bytest_template.bytest_template_id = dict_data.get("id")
        bytest_template.name = dict_data.get("name")
        bytest_template.biz = dict_data.get("biz")
        bytest_template.creator = dict_data.get("creator")
        bytest_template.create_at = dict_data.get("create_at")
        bytest_template.platform = "Andorid" if dict_data.get("platform") == 1 else "iOS"
        bytest_template.make_url()
        db.session.add(bytest_template)
        db.session.commit()
        return redirect(url_for("bytest.index"))
    
    templates = BytestTemplate.query.all()        

    return render_template('bytest_template.html',templates=templates,form=form)

@bytest_bp.route("/bytest/<int:bytest_template_id>/view")
def view_bytest(bytest_template_id):
    bytest_template:BytestTemplate = BytestTemplate.query.filter_by(bytest_template_id=bytest_template_id).first()
    tasks = bytest_template.get_task_list()


    return render_template("task.html")

@bytest_bp.route("/task/<int:task_id>/view",)
def tasks():
    return render_template("task.html")