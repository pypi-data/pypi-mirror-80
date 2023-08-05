ih2torrent
==========

``ih2torrent`` creates a trackerless torrent file from an infohash or a
magnet URI. It uses BitTorrent
`DHT <http://www.bittorrent.org/beps/bep_0005.html>`__ and the `metadata
protocol <http://www.bittorrent.org/beps/bep_0009.html>`__ to find peers
for the torrent and obtain its metadata.

In order to get the dependencies inside a virtualenv, run ``make``. You
need Python 3.5 or higher to run ih2torrent.

You can use pip to install ih2torrent: ``pip3 install ih2torrent``
