

class MetadataMessage:
    '''Metadata message.
    The METADATA message has these fields:
      * stream (string) - The name of the stream the metadata record belongs to.
      * metadata (dict) - The raw data for the message
    msg = MetadataMessage(
        stream='gam-export',
        metadata={'name': E2E Test GAM Automation', ...})
    '''

    def __init__(self, stream, metadata, time_extracted=None):
        self.stream = stream
        self.metadata = metadata
        self.time_extracted = time_extracted
        if time_extracted and not time_extracted.tzinfo:
            raise ValueError("'time_extracted' must be either None " +
                             "or an aware datetime (with a time zone)")

    def asdict(self):
        result = {
            'type': 'METADATA',
            'stream': self.stream,
            'metadata': self.metadata,
        }
        if self.time_extracted:
            as_utc = self.time_extracted.astimezone(pytz.utc)
            result['time_extracted'] = u.strftime(as_utc)
        return result

    def __str__(self):
        return str(self.asdict())
