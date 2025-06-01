# src/security/security.py

from flask_bcrypt import bcrypt
import codecs # Mantenha esta importação

def hash_senha(senha):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(senha.encode('utf-8'), salt)

def checar_senha(senha, senha_hash):
    print(f"DEBUG: checar_senha - senha_hash recebido: {senha_hash} (tipo: {type(senha_hash)})")

    try:
        if isinstance(senha_hash, str):
            # Tenta decodificar a string que representa bytes (como \x24...)
            # A 'unicode_escape' pode converter a representação literal '\xXX' para o byte real.
            # No entanto, se o hash original não era de fato uma string de bytes, isso pode não ser ideal.
            # O ideal é que o hash do DB seja uma string normal '$2b$...'
            
            # Vamos tentar uma abordagem mais robusta:
            # 1. Tentar decodificar como 'unicode_escape' se houver '\\x'
            if '\\x' in senha_hash: # Verifica se a string tem a representação de bytes escapada
                try:
                    # Converte a string '\xNN' de volta para o byte real.
                    # Ex: '\\x24' se torna o byte '$'.
                    senha_hash_bytes = senha_hash.encode('latin1').decode('unicode_escape').encode('latin1')
                    # Explicação:
                    # .encode('latin1') para transformar string em bytes sem erro para chars ASCII
                    # .decode('unicode_escape') para interpretar '\xNN' como byte real
                    # .encode('latin1') novamente para obter o objeto bytes final
                    
                    # Verificação para debug:
                    print(f"DEBUG: Após unicode_escape: {senha_hash_bytes} (tipo: {type(senha_hash_bytes)})")

                    # Se a string original NÃO COMEÇA com \x mas contem $2b$, então é uma string normal.
                    # Se o hash original é do tipo '$2b$...', então não precisa dessa decodificação complexa.
                    # Um hash Bcrypt sempre deve começar com '$2a$', '$2b$', etc.
                    # Se a string do DB é literalmente '\x242b...', então a abordagem 'hex' ou 'unicode_escape' seria necessária.
                    
                    # Vamos verificar se o resultado é um hash bcrypt válido
                    if senha_hash_bytes.startswith(b'$2a$') or senha_hash_bytes.startswith(b'$2b$'):
                        return bcrypt.checkpw(senha.encode('utf-8'), senha_hash_bytes)
                    else:
                        print(f"DEBUG: Hash decodificado não parece ser bcrypt: {senha_hash_bytes}")
                        return False

                except Exception as e:
                    print(f"DEBUG: Erro na decodificação de \\x: {e}")
                    # Se falhar a decodificação de '\x', tenta como string normal
                    senha_hash_bytes = senha_hash.encode('utf-8')
            else:
                # Se não tem '\x', assume que é uma string normal de hash (ex: '$2b$...')
                senha_hash_bytes = senha_hash.encode('utf-8')
        elif isinstance(senha_hash, bytes):
            # Se já for bytes, usa diretamente
            senha_hash_bytes = senha_hash
        else:
            print(f"DEBUG: Tipo inesperado para senha_hash: {type(senha_hash)}")
            return False # Tipo de hash inesperado

        # Se chegou aqui, e já tentou decodificar de \x ou já era string/bytes
        # Agora, a checagem final caso o IF acima não tenha retornado.
        return bcrypt.checkpw(senha.encode('utf-8'), senha_hash_bytes)

    except ValueError as e:
        print(f"DEBUG: Erro ValueError em bcrypt.checkpw para hash: {senha_hash} (tipo: {type(senha_hash)}) - Erro: {e}")
        raise # Re-levante para ver o erro completo
    except Exception as e:
        print(f"DEBUG: Erro inesperado em checar_senha: {e}")
        raise # Re-levante para ver o erro completo