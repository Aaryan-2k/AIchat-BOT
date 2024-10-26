from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import PyPDF2
import google.generativeai as genai
genai.configure(api_key="AIzaSyCrxJ9Mnl21_AQIa4doklb7YEwNNs5MC5Y")#will be set in env variables for sec purpose
model = genai.GenerativeModel("gemini-1.5-flash")

@csrf_exempt
def extract_text_from_pdf(uploaded_pdf):
    pdf_text = ""
    pdf_reader = PyPDF2.PdfReader(uploaded_pdf)
    for page in pdf_reader.pages:
        pdf_text += page.extract_text()
    return pdf_text
@csrf_exempt
def rag(request):
    pdf=request.FILES.get('pdf')
    question = request.POST.get("question")
    chat=request.POST.get("chat")
    pdf_text=extract_text_from_pdf(pdf)
    ai_msg=ai_response(pdf_text,question,chat)
    return JsonResponse(ai_msg, safe=True)

@csrf_exempt
def ai_response(pdf,ques,chat):
    prompt=f"""i will provide you the pdf data based on which u have to answer the question/query user gave accordingly also u can take help from your llm and also u can get context from previous chats i have provided
            PDF-DATA: {pdf}
            Question/query/comment: {ques}
            chat:{chat}"""
    res=model.generate_content(prompt)
    response_text=res.text
    return {"text": response_text}
