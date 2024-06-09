from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from pytube import YouTube
from django.conf import settings
import os
import openai
import assemblyai as aai
import logging
from .models import BlogPost

# Configure logging
logger = logging.getLogger(__name__)

# Load API keys from Django settings
OPENAI_API_KEY = getattr(settings, 'OPENAI_API_KEY', None)
ASSEMBLYAI_API_KEY = getattr(settings, 'ASSEMBLYAI_API_KEY', None)

openai.api_key = OPENAI_API_KEY
aai.settings.api_key = ASSEMBLYAI_API_KEY

@login_required
def index(request):
    return render(request, 'index.html') 

@csrf_exempt
def generate_blog(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            yt_link = data.get("link")
            if not yt_link:
                return JsonResponse({'error': 'No YouTube link provided'}, status=400)
        except (KeyError, json.JSONDecodeError) as e:
            logger.error(f"Invalid data sent: {e}")
            return JsonResponse({'error': 'Invalid data sent'}, status=400)

        try:
            title = yt_title(yt_link)
            transcription = get_transcription(yt_link)
            if not transcription:
                logger.error("Failed to get transcript")
                return JsonResponse({'error': 'Failed to get transcript'}, status=500)
            
            blog_content = generate_blog_content(transcription)
            if not blog_content:
                logger.error("Failed to generate blog content")
                return JsonResponse({'error': 'Failed to generate blog'}, status=500)
            
            new_blog_article = BlogPost.objects.create(
                user=request.user,
                youtube_title=title,
                youtube_link=yt_link,
                generated_content=blog_content,
            )
            new_blog_article.save()
            return JsonResponse({'content': blog_content})
        except Exception as e:
            logger.error(f"Error generating blog: {e}")
            return JsonResponse({'error': 'Internal server error'}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

def yt_title(link):
    try:
        yt = YouTube(link)
        title = yt.title 
        return title
    except Exception as e:
        logger.error(f"Error fetching YouTube title: {e}")
        return None

def generate_blog_content(transcription):
    prompt = f"Based on the following transcript from a YouTube video, write a comprehensive blog article. Write it based on the transcript, but don't make it look like a YouTube video. Make it look like a proper blog article:\n\n{transcription}\n\n"
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-instruct",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=1000
        )
        generated_content = response.choices[0].message['content'].strip()
        return generated_content
    except openai.error.RateLimitError as e:
        logger.error(f"Rate limit error: {e}")
        return None
    except Exception as e:
        logger.error(f"Error generating blog content: {e}")
        return None

def get_transcription(link):
    try:
        audio_file = download_audio(link)
        transcriber = aai.Transcriber()
        transcription = transcriber.transcribe(audio_file)
        return transcription.text
    except Exception as e:
        logger.error(f"Error getting transcription: {e}")
        return None

def download_audio(link):
    try:
        yt = YouTube(link)
        video = yt.streams.filter(only_audio=True).first()
        out_file = video.download(output_path=settings.MEDIA_ROOT)
        base, ext = os.path.splitext(out_file)
        new_file = base + '.mp3'
        if os.path.exists(new_file):
            os.remove(new_file)  # Delete the existing file
        os.rename(out_file, new_file)
        return new_file
    except Exception as e:
        logger.error(f"Error downloading audio: {e}")
        return None

@login_required
def blog_list(request):
    blog_articles = BlogPost.objects.filter(user=request.user)
    print(blog_articles)
    return render(request, 'all-blogs.html', {'blog_articles': blog_articles})
def blog_details(request,pk):
    blog_article_detail =BlogPost.objects.get(id=pk)
    if request.user == blog_article_detail.user:
        return render(request,"blog-details.html",{'blog_article_detail':blog_article_detail })
    else:
        return redirect ('/')
def userlogin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            error_message = "Invalid username or password"
            return render(request, 'login.html', {'error_message': error_message})
    return render(request, 'login.html')

def usersignup(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        repeatpassword = request.POST['repeatpassword']

        if password == repeatpassword:
            try:
                user = User.objects.create_user(username, email, password)
                user.save()
                login(request, user)
                return redirect('/')
            except Exception as e:
                logger.error(f"Error creating account: {e}")
                error_message = 'Error creating account'
                return render(request, 'signup.html', {'error_message': error_message})
        else:
            error_message = "Passwords do not match"
            return render(request, 'signup.html', {'error_message': error_message})
    return render(request, 'signup.html')

def userlogout(request):
    logout(request)
    return redirect('/')
