
from flask import Flask,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///patients.db'
db=SQLAlchemy(app)

class Patient(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    full_name=db.Column(db.String(100))
    email=db.Column(db.String(100))
    dob=db.Column(db.String(20))
    glucose=db.Column(db.Float)
    haemoglobin=db.Column(db.Float)
    cholesterol=db.Column(db.Float)
    remarks=db.Column(db.String(500))

def predict(g,h,c):
    if g>140:
        return "AI Assessment: Elevated glucose levels indicate possible diabetes risk."
    elif c>240:
        return "AI Assessment: Cholesterol is high. Lifestyle changes recommended."
    elif h<12:
        return "AI Assessment: Haemoglobin is low. Possible anaemia risk."
    return "AI Assessment: Values are within healthy range."

@app.route('/')
def home():
    q=request.args.get('q','')
    patients=Patient.query.filter(Patient.full_name.contains(q)).all() if q else Patient.query.all()
    return render_template('index.html',patients=patients)

@app.route('/add',methods=['POST'])
def add():
    g=float(request.form['glucose'])
    h=float(request.form['haemoglobin'])
    c=float(request.form['cholesterol'])
    p=Patient(full_name=request.form['full_name'],email=request.form['email'],
              dob=request.form['dob'],glucose=g,haemoglobin=h,
              cholesterol=c,remarks=predict(g,h,c))
    db.session.add(p); db.session.commit()
    return redirect('/')

@app.route('/edit/<int:id>',methods=['GET','POST'])
def edit(id):
    p=Patient.query.get_or_404(id)
    if request.method=='POST':
        p.full_name=request.form['full_name']
        p.email=request.form['email']
        p.dob=request.form['dob']
        p.glucose=float(request.form['glucose'])
        p.haemoglobin=float(request.form['haemoglobin'])
        p.cholesterol=float(request.form['cholesterol'])
        p.remarks=predict(p.glucose,p.haemoglobin,p.cholesterol)
        db.session.commit()
        return redirect('/')
    return render_template('edit.html',p=p)

@app.route('/delete/<int:id>')
def delete(id):
    p=Patient.query.get_or_404(id)
    db.session.delete(p)
    db.session.commit()
    return redirect('/')

if __name__=='__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
