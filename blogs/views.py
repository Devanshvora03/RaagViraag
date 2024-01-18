from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseNotAllowed
from django.views.generic import ListView, DetailView
from django.shortcuts import render, redirect
from django.shortcuts import reverse
from django.contrib.auth import logout
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q
from django.views import View
from .models import *
from .forms import *

PAGE_SIZE = 10

def contact(request):
    return render(request, 'contact.html')

def about(request):
    about_content = AboutContent.objects.first()
    admin_info_list = AdminInfo.objects.all()

    context = {
        'about_content': about_content,
        'admin_info_list': admin_info_list,
    }

    return render(request, 'about.html', context)

def category(request) :
    category_posts = Post.objects.all()
    return render(request, 'categories.html',{"category_posts" : category_posts})
    
    
def blog_detail(request,slug):
    blog = Post.objects.get(slug=slug)
    latestpost_list = Post.objects.all().order_by('-post_date')[:3]
    print("helloo",blog.slug)
    return render(request, 'blog-detail.html',{"blog" : blog , "latestpost_list" : latestpost_list})

class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'register.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(to='/')

        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')

            return redirect(to='login')

        return render(request, self.template_name, {'form': form})

@login_required
def splash_screen(request):
    return render(request, 'splash_screen.html')

def custom_logout(request):
    logout(request)
    # Redirect to the homepage or any other desired URL after logout
    return redirect('index')  # Replace 'index' with the name of your home page URL pattern


class CustomLoginView(LoginView):
    form_class = LoginForm

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')

        if not remember_me:
            self.request.session.set_expiry(0)
            self.request.session.modified = True

        response = super(CustomLoginView, self).form_valid(form)

        return redirect(reverse('splash_screen'))


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'password_reset.html'
    email_template_name = 'password_reset_email.html'
    subject_template_name = 'password_reset_subject'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('index')


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('index')


class BlogListView(ListView):
    model = Post
    template_name = 'index.html'
    context_object_name = 'posts'
    paginate_by = PAGE_SIZE

    def get_context_data(self, *args, **kwargs):
        cat_list = Categories.objects.all()
        latestpost_list = Post.objects.all().order_by('-post_date')[:3]
        star_post = Post.objects.first()  # Get the first post or None
        sidebar_content = SidebarContent.objects.first()  # Get the first SidebarContent instance

        context = super().get_context_data(*args, **kwargs)
        context["cat_list"] = cat_list
        context["latestpost_list"] = latestpost_list
        context["star_post"] = star_post
        context["sidebar_content"] = sidebar_content
        return context


class BlogDetailView(DetailView):
    model = Post
    template_name = 'blog-details.html'

    def get_context_data(self, *args, **kwargs):
        cat_list = Categories.objects.all()
        latestpost_list = Post.objects.all().order_by('-post_date')[:3]
        sidebar_content = SidebarContent.objects.first()  # Get the first SidebarContent instance

        context = super().get_context_data(*args, **kwargs)
        context["cat_list"] = cat_list
        context["latestpost_list"] = latestpost_list
        context["blog"] = True
        context["cat_list"] = cat_list
        context["sidebar_content"] = sidebar_content
        return context


# @login_required(login_url='/login')
# def send_comment(request, slug):
#     if request.method == 'POST':
#         message = request.POST.get('message')
#         post_id = request.POST.get('post_id')        
#         post_comment = PostComment.objects.create(sender=request.user, message=message)
#         post = Post.objects.filter(id=post_id).first()
#         post.comments.add(post_comment)        
#         return redirect('blog-details', slug=slug)
#     else:
#         # Handle other HTTP methods if needed
#         return HttpResponseNotAllowed(['POST'])


def search(request):
    template = 'search_list.html'
    query = request.GET.get('q')
    if query:
        posts = Post.objects.filter(Q(title__icontains=query) | Q(body__icontains=query)).order_by('-post_date')
    else:
        posts = Post.objects.all()

    cat_list = Categories.objects.all()
    latestpost_list = Post.objects.all().order_by('-post_date')[:3]
    paginator = Paginator(posts, PAGE_SIZE)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    return render(request, 'search_list.html', {'posts': posts, 'cat_list': cat_list, 'latestpost_list': latestpost_list, 'query': query})


def CategoryView(request, slug):
   if Categories.objects.filter(slug=slug).exists():
      slug1 = slug
      cats = Categories.objects.get(slug=slug)
      category_posts = Post.objects.filter(category__slug=slug).order_by('-post_date')
      cat_list = Categories.objects.all()
      latestpost_list = Post.objects.all().order_by('-post_date')[:3]
      paginator = Paginator(category_posts, PAGE_SIZE)
      page = request.GET.get('page')
      category_posts = paginator.get_page(page)
      return render(request, 'categories.html', {'cats': cats, 'category_posts': category_posts, 'cat_list': cat_list, 'latestpost_list': latestpost_list, 'slug1' : slug1})
   else:
      raise Http404
