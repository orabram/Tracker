__author__ = 'Or'
from SeedersManager import *
sm = seeder_communication_manager()
#sm.build_meta_file(700, "C:\\Users\\Or\\Downloads\\Austin Powers - International Man of Mystery (1997)\\Austin.Powers.International.Man.of.Mystery.1997.720p.Brrip.x264.Deceit.YIFY.mp4", )
print sm.divide_files("C:\\Users\\Or\\Downloads\\Austin Powers - International Man of Mystery (1997)\\Austin.Powers.International.Man.of.Mystery.1997.720p.Brrip.x264.Deceit.YIFY.mp4")
f = open("[kat.cr]the.flash.2014.s02e19.hdtv.x264.lol.ettv.torrent", 'rb')
f2 = f.read()
f2 = bencode.bdecode(f2)
print f2["info"]