import time

from ml_platform_client.logger import log
from .dispatcher import dispatcher
from .api_util import arg_parse_validation, adapt_to_http_response
from .base import BaseApi
from .setup import *
from .algorithm_manager import alg_manager


class TrainApi(BaseApi):
    api_url = '/train'

    @arg_parse_validation(arg_setup=train_arg_setup, validate_setup=train_validate_setup)
    @adapt_to_http_response
    def post(self, args):
        return alg_manager.train(args['algorithm'], args['model_path'], args['data'],
                                 args['parameter'], args['extend'])


class StatusApi(BaseApi):
    api_url = '/status'

    @arg_parse_validation(arg_setup=status_arg_setup, validate_setup=status_validate_setup)
    @adapt_to_http_response
    def get(self, args):
        start = time.time()
        status = alg_manager.status(args['algorithm'], args['model_id'])
        end = time.time()
        log.info('{}.{} status cost: {}'.format(args['algorithm'], args['model_id'], end - start))
        return status


class PredictApi(BaseApi):
    api_url = '/predict'

    @arg_parse_validation(arg_setup=predict_arg_setup, validate_setup=predict_validate_setup)
    @adapt_to_http_response
    def post(self, args):
        start = time.time()
        prediction = dispatcher.dispatch_predict(args['model_id'], args['features'], args['uuid'])
        end = time.time()
        log.info('{} prediction cost: {}'.format(args['model_id'], end - start))
        return prediction


class LoadApi(BaseApi):
    api_url = '/load'

    @arg_parse_validation(arg_setup=load_arg_setup, validate_setup=load_validate_setup)
    @adapt_to_http_response
    def post(self, args):
        start = time.time()
        result = dispatcher.dispatch_load(args['algorithm'], args['model_id'], args['model_path'])
        end = time.time()
        log.info('{} load cost: {}'.format(args['model_id'], end - start))
        return result


class UnloadApi(BaseApi):
    api_url = '/unload'

    @arg_parse_validation(arg_setup=unload_arg_setup, validate_setup=unload_validate_setup)
    @adapt_to_http_response
    def post(self, args):
        start = time.time()
        result = dispatcher.dispatch_unload(args['algorithm'], args['model_id'])
        end = time.time()
        log.info('{} load cost: {}'.format(args['model_id'], end - start))
        return result


class MonitorApi(BaseApi):
    api_url = '/monitor'

    @arg_parse_validation()
    @adapt_to_http_response
    def get(self, args):
        return dispatcher.get_load_info()
