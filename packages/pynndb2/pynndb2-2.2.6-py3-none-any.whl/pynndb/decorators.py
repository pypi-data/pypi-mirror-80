#####################################################################################
#
#  Copyright (c) 2020 - Mad Penguin Consulting Ltd
#
#####################################################################################
from typing import Any, Callable, Generator
from lmdb import MapResizedError, MapFullError, Transaction
import functools

SIZE_MULTIPLIER = 1.2   # how much to scale the map_size by
PAGE_SIZE = 4096        # page size to round to

try:
    from loguru import logger as log
except Exception:   # pragma: no cover
    pass            # pragma: no cover


class PyNNDBTransaction:

    def __init__(self, database, write):
        self._env = database.env
        self._flush = database.replication.flush
        self._write = write
        self.journal = []

    def __enter__(self):
        try:
            self.txn = Transaction(env=self._env, write=self._write)
            return self
        except MapResizedError as e:  # pragma: no cover
            if 'log' in globals():
                log.warning(f'database RESIZED')  # pragma: no cover
                # log.exception(e)

            self._env.set_mapsize(0)  # pragma: no cover
            self.txn = Transaction(env=self._env, write=self._write)  # pragma: no cover
            return self  # pragma: no cover

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            if self.journal:
                self._flush(self.journal, self.txn)
            else:
                self.txn.commit()
        else:
            self.txn.abort()


class ReadTransaction(PyNNDBTransaction):

    def __init__(self, database):
        super().__init__(database, False)


class WriteTransaction(PyNNDBTransaction):

    def __init__(self, database):
        super().__init__(database, True)


def transparent_resize(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapped(*args, **kwargs) -> Any:
        if kwargs.get('txn'):
            return func(*args, **kwargs)
        while True:
            try:
                with WriteTransaction(getattr(args[0], '_database', args[0])) as kwargs['txn']:
                    return func(*args, **kwargs)
            # except MapResizedError:
            #     database = getattr(args[0], '_database', args[0])  # pragma: no cover
            #     if not database.auto_resize:  # pragma: no cover
            #         raise  # pragma: no cover
            #     if 'log' in globals():  # pragma: no cover
            #         log.warning(f'database ({database.name}) resized')  # pragma: no cover
            #     try:  # pragma: no cover
            #         kwargs['txn'].txn.abort()  # pragma: no cover
            #     except Exception:  # pragma: no cover
            #         raise  # pragma: no cover
            #     database.env.set_mapsize(0)  # pragma: no cover
            #     mapsize = database.env.info()['map_size']  # pragma: no cover
            #     database._conf['map_size'] = mapsize  # pragma: no cover
            #     database.reopen()  # pragma: no cover
            except MapFullError:
                database = getattr(args[0], '_database', args[0])
                if not database.auto_resize:
                    raise  # pragma: no cover
                #
                #   Caveat central :: lots of dependencies here ...
                #
                mapsize = database.env.info()['map_size']
                extend_to = int(mapsize * SIZE_MULTIPLIER // PAGE_SIZE * PAGE_SIZE)
                #
                if 'log' in globals():
                    log.warning(f'database ({database.name}) extended from {mapsize} to {extend_to}')  # pragma: no cover
                #
                #   FIXME: should we raise if abort() fails?
                #
                try:
                    kwargs['txn'].txn.abort()
                except Exception:  # pragma: no cover
                    raise  # pragma: no cover
                database.env.set_mapsize(extend_to)
                database._conf['map_size'] = extend_to
                mapsize = database.env.info()['map_size']
                database.reopen()

    return wrapped


def wrap_reader_yield(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapped(*args, **kwargs) -> Generator[Any, None, None]:
        if kwargs.get('txn'):
            yield from func(*args, **kwargs)
        else:
            while True:
                try:
                    with args[0].env.begin() as kwargs['txn']:
                        yield from func(*args, **kwargs)
                        return
                except MapResizedError:
                    args[0].env.set_mapsize(0)                         # pragma: no cover
    return wrapped


def wrap_reader(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapped(*args, **kwargs) -> Any:
        if kwargs.get('txn'):
            return func(*args, **kwargs)
        else:
            while True:
                try:
                    with args[0].env.begin() as kwargs['txn']:
                        return func(*args, **kwargs)
                except MapResizedError:
                    args[0].env.set_mapsize(0)                         # pragma: no cover
    return wrapped
