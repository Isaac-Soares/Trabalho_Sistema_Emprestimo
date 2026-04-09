from src.emprestimos_app import create_app, db
from src.emprestimos_app.models import Categoria

app = create_app()

with app.app_context():
    db.create_all()
    print("Tabelas criadas com sucesso!")

    
    categoria = Categoria.query.filter_by(nome="Geral").first()

    if not categoria:
        categoria = Categoria(nome="Geral")
        db.session.add(categoria)
        db.session.commit()
        print("Categoria padrão criada!")

if __name__ == "__main__":
    app.run(debug=True)