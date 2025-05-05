from flask import Blueprint, request, jsonify
from extensions import db  # Importe db de extensions.py
from models import Transacao, Categoria
from sqlalchemy import func
from datetime import datetime, timedelta  # Importe timedelta
from collections import defaultdict

transacoes_bp = Blueprint('transacoes', __name__)
categorias_bp = Blueprint('categorias', __name__)
relatorios_bp = Blueprint('relatorios', __name__)  # Correção: "relatorios"

# --- Rotas para Transações ---

@transacoes_bp.route('', methods=['POST'])
def criar_transacao():
    data = request.get_json()
    if not data or 'descricao' not in data or 'valor' not in data or 'tipo' not in data or 'categoria_id' not in data:
        return jsonify({'message': 'Dados inválidos'}), 400

    categoria = Categoria.query.get(data['categoria_id'])
    if not categoria:
        return jsonify({'message': 'Categoria não encontrada'}), 404

    nova_transacao = Transacao(
        descricao=data['descricao'],
        valor=data['valor'],
        tipo=data['tipo'],
        categoria=categoria
    )
    db.session.add(nova_transacao)
    db.session.commit()
    return jsonify({'message': 'Transação criada com sucesso!', 'id': nova_transacao.id}), 201

@transacoes_bp.route('', methods=['GET'])
def listar_transacoes():
    transacoes = Transacao.query.all()
    output = []
    for transacao in transacoes:
        transacao_data = {
            'id': transacao.id,
            'descricao': transacao.descricao,
            'valor': transacao.valor,
            'data': transacao.data.isoformat(),
            'tipo': transacao.tipo,
            'categoria_id': transacao.categoria_id,
            'categoria': transacao.categoria.nome
        }
        output.append(transacao_data)
    return jsonify(output)

@transacoes_bp.route('/<int:id>', methods=['GET'])
def obter_transacao(id):
    transacao = Transacao.query.get_or_404(id)
    transacao_data = {
        'id': transacao.id,
        'descricao': transacao.descricao,
        'valor': transacao.valor,
        'data': transacao.data.isoformat(),
        'tipo': transacao.tipo,
        'categoria_id': transacao.categoria_id,
        'categoria': transacao.categoria.nome
    }
    return jsonify(transacao_data)

@transacoes_bp.route('/<int:id>', methods=['PUT'])
def atualizar_transacao(id):
    transacao = Transacao.query.get_or_404(id)
    data = request.get_json()
    if not data:
        return jsonify({'message': 'Dados inválidos'}), 400

    if 'descricao' in data:
        transacao.descricao = data['descricao']
    if 'valor' in data:
        transacao.valor = data['valor']
    if 'tipo' in data:
        transacao.tipo = data['tipo']
    if 'categoria_id' in data:
        categoria = Categoria.query.get(data['categoria_id'])
        if not categoria:
            return jsonify({'message': 'Categoria não encontrada'}), 404
        transacao.categoria = categoria

    db.session.commit()
    return jsonify({'message': 'Transação atualizada com sucesso!'})

@transacoes_bp.route('/<int:id>', methods=['DELETE'])
def deletar_transacao(id):
    transacao = Transacao.query.get_or_404(id)
    db.session.delete(transacao)
    db.session.commit()
    return jsonify({'message': 'Transação excluída com sucesso!'})

# --- Rotas para Categorias ---

@categorias_bp.route('', methods=['POST'])
def criar_categoria():
    data = request.get_json()
    if not data or 'nome' not in data:
        return jsonify({'message': 'Dados inválidos'}), 400

    if Categoria.query.filter_by(nome=data['nome']).first():
        return jsonify({'message': 'Categoria já existe'}), 409

    nova_categoria = Categoria(nome=data['nome'])
    db.session.add(nova_categoria)
    db.session.commit()
    return jsonify({'message': 'Categoria criada com sucesso!', 'id': nova_categoria.id}), 201

@categorias_bp.route('', methods=['GET'])
def listar_categorias():
    categorias = Categoria.query.all()
    output = []
    for categoria in categorias:
        categoria_data = {'id': categoria.id, 'nome': categoria.nome}
        output.append(categoria_data)
    return jsonify(output)

@categorias_bp.route('/<int:id>', methods=['GET'])
def obter_categoria(id):
    categoria = Categoria.query.get_or_404(id)
    categoria_data = {'id': categoria.id, 'nome': categoria.nome}
    return jsonify(categoria_data)

