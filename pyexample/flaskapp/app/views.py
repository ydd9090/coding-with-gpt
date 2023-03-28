from . import app
from .forms import AccountForm
from .models import Account
from flask import render_template,redirect,url_for

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/account',methods=['GET','POST'])
def account():
    form = AccountForm()
    if form.validate_on_submit():
        account = Account(phone_num=form.phone_num.data,phone_code=form.phone_code.data,session_id=form.session_id.data)
        if account.session_id is None:
            account.set_session_id()  # 改为异步的方式来获取session_id
        account.save()
        return redirect(url_for('account'))
        
    return render_template('account.html',form=form)


@app.route('/account/edit/<int:id>')
def account_edit(id):
    pass

@app.route('/account/delete/<int:id>')
def account_delete(id):
    pass



