python-logstash-tradingstrategy
===============================

Python logging handler for `Logstash <git@github.com:tradingstrategy-ai/python-logstash.git>`_.

**Note**: This is a forked from the original `python-logstash project <git@github.com:vklochan/python-logstash.git>`_
for `Trading Strategy <https://tradingstrategy.ai>`_. It has been updated and modified with
some patches for advanced functionality.

Changelog
=========

0.5.1:
  - Bette exception message if LogStash formatter has problems to make the message out as JSON,
    to give a clue what could be wrong
0.5.0:
  - Forked to have a new release
  - Added ``extra_fields`` parameter to handler
0.4.7
  - Add couple of sensitive fields to the skip_list
0.4.6
  - Updated field names to match java counterparts supported by logstash crew
0.4.5
  - Allow passing exchange's routing key to AMQP handler
0.4.4
  - Fixed urllib import python3 compatibility.
  - Added long type to easy_types.
0.4.3
  - Added AMQP handler.
0.4.2
  - Updated README
  - Added ``tags`` parameter to handler
0.4.1
  - Added TCP handler.
0.3.1
  - Added support for Python 3
0.2.2
  - Split Handler into Handler and Formatter classes
0.2.1
  - Added support for the new JSON schema in Logstash 1.2.x. See details in
    http://tobrunet.ch/2013/09/logstash-1-2-0-upgrade-notes-included/ and
    https://logstash.jira.com/browse/LOGSTASH-675

    - Added ``version`` parameter. Available values: 1 (Logstash 1.2.x version format), 0 - default (previous version).


Installation
============

Using pip::

  pip install python-logstash

Usage
=====

``LogstashHandler`` is a custom logging handler which sends Logstash messages using UDP.

For example::

  import logging
  import logstash
  import sys

  host = 'localhost'

  test_logger = logging.getLogger('python-logstash-logger')
  test_logger.setLevel(logging.INFO)
  test_logger.addHandler(logstash.LogstashHandler(host, 5959, version=1))
  # test_logger.addHandler(logstash.TCPLogstashHandler(host, 5959, version=1))

  test_logger.error('python-logstash: test logstash error message.')
  test_logger.info('python-logstash: test logstash info message.')
  test_logger.warning('python-logstash: test logstash warning message.')

  # add extra field to logstash message
  extra = {
      'test_string': 'python version: ' + repr(sys.version_info),
      'test_boolean': True,
      'test_dict': {'a': 1, 'b': 'c'},
      'test_float': 1.23,
      'test_integer': 123,
      'test_list': [1, 2, '3'],
  }
  test_logger.info('python-logstash: test extra fields', extra=extra)

When using ``extra`` field make sure you don't use reserved names. From `Python documentation <https://docs.python.org/2/library/logging.html>`_.
     | "The keys in the dictionary passed in extra should not clash with the keys used by the logging system. (See the `Formatter <https://docs.python.org/2/library/logging.html#logging.Formatter>`_ documentation for more information on which keys are used by the logging system.)"

To use the AMQPLogstashHandler you will need to install pika first.

   pip install pika

For example::

  import logging
  import logstash

  test_logger = logging.getLogger('python-logstash-logger')
  test_logger.setLevel(logging.INFO)
  test_logger.addHandler(logstash.AMQPLogstashHandler(host='localhost', version=1))

  test_logger.info('python-logstash: test logstash info message.')
  try:
      1/0
  except:
      test_logger.exception('python-logstash-logger: Exception with stack trace!')


You can also pass extra fields to the handler, so that those fields will appear in Logstash::

    # Pass `application` field and `tags` to Logstash
    # with every log message
    tags = ["python"]
    extra_fields = {"application": "my_application_name}
    handler = logstash.UDPLogstashHandler(
        logstash_server,
        5959,
        version=1,
        tags=tags,
        extra_fields==extra_fields,
        )


Using with Django
=================

Modify your ``settings.py`` to integrate ``python-logstash`` with Django's logging::

  LOGGING = {
    ...
    'handlers': {
        'logstash': {
            'level': 'DEBUG',
            'class': 'logstash.LogstashHandler',
            'host': 'localhost',
            'port': 5959, # Default value: 5959
            'version': 1, # Version of logstash event schema. Default value: 0 (for backward compatibility of the library)
            'message_type': 'logstash',  # 'type' field in logstash message. Default value: 'logstash'.
            'fqdn': False, # Fully qualified domain name. Default value: false.
            'tags': ['tag1', 'tag2'], # list of tags. Default: None.
            'extra_fields': {
                'server_name': 'myserver.local',
                'server_ip': '10.74.22.12',
            }, # dict of extra fields, always added to the log. Default: None.
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['logstash'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
    ...
  }

Example Logstash Configuration
==============================

Example Logstash Configuration (``logstash.conf``) for Receiving Events from python-logstash is::

  input {
    udp {
      port => 5959
      codec => json
    }
  }
  output {
    stdout {
      codec => rubydebug
    }
  }

For TCP input you need to change the logstash's input to ``tcp`` and modify django log handler's class to ``logstash.TCPLogstashHandler``

Release
=======

.. code-block:: shell

    python3 -m venv venv
    source venv/bin/activate
    pip install setuptools twine
    python setup.py sdist
    twine upload
    twine upload dist/*