@categorias_bp.route('/<int:id>', methods=['PUT'])
def atualizar_categoria(id):
    categoria = Categoria.query.get_or_404(id)
    data = request.get_json()
    if not data or 'nome' not in data:
        return jsonify({'message': 'Dados inválidos'}), 400

    if Categoria.query.filter(Categoria.nome == data['nome'], Categoria.id != id).first():
        return jsonify({'message': 'Categoria com este nome já existe'}), 409

    categoria.nome = data['nome']
    db.session.commit()
    return jsonify({'message': 'Categoria atualizada com sucesso!'})

@categorias_bp.route('/<int:id>', methods=['DELETE'])
def deletar_categoria(id):
    categoria = Categoria.query.get_or_404(id)
    db.session.delete(categoria)
    db.session.commit()
    return jsonify({'message': 'Categoria excluída com sucesso!'})

# --- Rotas para Relatórios ---

@relatorios_bp.route('/gastos_por_categoria', methods=['GET'])
def gastos_por_categoria():
    ano = request.args.get('ano')
    mes = request.args.get('mes')

    if not ano or not mes:
        hoje = datetime.now()
        ano = hoje.year
        mes = hoje.month
    else:
        try:
            ano = int(ano)
            mes = int(mes)
            if not (1 <= mes <= 12):
                return jsonify({'message': 'Mês inválido'}), 400
        except ValueError:
            return jsonify({'message': 'Ano e mês devem ser números'}), 400

    gastos = db.session.query(Categoria.nome, func.sum(Transacao.valor)).\
        join(Transacao).\
        filter(Transacao.tipo == 'despesa').\
        filter(func.strftime('%Y', Transacao.data) == str(ano)).\
        filter(func.strftime('%m', Transacao.data) == f'{mes:02d}').\
        group_by(Categoria.nome).\
        all()

    resultado = []
    for categoria, total in gastos:
        resultado.append({'categoria': categoria, 'total_gasto': float(total)})

    return jsonify(resultado)

@relatorios_bp.route('/comparar_gastos_mensais', methods=['GET'])
def comparar_gastos_mensais():
    num_meses = request.args.get('num_meses', default=3, type=int)
    hoje = datetime.now()
    resultados = []

    for i in range(num_meses):
        ano = hoje.year
        mes = hoje.month - i
        if mes <= 0:
            ano -= 1
            mes += 12

        total_gastos = db.session.query(func.sum(Transacao.valor)).\
            filter(Transacao.tipo == 'despesa').\
            filter(func.strftime('%Y', Transacao.data) == str(ano)).\
            filter(func.strftime('%m', Transacao.data) == f'{mes:02d}').\
            scalar()

        resultados.append({
            'ano': ano,
            'mes': mes,
            'total_gasto': float(total_gastos) if total_gastos else 0.0
        })

    return jsonify(resultados)

@relatorios_bp.route('/gastos_recorrentes', methods=['GET'])
def gastos_recorrentes():
    num_meses = request.args.get('num_meses', default=3, type=int)
    hoje = datetime.now()
    data_fim = hoje
    data_inicio = datetime(hoje.year, hoje.month, 1)
    recorrencias = defaultdict(int)

    for _ in range(num_meses):
        transacoes = Transacao.query.filter(
            Transacao.tipo == 'despesa',
            Transacao.data >= data_inicio,
            Transacao.data <= data_fim
        ).all()
        for transacao in transacoes:
            recorrencias[transacao.descricao.lower()] += 1

        # Retrocede um mês
        data_fim = datetime(data_inicio.year, data_inicio.month, 1) - timedelta(days=1)
        data_inicio = datetime(data_fim.year, data_fim.month, 1)

    resultado = [{'descricao': desc, 'frequencia': freq} for desc, freq in recorrencias.items() if freq > 1]
    return jsonify(resultado)

