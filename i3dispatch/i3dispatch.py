#!/usr/bin/env python
from neovim import attach
import argparse
import subprocess
import os
import traceback
import logging
import psutil
import socket

'''
To test with qutebrowser
:set tab.position left (or top)
qutebrowser ':tab-next' works
'''

log = logging.getLogger(__name__)
# log.setLevel(logging.INFO)
log.setLevel(logging.DEBUG)

log.addHandler(logging.FileHandler(os.path.join(os.getenv("HOME","") , "i3dispatch.log"), delay=False))

"""
Exit value:
0 => success
1 => failure
"""
directions = {
        'left' : 'h',
        'right' : "l",
        'up': 'k',
        'down': 'j',
        }

def thunderbird_dispatcher(direction):
    if direction == 'right':
        key = "Ctrl+Tab"
    elif direction == 'left':
        key = "Ctrl+Shift+Tab"
    else:
        return False
    cmd = "xdotool search '{name}' key '{key}'".format(
            name=get_focused_window_name(),
            key=key,
            )
    log.debug('Launching command %s' % cmd)
    os.system(cmd)
    return True

def qutebrowser_dispatcher(direction):
    """
    direction should depend on the setting
    tabs.position
    https://github.com/qutebrowser/qutebrowser/blob/master/scripts/open_url_in_instance.sh
    """
    # if direction == 'down':
    #     key = ":tab-next"
    # elif direction == 'up':
    #     key = ":tab-prev"
    # else:
    #     return False
    # cmd = ["qutebrowser", key ]
    # log.debug("Launching command %s" % cmd)
    # subprocess.check_call(cmd)

    #!/bin/bash
    # initial idea: Florian Bruhin (The-Compiler)
    # author: Thore Bödecker (foxxx0)

    _url="$1"
    _qb_version='1.0.4'
    _proto_version=1
    # $USER" | md5sum | cut -d' ' -f1
    user=os.getenv("USER")
    import hashlib
    import json
    m = hashlib.md5()
    m.update(user.encode())

    _ipc_socket="{runtime_dir}/qutebrowser/ipc-{digest}".format(
        runtime_dir=os.getenv("XDG_RUNTIME_DIR"),
        digest=m.hexdigest()
    )

    req = {
        "args": [":tab-next"],
        "target_arg": "null",
        "version": "1",
        "protocol_version": "1", 
        "cwd": "/home/teto", # why do we care ?
    }
        # "${PWD}" | socat - UNIX-CONNECT:"${_ipc_socket}" 2>/dev/null || "$_qute_bin" "$@" &

    # with open(_ipc_socket) as fd:
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.connect(_ipc_socket)
    js = json.dumps(req)
    print("sedning js")
    print(js)
    sock.sendall(js.encode())
    data = sock.recv(1024)
    sock.close()
    print("received %r", data)
    # cmd = ["qutebrowser", key ]
    # log.debug("Launching command %s" % cmd)
    # subprocess.check_call(cmd)
    return True


def weechat_dispatcher(direction):
    if direction == 'right':
        key = "F5"
    elif direction == 'left':
        key = "F6"
    else:
        return False
    cmd = "xdotool key {key}".format(
            # name=get_focused_window_name(),
            key=key,
            )
    log.debug('Launching command %s' % cmd)
    os.system(cmd)
    return True


def neovim_dispatcher(direction):
    res, socket = get_nvim_socket()

    if not res:
        log.error("Could not find vim socket")
    elif send_nvim_wincmd(socket, directions[direction]):
        log.debug("nvim changed its focus")
        # if neovim succeeded changing buffer 
        return True
    else:
        log.debug("nvim did not change focus")
    return False

def get_dispatcher(name):
    log.debug("Window name=%s" % name)
# if we are focusing neovim
    if name.endswith("NVIM"):
        return neovim_dispatcher
    elif name.endswith("qutebrowser"):
        return qutebrowser_dispatcher
    # elif name.startswith("matt@"):
        # return weechat_dispatcher
    # elif name.endswith("Thunderbird"):
    #         return thunderbird_dispatcher
    return i3_dispatcher

def get_focused_window_name():
    try:
        # might be possible to get X via an X library or psutils ?
        out = subprocess.check_output(["xdotool", "getwindowfocus", "getwindowname"], shell=False).decode('utf-8').rstrip()
        return out
    except Exception as e:
        log.error(e)
    return ""


def get_nvim_socket():
    """
    1/ get pid of focused window
    2/ look for nvim processes in its children
    3/ search for socket name in the nvim child process
    """
    try:
        pid = subprocess.check_output("xdotool getwindowfocus getwindowpid", shell=True).decode()
        pid = pid.rstrip()
        pid = int(pid)
        log.debug("Retreived terminal pid %d, nvim should be one of its children" % pid)
        proc = psutil.Process(pid)
        log.debug( "proc name %s with %d children" % (proc.name(), len(proc.children(recursive=True))))
        for child in proc.children(recursive=True):
            log.debug("child name & pid %s/%d" % (child.name(), child.pid))
            if child.name() == "nvim":
                unix_sockets = child.connections(kind="unix")
                log.debug("Found an nvim subprocess with %d " % len(unix_sockets))
                # look for socket 
                # for filename, fd in child.open_files():
                # log.debug("Open file %s " % filename)
                for con in unix_sockets:
                    filename = con.laddr
                    log.debug("Socket %s " % filename)
                    if "/tmp/nvim" in filename:
                        log.debug("Found a match: %s" % filename) 
                        return True, filename
                    return False, ""
    except Exception as e:
        log.error('Could not find neovim socket %s' % e)
        log.error(traceback.format_exc())
        return False, ""

        # instead of using psutil one could do sthg like:
        # lsof -a -U -p 15684 -F n | grep /tmp/nvim |head -n1

def send_nvim_wincmd(path_to_socket, direction):
    log.info("Sending %s to socket %s" % (direction, path_to_socket))
    try:
    # path=os.environ["NVIM_LISTEN_ADDRESS"]
        # https://github.com/neovim/python-client/issues/124
        nvim = attach('socket', path=path_to_socket)
        log.debug("nvim attached")
        nvim.command('let oldwin = winnr()') 
        nvim.command('wincmd ' + direction)
        res = nvim.eval('oldwin != winnr()')
        log.debug("Result of command %d" % res)
        return res
    except Exception as e:
        log.error("Exception %s" % e)
        return False

    return False

def i3_dispatcher(direction):
    cmd = ["i3-msg", "focus", direction]
    log.info("running command: %s" % cmd)
    subprocess.check_call(cmd)
    return True

dispatchers = {
    "neovim": neovim_dispatcher,
    "qutebrowser": qutebrowser_dispatcher,
    "i3": i3_dispatcher,
}



def main():
    """
    Program starts here
    """
    # TODO we can set NVIM_LISTEN_ADDRESS before hand
    parser = argparse.ArgumentParser(description="parameter to send to wincmd")
    parser.add_argument("direction", choices=directions.keys())
    parser.add_argument("--test", action="store", choices=dispatchers.keys(), )
    parser.add_argument("--test-title", action="store", type=str, default=None)

    args = parser.parse_args()

    """
    get dispatcher function
    """


    # if anything failed or nvim didn't change buffer focus, we forward the command o i3

    if args.test:
        dispatcher = dispatchers.get(args.test)
    else:
        window_title = args.test_title or get_focused_window_name()
        dispatcher = get_dispatcher(window_title)

    log.info("Calling dispatcher %r with direction %s" % (dispatcher, args.direction))


    if not dispatcher(args.direction):
        i3_dispatcher(args.direction)

    exit(0)
