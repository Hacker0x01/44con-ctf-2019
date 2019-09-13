About
=====

This was originally run September 11-13, 2019 in London at 44CON as the official CTF.  Thank you to the 44CON staff for giving us the opportunity to be a part of this fantastic event and for all their support.

Installation
============

Ensure you have Docker, docker-compose, and GNU Make installed, then clone this repo and run:

	docker network create instances
	make start

Playing
=======

**Don't read the source!** (At first.)  For your own education and entertainment, just run this and pretend you don't have access to any of the code.  You'll thank yourself for playing this the way it's meant to be played.

The service will run a telnet service on port 2323 and SSH service on port 2222.  Telnet will allow you to register and give you a hint for accessing the SSH service (the SSH credentials are not the ones you register on telnet).

Hints
=====

See [hints.md](hints.md) for the hints released during 44con.  Use them -- that's what they're there for!
