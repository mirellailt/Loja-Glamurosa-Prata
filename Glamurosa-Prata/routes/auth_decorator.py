from functools import wraps
from flask import session, redirect, url_for
from services.user_service import get_user_by_id

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):

        user_id = session.get('user_id')

        if not user_id:
            return redirect(url_for('auth.login'))

        usuario = get_user_by_id(user_id)

        if usuario is None:
            session.clear()
            return redirect(url_for('auth.login'))

        return func(*args, **kwargs)

    return wrapper