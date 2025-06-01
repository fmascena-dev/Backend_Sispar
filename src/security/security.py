# src/security/security.py

from flask_bcrypt import bcrypt

def hash_senha(senha):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(senha.encode('utf-8'), salt)

def checar_senha(senha, senha_hash):
    print(f"DEBUG: checar_senha - senha_hash recebido: {senha_hash} (tipo: {type(senha_hash)})") # <-- Adicione esta linha de debug
    try:
        return bcrypt.checkpw(senha.encode('utf-8'), senha_hash.encode('utf-8'))
    except ValueError as e:
        print(f"DEBUG: Erro ValueError em bcrypt.checkpw para hash: {senha_hash} (tipo: {type(senha_hash)}) - Erro: {e}") # <-- Adicione esta linha de debug
        raise # Re-levante a exceção para vê-la completa nos logs do Render