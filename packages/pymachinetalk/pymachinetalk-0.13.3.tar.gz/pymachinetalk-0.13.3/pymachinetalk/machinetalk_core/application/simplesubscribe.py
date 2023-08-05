import zmq
import threading
import uuid
from fysom import Fysom

import machinetalk.protobuf.types_pb2 as pb
from machinetalk.protobuf.message_pb2 import Container


class SimpleSubscribe(object):
    def __init__(self, debuglevel=0, debugname='Simple Subscribe'):
        self.debuglevel = debuglevel
        self.debugname = debugname
        self._error_string = ''
        self.on_error_string_changed = []
        # ZeroMQ
        context = zmq.Context()
        context.linger = 0
        self._context = context
        # pipe to signalize a shutdown
        self._shutdown = context.socket(zmq.PUSH)
        self._shutdown_uri = b'inproc://shutdown-%s' % uuid.uuid4()
        self._shutdown.bind(self._shutdown_uri)
        self._thread = None  # socket worker tread
        self._tx_lock = threading.Lock()  # lock for outgoing messages

        # Socket
        self.socket_uri = ''
        self._socket_topics = set()
        # more efficient to reuse protobuf messages
        self._socket_rx = Container()

        # callbacks
        self.on_socket_message_received = []
        self.on_state_changed = []

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

    def start(self):
        if self._fsm.isstate('down'):
            self._fsm.start()

    def stop(self):
        if self._fsm.isstate('up'):
            self._fsm.stop()

    def add_socket_topic(self, name):
        self._socket_topics.add(name)

    def remove_socket_topic(self, name):
        self._socket_topics.remove(name)

    def clear_socket_topics(self):
        self._socket_topics.clear()

    def _socket_worker(self, context, uri):
        poll = zmq.Poller()
        socket = context.socket(zmq.SUB)
        socket.setsockopt(zmq.LINGER, 0)
        socket.connect(uri)
        poll.register(socket, zmq.POLLIN)
        # subscribe is always connected to socket creation
        for topic in self._socket_topics:
            socket.setsockopt(zmq.SUBSCRIBE, topic)

        shutdown = context.socket(zmq.PULL)
        shutdown.connect(self._shutdown_uri)
        poll.register(shutdown, zmq.POLLIN)

        while True:
            s = dict(poll.poll())
            if shutdown in s:
                shutdown.recv()
                return  # shutdown signal
            if socket in s:
                self._socket_message_received(socket)

    def start_socket(self):
        self._thread = threading.Thread(
            target=self._socket_worker,
            args=(
                self._context,
                self.socket_uri,
            ),
        )
        self._thread.start()

    def stop_socket(self):
        self._shutdown.send(' ')  # trigger socket thread shutdown
        self._thread = None

    # process all messages received on socket
    def _socket_message_received(self, socket):
        (identity, msg) = socket.recv_multipart()  # identity is topic

        try:
            self._socket_rx.ParseFromString(msg)
        except DecodeError as e:
            note = 'Protobuf Decode Error: ' + str(e)
            print(note)  # TODO: decode error
            return

        if self.debuglevel > 0:
            print('[%s] received message' % self.debugname)
            if self.debuglevel > 1:
                print(self.socket_rx)
        rx = self._socket_rx

        # react to any incoming message
        if self._fsm.isstate('up'):
            self._fsm.any_msg_received()

        for cb in self.on_socket_message_received:
            cb(identity, rx)
