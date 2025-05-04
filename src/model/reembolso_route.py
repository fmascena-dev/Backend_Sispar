from flask import Blueprint, request, jsonify
from src.model import db
from src.model.reembolso_model import Reembolso  # supondo que o model se chame assim
from datetime import datetime

reembolso_bp = Blueprint('reembolso', __name__, url_prefix='/reembolso')

@reembolso_bp.route('/reembolsos', methods=['POST', 'OPTIONS'])
def cadastrar_reembolso():
    if request.method == 'OPTIONS':
        # Resposta ao preflight CORS
        return '', 200
    
    dados = request.get_json()
    print("Dados recebidos:", dados)

    try:
        # Converte a data do formato 'DD/MM/YYYY' para datetime.date
        # data_formatada = datetime.strptime(dados['data'], '%d/%m/%Y').date()
        try:
            data_formatada = datetime.strptime(dados['data'], '%d/%m/%Y').date()
        except ValueError:
        # se falhar, tenta YYYY-MM-DD
            data_formatada = datetime.strptime(dados['data'], '%Y-%m-%d').date()

        novo_reembolso = Reembolso(
            colaborador=dados['colaborador'],
            empresa=dados['empresa'],
            num_prestacao=dados['num_prestacao'],
            descricao=dados['descricao'],
            data=data_formatada,
            tipo_reembolso=dados['tipo_reembolso'],
            centro_custo=dados['centro_custo'],
            ordem_interna=dados['ordem_interna'],
            divisao=dados['divisao'],
            pep=dados['pep'],
            moeda=dados['moeda'],
            distancia_km=dados['distancia_km'],
            valor_km=dados['valor_km'],
            valor_faturado=dados['valor_faturado'],
            despesa=dados['despesa']
        )

        db.session.add(novo_reembolso)
        db.session.commit()

        return jsonify({'mensagem': 'Reembolso cadastrado com sucesso!'}), 201

    except ValueError:
        return jsonify({'erro': 'Formato de data inválido. Use DD/MM/YYYY'}), 400

    except Exception as e:
        print("Erro no backend:", e)
        return jsonify({'erro': f'Erro ao cadastrar reembolso: {str(e)}'}), 500

@reembolso_bp.route('/reembolsos', methods=['GET'])
def listar_reembolsos():
    try:
        reembolsos = Reembolso.query.all()
        lista_reembolsos = []

        for r in reembolsos:
            lista_reembolsos.append({
                'id': r.id,
                'colaborador': r.colaborador,
                'empresa': r.empresa,
                'num_prestacao': r.num_prestacao,
                'descricao': r.descricao,
                'data': r.data.strftime('%Y-%m-%d'),
                'tipo_reembolso': r.tipo_reembolso,
                'centro_custo': r.centro_custo,
                'ordem_interna': r.ordem_interna,
                'divisao': r.divisao,
                'pep': r.pep,
                'moeda': r.moeda,
                'distancia_km': r.distancia_km,
                'valor_km': r.valor_km,
                'valor_faturado': r.valor_faturado,
                'despesa': r.despesa
            })

        return jsonify(lista_reembolsos), 200

    except Exception as e:
        return jsonify({'erro': f'Erro ao listar reembolsos: {str(e)}'}), 500
