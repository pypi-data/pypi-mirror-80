import logging
import sys

log = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)

formatter = logging.Formatter(
    '%(asctime)s %(levelname)s %(process)d --- [%(threadName)s] %(filename)s:%(lineno)-4d: [ml-platform-client]%(message)s'
)
handler.setFormatter(formatter)

log.addHandler(handler)
log.setLevel(logging.INFO)
