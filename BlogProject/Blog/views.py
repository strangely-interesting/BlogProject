from django.shortcuts import render, redirect, HttpResponseRedirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post, PostLike, PostComment, PostImage
from django.utils import timezone
from django.http import JsonResponse
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from .forms import PostForm, PostImageFormSet
from django.db.models import Count
from django.core import serializers

# Create your views here.
# Redirect to home
@login_required
def index(request):
    return redirect('Blog:home')

# Post List View on home page
class PostListView(LoginRequiredMixin,ListView):
    model = Post
    template_name = 'Blog/home.html'
    context_object_name = 'posts'
    ordering = '-post_date'
    paginate_by = 5

# Details of a post
class PostDetailView(LoginRequiredMixin,DetailView):
    model = Post
    template_name = 'Blog/postdetail.html'

# Create Post generic view with inline image forms
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'Blog/create_post.html'
    form_class = PostForm
    object = None

    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        post_image_forms = PostImageFormSet()
        return self.render_to_response(self.get_context_data(form=form,image_forms=post_image_forms))

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        image_forms = PostImageFormSet(self.request.POST,self.request.FILES)
        if form.is_valid() and image_forms.is_valid():
            return self.form_valid(form, image_forms)
        else:
            return self.form_invalid(form, image_forms)

    def form_valid(self, form, image_forms):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.post_date = timezone.now()
        self.object.save()
        post_id = self.object.id

        image_instances = image_forms.save(commit=False)
        for img in image_instances:
            img.post = self.object
            img.save()

        return redirect('Blog:post_details',pk=post_id)

    def form_invalid(self, form, image_froms):
        return self.render_to_response(self.get_context_data(form=form,image_forms=image_froms))

# Edit Post generic view
class PostEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'Blog/edit_post.html'
    form_class = PostForm
    object = None

    def get_object(self, queryset=None):
        self.object = super(PostEditView, self).get_object()
        return self.object

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = PostForm(instance=self.object)
        image_forms = PostImageFormSet(instance=self.object)
        return self.render_to_response(self.get_context_data(form=form,image_forms=image_forms))

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = PostForm(request.POST,instance=self.object)
        image_forms = PostImageFormSet(request.POST, request.FILES, instance=self.object)
        if form.is_valid() and image_forms.is_valid():
            return self.form_valid(form, image_forms)
        else:
            return self.form_invalid(form, image_forms)

    def form_valid(self, form, image_forms):
        self.object.save()
        image_instances = image_forms.save(commit=False)
        for img_dlt in image_forms.deleted_objects:
            img_dlt.delete()

        for img in image_instances:
            img.save()

        return render(self.request,'Blog/postdetail.html',context={'post': self.object})

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False

# Delete post generic view
class PostDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'Blog/delete_post.html'
    success_url = '/home/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False

# Like post
@login_required
def like_post(request):
    if request.is_ajax and request.method == 'GET':
        post_id = request.GET['post_id']
        post = Post.objects.get(pk=post_id)
        if post.postlike_set.filter(liked_by=request.user).exists():
            return JsonResponse({'user_msg':'You have already liked this post'},status=200)
        else:
            PostLike.objects.create(post=post,liked_by=request.user,liked_date_time=timezone.now())
            like_count = post.postlike_set.count()
            return JsonResponse({'like_count':like_count},status=200)
    else:
        return JsonResponse({'error':'Something went wrong'},status=400)

# Comment on post
@login_required
def add_comment(request):
    if request.is_ajax and request.method == 'GET':
        post_id = request.GET['post_id']
        comment_text = request.GET['comment_text']
        post = Post.objects.get(pk=post_id)
        PostComment.objects.create(post=post,
                                   comment_by=request.user,
                                   comment_date_time=timezone.now(),
                                   comment_text=comment_text)
        return JsonResponse({'message': 'Comment added.'}, status=200)
    else:
        return JsonResponse({'error': 'Something went wrong'}, status=400)

# Get all the unread posts
@login_required
def unread(request):
    unread_posts = request.user.unreadpost_set.all()
    return render(request,'Blog/new_posts.html', context={'unread_posts': unread_posts})

# Mark the post as read(remove from unread list)
@login_required
def mark_read(request):
    if request.is_ajax and request.method == 'GET':
        unread_post_id = request.GET['post_id']
        request.user.unreadpost_set.get(post=unread_post_id).delete()
        return JsonResponse({'message': "DELETED"}, status=200)
    else:
        return JsonResponse({'message': "Something went wrong"}, status=400)

# Mark all the posts as read at once
@login_required
def mark_all_read(request):
    if request.is_ajax and request.method == 'GET':
        request.user.unreadpost_set.all().delete()
        return JsonResponse({'message': "DELETED"}, status=200)
    else:
        return JsonResponse({'message': "Something went wrong"}, status=400)

@login_required
def get_most_liked(request):
    if request.is_ajax and request.method == 'GET':
        most_liked_posts = Post.objects.annotate(likes=Count('postlike')).order_by('-likes')
        posts = serializers.serialize("json",most_liked_posts,fields=['id','post_caption','author','post_date'])
        return JsonResponse({'posts': posts}, status=200)
    else:
        return JsonResponse({'error': "Something went wrong"}, status=400)

"""
@login_required
def create_new_post(request):
    PostImageFormSet = inlineformset_factory(Post, PostImage, fields=['image'], can_delete=False, max_num=0)
    if request.method == 'POST':
        post_form = PostForm(request.POST)
        image_forms = PostImageFormSet(request.POST,request.FILES)
        if post_form.is_valid() and image_forms.is_valid():
            post = post_form.save(commit=False)
            post.author = request.user
            post.post_date = timezone.now()
            post.save()
            image_instances = image_forms.save(commit=False)
            for img in image_instances:
                img.post = post
                img.save()

            return redirect('Blog:post_details',pk=post.id)
    else:
        post_form = PostForm()
        image_forms = PostImageFormSet()

    return render(request, 'Blog/create_post.html',context={'post_form': post_form, 'image_forms': image_forms})
"""