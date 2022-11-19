from .. import login_manager
import jwt
from flask import current_app

@login_manager.user_loader
def load_user(token):
    try:
        jwt_options = {
            'verify_signature': False,
            'verify_exp': True,
            'verify_nbf': False,
            'verify_iat': True,
            'verify_aud': False
        }

        data = jwt.decode(token, options=jwt_options, algorithms=['HS256'])
        return {'id': data['id'], 'email': data['email']}
    except jwt.excetions.InvalidTokenError:
        print('Invalid Token')
    except jwt.exceptions.DecodeError:
        print('Decode Error')


def check_jwt_expiration(token):
    try:
        header_data = jwt.get_unverified_header(token)
        key = current_app.config['SECRET_KEY']
        jwt.decode(token, key, algorithms=[header_data['alg']])
        return False
    # Token Expired
    except jwt.ExpiredSignatureError:
        return True
    # Token Invalido    
    except jwt.InvalidTokenError:
        return True
    except jwt.DecodeError:
        return True
