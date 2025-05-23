import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from models import db, Livro

load_dotenv()  # Carrega variáveis do .env

app = Flask(__name__)
CORS(app)

# Configuração do banco
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Criar as tabelas (executar uma vez)
@app.before_first_request
def create_tables():
    db.create_all()

# Rota para listar todos os livros
@app.route('/livros', methods=['GET'])
def listar_livros():
    livros = Livro.query.all()
    return jsonify([{'id': l.id, 'titulo': l.titulo, 'autor': l.autor} for l in livros])

# Rota para adicionar um livro
@app.route('/livros', methods=['POST'])
def adicionar_livro():
    data = request.get_json()
    novo = Livro(titulo=data['titulo'], autor=data['autor'], ano=data['ano'])
    db.session.add(novo)
    db.session.commit()
    return jsonify({'mensagem': 'Livro adicionado com sucesso'}), 201

# Rota para atualizar
@app.route('/livros/<int:id>', methods=['PUT'])
def atualizar_livro(id):
    data = request.get_json()
    idint= int(id)
    livro = Livro.query.get(idint)
    if not livro:
        return jsonify({'erro': 'Livro não encontrado'}), 404
    livro.titulo = data['titulo']
    livro.autor = data['autor']
    livro.ano = data.get('ano')
    db.session.commit()
    return jsonify({'mensagem': 'Livro atualizado com sucesso'})

# Rota para deletar
@app.route('/livros/<int:id>', methods=['DELETE'])
def deletar_livro(id):
    idint=int(id)
    livro = Livro.query.get(idint)
    if not livro:
        return jsonify({'erro': 'Livro não encontrado'}), 404
    db.session.delete(livro)
    db.session.commit()
    return jsonify({'mensagem': 'Livro deletado'})
