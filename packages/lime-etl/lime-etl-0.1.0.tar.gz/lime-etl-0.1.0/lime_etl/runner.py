from __future__ import annotations

import itertools
import typing

import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker

from adapters import email_adapter, orm, timestamp_adapter  # type: ignore
from domain import batch_delta, job_spec, value_objects  # type: ignore
from services import batch_runner, unit_of_work  # type: ignore
from services.admin import delete_old_logs  # type: ignore

DEFAULT_ADMIN_JOBS = [
    delete_old_logs.DeleteOldLogs(days_to_keep=value_objects.DaysToKeep(3)),
]


def run(
    *,
    engine_or_uri: typing.Union[sa.engine.Engine, str],
    etl_jobs: typing.Iterable[job_spec.JobSpec],
    admin_jobs: typing.Iterable[job_spec.JobSpec] = frozenset(DEFAULT_ADMIN_JOBS),
    schema: typing.Optional[str] = None,
    ts_adapter: timestamp_adapter.TimestampAdapter = timestamp_adapter.LocalTimestampAdapter(),
    email_adapter: typing.Optional[email_adapter.EmailAdapter] = None
) -> batch_delta.BatchDelta:
    if schema:
        orm.set_schema(schema=value_objects.SchemaName(schema))

    orm.start_mappers()
    if type(engine_or_uri) is sa.engine.Engine:
        engine = engine_or_uri
    else:
        engine = sa.create_engine(engine_or_uri, echo=True)
    orm.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine)
    uow = unit_of_work.DefaultUnitOfWork(session_factory=session_factory)
    result: batch_delta.BatchDelta = batch_runner.run(
        uow=uow, jobs=itertools.chain(admin_jobs, etl_jobs), ts_adapter=ts_adapter
    )
    if email_adapter:
        email_adapter.send(result=result)
    return result
