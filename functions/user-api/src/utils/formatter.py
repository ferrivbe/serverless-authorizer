from pythonjsonlogger import jsonlogger


class LoggerJSONFormatter(jsonlogger.JsonFormatter):
    """
    Custom JSON log formatter for logging module.
    """

    def process_log_record(self, log_record):
        """
        Process a log record and return a formatted JSON log record.

        :param log_record: The log record to process.
        :type log_record: dict
        :return: The formatted JSON log record.
        :rtype: dict
        """
        log_record = super(LoggerJSONFormatter, self).process_log_record(log_record)
        log_record = {
            key: self._extract_value(value)
            for key, value in log_record.items()
            if value is not None
        }
        return log_record

    def _extract_value(self, value):
        """
        Extract a value from a log record and return it.

        :param value: The value to extract.
        :type value: Any
        :return: The extracted value.
        :rtype: Any
        """
        if isinstance(value, dict):
            return {
                key: self._extract_value(val)
                for key, val in value.items()
                if val is not None
            }
        else:
            return value
