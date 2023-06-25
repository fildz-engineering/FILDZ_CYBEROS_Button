# The MIT License (MIT)
# Copyright (c) 2023 Edgaras Janušauskas and Inovatorius MB (www.fildz.com)

################################################################################
# FILDZ CYBEROS BUTTON LIBRARY
#
# Fully asynchronous button library for CYBEROS.
#
# Features:
# - Completely asynchronous.
# - Supports down, hold, up, click and double click events.
# - Adjustable debounce and double click ms.

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
        asyncio.create_task(self._event_down())
        self._on_hold = Event()
        asyncio.create_task(self._event_hold())
        self._on_up = Event()
        asyncio.create_task(self._event_up())
        self._on_click = Event()
        asyncio.create_task(self._event_click())
        self._on_double_click = Event()
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

    @property
    def on_hold(self):
        return self._on_hold

    @property
    def on_up(self):
        return self._on_up

    @property
    def on_click(self):
        return self._on_click

    @property
    def on_double_click(self):
        return self._on_double_click

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
            await cyberos.event.send('on_down', cyberware=cyberware, sync=self._sync)

    async def hold(self, cyberware=''):
        while True:
            await self._on_hold.wait()
            await cyberos.event.send('on_hold', cyberware=cyberware, sync=self._sync)

    async def up(self, cyberware=''):
        while True:
            await self._on_up.wait()
            await cyberos.event.send('on_up', cyberware=cyberware, sync=self._sync)

    async def click(self, cyberware=''):
        while True:
            await self._on_click.wait()
            await cyberos.event.send('on_click', cyberware=cyberware, sync=self._sync)

    async def double_click(self, cyberware=''):
        while True:
            await self._on_double_click.wait()
            await cyberos.event.send('on_double_click', cyberware=cyberware, sync=self._sync)