@relatorios_bp.route('/comparar_orcamento', methods=['GET'])
def comparar_orcamento():
    ano = request.args.get('ano')
    mes = request.args.get('mes')

    if not ano or not mes:
        hoje = datetime.now()
        ano = hoje.year
        mes = hoje.month
    else:
        try:
            ano = int(ano)
            mes = int(mes)
            if not (1 <= mes <= 12):
                return jsonify({'message': 'Mês inválido'}), 400
        except ValueError:
            return jsonify({'message': 'Ano e mês devem ser números'}), 400

    resultado = []
    categorias = Categoria.query.all()
    for categoria in categorias:
        total_gasto = db.session.query(func.sum(Transacao.valor)).\
            join(Categoria).\
            filter(Transacao.categoria_id == categoria.id).\
            filter(Transacao.tipo == 'despesa').\
            filter(func.strftime('%Y', Transacao.data) == str(ano)).\
            filter(func.strftime('%m', Transacao.data) == f'{mes:02d}').\
            scalar() or 0.0

        orcamento = categoria.orcamento if categoria.orcamento is not None else 0.0
        diferenca = orcamento - total_gasto
        porcentagem_gasta = (total_gasto / orcamento) * 100 if orcamento > 0 else 0.0

        resultado.append({
            'categoria': categoria.nome,
            'orcamento': float(orcamento),
            'total_gasto': float(total_gasto),
            'diferenca': float(diferenca),
            'porcentagem_gasta': float(porcentagem_gasta)
        })

    return jsonify(resultado)

@relatorios_bp.route('/sugestoes_economia', methods=['GET'])
def sugestoes_economia():
    ano = request.args.get('ano')
    mes = request.args.get('mes')

    if not ano or not mes:
        hoje = datetime.now()
        ano = hoje.year
        mes = hoje.month
    else:
        try:
            ano = int(ano)
            mes = int(mes)
            if not (1 <= mes <= 12):
                return jsonify({'message': 'Mês inválido'}), 400
        except ValueError:
            return jsonify({'message': 'Ano e mês devem ser números'}), 400

    sugestoes = []

    # 1. Categorias com gastos acima do orçamento
    categorias_acima_orcamento = db.session.query(Categoria.nome, func.sum(Transacao.valor)).\
        join(Transacao).\
        filter(Transacao.tipo == 'despesa').\
        filter(func.strftime('%Y', Transacao.data) == str(ano)).\
        filter(func.strftime('%m', Transacao.data) == f'{mes:02d}').\
        group_by(Categoria.nome, Categoria.orcamento).\
        having(func.sum(Transacao.valor) > Categoria.orcamento).\
        all()

    for categoria, total_gasto in categorias_acima_orcamento:
        sugestoes.append(f"Seus gastos com '{categoria}' ({total_gasto:.2f}) estão acima do orçamento.")

    # 2. Gastos recorrentes significativos
    num_meses_analise = 3
    hoje_analise = datetime.now()
    data_fim_analise = hoje_analise
    data_inicio_analise = datetime(hoje_analise.year, hoje_analise.month, 1)
    recorrencias_analise = defaultdict(int)
    gastos_recorrentes_total = defaultdict(float)

    for _ in range(num_meses_analise):
        transacoes_analise = Transacao.query.filter(
            Transacao.tipo == 'despesa',
            Transacao.data >= data_inicio_analise,
            Transacao.data <= data_fim_analise
        ).all()
        for transacao in transacoes_analise:
            recorrencias_analise[transacao.descricao.lower()] += 1
            gastos_recorrentes_total[transacao.descricao.lower()] += transacao.valor

        data_fim_analise = datetime(data_inicio_analise.year, data_inicio_analise.month, 1) - timedelta(days=1)
        data_inicio_analise = datetime(data_fim_analise.year, data_fim_analise.month, 1)

    for descricao, frequencia in recorrencias_analise.items():
        if frequencia == num_meses_analise and gastos_recorrentes_total[descricao] > 50: # Exemplo de valor significativo
            sugestoes.append(f"Você tem um gasto recorrente de '{descricao}' totalizando {gastos_recorrentes_total[descricao]:.2f} nos últimos {num_meses_analise} meses. Considere avaliar a necessidade.")

    # 3. Média de gastos por categoria (sugestão simples)
    media_gastos = db.session.query(Categoria.nome, func.avg(Transacao.valor)).\
        join(Transacao).\
        filter(Transacao.tipo == 'despesa').\
        filter(func.strftime('%Y', Transacao.data) == str(ano)).\
        filter(func.strftime('%m', Transacao.data) == f'{mes:02d}').\
        group_by(Categoria.nome).\
        all()

    for categoria, media in media_gastos:
        if media > 100: # Outro exemplo de valor significativo
            sugestoes.append(f"Seus gastos médios com '{categoria}' estão em torno de {media:.2f}. Avalie se é possível reduzir.")

    return jsonify({'sugestoes': sugestoes})