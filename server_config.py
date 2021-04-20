import os

proc_name = "DeepPepServer"

port = os.getenv("DEEPPEP_PORT", "80")
bind = "0.0.0.0:" + port
backlog = 64

workers = os.getenv("DEEPPEP_NWORKERS", 1)
worker_class = 'uvicorn.workers.UvicornWorker'
worker_connections = 1000
timeout = 30
keepalive = 2

model_dir = os.getenv("DEEPPEP_MODEL_DIR", "")
raw_env = [
    "DEEPPEP_MODEL_DIR=" + model_dir,
]

errorlog = os.getenv("DEEPPEP_ERROR_LOG", "-")
loglevel = 'info'
accesslog = os.getenv("DEEPPEP_ACCESS_LOG", "-")
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

print(
"""
{proc_name} config settings:
PORT:            {port}
WORKERS:         {workers}
MODEL DIRECTORY: {model_dir}
""".format(**locals())
)
