# SlowToris
## The low bandwidth, Tor routed, yet poisonous HTTP client

This is a version of slowloris implemented in python. It attempts to route all traffic through the Tor proxy on port 9150.

Correct args format: python3 slowtoris.py IPv4(str) port(int) num_sockets(int) isHTTPS(Y/N)

**This is for research purposes only. Don't do anything stupid with this, only DoS servers you own or use for pen-testing.**

## SlowLorisProbe

slowlorisprobe.py is a tool that can probe websites for the slowloris vulnerability without launching a full scale attack.

Correct args format: python3 slowlorisprobe.py IPv4(str) port(int) isHTTPS(Y/N) useTor(Y/N)