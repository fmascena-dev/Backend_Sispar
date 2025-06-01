from flask import Blueprint, request, jsonify
from src.model import db
from src.model.reembolso_model import Reembolso
from datetime import datetime
from src.model.colaborador_model import Colaborador 

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
            
            colaborador_nome = item['colaborador']
            colaborador_obj = Colaborador.query.filter_by(nome=colaborador_nome).first()

            if not colaborador_obj:
                return jsonify({'erro': f'Colaborador "{colaborador_nome}" não encontrado no sistema.'}), 404
            
            try:
                data_formatada = datetime.strptime(item['data'], '%d/%m/%Y').date()
            except ValueError:
                data_formatada = datetime.strptime(item['data'], '%Y-%m-%d').date()

            novo_reembolso = Reembolso(
                colaborador=colaborador_nome,
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
                id_colaborador=colaborador_obj.id,
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
    
@reembolso_bp.route('/reembolsos/<int:id>', methods=['DELETE'])
def deletar_reembolso(id):
    try:
        reembolso = Reembolso.query.get(id)

        if not reembolso:
            return jsonify({'erro': f'Reembolso com ID {id} não encontrado.'}), 404

        db.session.delete(reembolso)
        db.session.commit()

        return jsonify({'mensagem': f'Reembolso com ID {id} deletado com sucesso!'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': f'Erro ao deletar reembolso: {str(e)}'}), 500
    
#! LISTA O REEMBOLSO ATRAVÉS DO NÚMERO DE PRESTAÇÃO
@reembolso_bp.route('/reembolsos/prestacao/<string:num_prestacao>', methods=['GET'])
def listar_reembolsos_por_prestacao(num_prestacao):
    
    try:
        #! Busca todos os reembolsos que correspondem ao num_prestacao fornecido
        reembolsos = Reembolso.query.filter_by(num_prestacao=num_prestacao).all()

        if not reembolsos:
            return jsonify({'mensagem': f'Nenhum reembolso encontrado para o número de prestação "{num_prestacao}".'}), 404

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
        # Em caso de erro, retorna uma mensagem de erro 500
        return jsonify({'erro': f'Erro ao buscar reembolsos por número de prestação: {str(e)}'}), 500
