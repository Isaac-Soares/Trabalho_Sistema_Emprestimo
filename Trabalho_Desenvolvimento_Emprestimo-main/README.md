# 📚 Sistema de Empréstimos

## 📌 Descrição do Sistema

Este projeto é um sistema web de gerenciamento de empréstimos desenvolvido utilizando Flask.

O sistema permite:
- Cadastro de usuários
- Cadastro de itens (como livros ou objetos)
- Organização dos itens por categorias
- Controle de empréstimos e devoluções

O objetivo é facilitar o controle de quem pegou determinado item e se ele já foi devolvido.

---

## 🗄️ Estrutura do Banco de Dados

O sistema utiliza um banco de dados relacional com as seguintes tabelas:

### 👤 Usuários
Armazena as informações dos usuários do sistema.

- id (chave primária)
- nome
- email (único)

---

### 🏷️ Categorias
Responsável por organizar os itens.

- id (chave primária)
- nome

---

### 📦 Itens
Representa os objetos que podem ser emprestados.

- id (chave primária)
- nome
- descricao
- disponivel (booleano)
- categoria_id (chave estrangeira, opcional)

---

### 🔁 Empréstimos
Registra os empréstimos realizados no sistema.

- id (chave primária)
- data_emprestimo
- data_devolucao
- usuario_id (chave estrangeira)
- item_id (chave estrangeira)

---

## 🔗 Relacionamentos

- Um usuário pode ter vários empréstimos
- Um item pode estar em vários empréstimos
- Uma categoria pode ter vários itens
- Um empréstimo pertence a um usuário e a um item

---

## 🌐 Rotas do Sistema

As rotas estão organizadas utilizando Blueprints.

### 👤 Usuários
- `/usuarios` → lista todos os usuários
- `/usuarios/criar` → cria um novo usuário

---

### 📦 Itens
- `/itens` → lista todos os itens
- `/itens/criar` → cria um novo item

---

### 🏷️ Categorias
- `/categorias` → lista todas as categorias
- `/categorias/criar` → cria uma nova categoria

---

### 🔁 Operações (Empréstimos)
- `/emprestimos` → lista todos os empréstimos
- `/emprestimos/criar` → realiza um empréstimo
- `/emprestimos/devolver` → registra a devolução

---

## ⚙️ Regras de Negócio

O sistema segue as seguintes regras:

- Um item só pode ser emprestado se estiver disponível
- Ao realizar um empréstimo, o item fica indisponível
- Ao devolver, o item volta a ficar disponível
- Um item pode não ter categoria (campo opcional)
- Existe uma categoria padrão chamada **"Geral"**, criada automaticamente se não existir
- O email do usuário deve ser único

---

## ▶️ Como Executar o Projeto

### 1. Clonar o repositório
```bash
git clone <link-do-repositorio>
cd <nome-da-pasta>