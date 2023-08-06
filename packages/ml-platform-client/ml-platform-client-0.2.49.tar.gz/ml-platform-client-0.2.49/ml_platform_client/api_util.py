import json
import traceback
from datetime import datetime, date
from functools import wraps

from flask import Response
from flask_restful.reqparse import RequestParser
from werkzeug.datastructures import FileStorage

from ml_platform_client.logger import log
from .field_type import FieldType
from .validation.exceptions import ArgError, ArgTypeError
from .validation.validator import ValidatorBase, TypeValidator


class JsonSerializable(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)


type_mapping = {
    FieldType.Int: int,
    FieldType.Float: float,
    FieldType.String: str,
    FieldType.Bool: bool,
    FieldType.Array: list,
    FieldType.Object: dict,
}


def parse_args(rules):
    parser = RequestParser()
    try:
        for key, value in rules.items():
            if value == FieldType.File:
                parser.add_argument(key, type=FileStorage, location='files')
            elif value == FieldType.Array:
                parser.add_argument(key, action='append')
            elif value in type_mapping:
                parser.add_argument(key, type=type_mapping[value])
        return parser.parse_args()
    except Exception as e:
        if hasattr(e, 'data') and 'message' in e.data:
            key = list(e.data['message'].keys())[0]
            raise ArgTypeError(key, type_mapping[rules[key]])
        else:
            raise e


def validate(args, setup):
    for key, validator in setup.items():
        if isinstance(validator, list):
            for v in validator:
                v.set_para_name(key)
                v.validate(args[key])
        elif isinstance(validator, ValidatorBase):
            validator.set_para_name(key)
            validator.validate(args[key])


def arg_parse_validation(arg_setup=None, validate_setup=None):
    if arg_setup is None:
        arg_setup = {}
    if validate_setup is None:
        validate_setup = {}
    arg_setup['trace'] = FieldType.Bool
    arg_setup['debug'] = FieldType.Bool
    validate_setup['trace'] = TypeValidator(bool)
    validate_setup['debug'] = TypeValidator(bool)

    def outer(func):
        @wraps(func)
        def inner(*args, **kwargs):
            try:
                parsed_args = parse_args(arg_setup)
                validate(parsed_args, validate_setup)
                kwargs['args'] = parsed_args
                return func(*args, **kwargs)
            except ArgError as e:
                res, status = handle_exception(e, func)
                return Response(json.dumps(res, cls=JsonSerializable), mimetype="application/json", status=status)
        return inner

    return outer


def adapt_to_http_response(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            res = func(*args, **kwargs)
            if not res:
                status = 500
            elif res['status'] == 'success':
                status = 200
            elif res['status'] == 'fail':
                status = 500
            else:
                status = 400
        except Exception as e:
            res, status = handle_exception(e, func)
        return Response(json.dumps(res, cls=JsonSerializable), mimetype="application/json", status=status)

    return wrapper


def handle_exception(e, func):
    message = str(e)
    if isinstance(e, ArgError):
        status = 400
        api_status = 'arg_error'
        res = {'status': api_status, 'message': message}
    else:
        status = 500
        api_status = 'fail'
        res = {'status': api_status, 'message': message, 'trace': traceback.format_exc()}
    log.error("exception in {}.{}: {}".format(str(func), func.__name__, message))
    traceback.print_exc()
    return res, status


def catch_exception(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            message = str(e)
            if isinstance(e, ArgError):
                api_status = 'arg_error'
                res = {'status': api_status, 'message': message}
            else:
                api_status = 'fail'
                res = {'status': api_status, 'message': message, 'trace': traceback.format_exc()}
            log.error("exception in {}.{}: {}".format(str(func), func.__name__, message))
            traceback.print_exc()
            return res

    return wrapper
