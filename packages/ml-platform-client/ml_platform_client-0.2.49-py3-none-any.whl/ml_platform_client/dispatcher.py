import random
import traceback
from collections import defaultdict
from multiprocessing import Pipe
from threading import Lock

from ml_platform_client.logger import log
from .algorithm_manager import alg_manager
from .service_response import success_response, success_response_with_data, format_service_response, error_response
from .api_util import catch_exception
from .validation.exceptions import ArgValueError
from .worker import Worker
from .config import global_config


class Dispatcher:
    def __init__(self):
        self.num_worker = global_config.num_worker
        self.num_thread = global_config.num_thread
        self.workers = []
        self.pipes = defaultdict(list)
        self.load_info = defaultdict(set)
        self.all_loaded_models = set()
        self.model_mapping = defaultdict(list)
        for i in range(self.num_worker):
            worker_pipes = []
            for _ in range(self.num_thread):
                pipe1, pipe2 = Pipe(True)
                self.pipes[i].append((pipe1, Lock()))
                worker_pipes.append(pipe2)
            worker = Worker(worker_pipes)
            self.workers.append(worker)
            worker.start()

    def get_load_info(self):
        result = {}
        for idx in self.load_info:
            models = []
            for each in self.load_info[idx]:
                models.append(each)
            result[idx] = models
        return format_service_response(success_response_with_data({'info': result}))

    def register(self, name, alg):
        alg_manager.register(name, alg)
        try:
            for worker in self.pipes:
                pipes = self.pipes[worker]
                for pipe, lock in pipes:
                    with lock:
                        pipe.send(('init_alg', alg_manager.alg_mapping))
                        pipe.recv()
        except Exception as e:
            log.error('register fail')
            log.error(e)

    def set_config(self, config):
        try:
            for worker in self.pipes:
                pipes = self.pipes[worker]
                for pipe, lock in pipes:
                    with lock:
                        pipe.send(('init_config', config))
                        pipe.recv()
        except Exception as e:
            log.error('set config fail')
            log.error(e)

    @catch_exception
    def dispatch_predict(self, model_id, features, uuid):
        if model_id not in self.all_loaded_models:
            raise ArgValueError(message='model [{}] not loaded'.format(model_id))

        candidates = self.model_mapping[model_id]
        index = random.choice(candidates)
        pipe, lock = random.choice(self.pipes[index])
        try:
            with lock:
                pipe.send(('predict', {'model_id': model_id, 'features': features, 'uuid': uuid}))
                success, predictions = pipe.recv()
        except Exception as e:
            log.error(e)
            traceback.print_exc()
            log.error('fail to call worker')
            return format_service_response(error_response(message='worker fail'))

        if success:
            return format_service_response(success_response_with_data({'predictions': predictions}))
        else:
            return format_service_response(error_response(message='prediction fail'))

    @catch_exception
    def dispatch_unload(self, algorithm, model_id):
        if model_id not in self.all_loaded_models:
            return format_service_response(success_response())

        for index in self.load_info:
            load_set = self.load_info[index]
            if model_id in load_set:
                for pipe, lock in self.pipes[index]:
                    with lock:
                        pipe.send(('unload', {
                            'algorithm': algorithm,
                            'model_id': model_id
                        }))
                        success, _ = pipe.recv()
                    if success and model_id in load_set:
                        load_set.remove(model_id)
                    else:
                        return format_service_response(error_response())

        self.all_loaded_models.remove(model_id)
        self.model_mapping[model_id] = []
        return format_service_response(success_response())

    @catch_exception
    def dispatch_load(self, algorithm, model_id, model_path):
        if algorithm not in alg_manager.alg_mapping:
            raise ArgValueError(message='algorithm [{}] not support'.format(algorithm))

        if model_id in self.all_loaded_models:
            return format_service_response(success_response())
            # raise ArgValueError(message='model [{}] already loaded'.format(model_id))

        index = random.randint(0, self.num_worker - 1)
        pipe, lock = random.choice(self.pipes[index])
        with lock:
            pipe.send(('load', {
                'model_id': model_id,
                'model_path': model_path,
                'algorithm': algorithm
            }))
            success, _ = pipe.recv()
        if success:
            self.all_loaded_models.add(model_id)
            self.load_info[index].add(model_id)
            self.model_mapping[model_id].append(index)
            return format_service_response(success_response())
        else:
            return format_service_response(error_response())


dispatcher = Dispatcher()


def register(name, alg):
    global dispatcher
    dispatcher.register(name, alg())


def set_config(config):
    global dispatcher
    dispatcher.set_config(config)
