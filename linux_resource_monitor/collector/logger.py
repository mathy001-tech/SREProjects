# ========================
# collector/logger.py
# ========================
import logging
import json

def setup_logger():
    logger = logging.getLogger("monitor")
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()

    def json_formatter(record):
        log_record = {
            'level': record.levelname,
            'time': logger.handlers[0].formatter.formatTime(record),
            'message': record.getMessage(),
        }
        return json.dumps(log_record)

    class CustomFormatter(logging.Formatter):
        def format(self, record):
            return json_formatter(record)

    handler.setFormatter(CustomFormatter())
    logger.addHandler(handler)
    return logger