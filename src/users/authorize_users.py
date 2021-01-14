from functools import wraps
from flask import abort, request, current_app
import jwt



def authorize(f):
    @wraps(f)
    def decorated_function(*args, **kws):
        if not 'Authorization' in request.headers:
            abort(401)

        user = None
        data = request.headers['Authorization']
        access_token = str.replace(str(data), 'Bearer ', '')
        try:
            user = jwt.decode(access_token, current_app.config['SECRET_KEY'], algorithms="HS256")['sub']
        except:
            abort(401)
        return f(user)

    return decorated_function
