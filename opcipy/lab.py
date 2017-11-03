import requests
import sys
import json
import six 

"""
A Thin library for the OpenCellID web API products LocationIQ
and LocationAPI
"""

class LocationIQ(object):
	max_retries=10
	def __init__(self,requests_session=True,proxies=None,requests_timeout=None):
		self.prefix="https://unwiredlabs.com/v2/"
		self.requests_session = requests_session
		self.proxies=proxies
		self.requests_timeout=requests_timeout

		if isinstance(requests_session,requests.Session):
			self._session=requests_session
		else:
			#lets build a new session
			if requests_session:
				self._session = requests.Session()
			else:
				#lets use requests api as our new session
				from requests import api 
				self._session=api

	def _internal_calls(self,method,url,payload,params):
		args = dict(params=params)
		args["timeout"]=self.requests_timeout
		if not url.startswith("http"):
			url=self.prefix+url
		if payload:
			args["data"]=json.dump(payload)
		r = self._session.request(method,url,proxies=self.proxies,**args)
		try:
			r.raise_for_status()
		except Exception as e:
			return e 
		finally:
			r.connection.close()

	def _get(self,url,args=None,payload=None,**kwargs):
		if args:
			kwargs.update(args)
		return self._internal_calls('GET',url,payload,kwargs)

	def _post(self,url,args=None,payload=None,**kwargs):
		if args:
			kwargs.update(args)
		return self._internal_calls('POST',url,payload,kwargs)

	def _put(self,url,args=None,payload=None,**kwargs):
		if args:
			kwargs.update(args)
		return self._internal_calls('PUT',url,payload,kwargs)

	def _delete(self,url,args=None,payload=None,**kwargs):
		if args:
			kwargs.update(args)
		return self._internal_calls('DELETE',url,payload,kwargs)

	def search(self,q,limit=10,accept_langauge=None,country_codes=None):
		""" Searches a given query and converts addresses (like a street address) into 
		geographic coordinates (like latitude and longitude), which you can use to 
		place markers on a map, or position the map

		Parameters:
		    -q - Address which we want to search for
		    -limit Default is 10 - Integer value to limit the number of returned results
		    -accept_langauge - Preferred lanaguge order for showing search results Use ISO 639-1 Code (2 characters). 
		                       If the language is not available, use ISO 639-2 Code (3 characters)(Optional)
		    -country_codes -Limit search to a list of countries (Optional)
		"""

		return self._get('search.php',q=q,limit=limit,accept_langauge=accept_langauge,country_codes=country_codes)

	def reverse_geocoding(self,lat,lon,zoom=None,accept_langauge=None):
		""" Converts geographic coordinates into human-readable address
		Parameters:
		    -lat -Latitude of the location address
		    -lon -Longitude of the location address
		    -zoom -Zoom value lies between 0-18, Level of detail required
		           where 0 is country and 18 is building/house Use ISO 639-1 Code (2 characters). 
		           If the language is not available, use ISO 639-2 Code (3 characters)(Optional)
		    -accept_langauge - Preferred langauge order for showing search results
		"""

		return self._get('reverse.php',lat=lat,lon=lon,zoom=zoom,accept_langauge=accept_langauge)

	def time_zone(self,lat,lon):
		""" Provides time offset data for locations on the surface of the earth
		Parameters:
		    -lat -Latitude of the location
		    -lon -Longitude of the location
		"""

		return self._get('timezone.php',lat=lat,lon=lon)
