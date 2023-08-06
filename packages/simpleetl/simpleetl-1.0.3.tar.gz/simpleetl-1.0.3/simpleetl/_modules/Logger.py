import logging
import os
import queue
import time
from multiprocessing import Queue, Event, Process

from simpleetl._modules.PostgresLoggingHandler import pgLogHandler


class LOGCLASS:
    def __init__(self):

        self.__formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s'
                                             ' - %(message)s')

        self.__mainpid = os.getpid()
        self.__stdlog = None
        self.__errlog = None
        self.__log_console = None
        self.__pglogger = None

        self.__logqueue = Queue(5)
        self.__logqueue.cancel_join_thread()  # Makes sure queue does not make main thread hang if main thread dies
        self.__running = Event()

        self.__log_lines = 0
        self.__log_mapper = {"debug": self.__debug,
                             "info": self.__info,
                             "warning": self.__warning,
                             "error": self.__error}
        # self.__logthread = threading.Thread(target=self.__logworker)
        self.__log_batchkey = -1
        self.__logthread = None

        self.__start_stdlog()

    def start_parallel(self):
        self.__logthread = Process(target=self.__logworker)
        self.__running.set()

        self.__logthread.start()

    def __logworker(self):
        from simpleetl._processing.ETLProcess import ETLProcess

        while True:
            try:
                os.kill(self.__mainpid, 0)  # Test if main process is alive. Throws PermissionError if not
                data = self.__logqueue.get(timeout=3)
            except queue.Empty:
                continue
            except EOFError:
                break
            except KeyboardInterrupt:
                break
            except BrokenPipeError:
                break
            except PermissionError:
                break
            if data == "STOP":
                break
            self.__log_lines += 1
            msgtype, msg = data
            self.__log_mapper[msgtype](msg)

            if self.__log_lines > 1000:
                self.__log_mapper["error"]("Error, more than 1000 lines logged. Something is terribly wrong!")
                ETLProcess.set_shutdown()
                break

        self.__running.clear()
        for handler in self.__stdlog.handlers:
            handler.flush()

    def set_batchkey(self, batchkey):
        self.__log_batchkey = batchkey

    def stop_parallel(self):
        self.__logqueue.put("STOP")
        while self.__running.is_set():
            time.sleep(0.1)

    def connect_batchlog(self, batchkey):
        if self.__pglogger:
            self.__pglogger.connect_batch(batchkey)

    def set_name(self, name):
        """

        :param name: Define name of logging instance

        """
        self.__stdlog.name = name

    # def set_debug(self):
    #    self.__log_console.setLevel(logging.DEBUG)

    def log_file(self, logpath, filename):
        # full_path = self.__logpath + "/logs/" + time.strftime("%Y_%m/%d/")
        os.makedirs(logpath, exist_ok=True)

        log_path = (logpath + "/" + filename)
        __log_file = logging.FileHandler(log_path)

        __log_file.setFormatter(self.__formatter)
        __log_file.setLevel(logging.DEBUG)
        self.__stdlog.addHandler(__log_file)

    def log_db(self, db_host, db_name, db_user, db_pass, db_port):
        self.__pglogger = pgLogHandler(self.__log_batchkey, db_host, db_name, db_user, db_pass, db_port)
        self.__stdlog.addHandler(self.__pglogger)

    def __start_stdlog(self):

        self.__stdlog = logging.getLogger("SimpleETL")
        self.__stdlog.setLevel(logging.DEBUG)

        self.__log_console = logging.StreamHandler()
        self.__log_console.setFormatter(self.__formatter)
        self.__log_console.setLevel(logging.DEBUG)
        self.__stdlog.addHandler(self.__log_console)

    def __start_errlog(self):
        logpath = self.__logpath + "/errlogs/" + time.strftime("%Y_%m/%d/")

        os.makedirs(logpath, exist_ok=True)
        log_path = (logpath + time.strftime('/%H_%M_%S_') + self.__logname + ".log")

        self.__errlog = logging.getLogger("BI ETL ERRORS")
        self.__errlog.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s'
                                      ' - %(message)s')

        __log_file = logging.FileHandler(log_path)
        __log_file.setFormatter(formatter)
        __log_file.setLevel(logging.DEBUG)
        self.__errlog.addHandler(__log_file)

    def __debug(self, message):
        self.__stdlog.debug(message)

    def __info(self, message):
        self.__stdlog.info(message)

    def __warning(self, message):
        self.__stdlog.warning(message)

    def __error(self, message):
        self.__stdlog.error(message)


    def __handle_log(self, message):
        if self.__running.is_set():
            self.__logqueue.put(message)
        else:
            msgtype, msg = message
            self.__log_mapper[msgtype](msg)

    def debug(self, message):
        self.__handle_log(("debug", message))

    def info(self, message):
        self.__handle_log(("info", message))

    def warning(self, message):
        self.__handle_log(("warning", message))

    def error(self, message, tbstr=None):
        self.__handle_log(("error", message))
        if tbstr:
            self.__handle_log(("error", "Stack trace:\n" + tbstr))
