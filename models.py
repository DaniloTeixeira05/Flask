from flask_sqlalchemy import SQLAlchemy

# Instancia o SQLAlchemy
db = SQLAlchemy()

# Define o modelo Livro
class Livro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    autor = db.Column(db.String(100), nullable=False)
    ano = db.Column(db.Integer)
