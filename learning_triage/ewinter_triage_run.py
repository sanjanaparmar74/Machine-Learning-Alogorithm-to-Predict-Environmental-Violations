#!/usr/bin/env python

import yaml

from sqlalchemy.engine.url import URL
from triage.util.db import create_engine
from triage.experiments import MultiCoreExperiment
import logging

import os

from sqlalchemy.event import listens_for
from sqlalchemy.pool import Pool

andrew_id = os.getenv('USER')
user_path = os.path.join('/data/users/', andrew_id)

# add logging to a file (it will also go to stdout via triage logging config)
log_filename = os.path.join(user_path, 'triage.log')
logger = logging.getLogger('')
hdlr = logging.FileHandler(log_filename)
hdlr.setLevel(15)   # verbose level
hdlr.setFormatter(logging.Formatter('%(name)-30s  %(asctime)s %(levelname)10s %(process)6d  %(filename)-24s  %(lineno)4d: %(message)s', '%d/%m/%Y %I:%M:%S %p'))
logger.addHandler(hdlr)

# creating database engine
dbfile = os.path.join(user_path, 'database.yaml')

with open(dbfile, 'r') as dbf:
    dbconfig = yaml.safe_load(dbf)

# assume group role to ensure shared permissions
@listens_for(Pool, "connect")
def assume_role(dbapi_con, connection_record):
     logging.debug(f"setting role {dbconfig['role']};")
     dbapi_con.cursor().execute(f"set role {dbconfig['role']};")

db_url = URL(
            'postgres',
            host=dbconfig['host'],
            username=dbconfig['user'],
            database=dbconfig['db'],
            password=dbconfig['pass'],
            port=dbconfig['port'],
        )

db_engine = create_engine(db_url)

triage_output_path = os.path.join(user_path, 'triage_output')
os.makedirs(triage_output_path, exist_ok=True)

# loading config file
with open('%s_triage_config.yaml' % andrew_id, 'r') as fin:
    config = yaml.safe_load(fin)


# creating experiment object
experiment = MultiCoreExperiment(
    config = config,
    db_engine = db_engine,
    project_path = triage_output_path,
    n_processes=2,
    n_db_processes=2,
    replace=True,
    save_predictions=True
    )

# experiment.validate()
experiment.run()