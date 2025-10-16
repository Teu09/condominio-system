import jwt
from fastapi import HTTPException, Depends, Header
from typing import Optional, Dict, Any
import os


class AuthMiddleware:
    def __init__(self):
        self.jwt_secret = os.getenv('JWT_SECRET', 'SECRET_KEY')
        self.jwt_algorithm = 'HS256'
    
    def verify_token(self, authorization: Optional[str] = Header(None)) -> Dict[str, Any]:
        if not authorization:
            raise HTTPException(status_code=401, detail="Token de autorização necessário")
        
        try:
            token = authorization.replace("Bearer ", "")
            payload = jwt.decode(token, self.jwt_secret, algorithms=[self.jwt_algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expirado")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Token inválido")
    
    def require_permission(self, permission: str):
        def permission_checker(payload: Dict[str, Any] = Depends(self.verify_token)):
            user_permissions = payload.get('permissions', [])
            if 'all' not in user_permissions and permission not in user_permissions:
                raise HTTPException(status_code=403, detail=f"Permissão '{permission}' necessária")
            return payload
        return permission_checker
    
    def require_role(self, role: str):
        def role_checker(payload: Dict[str, Any] = Depends(self.verify_token)):
            user_role = payload.get('role')
            if user_role != role:
                raise HTTPException(status_code=403, detail=f"Role '{role}' necessária")
            return payload
        return role_checker
    
    def require_tenant_access(self, tenant_id: int):
        def tenant_checker(payload: Dict[str, Any] = Depends(self.verify_token)):
            user_tenant_id = payload.get('tenant_id')
            if user_tenant_id != tenant_id:
                raise HTTPException(status_code=403, detail="Acesso negado a este condomínio")
            return payload
        return tenant_checker


auth_middleware = AuthMiddleware()
