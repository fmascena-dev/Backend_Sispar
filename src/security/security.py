from flask_bcrypt import bcrypt
import codecs # <-- Adicione esta importação

def hash_senha(senha):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(senha.encode('utf-8'), salt)

def checar_senha(senha, senha_hash):
    print(f"DEBUG: checar_senha - senha_hash recebido: {senha_hash} (tipo: {type(senha_hash)})")

    try:
        # Se o hash do DB vem como uma string que representa bytes (ex: '\x242b...')
        # precisamos decodificá-la primeiro para bytes reais.
        if isinstance(senha_hash, str) and senha_hash.startswith('\\x'): # Verifica se começa com \x
            # Decodifica a string literal de bytes para um objeto bytes real
            senha_hash_bytes = codecs.decode(senha_hash.encode('ascii'), 'hex')
        elif isinstance(senha_hash, str):
            # Se for uma string normal (como '$2b$...'), encoda para bytes
            senha_hash_bytes = senha_hash.encode('utf-8')
        elif isinstance(senha_hash, bytes):
            # Se já for bytes (caso ideal), usa diretamente
            senha_hash_bytes = senha_hash
        else:
            print(f"DEBUG: Tipo inesperado para senha_hash: {type(senha_hash)}")
            return False # Tipo de hash inesperado

        # Agora, checa a senha com o hash convertido para bytes
        return bcrypt.checkpw(senha.encode('utf-8'), senha_hash_bytes)

    except ValueError as e:
        print(f"DEBUG: Erro ValueError em bcrypt.checkpw para hash: {senha_hash} (tipo: {type(senha_hash)}) - Erro: {e}")
        raise # Re-levante para ver o erro completo
    except Exception as e:
        print(f"DEBUG: Erro inesperado em checar_senha: {e}")
        raise # Re-levante para ver o erro completo