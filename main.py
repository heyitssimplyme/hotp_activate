import requests
import base64
from urllib.parse import urlparse, parse_qsl, unquote
import argparse
from sys import argv

description = 'See readme for instructions.'

parser = argparse.ArgumentParser(
  description=description
)
parser.add_argument('qr_url', type=str, help='The qr code url')

def get_activation_url (qr_url: str) -> str:
  qs = dict(parse_qsl(urlparse(qr_url).query))
  value = qs['value']

  code, b64host = value.split('-')
  b64host += '=' * (-len(b64host) % 4) # fix padding
  hostname = base64.b64decode(b64host).decode('utf-8')

  return f"https://{hostname}/push/v2/activation/{code}"

def get_hotp (activation_url: str) -> str:
  resp = requests.post(activation_url).json()

  if resp['stat'] != 'OK':
    print(resp)
    print('Activation failed!')
    exit(1)
  else:
    return resp['response']['hotp_secret']

def main():
  args = parser.parse_args()
  qr_url = args.qr_url.replace('\\', '')

  if 'duosecurity.com/frame/qr' not in qr_url:
    print('Invalid url!')
    exit(1)

  url = get_activation_url(qr_url)
  print('Activation url:', url)

  hotp_secret = get_hotp(url)
  print(f'''
{'-' * 5} Activation succeeded! {'-' * 5}
Secret:
  Hex: `{hotp_secret}`
  Base 32: `{base64.b32encode(hotp_secret.encode('ascii')).decode('utf-8').upper()}`
Counter starts at: 0
''')

if __name__ == '__main__':
  main()