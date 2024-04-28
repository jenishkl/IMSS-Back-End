from django.utils.deprecation import MiddlewareMixin
from corsheaders.middleware import CorsMiddleware

class YourAsyncMiddleware(MiddlewareMixin):
    async def process_response(self, request, response_coroutine):
        response = await response_coroutine  # Await the coroutine
        # Process the response as usual (modify response object here)

        return response
