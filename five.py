import robotparser
import urlparse

def get_robots(url):
    """Initialize robots parser for this domain
    """
    rp = robotparser.RobotFileParser()
    rp.set_url(urlparse.urljoin(url, '/robots.txt'))
    rp.read()
    return rp



AGENT_NAME = 'IPLAYPYTHON'
URL_BASE = 'http://www.iplaypy.com/'
parser = robotparser.RobotFileParser()
parser.set_url(urlparse.urljoin(URL_BASE,'robots.txt'))
parser.read()

PATHS = ['/','/admin','/tags']
for path in PATHS:
     print '%6s : %s' % (parser.can_fetch(AGENT_NAME,'search'), path)
url = urlparse.urljoin(URL_BASE, path)
print '%6s : %s' % (parser.can_fetch(AGENT_NAME,url), url)