from django.shortcuts import render, redirect, get_object_or_404
from .models import Article
from .forms import ArticleForm

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

from rest_framework import viewsets
from .serializers import ArticleSerializer
from rest_framework.permissions import IsAuthenticated

def hello_world(request):
    return render(request, 'hello.html')

def article_list(request):
    articles = Article.objects.all()
    return render(request, 'articles.html', {'articles': articles})

def add_article(request):
    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():  
            form.save()  
            return redirect('article_list')  
    else:
        form = ArticleForm()
    
    return render(request, 'add_article.html', {'form': form})

def edit_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    
    if request.method == "POST":
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect('article_list')
    else:
        form = ArticleForm(instance=article)
    
    return render(request, 'edit_article.html', {'form': form, 'article': article})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) 
            return redirect('article_list') 
    else:
        form = UserCreationForm()
    
    return render(request, 'registration/register.html', {'form': form})

@login_required
def add_article(request):
    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('article_list')
    else:
        form = ArticleForm()
    
    return render(request, 'add_article.html', {'form': form})

@login_required
def edit_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    
    if request.method == "POST":
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect('article_list')
    else:
        form = ArticleForm(instance=article)
    
    return render(request, 'edit_article.html', {'form': form, 'article': article})

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()  
    serializer_class = ArticleSerializer  
    permission_classes = [IsAuthenticated] 