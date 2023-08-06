import logging

logging.basicConfig(level=logging.NOTSET)
logger = logging.getLogger(__name__)

import base64

import socket
import socketserver
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.exceptions import InvalidSignature
import requests
import struct
import re
import subprocess


class DashboardAgentHandler(socketserver.BaseRequestHandler):
  def __init__(self, *args, **kwargs):
    self.messageHandlers = {
      b'HELLO': self.handler_HELLO,
      b'PORTC': self.handler_PORTC,
      b'SERVS': self.handler_SERVS,
      b'RAMUS': self.handler_RAMUS,
      b'CPUUS': self.handler_CPUUS,
      b'TUNNL': self.handler_TUNNL,
    }

    super().__init__(*args, **kwargs)

  def respond(self, message, key):
    signature = key.sign(message)
    self.request.sendall(signature + message)

  def respond_error(self, code, key):
    codebytes = struct.pack('<H', code)
    self.respond(b'ERROR' + codebytes, key)

  def handler_HELLO(self, message):
    key = self.server.client_keys[self.client_address[0]]
    public = key.public_key()
    self.respond(public.public_bytes(serialization.Encoding.Raw, serialization.PublicFormat.Raw), key)

  def handler_PORTC(self, message):
    key = self.server.client_keys[self.client_address[0]]
    port = struct.unpack('<H', message[5:7])[0]
    try:
      r = requests.get('http://127.0.0.1:{0}'.format(port), timeout=15)
      scode = r.status_code
    except Exception as e:
      scode = 0
    sbytes = struct.pack('<H', scode)
    self.respond(sbytes, key)

  def handler_SERVS(self, message):
    key = self.server.client_keys[self.client_address[0]]
    service = message[5:].decode('ascii')
    if re.fullmatch(r'^[a-zA-Z0-9].+$', service) is None:
      self.respond_error(11, key)
      logger.info('Requested service name {0} contains illegal characters'.format(service))
      return

    try:
      cp = subprocess.check_output(['systemctl', 'show', service, '--no-page'], text=True)
      for line in cp.split('\n'):
        kv = line.split('=', 1)
        if kv[0] == 'ActiveState':
          if kv[1].strip() != 'active':
            self.respond(b'\x00', key)
          else:
            self.respond(b'\x01', key)
          return
    except subprocess.CalledProcessError:
      pass
    self.respond(b'\x00', key)

  def handler_RAMUS(self, message):
    key = self.server.client_keys[self.client_address[0]]

    with open('/proc/meminfo', 'r') as meminfo:
      data = meminfo.read()
    availm = re.search(r'MemAvailable:\s+?(\d+)\s+?kB', data)
    avail = int(availm.group(1)) / 1024
    availb = struct.pack('<Q', int(avail))
    totalm = re.search(r'MemTotal:\s+?(\d+)\s+?kB', data)
    total = int(totalm.group(1)) / 1024
    totalb = struct.pack('<Q', int(total))
    self.respond(availb + totalb, key)

  def handler_TUNNL(self, message):
    key = self.server.client_keys[self.client_address[0]]

    try:
      ip_port = struct.unpack('<BBBBH', message[5:11])
      ip = '{0}.{1}.{2}.{3}'.format(ip_port[0], ip_port[1], ip_port[2], ip_port[3])
      port = ip_port[4]
    except:
      self.respond_error(21, key)
      return

    try:
      with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as conn:
        conn.connect((ip, port))
        conn.sendall(message[11:])
        data = conn.recv(1024)
      self.respond(data[64:], key)
    except:
      self.respond_error(22, key)

  def handler_CPUUS(self, message):
    key = self.server.client_keys[self.client_address[0]]
    with open('/proc/loadavg', 'r') as loadinfo:
      data = loadinfo.read()
    parts = data.split(' ', 3)
    resp = b''
    for i in range(3):
      flv = float(parts[i])
      resp += struct.pack('<f', flv)
    self.respond(resp, key)

  def handle(self):
    if self.client_address[0] not in self.server.client_keys:
      key = ed25519.Ed25519PrivateKey.generate()
      self.server.client_keys[self.client_address[0]] = key
    data = self.request.recv(1024)
    pubkey = ed25519.Ed25519PublicKey.from_public_bytes(base64.b64decode(self.server.config['public_key']))
    sig = data[:64]
    message = data[64:]
    try:
      pubkey.verify(sig, message)
    except InvalidSignature:
      self.respond_error(1, key)
      logger.info('Signature mismatch from client, dropping.')
      return

    logger.debug('{0}: {1}'.format(self.client_address[0], message[:5]))
    try:
      if message[:5] in self.messageHandlers:
        self.messageHandlers[message[:5]](message)
      else:
        self.respond_error(2, key)
    except:
      self.respond_error(3, key)

class DashboardAgentServer(socketserver.TCPServer):
  def __init__(self, config):
    self.config = config
    self.client_keys = {}
    super().__init__((config['listen_address'], int(config['port'])), DashboardAgentHandler)
