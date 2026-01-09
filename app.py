from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('form.html')

@app.route('/generar', methods=['POST'])
def generar():
    datos = request.form
    return render_template('cv_template.html', datos=datos)

if __name__ == '__main__':
    app.run(debug=True)