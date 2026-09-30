from abc import ABC, abstractmethod

class DatabaseAdapter(ABC):
    def __init__(self):
        self._connection = None

    @abstractmethod
    def close(self) -> None:
        ...

    @abstractmethod
    def get_database_info(self) -> dict:
        ...

    @abstractmethod
    def get_tables(self) -> list:
        ...

    @abstractmethod
    def get_columns(self, schema, table) -> list:
        ...

    @abstractmethod
    def get_constraints(self, schema, table) -> list:
        ...

    @abstractmethod
    def get_indexes(self, schema, table) -> list:
        ...

    @abstractmethod
    def get_views(self) -> list:
        ...
