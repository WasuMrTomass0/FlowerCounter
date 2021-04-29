from WasuLib.settings import TRACE_INFO, TRACE_ERROR, TRACE_WARNING, TRACE_ALLOW, TRACE_LOG_PATH_FILE, TRACE_DEBUG


class Trace:
    _traces = list()
    _msg_limit = 10
    _file_path = 'LOG_FILE_TRACES.txt'
    TRACE_DEBUG = TRACE_DEBUG
    TRACE_INFO = TRACE_INFO
    TRACE_WARNING = TRACE_WARNING
    TRACE_ERROR = TRACE_ERROR

    def __init__(self, msg, trace_type: int, file: str, function: str):
        # Create text
        if trace_type == TRACE_DEBUG:
            symbol = '[D]'
            msg = f'{symbol} {msg}'
        elif trace_type == TRACE_INFO:
            symbol = '[I]'
            msg = f'{symbol} {msg}'
        elif trace_type == TRACE_WARNING:
            symbol = '[W]'
            msg = f'{symbol} [{file}] ({function})\n{msg}'
        elif trace_type == TRACE_ERROR:
            symbol = '[E]'
            msg = f'{symbol} [{file}] ({function})\n{msg}'
        else:
            symbol = '[?]'
            msg = f'{symbol} [{file}] ({function})\n{msg}'
        msg = msg.replace('\n', '\n    ')
        # Save to log
        Trace.add_trace(msg.replace('\r', ''))
        # Print
        if trace_type >= TRACE_ALLOW:
            print(msg)
        pass

    @staticmethod
    def setup(file_path: str):
        Trace._traces = list()
        Trace._msg_limit = 10
        Trace._file_path = file_path
        open(Trace._file_path, 'w').close()  # Create file
        pass  # def __init__

    @staticmethod
    def update_file():
        with open(Trace._file_path, 'a') as token:
            token.write('\n' + '\n'.join(Trace._traces))
        Trace._traces.clear()
        pass  # def update_file

    @staticmethod
    def add_trace(msg: str):
        Trace._traces.append(msg)
        if len(Trace._traces) >= Trace._msg_limit:
            Trace.update_file()
        pass  # def add_trace

    pass  # _Traces


Trace.setup(TRACE_LOG_PATH_FILE)
