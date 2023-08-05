# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['xraysink', 'xraysink.asgi']

package_data = \
{'': ['*']}

install_requires = \
['aws_xray_sdk>=2,<3', 'wrapt>=1.11,<2.0']

setup_kwargs = {
    'name': 'xraysink',
    'version': '1.2.0',
    'description': 'Instrument asyncio Python for distributed tracing with AWS X-Ray.',
    'long_description': '# xraysink (aka `xray-asyncio`)\nExtra AWS X-Ray instrumentation to use distributed tracing with asyncio Python\nlibraries that are not (yet) supported by the official\n[aws_xray_sdk](https://github.com/aws/aws-xray-sdk-python) library.\n\n\n## Integrations Supported\n* Generic ASGI-compatible tracing middleware for *any* ASGI-compliant web\n  framework. This has been tested with:\n  - [aiohttp server](https://docs.aiohttp.org/en/stable/)\n  - [FastAPI](https://fastapi.tiangolo.com/)\n* asyncio [Task\'s](https://docs.python.org/3/library/asyncio-task.html)\n* Background jobs/tasks\n\n## Installation\nxraysink is distributed as a standard python package through\n[pypi](https://pypi.org/), so you can install it with your favourite Python\npackage manager. For example:\n\n    pip install xraysink \n\n\n## How to use\n\n### FastAPI\nInstrument incoming requests in your FastAPI web server by adding the `xray_middleware`. For example:\n\n    # Basic asyncio X-Ray configuration\n    xray_recorder.configure(context=AsyncContext(), service="my-cute-little-service")\n    \n    # Create a FastAPI app with various middleware\n    app = FastAPI()\n    app.add_middleware(MyTracingDependentMiddleware)  # Any middleware that is added earlier will have the X-Ray tracing context available to it\n    app.add_middleware(BaseHTTPMiddleware, dispatch=xray_middleware)\n\n\n### Asyncio Tasks\nIf you start asyncio [Task\'s](https://docs.python.org/3/library/asyncio-task.html)\nfrom a standard request handler, then the AWS X-Ray SDK will not correctly\ninstrument any outgoing requests made inside those Tasks.\n\nUse the fixed `AsyncContext` from `xraysink` as a drop-in replacement, like so:\n\n    from xraysink.context import AsyncContext  # Use the AsyncContext from xraysink\n    from aws_xray_sdk.core import xray_recorder\n    \n    xray_recorder.configure(context=AsyncContext(use_task_factory=True))\n\n\n### Background Jobs/Tasks\nIf your process starts background tasks that make network calls (eg. to the\ndatabase or an API in another service), then each execution of one of those\ntasks should be treated as a new X-Ray trace. Indeed, if you don\'t do so then\nyou will likely get context_missing errors.\n\nAn async function that implements a background task can be easily instrumented\nusing the `@xray_task_async()` decorator, like so:\n\n    # Basic asyncio X-Ray configuration\n    xray_recorder.configure(context=AsyncContext(), service="my-cute-little-service")\n    \n    # Any call to this function will start a new X-Ray trace\n    @xray_task_async()\n    async def cleanup_stale_tokens():\n        await database.get_table("tokens").delete(age__gt=1)\n    \n    schedule_recurring_task(cleanup_stale_tokens)\n\n\n### Process-Level Configuration\nYou can link your X-Ray traces to your CloudWatch Logs log records, which\nenhances the integration with AWS CLoudWatch ServiceLens. Take the following\nsteps:\n\n1.  Put the X-Ray trace ID into every log message. There is no convention for\n    how to do this (it just has to appear verbatim in the log message\n    somewhere), but if you are using structured logging then the convention is\n    to use a field called `traceId`. Here\'s an example\n    \n        trace_id = xray_recorder.get_trace_entity().trace_id\n        logging.getLogger("example").info("Hello World!", extra={"traceId": trace_id})\n\n1.  Explicitly set the name of the CloudWatch Logs log group associated with\n    your process. There is no general way to detect the Log Group from inside\n    the process, hence it requires manual configuration.\n    \n        set_xray_log_group("/example/service-name")\n\nNote that this feature relies on undocumented functionality, and is\n[not yet](https://github.com/aws/aws-xray-sdk-python/issues/188)\nsupported by the official Python SDK.\n\n## Licence\nThis project uses the Apache 2.0 licence, to make it compatible with\n[aws_xray_sdk](https://github.com/aws/aws-xray-sdk-python), the\nprimary library for integrating with AWS X-Ray.\n',
    'author': 'Gary Donovan',
    'author_email': 'gazza@gazza.id.au',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/garyd203/xraysink',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
