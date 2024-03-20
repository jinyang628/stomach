import logging
import os
from datetime import datetime
from typing import List

import libsql_client

from app.connectors.turso import TursoConnector


class ObjectStore:
    _table_name: str = None
    _db_client: TursoConnector = None

    def __init__(
        self,
        table_name: str,
    ):
        self._table_name = table_name
        self._db_client = TursoConnector(
            url=os.environ.get("TURSO_DB_URL"),
            auth_token=os.environ.get("TURSO_DB_AUTH_TOKEN"),
        )

    ####
    #### TABLE OPERATIONS
    ####

    def create_table(
        self,
        table_name: str,
        columns: dict,
    ) -> None:
        column_defs = []
        for column_name, column_type in columns.items():
            column_defs.append(f"{column_name} {column_type}")

        sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(column_defs)})"
        try:
            statement = libsql_client.Statement(sql=sql)
            self._db_client.execute(statement=statement)
            logging.info(f"Table {table_name} created successfully.")
        except Exception as e:
            logging.error(f"Error creating table {table_name}: {e}")
            raise e

    def delete_table(
        self,
        table_name: str,
    ) -> None:
        sql = f"DROP TABLE IF EXISTS {table_name}"
        try:
            statement = libsql_client.Statement(sql=sql)
            self._db_client.execute(statement=statement)
            logging.info(f"Table {table_name} deleted successfully.")
        except Exception as e:
            logging.error(f"Error deleting table {table_name}: {e}")
            raise e

    ####
    #### CRUD
    ####

    def get(
        self,
        ids: List[str],
    ) -> List[dict]:
        statement = self._ids_to_get_statement(table_name=self._table_name, ids=ids)
        try:
            rs = self._db_client.execute(statement=statement)
            logging.debug(rs.rows)
            _dicts = [
                {rs.columns[i]: row[i] for i in range(len(rs.columns))}
                for row in rs.rows
            ]
            return _dicts
        except Exception as e:
            logging.error(f"Error found for statement {statement.sql}: {e}")
            raise e

    def delete(
        self,
        ids: List[str],
    ) -> bool:
        statement = self._ids_to_delete_statement(table_name=self._table_name, ids=ids)
        try:
            rs = self._db_client.execute(statement=statement)
            logging.debug(rs.rows_affected)
            return rs.rows_affected == len(ids)
        except Exception as e:
            logging.error(f"Error found for statement {statement.sql}: {e}")
            raise e

    def insert(
        self,
        objs: List[dict],
    ) -> List[str]:
        statements = [
            self._dict_to_insert_statement(table_name=self._table_name, dict=obj)
            for obj in objs
        ]
        try:
            rss = self._db_client.batch_execute(statements=statements)
            rowids = [r.last_insert_rowid for r in rss]
            logging.debug(rowids)
            _dicts = self._get_by_rowids(rowids=rowids)
            return [d["id"] for d in _dicts]
        except Exception as e:
            logging.error(f"Error raised for SQL {[st.sql for st in statements]}: {e}")
            raise e

    def update(
        self,
        objs: List[dict],
    ) -> bool:
        statements = [
            self._dict_to_update_statement(table_name=self._table_name, dict=obj)
            for obj in objs
        ]
        try:
            rss = self._db_client.batch_execute(statements=statements)
            total_affected = sum([rs.rows_affected for rs in rss])
            logging.debug(total_affected)
            return total_affected == len(objs)
        except Exception as e:
            logging.error(f"Error raised for SQL {[st.sql for st in statements]}: {e}")
            raise e

    def execute(
        self,
        sql: str,
    ) -> List[dict]:
        statement = libsql_client.Statement(sql=sql)
        try:
            rs = self._db_client.execute(statement=statement)
            logging.debug(rs.rows)
            _dicts = [
                {rs.columns[i]: row[i] for i in range(len(rs.columns))}
                for row in rs.rows
            ]
            return _dicts
        except Exception as e:
            logging.error(f"Error found for statement {statement.sql}: {e}")
            raise e

    def _get_by_rowids(
        self,
        rowids: List[int],
    ) -> List[dict]:
        sql = f"""SELECT *
                    FROM {self._table_name}
                    WHERE rowid IN ({','.join([self._value_to_sql_value(rowid) for rowid in rowids])})"""
        return self.execute(sql=sql)

    ####
    #### SQL Statements
    ####

    def _dict_to_insert_statement(
        self,
        table_name: str,
        dict: dict,
    ) -> libsql_client.Statement:
        _dict = dict.copy()
        if "created_at" in _dict:
            _dict.pop("created_at")
        if "updated_at" in _dict:
            _dict.pop("updated_at")

        # _iter = _dict.copy()
        # for k, v in _iter.items():
        #     if v is None:
        #         _dict.pop(k)

        sql = f"""INSERT INTO {table_name} ({','.join([f'{k}' for k in _dict.keys()])})
                VALUES ({','.join([f'{self._value_to_sql_value(v)}' for v in _dict.values()])})"""
        logging.debug(sql)

        return libsql_client.Statement(sql=sql)

    def _dict_to_update_statement(
        self,
        table_name: str,
        dict: dict,
    ) -> libsql_client.Statement:
        _dict = dict.copy()
        _id = _dict.get("id")
        if "id" in _dict:
            _dict.pop("id")
        if "created_at" in _dict:
            _dict.pop("created_at")
        if "updated_at" in _dict:
            _dict.pop("updated_at")

        # _iter = _dict.copy()
        # for k, v in _iter.items():
        #     if v is None:
        #         _dict.pop(k)

        sql = f"""UPDATE {table_name}
                    SET {','.join([f'{k}={self._value_to_sql_value(v)}' for k, v in _dict.items()])}
                    WHERE id = {self._value_to_sql_value(_id)}"""
        logging.debug(sql)

        return libsql_client.Statement(sql=sql)

    def _ids_to_delete_statement(
        self,
        table_name: str,
        ids: List[str],
    ) -> libsql_client.Statement:
        sql = f"""DELETE 
                    FROM {table_name}
                    WHERE id IN ({','.join([self._value_to_sql_value(id) for id in ids])})"""
        logging.debug(sql)

        return libsql_client.Statement(sql=sql)

    def _ids_to_get_statement(
        self,
        table_name: str,
        ids: List[str],
    ) -> libsql_client.Statement:
        sql = f"""SELECT * 
                    FROM {table_name} 
                    WHERE id IN ({','.join([self._value_to_sql_value(id) for id in ids])})"""
        logging.debug(sql)
        return libsql_client.Statement(sql=sql)

    def _value_to_sql_value(
        self,
        value: any,
    ) -> str:
        if value is None:
            return f"NULL"
        elif isinstance(value, str):
            return f"'{value}'"
        elif isinstance(value, int):
            return f"{value}"
        elif isinstance(value, datetime):
            return f"'{value.strftime('%Y-%m-%d %H:%M:%S')}'"
        elif isinstance(value, bool):
            return f"{value}"
        elif isinstance(value, float):
            return f"{value}"
        elif isinstance(value, List) and all(isinstance(e, str) for e in value):
            return f"'{','.join([str(v) for v in value])}'"
        elif isinstance(value, List) and all(isinstance(e, int) for e in value):
            return f"'{','.join([str(v) for v in value])}'"
        # elif isinstance(value, None):
        #     return f"NULL"
        else:
            raise Exception(f"Unknown type: {type(value)}")
