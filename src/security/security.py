from flask_bcrypt import bcrypt

def hash_senha(senha):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(senha.encode('utf-8'), salt) # Retorna bytes

def checar_senha(senha, senha_hash):
    #* O senha_hash vindo do DB agora será uma string UTF-8 normal (sem \x ou b'')
    print(f"DEBUG: checar_senha - senha_hash recebido: {senha_hash} (tipo: {type(senha_hash)})") # Manter para debug
    #* Basta encodá-la para bytes para passar para bcrypt.checkpw
    
    try:
        #! Garante que senha_hash é uma string e a encoda para bytes
        if isinstance(senha_hash, str):
            hashed_password_bytes = senha_hash.encode('utf-8')
        elif isinstance(senha_hash, bytes): # Caso improvável após a correção no cadastro
            hashed_password_bytes = senha_hash
        else:
            print(f"DEBUG: Tipo inesperado para senha_hash: {type(senha_hash)}")
            return False
            
        return bcrypt.checkpw(senha.encode('utf-8'), hashed_password_bytes)
        
    except ValueError as e:
        print(f"DEBUG: Erro ValueError em bcrypt.checkpw para hash: {senha_hash} (tipo: {type(senha_hash)}) - Erro: {e}")
        raise # Lance novamente para ver o erro completo
    except Exception as e:
        print(f"DEBUG: Erro inesperado em checar_senha: {e}")
        raise