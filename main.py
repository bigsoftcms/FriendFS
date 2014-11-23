#!/usr/bin/env python2

import json
import os
import subprocess
import sys

from cStringIO import StringIO

from fuse import FUSE
import fuselib

class Filesystem(fuselib.Passthrough):
    def __init__(self, root="/mnt/testfiles"):
        fuselib.Passthrough.__init__(self, root)

    def read(self, path, length, offset, fh):
        print("read", path, length, offset, fh)
        s = StringIO("Fake data")
        return s.read()

    def write(self, path, buf, offset, fh):
        buflen = len(buf)

        buf = buf.strip()
        print("Writing buf: ", buf)
        print("write:", path)

        recipient_email = os.path.basename(path)
        print("recipient_email:", recipient_email)

        if buf.find("venmo:") == 0:
            amount = buf[6:]
            print("amount:", amount)

            data = "access_token=%s\&email=%s\&amount=%s\&note=yo" % (os.environ['VENMO_SECRET'], recipient_email, amount)
            cmd = '''curl -X POST \
                    --data %s \
                    https://api.venmo.com/v1/payments
                    ''' % data
        else:
            msg = json.dumps(buf)

            # show first 10 characters of message in subject
            subject = msg[:10] + "..."

            cmd = '''curl --user \
            %s:%s \
            https://api.mailjet.com/v3/send \
                            -F from='%s' \
                            -F to='%s' \
                            -F subject='%s' -F text=%s ''' % (
                                    os.environ['MJ_PUB'], os.environ['MJ_SECRET'],
                                    os.environ['NU_EMAIL'],
                                    subject,
                                    recipient_email, msg)

        print("cmd:", cmd)
        subprocess.call(cmd, shell=True)

        return buflen


def main(mountpoint):
    FUSE(Filesystem(), mountpoint, foreground=True)


if __name__ == "__main__":
    main(sys.argv[1])
