import logging
from logging import Handler, StreamHandler, Filter
from azure.eventhub import EventHubProducerClient, EventData

_logger = logging.getLogger(__name__)


class EventHubFilter(Filter):
    """
    EventHubFilter implements Filter to avoid deadlock when EventHubHandler is called
    as logging handler.
    """
    def __init__(self):
        super().__init__(name='uamqp')

    def filter(self, record):
        if self.name in record.name:
            return False
        else:
            return True


class EventHubHandler(StreamHandler):

    def __init__(self, endpoint, access_keyname, access_key, entity_path, **kwargs):
        """
        """
        StreamHandler.__init__(self)

        self.connection_str = "Endpoint=sb://{}/;SharedAccessKeyName={};SharedAccessKey={};EntityPath={}".format(
            endpoint,
            access_keyname,
            access_key,
            entity_path)
        self.kwargs = kwargs

        # EventHub Producer
        self.producer = EventHubProducerClient.from_connection_string(self.connection_str, **self.kwargs)

        self.event_batch_data = None
        self._create_batch_data()

        self.filters = [
            EventHubFilter()
        ]

    def flush(self):
        if self.event_batch_data:
            self.producer.send_batch(self.event_batch_data)
            self.event_batch_data = None

    def should_flush(self, record):
        event_data = EventData(record.msg)
        event_data_size = event_data.message.get_message_encoded_size()
        size_after_add = (
                self.event_batch_data.size_in_bytes
                + event_data_size
        )
        return size_after_add > self.event_batch_data.max_size_in_bytes

    def emit(self, record):
        # """
        # Emit a record.
        #
        # Send the record to the Web server as a percent-encoded dictionary
        # """
        if not self.event_batch_data:
            self._create_batch_data()

        if self.should_flush(record):
            self.flush()
            self._create_batch_data()
        else:
            try:
                self.event_batch_data.add(EventData(record.msg))
            except ValueError:
                logging.error("Message size too big to send to EventHub")

    def close(self):
        self.acquire()
        try:
            try:
                if self.producer:
                    try:
                        self.flush()
                    finally:
                        self.event_batch_data = None
                        self.producer.close()

            finally:
                StreamHandler.close(self)
        finally:
            self.release()

    def _create_batch_data(self):
        self.event_batch_data = self.producer.create_batch(
            **self.kwargs
        )
