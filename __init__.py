# The MIT License (MIT)
# Copyright (c) 2023 Edgaras Janušauskas and Inovatorius MB (www.fildz.com)

################################################################################
# FILDZ CYBEROS BUTTON LIBRARY
#
# Fully asynchronous button library for CYBEROS.
#
# Features:
# - Completely asynchronous.
# - Supports down, hold, up, click and, double-click events.
# - Adjustable debounce and double-click ms.
# - Supports user-defined coroutines.

import fildz_cyberos as cyberos
import uasyncio as asyncio
from uasyncio import Event


class Button:
    def __init__(self, pin):
        self._button = pin
        self._state = self._button.value()
        self._debounce_ms = 50
        self._double_click_ms = 350
        self._sync = True
        self._on_down = Event()
        self._down = None
        asyncio.create_task(self._event_down())
        self._on_hold = Event()
        self._hold = None
        asyncio.create_task(self._event_hold())
        self._on_up = Event()
        self._up = None
        asyncio.create_task(self._event_up())
        self._on_click = Event()
        self._click = None
        asyncio.create_task(self._event_click())
        self._on_double_click = Event()
        self._double_click = None
        asyncio.create_task(self._event_double_click())

    ################################################################################
    # Properties
    #
    @property
    def debounce_ms(self):
        return self._debounce_ms

    @debounce_ms.setter
    def debounce_ms(self, value):
        self._debounce_ms = value

    @property
    def double_click_ms(self):
        return self._double_click_ms

    @double_click_ms.setter
    def double_click_ms(self, value):
        self.double_click_ms = value

    @property
    def sync(self):
        return self._sync

    @sync.setter
    def sync(self, value):
        self._sync = value

    ################################################################################
    # Events
    #
    @property
    def on_down(self):
        return self._on_down

    @on_down.setter
    def on_down(self, value):
        self._down = value
        asyncio.create_task(self.down())

    @property
    def on_hold(self):
        return self._on_hold

    @on_hold.setter
    def on_hold(self, value):
        self._hold = value
        asyncio.create_task(self.hold())

    @property
    def on_up(self):
        return self._on_up

    @on_up.setter
    def on_up(self, value):
        self._up = value
        asyncio.create_task(self.up())

    @property
    def on_click(self):
        return self._on_click

    @on_click.setter
    def on_click(self, value):
        self._click = value
        asyncio.create_task(self.click())

    @property
    def on_double_click(self):
        return self._on_double_click

    @on_double_click.setter
    def on_double_click(self, value):
        self._double_click = value
        asyncio.create_task(self.double_click())

    ################################################################################
    # Tasks
    #
    async def _event_down(self):
        while True:
            if self._state:
                self._on_down.set()
                self._on_down.clear()
                # print('DOWN')
                await self._on_up.wait()
            await asyncio.sleep_ms(self._debounce_ms)
            self._state = self._button.value()

    async def _event_hold(self):
        while True:
            await self._on_down.wait()
            self._on_hold.set()
            while self._state:
                # print('HOLD')
                await asyncio.sleep_ms(self._debounce_ms)
                self._state = self._button.value()
            self._on_hold.clear()
            self._on_up.set()

    async def _event_up(self):
        while True:
            await self._on_up.wait()
            self._on_up.clear()
            # print('UP')

    async def _event_click(self):
        while True:
            await self._on_up.wait()
            self._on_click.set()
            self._on_click.clear()
            # print('CLICK')

    async def _event_double_click(self):
        while True:
            await self._on_click.wait()
            try:
                await asyncio.wait_for_ms(self._on_click.wait(), self._double_click_ms)
                self._on_double_click.set()
                self._on_double_click.clear()
                # print('DOUBLE CLICK')
            except asyncio.TimeoutError:
                pass

    async def down(self, cyberware=''):
        while True:
            await self._on_down.wait()
            if self._down is None:
                await cyberos.event.send('on_down', cyberware=cyberware, sync=self._sync)
            else:
                await self._down()

    async def hold(self, cyberware=''):
        while True:
            await self._on_hold.wait()
            if self._hold is None:
                await cyberos.event.send('on_hold', cyberware=cyberware, sync=self._sync)
            else:
                await self._hold()

    async def up(self, cyberware=''):
        while True:
            await self._on_up.wait()
            if self._up is None:
                await cyberos.event.send('on_up', cyberware=cyberware, sync=self._sync)
            else:
                await self._up()

    async def click(self, cyberware=''):
        while True:
            await self._on_click.wait()
            if self._click is None:
                await cyberos.event.send('on_click', cyberware=cyberware, sync=self._sync)
            else:
                await self._click()

    async def double_click(self, cyberware=''):
        while True:
            await self._on_double_click.wait()
            if self._double_click is None:
                await cyberos.event.send('on_double_click', cyberware=cyberware, sync=self._sync)
            else:
                await self._double_click()
