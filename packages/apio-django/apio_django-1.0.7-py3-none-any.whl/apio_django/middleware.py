from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
import time
import sys
import traceback
from django.conf import settings
import requests 
import json
import django

class ApioMiddleware(MiddlewareMixin):
	
	def process_exception(self, request, exception):
		"""posting error data"""
		try:
			headers = {"x-api-key": 
				settings.APIO_D["application_key"]
			}
			# collating data
			exception_data = {
				"path": request.environ["wsgi.url_scheme"] + "://" \
				+ request.environ["HTTP_HOST"] + request.get_full_path(),
				"exception": exception.__class__.__name__+ \
				": " + str(sys.exc_info()[1]),
				"traceback":traceback.format_exc(),
				"user": str(request.user),
				"ip_address": request.META.get("REMOTE_ADDR")
			}
			
			apio_url_exception = "https://apio.in/remote_data_exception"
			
			# posting data
			if exception_data["path"] != apio_url_exception:
				# Removing circular dependency
				r = requests.post(apio_url_exception, 
					data=json.dumps(exception_data), 
					headers=headers)
				print(r)

		except Exception as e:
			print(str(e))

		return None
        
	def process_request(self, request):
		"""adding timestamp"""
		request.start_timestamp = time.time()

	def process_response(self, request, response):
		"""posting request data"""
		try:
			headers = {"x-api-key": 
				settings.APIO_D["application_key"]
			}

			response_timestamp = time.time()
			apio_perf_data_url = "https://apio.in/remote_perf_data"

			# collating data
			perf_data = {
				"request_timestamp": request.start_timestamp,
				"response_timestamp": response_timestamp,
				"response_code": response.status_code,
				"path": request.environ["wsgi.url_scheme"] + "://" \
				+ request.environ["HTTP_HOST"] + request.get_full_path(),
				"requester": str(request.user.id),
				"ip_address": request.META.get("REMOTE_ADDR")
			}

			# posting data
			if perf_data["path"] != apio_perf_data_url:
				# Removing circular reference
				r = requests.post(apio_perf_data_url, 
					data=json.dumps(perf_data), 
					headers=headers)
				print(r)
		except Exception as e:
			print(str(e))

		return response

