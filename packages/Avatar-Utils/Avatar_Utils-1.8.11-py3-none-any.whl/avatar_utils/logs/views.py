from datetime import timedelta
from logging import getLogger

from flask import g
from flask import request
from sqlalchemy.exc import DatabaseError

from app import db
from . import logs
from .models import Log
from ..core import create_response

logger = getLogger(__name__)


@logs.before_app_request
def before_request():
    log_prefix = f'[ LOGGING BEFORE | {request.remote_addr} {request.method} > {request.url_rule} ]'
    try:
        log = Log.init(request)
        g.log = log
    except DatabaseError as err:
        logger.warning(f'{log_prefix} < Rollback transaction due to: {err}')
        db.session.rollback()
    except BaseException as err:
        logger.error(f'{log_prefix} < Error occurs: {err}')


@logs.after_app_request
def after_request(response):
    log_prefix = f'[ LOGGING AFTER | {request.remote_addr} {request.method} > {request.url_rule} ]'
    try:
        if g.log:
            Log.complete(g.log, response)
        else:
            logger.warning('log_id is None, cannot complete logging process')
    except DatabaseError as err:
        logger.warning(f'{log_prefix} < Rollback transaction due to: {err}')
        db.session.rollback()
    except BaseException as err:
        logger.error(f'{log_prefix} < Error occurs: {err}')
    return response


@logs.route('/logs/prune', methods=['POST'])
def logs_prune():
    default_interval = timedelta(days=30)

    logger.debug('Pruning logs with interval = %s', default_interval)

    Log.prune(default_interval)

    return create_response()
