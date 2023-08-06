from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519
import os
import base64
import struct
import socket
import sys
from .server import DashboardAgentServer
import logging

logger = logging.getLogger(__name__)

def configure():
  config = {
    'listen_address': os.getenv('DASHBOARD_AGENT_LISTEN_ADDRESS', '0.0.0.0'),
    'port': os.getenv('DASHBOARD_AGENT_PORT', '1437'),
    'public_key': os.getenv('DASHBOARD_AGENT_PUBLIC_KEY'),
  }
  return config

def cli(*args, **kwargs):
  conndata = None
  privkey = None
  def send(conn, privkey, msg):
    sig = privkey.sign(msg)
    conn.sendall(sig + msg)
  pubkey = None
  packet = b''
  while True:
    print('> ', end='')
    inval = input()
    parts = inval.split(' ', 1)
    cmd = parts[0].upper()
    if cmd == 'ADD':
      packet += parts[1].strip().encode('ascii')
      print(packet)
    elif cmd == 'PREADD':
      packet = parts[1].strip().encode('ascii') + packet
      print(packet)
    elif cmd == 'ADDBYTE':
      packet += struct.pack('B', int(parts[1].strip()))
      print(packet)
    elif cmd == 'PREADDBYTE':
      packet = struct.pack('B', int(parts[1].strip())) + packet
      print(packet)
    elif cmd == 'ADDSHORT':
      packet += struct.pack('<H', int(parts[1].strip()))
      print(packet)
    elif cmd == 'PREADDSHORT':
      packet = struct.pack('<H', int(parts[1].strip())) + packet
      print(packet)
    elif cmd == 'ADDLONG':
      packet += struct.pack('<L', int(parts[1].strip()))
      print(packet)
    elif cmd == 'SIGN':
      packet = privkey.sign(packet) + packet
    elif cmd == 'DIAL':
      if privkey is None:
        print('PRIVKEY first.')
        continue
      conndata = parts[1].strip().split(' ')
      with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as conn:
        conn.connect((conndata[0], int(conndata[1])))
        send(conn, privkey, b'HELLO')
        print("--> b'HELLO'")
        resp = conn.recv(1024)
        sig = resp[:64]
      print('<--', resp[64:])
      pubkey = ed25519.Ed25519PublicKey.from_public_bytes(resp[64:])
      pubkey.verify(sig, resp[64:])
    elif cmd == 'SEND':
      if privkey is None:
        print('PRIVKEY first.')
        continue
      if conndata is None:
        print('DIAL first.')
        continue
      with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as conn:
        conn.connect((conndata[0], int(conndata[1])))
        send(conn, privkey, packet)
        resp = conn.recv(1024)
        pubkey.verify(resp[:64], resp[64:])
      print('<--' , resp[64:])
      if packet[:5] == b'RAMUS':
        print(struct.unpack('<QQ', resp[64:80]))
      elif packet[:5] == b'CPUUS':
        print(struct.unpack('<fff', resp[64:76]))
      packet = b''
    elif cmd == 'BUF':
      print(packet)
    elif cmd == 'PRIVKEY':
      privkey = ed25519.Ed25519PrivateKey.from_private_bytes(base64.b64decode(parts[1].strip()))
      print('Ok.')
    elif cmd == 'EXIT':
      break

def keygen(*args, **kwargs):
  private = ed25519.Ed25519PrivateKey.generate()
  with open('private.key', 'wb') as f:
    f.write(base64.b64encode(private.private_bytes(serialization.Encoding.Raw, serialization.PrivateFormat.Raw, serialization.NoEncryption())))
  public = private.public_key()
  with open('public.key', 'wb') as f:
    f.write(base64.b64encode(public.public_bytes(serialization.Encoding.Raw, serialization.PublicFormat.Raw)))

def main(*args, **kwargs):
  logger.setLevel(logging.DEBUG)
  logger.addHandler(logging.StreamHandler(sys.stdout))
  config = configure()
  with DashboardAgentServer(config) as server:
    server.serve_forever()
