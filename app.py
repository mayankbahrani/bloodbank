from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bloodbank.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Donor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    blood_group = db.Column(db.String(5))
    contact = db.Column(db.String(20))

class EmergencyRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    blood_group_needed = db.Column(db.String(5))
    patient_name = db.Column(db.String(100))
    contact = db.Column(db.String(20))

class Receiver(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    blood_group = db.Column(db.String(5))
    contact = db.Column(db.String(20))


@app.cli.command("init-db")
def init_db():
    db.create_all()
    print("Database Initialized")

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/donors')
def donors():
    all_donors = Donor.query.all()
    return render_template('donors.html', donors=all_donors)

@app.route('/add-donor', methods=['GET', 'POST'])
def add_donor():
    if request.method == 'POST':
        name = request.form['name']
        blood_group = request.form['blood_group']
        contact = request.form['contact']
        new_donor = Donor(name=name, blood_group=blood_group, contact=contact)
        db.session.add(new_donor)
        db.session.commit()
        return redirect('/')
    return render_template('add_donor.html')


@app.route('/emergency', methods=['GET', 'POST'])
def emergency():
    if request.method == 'POST':
        blood_group_needed = request.form['blood_group']
        patient_name = request.form['patient_name']
        contact = request.form['contact']
        req = EmergencyRequest(blood_group_needed=blood_group_needed,
                               patient_name=patient_name, contact=contact)
        db.session.add(req)
        db.session.commit()
        return redirect('/')
    requests = EmergencyRequest.query.all()
    return render_template('emergency.html', requests=requests)

@app.route('/edit-emergency/<int:id>', methods=['GET', 'POST'])
def edit_emergency(id):
    req = EmergencyRequest.query.get_or_404(id)
    if request.method == 'POST':
        req.patient_name = request.form['patient_name']
        req.blood_group_needed = request.form['blood_group']
        req.contact = request.form['contact']
        db.session.commit()
        return redirect('/')
    return render_template('edit_emergency.html', req=req)

@app.route('/delete-emergency/<int:id>')
def delete_emergency(id):
    req = EmergencyRequest.query.get_or_404(id)
    db.session.delete(req)
    db.session.commit()
    return redirect('/')


@app.route('/receivers', methods=['GET', 'POST'])
def receivers():
    if request.method == 'POST':
        name = request.form['name']
        blood_group = request.form['blood_group']
        contact = request.form['contact']
        new_receiver = Receiver(name=name, blood_group=blood_group, contact=contact)
        db.session.add(new_receiver)
        db.session.commit()
        return redirect('/')
    all_receivers = Receiver.query.all()
    return render_template('receivers.html', receivers=all_receivers)

@app.route('/edit-receiver/<int:id>', methods=['GET', 'POST'])
def edit_receiver(id):
    receiver = Receiver.query.get_or_404(id)
    if request.method == 'POST':
        receiver.name = request.form['name']
        receiver.blood_group = request.form['blood_group']
        receiver.contact = request.form['contact']
        db.session.commit()
        return redirect('/')
    return render_template('edit_receiver.html', receiver=receiver)

@app.route('/delete-receiver/<int:id>', methods=['GET'])
def delete_receiver(id):
    receiver = Receiver.query.get_or_404(id)
    db.session.delete(receiver)
    db.session.commit()
    return redirect('/')


with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True)
