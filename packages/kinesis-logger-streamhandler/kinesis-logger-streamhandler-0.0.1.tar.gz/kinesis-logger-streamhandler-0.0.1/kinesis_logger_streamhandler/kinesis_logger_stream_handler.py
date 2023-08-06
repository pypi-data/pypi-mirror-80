import boto3
import logging
import datetime
import json
from datetime import datetime, timezone
from kinesis_logger_streamhandler.aws_session_management import AwsSessionManagement

logger = logging.getLogger(__name__)

class KinesisDataStreamHandler(logging.StreamHandler):
    def __init__(self, kinesis_stream_name, subsystem, component, action, project_name, env, version, aws_session_management:AwsSessionManagement):
        # By default, logging.StreamHandler uses sys.stderr if stream parameter is not specified
        logging.StreamHandler.__init__(self)
        self.__aws_session_management = aws_session_management
        self.__stream_buffer = []
        self.__kinesis_stream_name = kinesis_stream_name
        self.__project_name = project_name
        self.__env = env
        self.__version = version
        self.__action = action
        self.__subsystem = subsystem
        self.__component = component

    def format(self, record):
        data = {
                "src_timestamp": datetime.now(timezone.utc).isoformat(),
                "component": self.__component,
                "action": self.__action,
                "syslog_severity": record.levelname,
                "message": record.msg,
                "subsystem": self.__subsystem,
                "project": self.__project_name,
                "environment": self.__env,
                "version": self.__version,
            }
        return json.dumps(data)

    def emit(self, record):
        try:
            msg = self.format(record)
            if self.__kinesis_stream_name and self.__aws_session_management:
                self.__stream_buffer.append({
                    'Data': msg.encode(encoding="UTF-8", errors="strict"),
                    'PartitionKey': record.threadName
                })
            else:
                stream = self.stream
                stream.write(msg)
                stream.write(self.terminator)
            self.flush()
        except Exception as e:
            logger.error(f"Failed emitting record: {e}")
            self.handleError(record)

    def flush(self):
        self.acquire()
        try:
            if self.__kinesis_stream_name and self.__aws_session_management and self.__stream_buffer:
                kinesis_client = self.__aws_session_management.get_func_res()
                kinesis_client.put_records(StreamName=self.__kinesis_stream_name, Records=self.__stream_buffer)
                self.__stream_buffer.clear()
        except Exception as e:
            logger.error("An error occurred during flush operation.")
            logger.error(f"Exception: {e}")
            logger.error(f"Stream buffer: {self.__stream_buffer}")
            raise e
        finally:
            if self.stream and hasattr(self.stream, "flush"):
                self.stream.flush()
            self.release()
