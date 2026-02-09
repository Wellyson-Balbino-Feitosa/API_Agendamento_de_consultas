from http import HTTPStatus

from fastapi import HTTPException


class Exceptions:
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )


exceptions = Exceptions()
