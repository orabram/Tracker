import bencode
import struct
f = open("[kat.cr]the.flash.2014.s02e19.hdtv.x264.lol.ettv.torrent", 'rb')
f2 = f.read()
f2 = bencode.bdecode(f2)
print f2
f3 = f2["info"]["pieces"]
f3 = bytes(f3)
print f3
s = f3.decode("mbcs")
print s