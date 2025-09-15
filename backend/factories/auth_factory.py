from backend.models.auth import AuthRequest

def create_auth_payload(username: str = "admin", password: str = "password123") -> AuthRequest:
    """Фабрика для создания payload аутентификации."""
    return AuthRequest(username=username, password=password)