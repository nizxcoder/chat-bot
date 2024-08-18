from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
import os
import google.generativeai as genai
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages

# Set the API key as an environment variable
os.environ["API_KEY"] = "AIzaSyBLNiNdiYtZp05UggyVL9I9zaY_KwYBEnA"

# Configure the genai library using the environment variable
genai.configure(api_key=os.environ["API_KEY"])

# Load the model (assuming a model similar to GPT-4)
gen_model = genai.GenerativeModel('gemini-1.5-flash')

def index(request):
    return render(request, "home.html")

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            auth_login(request, user)
            messages.success(request, "Login Successful!")
            return redirect('model')
        else:
            messages.error(request, "Login Denied! Please retry.")
            return redirect('home')
    #return render(request, "login2.html")
    return HttpResponse("404!") 

def signup(request):
    return render(request, "signup2.html")

def model(request):
    return render(request, "model2.html")

def testbase(request):
    return render(request, "base.html")
def logout(request):
    return redirect('home')

def chat_with_model(request):
    if request.method == 'POST':
        prompt = request.POST.get('prompt', '')
        if prompt:
           
            response = gen_model.generate_content(prompt)
            
            formatted_response = format_response(response.text)
            
            return JsonResponse({'response': formatted_response})
    
    return JsonResponse({'response': 'Invalid request'}, status=400)

def format_response(text):
    # Replace newlines with HTML line breaks
    formatted_text = text.replace('\n', '<br>')
    
    # Bold and italic formatting (assuming the text uses markdown-like syntax)
    formatted_text = formatted_text.replace('**', '<b>').replace('**', '</b>')
    formatted_text = formatted_text.replace('*', '<i>').replace('*', '</i>')
    
    # Convert markdown-style links to clickable HTML links
    formatted_text = replace_links(formatted_text)
    
    return formatted_text

def replace_links(text):
    # Find and replace links with clickable HTML links using regex
    import re
    pattern = r'\[([^\]]+)\]\((https?://[^\)]+)\)'
    return re.sub(pattern, r'<a href="\2" target="_blank">\1</a>', text)