from crawlerPackage1 import *

class CoreCawler():
    def __init__(self):
        self.match = {}
        self.match['http://www.cnn.com/'] = fetchCNN_USA
        self.match['http://rss.cnn.com/rss/cnn_topstories.rss'] = fetchCNNCSS_USA
        self.match['http://www.rtb.bf/'] = fetchRTB_BFA
        self.match['http://www.omegabf.net/'] = fetchOMEGA_BFA
        self.match['http://www.rfi.fr/last24/rss'] = fetchRFI_FRANCE
        self.match['http://www.france24.com/fr/timeline/rss'] = fetchF24_FRANCE
        self.match['http://www.france24.com/en/timeline/rss'] = fetchF24_FRANCE
        self.match['http://www.france24.com/ar/timeline/rss'] = fetchF24_FRANCE
        self.match['http://www.africa24tv.com'] = fetchAF24_AFRIQUE
        self.match['http://www.2m.ma/fr'] = fetch2MFr_MA
        self.match['http://www.2m.ma'] = fetch2MAr_MA
        self.match['http://www.bfmtv.com/rss/info/flux-rss/flux-toutes-les-actualites/'] = fetchBFM_FRANCE
        self.match['http://info.arte.tv/fr'] = fetchArte_FRANCE
        self.match['http://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml'] = fetchNYCTimes_USA
        # self.match['http://www.france24.com/fr/timeline/rss'] = fetchF24CSS_En

# RSS:
# CNN: http://rss.cnn.com/rss/cnn_world.rss
# look for description and content split content to &lt;div and take 0
# Also:
# rss.cnn.com/rss/cnn_topstories.rss
# Global link is: http://www.cnn.com/services/rss/

# NewYork Times: http://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml
# Take directly description.

# France 24: http://www.france24.com/fr/timeline/rss
# Take the first line of description. between &lt;  [1] and p&gt; [1]
# The title is not that clear.
# Both fr and en and ar.

    def fetch(self, url):
        news = self.match[url](url)
        # print "<- news ->"
        # for n in news:
        #     print n
        #     print "<- news ->"
        return news

