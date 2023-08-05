# coding=utf-8
from fysom import Fysom
from ..common.rpcservice import RpcService

import machinetalk.protobuf.types_pb2 as pb
from machinetalk.protobuf.message_pb2 import Container


class CommandServiceBase(object):
    def __init__(self, debuglevel=0, debugname='Command Service Base'):
        self.debuglevel = debuglevel
        self.debugname = debugname
        self._error_string = ''
        self.on_error_string_changed = []

        # Command
        self._command_channel = RpcService(debuglevel=debuglevel)
        self._command_channel.debugname = '%s - %s' % (self.debugname, 'command')
        self._command_channel.on_state_changed.append(
            self._command_channel_state_changed
        )
        self._command_channel.on_socket_message_received.append(
            self._command_channel_message_received
        )
        # more efficient to reuse protobuf messages
        self._command_rx = Container()
        self._command_tx = Container()

        # callbacks
        self.on_command_message_received = []
        self.on_state_changed = []

        # fsm
        self._fsm = Fysom(
            {
                'initial': 'down',
                'events': [
                    {'name': 'start', 'src': 'down', 'dst': 'trying'},
                    {'name': 'command_up', 'src': 'trying', 'dst': 'up'},
                    {'name': 'stop', 'src': 'up', 'dst': 'down'},
                ],
            }
        )

        self._fsm.ondown = self._on_fsm_down
        self._fsm.onafterstart = self._on_fsm_start
        self._fsm.ontrying = self._on_fsm_trying
        self._fsm.onaftercommand_up = self._on_fsm_command_up
        self._fsm.onup = self._on_fsm_up
        self._fsm.onafterstop = self._on_fsm_stop

    def _on_fsm_down(self, _):
        if self.debuglevel > 0:
            print('[%s]: state DOWN' % self.debugname)
        for cb in self.on_state_changed:
            cb('down')
        return True

    def _on_fsm_start(self, _):
        if self.debuglevel > 0:
            print('[%s]: event START' % self.debugname)
        self.start_command_channel()
        return True

    def _on_fsm_trying(self, _):
        if self.debuglevel > 0:
            print('[%s]: state TRYING' % self.debugname)
        for cb in self.on_state_changed:
            cb('trying')
        return True

    def _on_fsm_command_up(self, _):
        if self.debuglevel > 0:
            print('[%s]: event COMMAND UP' % self.debugname)
        return True

    def _on_fsm_up(self, _):
        if self.debuglevel > 0:
            print('[%s]: state UP' % self.debugname)
        for cb in self.on_state_changed:
            cb('up')
        return True

    def _on_fsm_stop(self, _):
        if self.debuglevel > 0:
            print('[%s]: event STOP' % self.debugname)
        self.stop_command_channel()
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
    def command_uri(self):
        return self._command_channel.socket_uri

    @command_uri.setter
    def command_uri(self, value):
        self._command_channel.socket_uri = value

    @property
    def command_port(self):
        return self._command_channel.socket_port

    @property
    def command_dsn(self):
        return self._command_channel.socket_dsn

    def start(self):
        if self._fsm.isstate('down'):
            self._fsm.start()

    def stop(self):
        if self._fsm.isstate('up'):
            self._fsm.stop()

    def start_command_channel(self):
        self._command_channel.start()

    def stop_command_channel(self):
        self._command_channel.stop()

    # process all messages received on command
    def _command_channel_message_received(self, identity, rx):

        # react to ping message
        if rx.type == pb.MT_PING:
            self.ping_received(identity, rx)

        # react to emc task plan run message
        elif rx.type == pb.MT_EMC_TASK_PLAN_RUN:
            self.emc_task_plan_run_received(identity, rx)

        # react to emc task plan execute message
        elif rx.type == pb.MT_EMC_TASK_PLAN_EXECUTE:
            self.emc_task_plan_execute_received(identity, rx)

        # react to emc task set mode message
        elif rx.type == pb.MT_EMC_TASK_SET_MODE:
            self.emc_task_set_mode_received(identity, rx)

        for cb in self.on_command_message_received:
            cb(identity, rx)

    def ping_received(self, identity, rx):
        print('SLOT ping unimplemented')

    def emc_task_plan_run_received(self, identity, rx):
        print('SLOT emc task plan run unimplemented')

    def emc_task_plan_execute_received(self, identity, rx):
        print('SLOT emc task plan execute unimplemented')

    def emc_task_set_mode_received(self, identity, rx):
        print('SLOT emc task set mode unimplemented')

    def send_command_message(self, identity, msg_type, tx):
        self._command_channel.send_socket_message(identity.encode(), msg_type, tx)

    def send_ping_acknowledge(self, identity, tx):
        ids = [identity.encode()]
        for receiver in ids:
            self.send_command_message(receiver, pb.MT_PING_ACKNOWLEDGE, tx)

    def send_emccmd_executed(self, identity, tx):
        ids = [identity.encode()]
        for receiver in ids:
            self.send_command_message(receiver, pb.MT_EMCCMD_EXECUTED, tx)

    def send_emccmd_completed(self, identity, tx):
        ids = [identity.encode()]
        for receiver in ids:
            self.send_command_message(receiver, pb.MT_EMCCMD_COMPLETED, tx)

    def send_error(self, identity, tx):
        ids = [identity.encode()]
        for receiver in ids:
            self.send_command_message(receiver, pb.MT_ERROR, tx)

    def _command_channel_state_changed(self, state):

        if state == 'up':
            if self._fsm.isstate('trying'):
                self._fsm.command_up()
