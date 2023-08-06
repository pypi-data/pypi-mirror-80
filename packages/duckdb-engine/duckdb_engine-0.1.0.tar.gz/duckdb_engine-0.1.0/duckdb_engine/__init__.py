import re
from dataclasses import dataclass, field
from typing import List

import duckdb
from sqlalchemy import Sequence
from sqlalchemy.dialects.postgresql import dialect as postgres_dialect


class DBAPI:
    paramstyle = "qmark"

    class Error(Exception):
        pass


DNE = re.compile(r"Catalog: ([^ ]+) with name ([^ ]+) does not exist!")


@dataclass
class ConnectionWrapper:
    c: duckdb.DuckDBPyConnection
    description: List[str] = field(default_factory=list)
    notices: List[str] = field(default_factory=list)

    def cursor(self):
        return self

    @property
    def connection(self):
        return self

    def close(self):
        # duckdb doesn't support 'soft closes'
        pass

    @property
    def rowcount(self):
        return self.c.rowcount

    def execute(self, statement, parameters, context):
        self.c.execute(statement, parameters)
        if context.result_column_struct:
            self.description = context.result_column_struct[0]
        else:
            self.description = []

    def fetchone(self):
        self.description = [(None, None)]
        return self.c.fetchone()

    def fetchall(self):
        return self.c.fetchall()

    def commit(self):
        self.c.commit()


def check_existance(connection, function: str, name: str, type_: str) -> bool:
    try:
        connection.execute(f"{function}('{name}');")
    except RuntimeError as e:
        if e.args[0] == f"Catalog: {type_} with name {name} does not exist!":
            return False
        else:
            raise
    else:
        return True


class Dialect(postgres_dialect):
    _has_events = False
    identifier_preparer = None
    # colspecs TODO: remap types to duckdb types

    def connect(self, *args, **kwargs):
        return ConnectionWrapper(duckdb.connect(*args, **kwargs))

    def on_connect(self):
        pass

    class ddl_compiler(postgres_dialect.ddl_compiler):
        def __init__(self, dialect, ddl, **kwargs):
            ddl.include_foreign_key_constraints = {}
            super().__init__(dialect, ddl, **kwargs)

        def get_column_specification(self, column, **kwargs):
            if column.primary_key and column is column.table._autoincrement_column:
                assert isinstance(
                    column.default, Sequence
                ), "Primary keys must have a default sequence"
            return super().get_column_specification(column, **kwargs)

    def do_execute(self, cursor, statement, parameters, context):
        cursor.execute(statement, parameters, context)

    def has_table(self, connection, table_name, schema=None):
        return check_existance(connection, "PRAGMA show", table_name, "Table")

    def has_sequence(self, connection, sequence_name, schema=None):
        return check_existance(connection, "SELECT nextval", sequence_name, "Sequence")

    def has_type(self, connection, type_name, schema=None):
        return False

    @staticmethod
    def dbapi():
        return DBAPI

    def create_connect_args(self, u):
        return (), {"database": u.__to_string__(hide_password=False).split("///")[1]}

    def initialize(self, connection):
        pass

    def do_rollback(self, connection):
        pass

    @classmethod
    def get_dialect_cls(cls, u):
        return cls


dialect = Dialect
