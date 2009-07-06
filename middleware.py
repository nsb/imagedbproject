"""Django middleware to redirect requests based on originating IP address

   Contains the IPAddressMiddleware class used to redirect requests based
   on whether the originating IP is in a set of registered addresses or
   not. Both IPv4, and IPv6 addresses can be handled.

   External dependencies: The netaddr library,
   http://code.google.com/p/netaddr/ , is used for handling IP addresses

   Currently tested with Django 1.1-beta-1 (SVN checkout on 2009-JUL-02,
   and IPy 1:0.62-1. Live testing has only been done with IPv4 addresses.
   Please see the unit tests for some pseudo-IPv6 tests.

"""
import netaddr
from django.conf import settings
from django.contrib import admin
import django.contrib.auth.views
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
import files.views

class IPAddressMiddleware(object):
    """Middleware to redirect requests based on originating IP address.

    IP addresses are classified into two categories:
      - Registered addresses defined in settings.py as a list
      - Non-registered addresses: Anything that is not listed in the above
        set of registered addresses.

    Requests from registered IP addresses are handled as follows:
      - Allow access without logging in for non-admin. views. Users are
        shown a login screen, but can just click the login button to
        get in.
      - Normal admin. login for admin. views, except for a special
        login page.

    No special handling of requests from non-registered IP addresses. Log
    in, and proceed as normal for all users, showing the standard login
    page.

    """
    def __init__(self):
        """Initialises the list of registered IP addresses.
        """
        self.ip_reg = []
        try:
            ip_settings = eval( str(getattr(settings, 'SRJ_IP_REG', '[]')) )
            for ip in ip_settings:
                if hasattr( ip, '__iter__' ):
                    # Sequence value => range of IP addresses
                    self.ip_reg.append( netaddr.IPRange( ip[0], ip[1] ) )
                else:
                    # Single value => normal IP, though can also be range
                    self.ip_reg.append( netaddr.IP( ip ) )
        except Exception:
            raise

    def _call_viewfunc(self, func, request, args, kwargs):
        """Calls a Django view function passed to process_view()

           Needs to be done this way as else it apparently exercises a
           bug in Django, with an error 'dict objects are unhashable'
        """
        if args:
            return func( request, *args, **kwargs ) if kwargs else \
                func( request, *args )
        else:
            return func( request, **kwargs ) if kwargs else func( request )

    def process_view(self, request, viewfunc, args, kwargs):
        view = request.get_full_path()
        incoming = request.META.get('REMOTE_ADDR')
        is_ip_reg = False
        for ip in self.ip_reg:
            # Following covers single addresses, and all address ranges
            if incoming in ip.iprange():
                is_ip_reg = True
                break

        if view.startswith('/login/'):
            # For login view setup appropriate templates
            if is_ip_reg:
                kwargs['template_name'] = getattr( settings,
                                                   'SRJ_TMPL_LOGIN_REG',
                                                   'login_reg.html' )
            else:
                kwargs['template_name'] = getattr( settings,
                                                   'SRJ_TMPL_LOGIN_UNREG',
                                                   'login.html' )
            return self._call_viewfunc( django.contrib.auth.views.login,
                                        request, args, kwargs )
        elif view.startswith('/logout/') or view.startswith('/password/'):
            return self._call_viewfunc( eval( 'django.contrib.auth.views.' + \
                                           viewfunc.__name__ ),
                                 request, (), {} )
        elif view.startswith('/login_reg'):
            if not is_ip_reg:
                return HttpResponseRedirect( '/login/' )
        elif view.startswith('/static/') or view.startswith('/media/'):
            # Simply serve static media, and Django admin. media
            return self._call_viewfunc( viewfunc, request, args, kwargs )
        else:
            # For all other views, if non-admin views are required, return
            # them for users from registered IPs.
            if is_ip_reg:
                # FIXME: Change this to non-deprecated mode.
                admin_root = reverse( admin.site.root, args=[''] )
                if not view.startswith( admin_root ):
                    return self._call_viewfunc( eval( 'files.views.' + \
                                                  viewfunc.__name__ ),
                                         request, args, kwargs )


