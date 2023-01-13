from django.shortcuts import render, get_object_or_404
from datetime import date
from .models import Post
from django.views.generic import ListView, DetailView
from .forms import CommentForm
from django.views import View
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.


# def index(request):
#     all_posts = Post.objects.all().order_by('-date')[:3]
#     return render(request, 'blog/index.html', {'posts': all_posts})


class StartingPageView(ListView):
    template_name = 'blog/index.html'
    model = Post
    ordering = ['-date']
    context_object_name = 'posts'

    def get_queryset(self):
        query_set = super().get_queryset()
        data = query_set[:3]
        return data


# def posts(request):
#     all_posts = Post.objects.all().order_by('-date')
#     return render(request, 'blog/posts.html', {'posts': all_posts})


class AllPostsView(ListView):
    template_name = 'blog/index.html'
    model = Post
    ordering = ['-date']
    context_object_name = 'posts'


# def single_post(request, slug):
#     # Post.objects.get(slug=slug)
#     post = get_object_or_404(Post, slug=slug)
#     return render(request, 'blog/post-detail.html', {'post': post, 'tags': post.tags.all()})


# class PostDetailView(DetailView):
#     template_name = 'blog/post-detail.html'
#     model = Post

#     def get_context_data(self, **kwargs):
#         form = CommentForm()
#         context = super().get_context_data(**kwargs)
#         context['tags'] = self.object.tags.all()
#         context['form'] = form
#         return context


class PostDetailView(View):

    def get(self, request, slug):
        post = Post.objects.get(slug=slug)
        stored_posts = request.session.get('stored_posts')

        if not stored_posts:
            is_saved = False
        else:
            is_saved = post.id in stored_posts

        context = {
            'post': post,
            'tags': post.tags.all(),
            'comments': post.comments.all().order_by('-id'),
            'form': CommentForm(),
            'is_saved': is_saved
        }
        return render(request, 'blog/post-detail.html', context)

    def post(self, request, slug):
        form = CommentForm(request.POST)
        post = Post.objects.get(slug=slug)

        stored_posts = request.session.get('stored_posts')

        if not stored_posts:
            is_saved = False
        else:
            is_saved = post.id in stored_posts

        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            return HttpResponseRedirect(reverse('single-post-page', args=[slug]))

        context = {
            'post': post,
            'tags': post.tags.all(),
            'comments': post.comments.all().order_by('-id'),
            'form': form,
            'is_saved': is_saved
        }
        return render(request, 'blog/post-detail.html', context)


class ReadLaterView(View):

    def get(self, request):
        stored_posts = request.session.get('stored_posts')
        if not stored_posts or len(stored_posts) == 0:
            return render(request, 'blog/stored-posts.html', {'posts': []})

        posts = Post.objects.filter(id__in=stored_posts)
        return render(request, 'blog/stored-posts.html', {'posts': posts})

    def post(self, request):
        post_id = int(request.POST.get('post_id'))
        stored_posts = request.session.get('stored_posts')

        if not stored_posts:
            stored_posts = []

        if post_id not in stored_posts:
            stored_posts.append(post_id)
        else:
            stored_posts.remove(post_id)

        request.session['stored_posts'] = stored_posts

        return HttpResponseRedirect('/')
