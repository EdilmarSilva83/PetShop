from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'chave_secreta_para_flask'
app.secret_key = 'sua_chave_secreta'
app.static_folder = 'static'  # Define a pasta 'static' como a pasta para arquivos estáticos


def conectar_banco():
    try:
        conn = mysql.connector.connect(
            host='localhost',  
            user='root',  
            password='admin123',  
            database='petshop' 
        )
        print("Conexão com o banco de dados bem-sucedida!")
        return conn
    except mysql.connector.Error as err:
        print(f"Erro ao conectar ao banco de dados: {err}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    if 'usuario_tipo' not in session or session['usuario_tipo'] != 'admin':
        flash("Acesso restrito para administradores!", "error")
        return redirect(url_for('login'))  # Redireciona para a página de login, caso não seja admin

    # Consultar dados do banco
    conn = conectar_banco()
    if conn is None:
        flash("Erro ao conectar ao banco de dados", "error")
        return redirect(url_for('index'))

    cursor = conn.cursor(dictionary=True)
    
    try:
        # Consultar produtos
        cursor.execute("SELECT * FROM produtos")
        produtos = cursor.fetchall()

        # Consultar vendas (últimas 5 vendas ou por data)
        cursor.execute("SELECT * FROM vendas ORDER BY data_venda DESC LIMIT 5")
        vendas = cursor.fetchall()

        # Consultar agendamentos (últimos 5)
        cursor.execute("SELECT * FROM agendamentos ORDER BY data_hora_agendamento DESC LIMIT 5")
        agendamentos = cursor.fetchall()

        return render_template('dashboard.html', produtos=produtos, vendas=vendas, agendamentos=agendamentos)

    except Exception as e:
        flash(f"Erro ao carregar os dados do dashboard: {str(e)}", "error")
        return redirect(url_for('index'))

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['name']
        email = request.form['email']
        contato = request.form['contact']
        senha = request.form['password']
        confirmar_senha = request.form['confirm_password']
        tipo = 'cliente'  #Defina o tipo como 'cliente' por padrão, ou pode ser ajustado conforme a necessidade

        # Verificando se as senhas coincidem
        if senha != confirmar_senha:
            flash("As senhas não coincidem!", "error")
            return redirect(url_for('cadastro'))
        
        senha_hash = generate_password_hash(senha)

        conn = None
        cursor = None

        try:
            conn = conectar_banco()
            cursor = conn.cursor()

            # Verifique se 'tipo' está correto
            print(f"Inserindo valores: {nome}, {email}, {contato}, {senha_hash}, {tipo}")

            # Defina os valores diretamente como parâmetros
            sql = "INSERT INTO usuarios (nome, email, senha, tipo, contato) VALUES (%s, %s, %s, %s, %s)"
            valores = (nome, email, senha_hash, tipo, contato)
            cursor.execute(sql, valores)
            conn.commit()

            # Adicione um print para confirmar que a inserção foi realizada
            print(f"Usuário {nome} inserido com sucesso!")

            flash("Cadastro realizado com sucesso!", "success")
            return redirect(url_for('index'))

        except Exception as e:
            flash(f"Erro ao realizar o cadastro: {str(e)}", "error")
            return redirect(url_for('cadastro'))

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    return render_template('cadastro.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        conn = None
        cursor = None

        try:
            conn = conectar_banco()
            if conn is None:
                flash("Erro ao conectar ao banco de dados", "error")
                return redirect(url_for('login'))

            cursor = conn.cursor(dictionary=True)

            sql = "SELECT * FROM usuarios WHERE email = %s"
            cursor.execute(sql, (email,))
            usuario = cursor.fetchone()

            if usuario and check_password_hash(usuario['senha'], password):
                session['usuario_id'] = usuario['id'] 
                session['usuario_nome'] = usuario['nome']
                session['usuario_tipo'] = usuario['tipo'] # Adiciona o tipo do usuário

                flash("Login realizado com sucesso!", "success")

                # Verificar se o usuário é admin ou cliente
                if usuario['tipo'] == 'admin':
                    print("Redirecionando para a página de admin")
                    return redirect(url_for('dashboard'))  # Redireciona para a página de administração/dashboard
                else:
                    print("Redirecionando para a página do cliente")  # Confirma o redirecionamento para cliente
                    return redirect(url_for('cliente'))  # Redireciona para a página do cliente
                                
            else:
                flash("Email ou senha incorretos!", "error")
                return redirect(url_for('index'))

        except Exception as e:
            flash(f"Erro ao fazer login: {str(e)}", "error")
            return redirect(url_for('login'))

        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

    return render_template('index.html')

@app.route('/logout')
def logout():
    session.clear() # Limpa todos os dados da sessão
    #session.pop('usuario_id', None)  # Remove o ID do usuário da sessão
    #session.pop('usuario_nome', None)  # Remove o nome do usuário da sessão
    flash("Você foi desconectado com sucesso!", "success") # Mensagem so logout
    return redirect(url_for('index'))  # Redireciona para a página de login

@app.route('/gatos')
def gatos():
    return render_template('gatos.html')

@app.route('/cachorro')
def cachorro():
    return render_template('cachorro.html')

@app.route('/cliente')
def cliente():
    return render_template('cliente.html')

# Página de agendamento de banho
@app.route('/agendamento', methods=['GET'])
def agendamento():
    return render_template('agendamento.html')  # Página de agendamento com o formulário

# Rota para processar o agendamento
@app.route('/agendar_banho', methods=['POST'])
def agendar_banho():
    # Pega os dados do formulário
    data = request.form['data']
    hora = request.form['hora']
    pet_nome = request.form['pet_nome']
    usuario_id = session.get('usuario_id')  # Supondo que o ID do usuário esteja na sessão
    
    # Junta data e hora
    data_hora_agendamento = f"{data} {hora}"
    data_hora_agendamento = datetime.strptime(data_hora_agendamento, "%Y-%m-%d %H:%M")

    try:
        # Conecta ao banco de dados
        conn = conectar_banco()
        if conn is None:
            flash("Erro ao conectar ao banco de dados", "error")
            return redirect(url_for('agendamento'))
        
        cursor = conn.cursor()

        # Insere o agendamento no banco de dados
        sql = """
            INSERT INTO agendamentos (usuario_id, pet_nome, data_hora_agendamento)
            VALUES (%s, %s, %s)
        """
        cursor.execute(sql, (usuario_id, pet_nome, data_hora_agendamento))
        conn.commit()

        flash("Agendamento realizado com sucesso!", "success")
        return redirect(url_for('cliente'))  # Redireciona para a página do cliente

    except Exception as e:
        flash(f"Erro ao agendar: {str(e)}", "error")
        return redirect(url_for('agendamento'))

    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()

# Rota para Exibir Detalhes do Produto
@app.route('/detalhes_produto/<int:produto_id>')
def detalhes_produto(produto_id):
    conn = conectar_banco()
    if conn is None:
        flash("Erro ao conectar ao banco de dados", "error")
        return redirect(url_for('index'))

    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM produtos WHERE id = %s", (produto_id,))
        produto = cursor.fetchone()

        if not produto:
            return "Produto não encontrado", 404

        return render_template('detalhes_produto.html', produto=produto)
    except Exception as e:
        flash(f"Erro ao buscar produto: {str(e)}", "error")
        return redirect(url_for('index'))
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# Rota para processar a compra
@app.route('/finalizar_compra/<int:produto_id>', methods=['POST'])
def finalizar_compra(produto_id):
    quantidade = request.form['quantidade']
    forma_pagamento = request.form['forma_pagamento']

    # Validação da quantidade
    if not quantidade.isdigit() or int(quantidade) <= 0:
        flash("Quantidade inválida!", "error")
        return redirect(url_for('detalhes_produto', produto_id=produto_id))

    # Conectando ao banco para buscar o produto
    conn = conectar_banco()
    if conn is None:
        flash("Erro ao conectar ao banco de dados", "error")
        return redirect(url_for('index'))

    cursor = conn.cursor(dictionary=True)
    try:
        # Consultar produto
        cursor.execute("SELECT * FROM produtos WHERE id = %s", (produto_id,))
        produto = cursor.fetchone()

        if not produto:
            flash("Produto não encontrado!", "error")
            return redirect(url_for('index'))

        # Calcular o valor total da compra
        valor_total = produto['preco'] * int(quantidade)

        # Recuperar o ID do usuário da sessão
        usuario_id = session.get('usuario_id')

        # Se o pagamento for via cartão de crédito, obter os dados do cartão
        if forma_pagamento == "Cartão de Crédito":
            numero_cartao = request.form['numero_cartao']
            nome_cartao = request.form['nome_cartao']
            validade_cartao = request.form['validade_cartao']
            cvv_cartao = request.form['cvv_cartao']

            # Aqui você integraria com uma API de pagamento real (Stripe, PagSeguro, etc)
            # Por enquanto, vamos apenas simular uma aprovação de pagamento
            aprovado = True  # Simulação

            if not aprovado:
                flash("Pagamento não aprovado", "error")
                return redirect(url_for('detalhes_produto', produto_id=produto_id))

        # Criando a venda no banco de dados
        sql = """
            INSERT INTO vendas (usuario_id, produto_id, quantidade, valor_total, forma_pagamento)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (usuario_id, produto_id, quantidade, valor_total, forma_pagamento))
        conn.commit()

        flash("Compra realizada com sucesso!", "success")
        return render_template('confirmacao_compra.html', produto=produto, quantidade=quantidade, valor_total=valor_total, forma_pagamento=forma_pagamento)

    except Exception as e:
        flash(f"Erro ao processar a compra: {str(e)}", "error")
        return redirect(url_for('detalhes_produto', produto_id=produto_id))

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == '__main__':
    app.run(debug=True)

# Link do projeto GitHub: https://github.com/users/EdilmarSilva83/projects/2

# app.run(debug=True)
# Precisa criar um ambiente virtual no linux
# python3 -m venv petshop
# source petshop/bin/activate
# pip install flask werkzeug datetime
# python3 app.py