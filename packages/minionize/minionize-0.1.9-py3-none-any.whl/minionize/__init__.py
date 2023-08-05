from abc import ABC, abstractmethod
import logging
import os
from pathlib import Path
import traceback

from dotenv import load_dotenv

from .env import ENGINE_EXECO, ENGINE_GOOGLE, ENV_DRY_MODE, ENV_ENGINE, ENGINE_PULSAR
from .types import Param

# first thing first ... load dotenv file if any in the cwd
load_dotenv(dotenv_path=Path.cwd() / ".env")

LOGGER = logging.getLogger(__name__)


class Engine(ABC):
    """Base class for our Engines.

    An engine is responsible for getting data(param) from a queue.
    It acknowleges (positively or negatively) the data back to the queue.
    The exact semantic of ack/nack is still under intense discussion. Please
    refer to the concrete implementation for further information.
    """

    @abstractmethod
    def next(self) -> Param:
        pass

    @abstractmethod
    def ack(self, param: Param):
        pass

    @abstractmethod
    def nack(self, param: Param):
        pass


class Callback(ABC):
    """Base class for the (user defined) callbacks.

    A Callback modelizes the behaviour of the application inputs/outputs.
    """

    @abstractmethod
    def setup(self, param: Param, engine: Engine):
        """Called right after a new param is fetched from the queue."""
        pass

    @abstractmethod
    def process(self, param: Param, engine: Engine):
        """This is where process will happen."""
        pass

    @abstractmethod
    def teardown(self, param: Param, engine: Engine, exception: Exception):
        """Called at the before a new iteration."""
        pass

    def dry_mode(self):
        return os.getenv(ENV_DRY_MODE) is not None


class PrintCallback(Callback):
    """Dummy callback for debug purpose.

    Acknowledges right after printing. It never uses nack.
    """

    def setup(self, param, engine):
        print(f"setup {param}")

    def process(self, param, engine):
        print(f"process {param}")
        engine.done(param)

    def teardown(self, param, engine, exception):
        print(f"finished {param}")


class ProcessCallback(Callback):
    """A callback that spawn a process upon reception.

    It's designed to be a good enough callback for most use cases. User must
    subclass it and define how the actual shell command is built from the
    incoming param.
    - Acknowlege if the sub process return code is 0
    - Nack otherwise
    """

    def to_cmd(self, param: Param):
        return f"echo {param}"

    def setup(self, param, engine):
        return super().setup(param, engine)

    def process(self, param: Param, engine: Engine):
        import subprocess

        if self.dry_mode():
            print(f"[dry mode] {self.to_cmd(param)}")
        else:
            try:
                subprocess.run(self.to_cmd(param), shell=True, check=True)
            except Exception as e:
                raise e

    def teardown(self, param, engine, exception):
        if exception is None:
            # everything is alright
            self.teardown_ok(param, engine)
            # we ack when ok hook has been successfully ran
            engine.ack(param)
            return
        try:
            raise exception
        except KeyboardInterrupt:
            engine.nack(param)
            raise exception
        except Exception:
            pass
        finally:
            engine.nack(param)
            self.teardown_ko(param, engine, exception)

    def teardown_ok(self, param, engine):
        pass

    def teardown_ko(self, param, engine, exception):
        pass


class EntryPoint:
    """This is the framework.

    It's mainly a loop that continuously fetch the next param and call the
    callback methods.
    """

    def __init__(self, callback: Callback, engine: Engine):
        self.cb = callback
        self.engine = engine

    def run(self):
        """Routine."""
        while True:
            LOGGER.debug("get next param")
            param = self.engine.next()
            exception = None
            if param is None:
                LOGGER.debug("No more params to handle, leaving")
                break
            try:
                # The user may want the setup to fail
                # so we let the teardown decides what
                # to do in this case
                LOGGER.debug(param)
                self.cb.setup(param, self.engine)
                self.cb.process(param, self.engine)
            except Exception as e:
                exception = e
                LOGGER.error(
                    "--> exception raised during execution" "(printing stack trace)"
                )
                LOGGER.error(traceback.format_exc())
            self.cb.teardown(param, self.engine, exception)


def minionizer(callback: Callback):
    """Take a user callback and minionize it !"""
    # NOTE(msimonin): use dotenv
    ep = os.getenv(ENV_ENGINE)
    if ep == ENGINE_EXECO:
        from minionize.execo import Execo

        engine = Execo.from_env()
    elif ep == ENGINE_GOOGLE:
        from minionize.google import GooglePubSub

        engine = GooglePubSub.from_env()
    elif ep == ENGINE_PULSAR:
        from minionize.pulsar import PulsarPubSub

        engine = PulsarPubSub.from_env()
    else:
        raise Exception(f"EntryPoint {ep} not supported")
    return EntryPoint(callback, engine)
