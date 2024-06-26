#from Databases import DataBase, User
import pdb

from Database import DataBase, Usuario, create_engine_easily
from datetime import datetime
from analytics import *
import os
from flask import Flask,  render_template, request,  flash, redirect, session, url_for
from Validations import *
import string
import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import hashlib

app = Flask(__name__)
app.debug = True


@app.route('/')
def index():
    return render_template('start.html')

@app.route('/inscricao')
def inscricao():
    return render_template('inscricao.html')

@app.route('/status')
def status():
    return render_template('status.html')


@app.route('/valida_cep/<cep>', methods=['GET', 'POST'])
def valida_cep(cep):
    validacao = Validations.valida_cep(cep)
    if validacao:
        return 'True'
    else:
        return f'INSCRIÇÃO PERMITIDA SOMENTE PARA MORADORES DE VALINHOS!\n' \
               f'O CEP {cep} NÃO PERTENCE A CIDADE DE VALINHOS!'


@app.route('/valida_cpf/<cpf>', methods=['GET', 'POST'])
def valida_cpf(cpf):

    first_validation = Validations.cpf_validate(cpf)
    if first_validation:
        second_validation = Validations.check_cpf_db(cpf)
        if second_validation:
            return 'True'
        else:
            return 'ESTE CPF JÁ FOI USADO EM UMA INSCRIÇÃO!'
    else:
        return 'ESTE NÃO É UM NÚMERO VÁLIDO DE CPF!'

@app.route('/valida_email/<email>', methods=['GET'])
def valida_mail(email):
    validation = Validations.get_user(email)
    if validation:
        return 'True'
    else:
        return 'ESTE EMAIL JÁ EXISTE EM NOSSA BASE DE DADOS!'


@app.route('/submit', methods=['POST'])
def submit():
    cep = request.form['cep']
    cpf = request.form['cpf']
    name = request.form['nome']
    born = request.form['nascimento']
    address = request.form['endereco']
    phone = request.form['telefone']
    email = request.form['email']
    turma = int(request.form['turma_select'])

    # limpeza dos dados
    cep = cep.translate(str.maketrans('', '', string.punctuation))
    cpf = cpf.translate(str.maketrans('', '', string.punctuation))
    protocol = str(datetime.datetime.now())
    protocol = protocol.translate(str.maketrans('', '', string.punctuation))
    protocol = protocol.replace(' ', '')

    obj = DataBase()
    obj.create_connection()
    post = (cpf, name, born, cep, address, phone, email, protocol, turma)
    obj.insert_inscritos(post)

    if not Validations.check_cpf_db(cpf):
        flash(f"SUA INSCRIÇÃO FOI REALIZADA COM SUCESSO! ESTE É O SEU PROTOCOLO: {protocol}")
        return render_template('confirm.html')
    else:
        flash("POR ALGUM ERRO DESCONHECIDO, SUA INSCRIÇÃO NÃO FOI REALIZADA. POR FAVOR, TENTE NOVAMENTE DENTRO DE ALGUNS INSTANTES.")
        return render_template('confirm.html')

@app.route('/stats/<id_turma>', methods=['GET'])
def inscritos_por_turma(id_turma):

    inscritos = organize_inscritos()

    if id_turma != 'ALL':
        id_turma = int(id_turma)
        filtro_inscritos = inscritos.loc[inscritos['ID_TURMA'] == id_turma]
        filtro_inscritos = filtro_inscritos.reset_index(drop='True')
    else:
        filtro_inscritos = inscritos.copy()

    filtro_inscritos = filtro_inscritos.drop(columns=['ID_TURMA'])
    return filtro_inscritos.to_html(classes='data')

@app.route('/estatisticas')
def estatisticas():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        inscritos = organize_inscritos()
        return render_template('stats.html', tables=[inscritos.to_html(classes='data')], titles=inscritos.columns)

@app.route('/status/<cpf>', methods=['GET'])
def get_inscricao(cpf):

    cpf_user = cpf.translate(str.maketrans('', '', string.punctuation))
    validation = Validations.cpf_validate(cpf_user)
    if validation:
        inscrito = get_inscrito_by_cpf(cpf_user)
        if type(inscrito) == str:
            return inscrito
        else:
            return inscrito.to_html(classes='data')
    else:
        return 'Este não é um CPF válido!'


@app.route('/admin')
def admin():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('admin.html')

@app.route('/login', methods=['POST'])
def do_admin_login():

    engine = create_engine_easily()

    POST_USERNAME = str(request.form['email'])
    POST_PASSWORD = str(request.form['password'])

    hash_object = hashlib.sha256(POST_PASSWORD.encode())
    hex_pass = hash_object.hexdigest()

    Session = sessionmaker(bind=engine)

    with Session() as session_db:
        usuario = session_db.query(Usuario).filter(Usuario.email == POST_USERNAME, Usuario.password == hex_pass)

    if usuario:
        session['logged_in'] = True
        return redirect(url_for('admin'))
    else:
        flash('Senha Incorreta!')
        return redirect(url_for('login'))
    #return admin()

@app.route('/signup')
def signup():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def signup_post():
    mail = request.form.get('email')
    nome = request.form.get('name')
    password = request.form.get('password')

    hash_object = hashlib.sha256(password.encode())
    hex_pass = hash_object.hexdigest()

    obj = DataBase()
    obj.create_connection()
    obj.insert_users((nome, mail, hex_pass))

    validation = Validations.get_user(mail)
    if not validation:
        flash('CADASTRO REALIZADO COM SUCESSO!')
        return redirect(url_for('signup'))


@app.route("/logout")
def logout():
    session['logged_in'] = False
    return admin()

@app.route('/sorteio')
def sorteio():

    if not session.get('logged_in'):
        return render_template('login.html')
    else:

        today = datetime.datetime.today().date()
        data_sorteio = datetime.datetime(2024, 3, 14).date()

        if today < data_sorteio:
            data_br = data_sorteio.strftime('%d/%m/%Y')
            flash(f'AINDA NÃO CHEGOU A DATA DO SORTEIO. \nVOLTE AQUI DEPOIS DE {data_br}')
            return render_template('sorteio.html')
        else:
            sorteados = create_sorteio()
            return render_template('sorteio.html', tables=[sorteados.to_html(classes='data')], titles=sorteados.columns)

if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True)  # Executa a aplicação

