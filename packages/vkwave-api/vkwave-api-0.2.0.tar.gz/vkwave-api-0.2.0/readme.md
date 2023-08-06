# VKWave-API

Accessing VK API for humans.

## Install

```sh
pip install vkwave-api
```

## Example
```python
from vkwave_api import API, run

async def main():
    api = API("MY TOKEN")
    vk = api.get_api()
    me = await vk.users.get()
    print(me)

run(main())
```
