from datetime import datetime, timedelta
import jwt
from flask import current_app

def generate_token(user, token_type='access'):
    """Generate JWT token for user"""
    payload = {
        'user_id': user.id,
        'username': user.username,
        'role': user.role,
        'type': token_type,
        'exp': datetime.utcnow() + (
            current_app.config['JWT_ACCESS_TOKEN_EXPIRES'] if token_type == 'access'
            else current_app.config['JWT_REFRESH_TOKEN_EXPIRES']
        )
    }
    return jwt.encode(
        payload,
        current_app.config['JWT_SECRET_KEY'],
        algorithm='HS256'
    )

def verify_token(token):
    """Verify JWT token and return payload"""
    try:
        payload = jwt.decode(
            token,
            current_app.config['JWT_SECRET_KEY'],
            algorithms=['HS256']
        )
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None 