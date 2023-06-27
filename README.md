# FILDZ CYBEROS Button Library

Fully asynchronous button library for CYBEROS.

## Features

* Completely asynchronous.
* Supports down, hold, up, click, and double-click events.
* Adjustable debounce and double-click ms.
* Supports user-defined coroutines.

## Setup

1. Download and extract .zip file contents to "fildz_button" folder.
2. "fildz_button" folder should contain only `__init__.py` file.
3. Upload "fildz_button" folder to your MicroPython powered device.

## Usage

### Default:

```Python
from machine import Pin
import uasyncio as asyncio
import fildz_cyberos as cyberos
from fildz_button import Button


async def main():
    await cyberos.init()
    btn = Button(Pin(13, Pin.OUT))
    asyncio.create_task(btn.click())  # Send clicks to all paired cyberwares.
    # asyncio.create_task(btn.click(cyberware='DISPLAY-0F889A-ABW'))  # Send clicks to specific cyberware.
    await cyberos.run_forever()

asyncio.run(main())
```

### User Defined Coroutine + Property:

```Python
async def btn_clicked():
    print('Button clicked')

async def main():
    await cyberos.init()
    btn = Button(Pin(13, Pin.OUT))
    btn.on_click = btn_clicked
    await cyberos.run_forever()
    
asyncio.run(main())
```

### User Defined Coroutine + Task + Event:

```Python
btn = Button(Pin(13, Pin.OUT))

async def btn_clicked():
    while True:
        await btn.on_click.wait()
        print('Button clicked')

async def main():
    await cyberos.init()
    asyncio.create_task(btn_clicked())
    asyncio.create_task(btn.click())  # Send clicks to all paired cyberwares.
    await cyberos.run_forever()

asyncio.run(main())
```

## Documentation

The documentation for the FILDZ CYBEROS Button Library is currently a work in progress. It will be available soon to provide detailed explanations of the library's API, usage examples, and best practices.

## Contributing

FILDZ CYBEROS is an open-source project that thrives on community contributions. We welcome developers to contribute to the project by following the MIT license guidelines. Feel free to submit pull requests, report issues, or suggest enhancements to help us improve the project further.

## Acknowledgment 

We are immensely thankful to the [MicroPython](https://github.com/micropython/micropython) community for developing and maintaining this incredible open-source project. Their dedication and hard work have provided us with a powerful and versatile platform to build upon.
