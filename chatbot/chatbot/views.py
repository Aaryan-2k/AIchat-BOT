from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import google.generativeai as genai
import json
genai.configure(api_key="AIzaSyCrxJ9Mnl21_AQIa4doklb7YEwNNs5MC5Y")#will be set in env variables for sec purpose
model = genai.GenerativeModel("gemini-1.5-flash")

@csrf_exempt
def ai_response(request):
    if request.method=="POST":
        try:
            data=json.loads(request.body)
            question=data.get("question")
            chat=data.get("chat", [])
            prompt=f"""You are the assistant to whom i will give chat for context and 1 question u have to answer the question with help of your large language model at the same time in the context of chat given dont write chat and question in your answer
                         Chat: {chat}
                         Question: {question}"""
            res=model.generate_content(prompt)
            response_text=res.text
            print(response_text)
            return JsonResponse({"text": response_text}, safe=True)
        except Exception as e:
            return JsonResponse({"error":str(e)}, status=500)
    return JsonResponse({"error": "Invalid request method."}, status=405)
