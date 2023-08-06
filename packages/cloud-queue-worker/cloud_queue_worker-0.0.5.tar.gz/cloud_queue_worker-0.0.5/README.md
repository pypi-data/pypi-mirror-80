# CloudQueueWorker - Python worker for cloud provider's queues

CloudQueueWorker is a worker to consume messages from any cloud provider queue with multiple processes. 

**WARNING: Currently, only Amazon SQS are supported. Moreover, we're still in a early stage development, more features are coming...**.


## Why?

The main library used to manage asynchronous tasks in python is Celery. Celery has its own internal message pattern that must be respected for celery to be able to interpret the messages correctly. In our architecture, we use microservices with multiple language where their task client does not follow Celery's message principle. 

The scope of this library is to make an simple library to manage every kind of message from cloud provider queue systems.

## Installation

CloudQueueWorker is available from [PyPI](https://pypi.python.org/). You can install it with pip.
```
$ pip install cloud_queue_worker
```

## Usage

Instanciate a `CloudQueueWorker` object with the appropriate configuration to your needs and run it. E.g:
```python
    cloud_queue_worker = CloudQueueWorker(
        queue_mapping={'my_queue_url': 'function_path_related_to_the_queue_to_execute'},
        concurrency=5,
        cloud_provider_config={
	  "cloud_provider": "aws",
	  "region_name": "us-west-1"
	},
    )
    cloud_queue_worker.run()
```
