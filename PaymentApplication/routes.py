from PaymentApplication.models import User, Transaction,DebitCardInfo
from flask import render_template, url_for, flash, redirect, request
from PaymentApplication.forms import RegistrationForm, LoginForm, PaymentForm,NetBankingForm,UpiForm,CardForm
from PaymentApplication import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required

@app.route("/about")
@login_required
def about():
    return render_template('about.html', title="About")


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('payment'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, rollnumber=form.rollnumber.data,
                    branch=form.branch.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash('Your Account has been created! You are now able to login', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)



@app.route("/home")
@login_required
def home():
    return render_template('home.html')

@app.route("/",methods=['GET', 'POST'])
@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)            
            return  redirect(url_for('home'))
        else:
            flash('Login Unsuccessful! Please check your Email and Password', 'danger')
    return render_template('login.html', title='login', form=form)


@app.route("/paytype/<int:user_id>/<string:typee>/<int:amount>",methods=['POST', 'GET'])
@login_required
def paytype(user_id, typee, amount):
    if request.method=='POST':
        option=request.form['flexRadioDefault']
        if option == 'Card':
            return redirect(url_for('card', user_id=user_id, typee=typee, amount=amount))
        elif option == 'Cod':
            return redirect(url_for('reports'))
        elif option == 'Upi':
            return redirect(url_for('upi', user_id=user_id, typee=typee, amount=amount))
        else:
            return redirect(url_for('netbanking', user_id=user_id, typee=typee, amount=amount))
        

    return render_template('Payment/paytype.html')

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/payment', methods=['POST', 'GET'])
@login_required
def payment():
    form = PaymentForm()
    if form.cancel.data:
        return redirect(url_for('home'))
    if form.submit.data:
        typee = form.myField.data
        user = current_user
        return redirect(url_for('paytype',typee=typee,user_id=user.id,amount=form.amount.data))
    return render_template('Payment/payment.html', form=form)


@app.route('/reports', methods=['GET'])
@login_required
def reports():
    page=request.args.get('page', 1, type=int)
    t = Transaction.query.order_by(Transaction.date.desc()).filter_by(user_id=current_user.id).paginate(page=page,per_page=7)
    return render_template('report.html', t=t)


@app.route('/card/<int:user_id>/<string:typee>/<int:amount>', methods=['POST', 'GET'])
@login_required
def card(user_id, typee, amount):
    form = CardForm()
    cards=DebitCardInfo.query.filter_by(user_id=current_user.id).limit(1).all()
    if form.cvv.data:
        t = Transaction(user_id=user_id, type=typee, amount=amount)
        db.session.add(t)
        d=DebitCardInfo(user_id=user_id,cardholderName=form.name.data,cardNumber=str(form.number.data),expiryDate=form.expiry.data,cvv=form.cvv.data)
        db.session.add(d)
        db.session.commit()
        flash('Your Payment is Successful!', 'success')
        return redirect(url_for('home'))
    return render_template('Payment/debitcard.html', form=form,cards=cards)


@app.route('/netbanking/<int:user_id>/<string:typee>/<int:amount>', methods=['POST', 'GET'])
@login_required
def netbanking(user_id, typee, amount):
    form=NetBankingForm()
    if form.bank.data:
        t = Transaction(user_id=user_id, type=typee, amount=amount)
        db.session.add(t)
        db.session.commit()
        flash('Your Payment is Successful!', 'success')
        return redirect(url_for('home'))
    return render_template('Payment/netbanking.html',form=form)


@app.route('/upi/<int:user_id>/<string:typee>/<int:amount>', methods=['POST', 'GET'])
@login_required
def upi(user_id, typee, amount):
    form = UpiForm()
    if form.upiid.data:
        t = Transaction(user_id=user_id, type=typee, amount=amount)
        db.session.add(t)
        db.session.commit()
        flash('Your Payment is Successful!', 'success')
        return redirect(url_for('home'))
    return render_template('Payment/upi.html', form=form)
