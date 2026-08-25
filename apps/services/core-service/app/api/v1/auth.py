from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_admin, get_current_user
from app.core.database import get_db
from app.models.usuario import Usuario
from app.schemas.usuario import LoginRequest, Token, UsuarioCreate, UsuarioPublic
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Autenticação e Segurança"])


@router.post("/register", response_model=UsuarioPublic, status_code=status.HTTP_201_CREATED)
def cadastrar_usuario(payload: UsuarioCreate, db: Session = Depends(get_db)):
    """Cadastra um novo cliente na plataforma com a senha criptografada em Bcrypt."""
    service = AuthService(db)
    novo_usuario = service.registrar(payload)
    return novo_usuario


@router.post("/login", response_model=Token)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    """Autentica o e-mail e a senha do usuário e retorna o Token JWT real."""
    service = AuthService(db)
    usuario = service.autenticar(payload.email, payload.senha)
    return service.gerar_token(usuario)


@router.get("/me", response_model=UsuarioPublic)
def obter_perfil_logado(usuario_atual: Usuario = Depends(get_current_user)):
    """Rota protegida: Retorna o perfil do usuário logado (exige Token Bearer JWT)."""
    return usuario_atual


@router.get("/admin/verificacao")
def verificar_acesso_admin(admin_atual: Usuario = Depends(get_current_admin)):
    """Rota administrativa de exemplo: Exige que o usuário logado seja is_admin=True."""
    return {"mensagem": f"Acesso administrativo verificado com sucesso para {admin_atual.nome}"}