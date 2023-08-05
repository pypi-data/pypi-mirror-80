# coding=utf-8
from fysom import Fysom
from ..common.publish import Publish

import machinetalk.protobuf.types_pb2 as pb
from machinetalk.protobuf.message_pb2 import Container


class ErrorServiceBase(object):
    def __init__(self, debuglevel=0, debugname='Error Service Base'):
        self.debuglevel = debuglevel
        self.debugname = debugname
        self._error_string = ''
        self.on_error_string_changed = []

        # Error
        self._error_channel = Publish(debuglevel=debuglevel)
        self._error_channel.debugname = '%s - %s' % (self.debugname, 'error')
        # more efficient to reuse protobuf messages
        self._error_tx = Container()

        # callbacks
        self.on_state_changed = []

        # fsm
        self._fsm = Fysom(
            {
                'initial': 'down',
                'events': [
                    {'name': 'connect', 'src': 'down', 'dst': 'up'},
                    {'name': 'disconnect', 'src': 'up', 'dst': 'down'},
                ],
            }
        )

        self._fsm.ondown = self._on_fsm_down
        self._fsm.onafterconnect = self._on_fsm_connect
        self._fsm.onup = self._on_fsm_up
        self._fsm.onafterdisconnect = self._on_fsm_disconnect

    def _on_fsm_down(self, _):
        if self.debuglevel > 0:
            print('[%s]: state DOWN' % self.debugname)
        for cb in self.on_state_changed:
            cb('down')
        return True

    def _on_fsm_connect(self, _):
        if self.debuglevel > 0:
            print('[%s]: event CONNECT' % self.debugname)
        self.start_error_channel()
        return True

    def _on_fsm_up(self, _):
        if self.debuglevel > 0:
            print('[%s]: state UP' % self.debugname)
        for cb in self.on_state_changed:
            cb('up')
        return True

    def _on_fsm_disconnect(self, _):
        if self.debuglevel > 0:
            print('[%s]: event DISCONNECT' % self.debugname)
        self.stop_error_channel()
        return True

    @property
    def error_string(self):
        return self._error_string

    @error_string.setter
    def error_string(self, string):
        if self._error_string is string:
            return
        self._error_string = string
        for cb in self.on_error_string_changed:
            cb(string)

    @property
    def error_uri(self):
        return self._error_channel.socket_uri

    @error_uri.setter
    def error_uri(self, value):
        self._error_channel.socket_uri = value

    @property
    def error_port(self):
        return self._error_channel.socket_port

    @property
    def error_dsn(self):
        return self._error_channel.socket_dsn

    def start(self):
        if self._fsm.isstate('down'):
            self._fsm.connect()

    def stop(self):
        if self._fsm.isstate('up'):
            self._fsm.disconnect()

    def add_error_topic(self, name):
        self._error_channel.add_socket_topic(name)

    def remove_error_topic(self, name):
        self._error_channel.remove_socket_topic(name)

    def clear_error_topics(self):
        self._error_channel.clear_socket_topics()

    def start_error_channel(self):
        self._error_channel.start()

    def stop_error_channel(self):
        self._error_channel.stop()

    def send_error_message(self, identity, msg_type, tx):
        self._error_channel.send_socket_message(identity.encode(), msg_type, tx)

    def send_emc_nml_error(self, identity, tx):
        ids = [identity.encode()]
        for receiver in ids:
            self.send_error_message(receiver, pb.MT_EMC_NML_ERROR, tx)

    def send_emc_nml_text(self, identity, tx):
        ids = [identity.encode()]
        for receiver in ids:
            self.send_error_message(receiver, pb.MT_EMC_NML_TEXT, tx)

    def send_emc_nml_display(self, identity, tx):
        ids = [identity.encode()]
        for receiver in ids:
            self.send_error_message(receiver, pb.MT_EMC_NML_DISPLAY, tx)

    def send_emc_operator_text(self, identity, tx):
        ids = [identity.encode()]
        for receiver in ids:
            self.send_error_message(receiver, pb.MT_EMC_OPERATOR_TEXT, tx)

    def send_emc_operator_error(self, identity, tx):
        ids = [identity.encode()]
        for receiver in ids:
            self.send_error_message(receiver, pb.MT_EMC_OPERATOR_ERROR, tx)

    def send_emc_operator_display(self, identity, tx):
        ids = [identity.encode()]
        for receiver in ids:
            self.send_error_message(receiver, pb.MT_EMC_OPERATOR_DISPLAY, tx)
