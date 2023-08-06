from multiprocessing import cpu_count


class Configuration():
    def __init__(self):
        self.__print_progress_line = 100000
        self.__simulate = False
        self.__debug = False
        self.__batch_size = 1000
        self.__parallel_processes = cpu_count()
        self.__batch_logging_table = True


    @property
    def print_progress_line(self):
        """Print simpleETL progress for every n lines"""
        return self.__print_progress_line

    @print_progress_line.setter
    def print_progress_line(self, value):
        if value < 1:
            raise ValueError("Print progress line must be at least 1")
        self.__print_progress_line = value

    @property
    def batch_size(self):
        """Batch size of rows distributes to each worker"""
        return self.__batch_size

    @batch_size.setter
    def batch_size(self, value):
        if value < 1:
            raise ValueError("Batch size must be at least 1")
        self.__batch_size = value

    @property
    def simulate(self):
        """Enable simulation of simpleETL. Will not commit data to fact table but dimensions can be affected"""
        return self.__simulate

    @simulate.setter
    def simulate(self, value):
        if value not in (True, False):
            raise ValueError("CONFIG.simulate value must be True og False")
        self.__simulate = value

    @property
    def debug(self):
        """Enables debug print and will not drop temporary tables"""
        return self.__debug

    @debug.setter
    def debug(self, value):
        if value not in (True, False):
            raise ValueError("CONFIG.debug value must be True og False")
        self.__debug = value

    def parallel(self, value):
        raise ValueError("CONFIG.parallel is obsolete and should not be used anymore")

    @property
    def parallel_processes(self):
        """If running in parallel, determine how many parallel process workers to spawn. Defaults to cpu_count()"""
        return self.__parallel_processes

    @parallel_processes.setter
    def parallel_processes(self, value):
        if value < 1 or value > 100:
            raise ValueError("Number of parallel processes must be in range 1-100")
        self.__parallel_processes = value

    @property
    def batch_logging_table(self):
        """Determines if simpleetl will log each batch load to a simpleetl.batchload table in the database"""
        return self.__batch_logging_table

    @batch_logging_table.setter
    def batch_logging_table(self, value):
        if value not in (True, False):
            raise ValueError("CONFIG.batch_logging_table value must be True og False")
        print("setting batch lot table to " + str(value))
        self.__batch_logging_table = value
