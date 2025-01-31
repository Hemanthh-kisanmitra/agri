
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import json
import requests
import markdown
import bleach

# Replace with your actual API details
AUTH_TOKEN = os.environ.get('AUTH_TOKEN')
API_URL = os.environ.get('API_URL')

@csrf_exempt
def chat_api(request):
    if request.method == "POST":
        try:
            # Parse the incoming JSON data
            data = json.loads(request.body)
            user_message = data.get("message", "")

            # Prepare the payload for the external API
            payload = {
                "input_value": user_message,
                "output_type": "chat",
                "input_type": "chat"
            }

            # Set up headers
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {AUTH_TOKEN}"
            }

            # Make the API call
            response = requests.post(API_URL, json=payload, headers=headers)

            if response.status_code == 200:
                response_data = response.json()

                # Extract the bot's response
                bot_message = response_data.get("outputs", [])[0].get("outputs", [])[0].get("results", {}).get("message", {}).get("text", "")

                # Convert markdown to HTML
                html_content = markdown.markdown(bot_message)

                # Sanitize HTML to prevent XSS
                allowed_tags = ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ul', 'ol', 'li',
                              'strong', 'em', 'code', 'pre', 'blockquote', 'a', 'br']
                allowed_attributes = {'a': ['href']}
                clean_html = bleach.clean(html_content,
                                       tags=allowed_tags,
                                       attributes=allowed_attributes)

                return JsonResponse({
                    "message": bot_message,  # Original markdown
                    "html": clean_html       # Sanitized HTML version
                }, status=200)

            return JsonResponse({"error": "API Error", "details": response.text},
                              status=response.status_code)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)

def chat_interface(request):
    """Render the chat interface page."""
    return render(request, 'chat.html')