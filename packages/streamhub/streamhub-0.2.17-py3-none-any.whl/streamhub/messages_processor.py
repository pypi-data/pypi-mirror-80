import json
import singer
from jsonschema.validators import Draft4Validator
from jsonschema.exceptions import ValidationError
from simplejson.scanner import JSONDecodeError

LOGGER = singer.get_logger()


def process(messages, config, recordHandlerFunc, stateHandlerFunc, schemaHandlerFunc, onCompleteHandler, onMetadataHandler, exceptionHandlerFunc):

    state = None
    schemas = {}
    key_properties = {}
    validators = {}

    try:
        for message in messages:
            try:
                # o = singer.parse_message(message).asdict()
                """
                singer.parse_message is doing more that just loading the Json message asdict
                Since we added a new (non-singer) METADATA message, we need to be able to load any message types
                """
                o = json.loads(message)
            except json.decoder.JSONDecodeError:
                LOGGER.error("Unable to parse:\n{}".format(message))
                raise

            message_type = o['type']

            if message_type == 'RECORD':  # RECORD message
                if o['stream'] not in schemas:
                    raise Exception("A record for stream {}"
                                    "was encountered before a corresponding schema".format(o['stream']))

                try:
                    validators[o['stream']].validate(o['record'])
                except ValidationError:
                    LOGGER.error("Unable to validate:\n{}".format(message))
                    raise Exception(ValidationError.message)

                record = o['record']
                recordHandlerFunc(record, config)  # triggers callback in client app

            elif message_type == 'METADATA':  # METADATA message

                metadata = o['metadata']
                LOGGER.debug('Received metadata: {}'.format(metadata))
                onMetadataHandler(metadata, config)

            elif message_type == 'STATE':  # STATE message
                LOGGER.debug('Setting state to {}'.format(o['value']))
                state = o['value']
                stateHandlerFunc(state, config)  # triggers callback in client app

            elif message_type == 'SCHEMA':  # SCHEMA message
                stream = o['stream']
                schemas[stream] = o['schema']
                validators[stream] = Draft4Validator(o['schema'])
                key_properties[stream] = o['key_properties']
                schemaHandlerFunc(stream, schemas, validators, key_properties,
                                  config)  # triggers callback in client app

            else:
                LOGGER.warning("Unknown message type {} in message {}"
                               .format(o['type'], o))

        onCompleteHandler(config)  # triggers callback in client app

    except Exception as e:
        exceptionHandlerFunc(e, config)
