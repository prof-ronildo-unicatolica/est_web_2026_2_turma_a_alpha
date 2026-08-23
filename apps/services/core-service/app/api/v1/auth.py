"""Rotas de autenticacao/autorizacao (JWT + bcrypt + RBAC via banco)."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import autenticar_credenciais, get_current_admin, get_current_user
from app.core.database import get_db
from app.core.security import criar_access_token, gerar_hash_senha
from app.models.usuario import Usuario
from app.repositories.usuario_repository import UsuarioRepository
from app.schemas.usuario import (
    LoginRequest,
    Token,
    UsuarioCreateSchema,
    UsuarioPublic,
)

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    "/register", response_model=UsuarioPublic, status_code=status.HTTP_201_CREATED
)
def register(payload: UsuarioCreateSchema, db: Session = Depends(get_db)):
    """Cadastra um novo usuario (sempre com is_admin=False)."""
    repository = UsuarioRepository(db)

    if repository.buscar_por_email(payload.email) is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ja existe um usuario com esse e-mail",
        )

    usuario = Usuario(
        nome=payload.nome,
        email=payload.email,
        senha_hash=gerar_hash_senha(payload.senha),
        is_admin=False,
    )
    return repository.criar(usuario)


@router.post("/login", response_model=Token)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    """Login: valida as credenciais contra o banco e devolve um JWT."""
    usuario = autenticar_credenciais(db, payload.email, payload.senha)
    if usuario is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos",
        )
    access_token = criar_access_token({"sub": usuario.email})
    return Token(access_token=access_token)


@router.get("/me", response_model=UsuarioPublic)
def get_me(usuario_atual: Usuario = Depends(get_current_user)):
    """Rota protegida: retorna o perfil do usuario autenticado."""
    return usuario_atual


@router.get("/admin/verificacao")
def somente_admin(admin: Usuario = Depends(get_current_admin)):
    """Rota administrativa de exemplo (autorizacao por is_admin)."""
    return {"mensagem": f"Acesso administrativo concedido para {admin.nome}"}