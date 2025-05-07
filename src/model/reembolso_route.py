from flask import Blueprint, request, jsonify
from src.model import db
from src.model.reembolso_model import Reembolso
from datetime import datetime

reembolso_bp = Blueprint('reembolso', __name__, url_prefix='/reembolso')

@reembolso_bp.route('/reembolsos', methods=['POST', 'OPTIONS'])
def cadastrar_reembolso():
    if request.method == 'OPTIONS':
        return '', 200
    
    dados = request.get_json()
    print("Dados recebidos:", dados)

    try:
        # Verifica se é uma lista ou um único objeto
        reembolsos = []
        data_list = dados if isinstance(dados, list) else [dados]
        
        for item in data_list:
            try:
                data_formatada = datetime.strptime(item['data'], '%d/%m/%Y').date()
            except ValueError:
                data_formatada = datetime.strptime(item['data'], '%Y-%m-%d').date()

            novo_reembolso = Reembolso(
                colaborador=item['colaborador'],
                empresa=item['empresa'],
                num_prestacao=item['num_prestacao'],
                descricao=item['descricao'],
                data=data_formatada,
                tipo_reembolso=item['tipo_reembolso'],
                centro_custo=item['centro_custo'],
                ordem_interna=item.get('ordem_interna'),
                divisao=item.get('divisao'),
                pep=item.get('pep'),
                moeda=item['moeda'],
                distancia_km=item.get('distancia_km'),
                valor_km=item.get('valor_km'),
                valor_faturado=item['valor_faturado'],
                despesa=item.get('despesa'),
                id_colaborador=item.get('id_colaborador'),  # Agora opcional
                status=item.get('status', 'Em analise')
            )
            reembolsos.append(novo_reembolso)
        
        db.session.add_all(reembolsos)
        db.session.commit()
        print(f"ID gerado: {novo_reembolso.id}")
        
        return jsonify({
            'mensagem': f'{len(reembolsos)} reembolso(s) cadastrado(s) com sucesso!',
            'total_itens': len(reembolsos)
        }), 201

    except ValueError as ve:
        return jsonify({'erro': f'Formato de data inválido: {str(ve)}'}), 400
    except Exception as e:
        db.session.rollback()
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
                'despesa': r.despesa,
                'status': r.status
            })

        return jsonify(lista_reembolsos), 200

    except Exception as e:
        return jsonify({'erro': f'Erro ao listar reembolsos: {str(e)}'}), 500