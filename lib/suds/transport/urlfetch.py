# This program is free software; you can redistribute it and/or modify
# it under the terms of the (LGPL) GNU Lesser General Public License as
# published by the Free Software Foundation; either version 3 of the 
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Library Lesser General Public License for more details at
# ( http://www.gnu.org/licenses/lgpl.html ).
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
# written by: Jeff Ortel ( jortel@redhat.com )

"""
Contains classes for basic HTTP transport implementations.
"""

from suds.transport import AsyncTransport, Reply, TransportError
from suds.properties import Unskin
from cookielib import CookieJar
from logging import getLogger
from lib.future import Future
from google.appengine.runtime import apiproxy_errors
from webapp2 import abort

from google.appengine.api import urlfetch

log = getLogger(__name__)


class UrlfetchTransport(AsyncTransport):
    """
    HTTP transport using urllib2.  Provided basic http transport
    that provides for cookies, proxies but no authentication.
    """
    
    def __init__(self, **kwargs):
        """
        @param kwargs: Keyword arguments.
            - B{proxy} - An http proxy to be specified on requests.
                 The proxy is defined as {protocol:proxy,}
                    - type: I{dict}
                    - default: {}
            - B{timeout} - Set the url open timeout (seconds).
                    - type: I{float}
                    - default: 90
        """
        AsyncTransport.__init__(self)
        Unskin(self.options).update(kwargs)
        self.cookiejar = CookieJar()
        self.proxy = {}
        self.urlopener = None

    def send(self, request):
        url = request.url
        msg = request.message
        headers = request.headers

        rpc = urlfetch.create_rpc(deadline=20)
        urlfetch.make_fetch_call(rpc, url, msg, method=urlfetch.POST, headers=headers)

        def callback(future):
            try:
                result = future.get_result()
                if 200 > result.status_code > 299:
                    raise TransportError(result.content, result.status_code)
            except apiproxy_errors.DeadlineExceededError:
                raise
            except urlfetch.DownloadError:
                log.exception('Server is not responding')
                raise abort(502, 'Server is not responding')

            return Reply(200, result.headers, result.content)

        return Future(rpc, callback)

    def __deepcopy__(self, memo={}):
        clone = self.__class__()
        p = Unskin(self.options)
        cp = Unskin(clone.options)
        cp.update(p)
        return clone
