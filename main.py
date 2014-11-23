#!/usr/bin/env python2

import json
import os
import random
import subprocess
import sys
import time

from cStringIO import StringIO

from fuse import FUSE
import fuselib

class Filesystem(fuselib.Passthrough):

    def __init__(self, root="/mnt/testfiles"):
        fuselib.Passthrough.__init__(self, root)
        self.nicolas_cage = False

    def send_venmo(self, recipient_email, amount):
        print("amount:", amount)

        data = "access_token=%s\&email=%s\&amount=%s\&note=yo" % (os.environ['VENMO_SECRET'], recipient_email, amount)
        cmd = '''curl -X POST \
                --data %s \
                https://api.venmo.com/v1/payments
                ''' % data

        print("cmd:", cmd)
        subprocess.call(cmd, shell=True)

    def send_email(self, recipient_email, msg, attachment=None):
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
                                recipient_email,
                                subject, msg)

        if "cage" in msg:
            print("Attaching nicolas cage")
            cmd += ''' -F attachment="@nicolascage.jpg;filename=nicolascage.jpg" '''

        print("cmd:", cmd)
        subprocess.call(cmd, shell=True)

    def display_img(self, filename, delay=5):
        if not filename:
            # Use random file
            files = os.listdir("img")
            ran = random.randrange(0, len(files))
            filename = "img/" + files[ran]

        cmd = '''(sxiv "%s" & pid=$!; echo $pid; sleep %d ; kill -9 $pid) &''' % (
                filename, delay)
        print("cmd:", cmd)
        subprocess.call(cmd, shell=True)

    def espeak(self, msg):
        cmd = '''espeak "%s" -a 200 -s 80''' % msg
        print("cmd:", cmd)
        subprocess.call(cmd, shell=True)


    # Filesystem functions

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
            self.send_venmo(recipient_email, amount)
        else:
            msg = json.dumps(buf)
            self.send_email(recipient_email, msg)

        return buflen

    def unlink(self, path):
        print("path:", path)
        if "nicolascage" in path:
            if not self.nicolas_cage:
                self.espeak("You cannot delete Nicolas Cage")
                self.display_img("img/01.jpg")
                self.nicolas_cage = True
            else:
                self.espeak("All your friends are belong to Nicolas Cage")

                for i in range(4):
                    self.display_img(None, delay=1)
                    time.sleep(0.7)
                for i in range(20):
                    self.display_img(None, delay=1)
                    time.sleep(0.2)
        else:
            fuselib.Passthrough.unlink(self, path)


    def readdir(self, path, fh):
        if not self.nicolas_cage:
            for x in fuselib.Passthrough.readdir(self, path, fh):
                yield x
        else:
            for x in ['nicolascage'] * 100:
                yield x


def main(mountpoint):
    FUSE(Filesystem(), mountpoint, foreground=True)


if __name__ == "__main__":
    main(sys.argv[1])
