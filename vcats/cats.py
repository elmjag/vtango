#!/usr/bin/env python
import time
from json import loads
from sys import stdin
from threading import Thread
from PyTango import ConnectionFailed
from tango.server import Device, attribute
from tango import Database, DbDevInfo, AttrDataFormat, CmdArgType

TANGO_CONNECT_RETRY_TIME = 2.1
DEVICE_NAME = "b311a-e/ctl/cats-01"


def _connect_to_db():
    db = None
    while db is None:
        try:
            db = Database()
        except ConnectionFailed:
            print(
                f"failed to connect to tango host, retrying in {TANGO_CONNECT_RETRY_TIME} seconds"
            )
            time.sleep(TANGO_CONNECT_RETRY_TIME)

    return db


def register_device():
    db = _connect_to_db()

    db_info = DbDevInfo()
    db_info._class = "CATS"
    db_info.server = "CATS/1"
    db_info.name = DEVICE_NAME

    db.add_device(db_info)


def _no_cassettes_preset():
    return [0] * 29


class CATS(Device):
    CAS_ATTR_NAME = "CassettePresence"
    _Cassettes = _no_cassettes_preset()

    def init_device(self):
        super().init_device()
        Thread(target=self.update_cassettes).start()

    def update_cassettes(self):
        attrs = self.get_device_attr()
        cas_attr = attrs.get_attr_by_name(self.CAS_ATTR_NAME)
        cas_attr.set_change_event(True)

        while True:
            json_text = stdin.readline()
            if json_text == "":
                # stdin have been closed, we are done
                return

            present_positions = loads(json_text)

            self._Cassettes = _no_cassettes_preset()
            for pos in present_positions:
                self._Cassettes[pos - 1] = 1

            self.push_change_event(self.CAS_ATTR_NAME, self._Cassettes)

    @attribute(
        dformat=AttrDataFormat.SPECTRUM,
        max_dim_x=len(_Cassettes),
        dtype=CmdArgType.DevShort,
        abs_change=1,
    )
    def CassettePresence(self):
        return self._Cassettes


register_device()
CATS.run_server()
