# swtich-py

[![PyPI version](https://badge.fury.io/py/switcher.svg)](https://badge.fury.io/py/switcher)
[![Build Status:](https://github.com/Kareem-Emad/switch-py/workflows/build/badge.svg)](https://github.com/Kareem-Emad/switch-py/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

python version of switch sdk, allows to publish messages on any topic to trigger all configured
subscribers at switch service.

## Setup

To install the package

```shell
pip install switcher
```

## How To Use

first make sure you set up the env variable properlly for:

- `SWITCH_JWT_SECRET` the secret key used to sign tokens for switch service, should be same env as the service itself

- `SWITCH_BASE_URL` the base url of the hosted switch service

```python
from switcher import publisher
publisher.publish('hellow', 'me', {'body': {'hello': 'world'}})
```

params in order:

- `topic` the topic name you wish to trigger subscribers on
- `author` your service identifier string(anything you want)
- `options` a dict containing the data you wish to include in your request:

  - `body` body dict of your request if it's a post/patch/.. request
  - `headers` headers to be sent to the subscriber in the request headers
  - `query_params` a dict containing any query params you wish to add to the subscribers' url (`{param: value}` `=>` `https://google.com?param=value`)
  - `path_params` a dict containing any path variables you wish to subtitute if exits in any of the subscirbers url, example `{id: 1}` `https://googl.com/:id` will be transformed to `https://googl.com/1`
  - `http_method` string representing the http method you wish to use when triggering the subscribers for this topic
