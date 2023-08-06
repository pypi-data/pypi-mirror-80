# Streamhub Export Lib #

This is a library to facilitate the creation of Singer taps and targets for the Streamhub platform.

### How do deploy a new version ? ###

* update the version number in setup.py
* run ./deploy-qa.sh to deploy the version to the testPyPI network https://test.pypi.org/project/streamhub/
    * you will prompted for credentials: tony_streamhub / 82E45630-9C1E-4634-B3C2-8C9EBF0D1084 
* run ./deploy-prod.sh to deploy to the PyPI production network https://pypi.org/project/streamhub/
    * you will prompted for credentials: streamhub_engineering / 9A983842-2DC3-4078-9841-B88AD5581D9C

### Hot to use this library to create Singer targets ###

* Use the notifications package and the messages_processor package
* Reference the lib as you would for any other dependency

```python
install_requires=[
          ... 
          'streamhub==0.2.12'
      ]
```


* Snippet of code 

```python
def process_on_complete(config):
    """
    Will be triggered once messages_processor.process has processed all the messages.
    """
	
def process_record(record, config):
    """
    Will be triggered for each RECORD message in the messages loop.
    """
	
def process_state(state, config):
    """
    Will be triggered once the STATE message is processed by messages_processor.process
    A default logic is implemented in the streamhub lib. This callback is provided to allow additional logic.
    """
	
def process_schema(stream, schemas, validators, key_properties, config):
    """
    Will be triggered once the SCHEMA message is processed by messages_processor.process
    A default logic is implemented in the streamhub lib. This callback is provided to allow additional logic.
    """	
 
def process_exception(e, config):
    """
    Will be triggered if an expection occurs while processing messages in the message loop
    """
	
def main: 
	messages_processor.process(messages, config, process_record, process_state, process_schema, process_on_complete,
                               process_exception)
```

### How to use this library in Singer taps ? ###

* For taps, only the send_aws_email function will be useful.
* More features to come.