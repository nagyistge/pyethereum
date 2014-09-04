
import os
import uuid
import StringIO
import ConfigParser
from pyethereum.utils import data_dir
from pyethereum.packeter import Packeter
from pyethereum.utils import sha3


def default_data_dir():
    return data_dir.path

def default_config_path():
    return os.path.join(default_data_dir(), 'config.txt')

def default_client_version():
    return Packeter.CLIENT_VERSION # FIXME

def default_node_id():
    return sha3(str(uuid.uuid1())).encode('hex')

config_template = \
"""
# NETWORK OPTIONS ###########

[network]

# Connect to remote host/port
remote_host = 54.76.56.74
remote_port = 30303

# Listen on the given host/port for incoming connections
listen_host = 0.0.0.0
listen_port = 30302

# Number of peer to connections to establish
num_peers = 10

# Name of the client
client_version = {0}

# unique id of this node
node_id = {1}

# API OPTIONS ###########
[api]

# Serve the restful json api on the given host/port
listen_host = 0.0.0.0
listen_port = 30203


# MISC OIPTIONS #########
[misc]

# Load database from path
data_dir = {2}

# percent cpu devoted to mining 0=off
mining = 30


# how verbose should the client be (1-3)
verbosity = 3

# set log level and filters (WARM, INFO, DEBUG)
# examples:
#   get every log message from every module
#      :DEBUG
#   get every warning from every module
#       :WARN
#   get every message from module chainmanager and all warnings
#       pyethereum.chainmanager:DEBUG,:WARN
logging = :INFO


# WALLET OPTIONS ##################
[wallet]

# Set the coinbase (mining payout) address
coinbase = 6c386a4b26f73c802f34673f7248bb118f97424a


""".format(default_data_dir(), default_client_version(), default_node_id())


def get_default_config():
    f = StringIO.StringIO()
    f.write(config_template)
    f.seek(0)
    config = ConfigParser.ConfigParser()
    config.readfp(f)
    assert config.get('misc', 'verbosity')
    return config

def read_config(cfg_path = default_config_path()):
    # create default if not existent
    if not os.path.exists(cfg_path):
        open(cfg_path, 'w').write(config_template)
    config = ConfigParser.ConfigParser()
    config.read(cfg_path)
    return config

def dump_config(config):
    r = ['']
    for section in config.sections():
        for a,v in config.items(section):
            r.append('[%s] %s = %r' %( section, a, v))
    return '\n'.join(r)
