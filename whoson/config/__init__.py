
#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from derpconf.config import Config  # NOQA

Config.define(
    'SENTINEL_HOSTS',
    os.environ.get('SENTINEL_HOSTS', '["127.0.0.1:57574", "127.0.0.1:57573"]'),
    'Redis sentinels',
    'Redis'
)

Config.define('REDIS_MASTER', os.environ.get('REDIS_MASTER', 'master'), 'Redis master', 'Redis')
