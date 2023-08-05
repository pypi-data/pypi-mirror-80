#!/usr/bin/env python3
import hmac
import array
import base64
import hashlib
import argparse
from pathlib import Path
from configparser import ConfigParser, NoOptionError


CONFIGURATION_FILE = Path.home() / '.mobilepasser.cfg'


def main():
    cli_args = get_cli_args()

    # try:
    cfg = Path(cli_args.config) if cli_args.config else CONFIGURATION_FILE
    config = ConfigParser()
    config.read(cfg)

    if cfg.is_file() and config.has_section('MobilePASS'):
        key = config.get('MobilePASS', 'ActivationCode')
        policy = config.get('MobilePASS', 'Policy')
        index = config.getint('MobilePASS', 'Index')
        auto_update = config.getboolean('MobilePASS', 'AutoUpdateIndex')
    else:
        key = cli_args.key
        policy = cli_args.policy
        index = cli_args.index
        auto_update = cli_args.update

    print(generate_token(
        activation_code=key,
        index=index,
        policy=policy
    ))

    if auto_update:
        index += 1
        config.set('MobilePASS', 'Index', str(index))

        with open(cfg, 'w') as file:
            config.write(file)

    # except TypeError as error:
    #     print(error)
    # except NoOptionError as error:
    #     print(error)

# I ported the KDF1 algorithm from the bouncycastle library that shipped with
# the app as the python libraries that included this function seemed to be
# returning different values.
def KDF1(hash, secret, iv, start_position, key_length): #key should be passed by reference
    counter_start = 0
    counter = counter_start

    digest_size = hash.digest_size
    digests_required = (int) ((key_length + digest_size - 1) / digest_size)
    digest_counter = 0

    key = bytearray()

    while True:
        if digest_counter >= digests_required:
            return key

        hash.update(secret)

        # In java the counter was being cast to a byte before being passed to the hash update
        # function. Java uses narrowing primitive conversion for this type of casting which
        # only preserves the last byte. So it needed to do some bit math to preserve the whole
        # counter. This is what we're trying to replicate here.
        # See: http://stackoverflow.com/questions/2458495/how-are-integers-casted-to-bytes-in-java
        hash.update(chr((counter >> 24) & 0xff).encode())
        hash.update(chr((counter >> 16) & 0xff).encode())
        hash.update(chr((counter >> 8) & 0xff).encode())
        hash.update(chr(counter & 0xff).encode())

        if iv != "":
            hash.update(iv)

        digest = hash.digest()

        if (key_length > digest_size):
            key[start_position:start_position+digest_size] = digest[0:digest_size]
            start_position += digest_size
            key_length -= digest_size
        else:
            key[start_position:start_position+key_length] = digest[0:key_length]

        counter += 1
        digest_counter += 1


def get_entropy(activation_code):
    # Remove hyphens.
    activation_code = activation_code.replace('-', '')
    
    # Remove every 5th chracter.
    activation_code = ''.join('' if i % 5 == 0 else char for i, char in enumerate(activation_code, 1))

    return base64.b32decode(activation_code, True, "I")


def get_key(entropy, policy):
    secret = bytearray(entropy)

    if len(policy) != 0:
        policy_bytes = bytearray(policy, "ascii")
        secret.extend(policy_bytes)

    hash = hashlib.new('sha256')

    return KDF1(hash, secret, bytearray(), 0, 32)


def long_to_byte_array(long_num):
    """
    helper function to convert a long number into a byte array
    """
    byte_array = array.array('B')
    for i in range(8):
        byte_array.insert(0, long_num & 0xff)
        long_num >>= 8
    return byte_array


def truncated_value(h):
    bytes = h.digest()
    offset = bytes[-1] & 0xf
    v = (bytes[offset] & 0x7f) << 24 | (bytes[offset+1] & 0xff) << 16 | \
            (bytes[offset+2] & 0xff) << 8 | (bytes[offset+3] & 0xff)
    return v


def generate_token(activation_code, index, policy=''):
    '''
    activation_code is the string the MobilePass client generated.

    index is a 0-based index of the token to generate. The first
    generated token is for index=0, the second for index=1, and
    so on. It is the caller’s responsibility to keep track of the
    current index.
    '''
    message = long_to_byte_array(index)

    entropy = get_entropy(activation_code)
    key = get_key(entropy, policy)

    h = hmac.new(key, message, hashlib.sha256)
    h = truncated_value(h)
    h = h % (10**6)
    return '%0*d' % (6, h)


def get_cli_args():
    parser = argparse.ArgumentParser(
        description='Generate one-time passcodes based on activation code')
    parser.add_argument('-c',
                        '--config',
                        type=str,
                        help='path to the configuration file')
    parser.add_argument('-k',
                        '--key',
                        type=str,
                        help='activation code is generated by SafeNet MobilePASS')
    parser.add_argument('-i',
                        '--index',
                        type=int,
                        help='the index number of the one-time passcode')
    parser.add_argument('-p',
                        '--policy',
                        type=str,
                        default='',
                        help='token policy string')
    parser.add_argument('-u',
                        '--update',
                        action='store_true',
                        help='automatically increses the index by 1 and saves to configuration file')

    return parser.parse_args()


if __name__ == '__main__':
    main()
