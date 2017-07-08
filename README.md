# SlowToris
## The low bandwidth, Tor routed, yet poisonous HTTP client

This is a version of slowloris implemented in python. It attempts to route all traffic through the Tor proxy on port 9150.

Slowloris works by sending malformed http headers on a lot of different connections. It makes the webserver think that each connection has poor connectivity and is dropping packets so the webserver will wait for the client. The clients then continue to send keep-alive packets until they are timed out by the webserver. Once a connection times out a new connection is made to take its place. This ensures that all connections allowed on the server are tied up with minimal bandwidth. Slowloris also only affects the targeted server since it doesn't require large amounts of data to be sent over a network.

Correct args format: python3 slowtoris.py IPv4(str) port(int) num_sockets(int) isHTTPS(Y/N)

**This is for research purposes only. Don't do anything stupid with this, only DoS servers you own or use for pen-testing.**

## SlowLorisProbe

slowlorisprobe.py is a tool that can probe websites for the slowloris vulnerability without launching a full scale attack.

It works by creating two connections at the same time. It uses the same malformed headders as slowloris. One connection simply times out while the other waits 10 seconds and then sends a malformed keep-alive packet. If the time out time between the two connections is greater than or equal to 10 then the slowloris exploit is likely possible on that server.

Correct args format: python3 slowlorisprobe.py IPv4(str) port(int) isHTTPS(Y/N) useTor(Y/N)