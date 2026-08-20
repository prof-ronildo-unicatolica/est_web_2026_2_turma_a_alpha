from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import create_access_token, get_password_hash, verify_password
from app.models.usuario import Usuario
from app.schemas.usuario import Token, UsuarioCreate


class AuthService:
    def __init__(self, db: Session):
        self.db = db

    def registrar(self, usuario_in: UsuarioCreate) -> Usuario:
        """Cadastra um novo cliente no banco de dados com a senha criptografada."""
        # 1. Verifica se já existe um usuário cadastrado com este e-mail
        usuario_existente = self.db.query(Usuario).filter(Usuario.email == usuario_in.email).first()
        if usuario_existente:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Este e-mail já está cadastrado no sistema.",
            )

        # 2. Transforma a senha digitada em um hash seguro com Bcrypt
        senha_criptografada = get_password_hash(usuario_in.senha)

        # 3. Cria a nova instância do modelo Usuario
        novo_usuario = Usuario(
            nome=usuario_in.nome,
            email=usuario_in.email,
            senha_hash=senha_criptografada,
            is_admin=False,  # Novos cadastros sempre começam como clientes normais
        )

        # 4. Salva no PostgreSQL
        self.db.add(novo_usuario)
        self.db.commit()
        self.db.refresh(novo_usuario)
        return novo_usuario

    def autenticar(self, email: str, senha: str) -> Usuario:
        """Valida se as credenciais (e-mail e senha) fornecidas estão corretas."""
        usuario = self.db.query(Usuario).filter(Usuario.email == email).first()
        if not usuario or not verify_password(senha, usuario.senha_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="E-mail ou senha incorretos.",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return usuario

    def gerar_token(self, usuario: Usuario) -> Token:
        """Gera o Token JWT assinado contendo o ID do usuário."""
        access_token = create_access_token(subject=str(usuario.id))
        return Token(access_token=access_token, token_type="bearer")