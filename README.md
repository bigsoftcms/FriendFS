# FriendFS
A FUSE filesystem that allows you to interact with your friends as files.

Made at HackNorthwestern, 2014

## Usage
(Remember, this is just for fun!)

Run:
```shell
./main.py MOUNTPOINT ROOT
```
where MOUNTPOINT is where you want to mount the filesystem and ROOT is where
you want to persist changes. (It's recommended that both MOUNTPOINT and ROOT
are empty directories)

Now in MOUNTPOINT, if you create a file whose name is an email, you can send
emails with mailjet by writing to the file
(e.g. `echo "Hello world!" > test@example.com`)
or send money with venmo to the user with that email address by writing to the
file "venmo:X.XX" where X is a number
(e.g. `echo "venmo:1.50" > test@example.com`)

To send emails with Mailjet, you must have a developer account and set
environment variables `MJ_PUB`, `MJ_SECRET`, and `MJ_EMAIL` with your public
developer key, secret developer key, and email address.

To send money with Venmo, you also must have a developer account and set
the environment variable `VENMO_SECRET` with your developer secret key.

There are also Nicolas Cage easter eggs, if you can find them!


## APIs
* Mailjet
* Venmo


## Special thanks
* [fusepy](https://github.com/terencehonles/fusepy)
* [sample FUSE filesystem](http://www.stavros.io/posts/python-fuse-filesystem/)
