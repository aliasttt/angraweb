from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.utils import translation
from .models import (
    Service, Package, Project, ProjectVideo, Certificate,
    ContactMessage, QuoteRequest, BlogPost, Testimonial, SiteSetting, TeamMember, UserProfile
)
from .forms import ContactForm, QuoteRequestForm, UserRegistrationForm


def get_language_context(request):
    """دریافت زبان فعلی و تنظیمات مربوطه"""
    from django.utils import translation
    lang = translation.get_language() or 'tr'
    return {
        'current_lang': lang,
        'is_rtl': lang in ['fa', 'ar']
    }


def index(request):
    """صفحه اصلی"""
    services = Service.objects.filter(active=True).order_by('order')[:6]
    packages = Package.objects.filter(active=True).order_by('order')
    projects = Project.objects.filter(active=True, featured=True).order_by('order')[:6]
    testimonials = Testimonial.objects.filter(active=True, featured=True).order_by('order')[:3]
    blog_posts = BlogPost.objects.filter(published=True).order_by('-published_at')[:3]
    
    context = {
        'services': services,
        'packages': packages,
        'projects': projects,
        'testimonials': testimonials,
        'blog_posts': blog_posts,
    }
    context.update(get_language_context(request))
    return render(request, 'main/index.html', context)


def services_list(request):
    """لیست خدمات"""
    services = Service.objects.filter(active=True).order_by('order')
    context = {
        'services': services,
    }
    context.update(get_language_context(request))
    return render(request, 'main/services.html', context)


def service_detail(request, slug):
    """جزئیات یک خدمت"""
    service = get_object_or_404(Service, slug=slug, active=True)
    related_services = Service.objects.filter(
        active=True,
        service_type=service.service_type
    ).exclude(id=service.id)[:3]
    
    context = {
        'service': service,
        'related_services': related_services,
    }
    context.update(get_language_context(request))
    return render(request, 'main/service_detail.html', context)


def web_design(request):
    """صفحه طراحی وبسایت"""
    services = Service.objects.filter(service_type='web_design', active=True)
    projects = Project.objects.filter(project_type='web', active=True).order_by('-created_at')[:6]
    
    context = {
        'services': services,
        'projects': projects,
        'page_title': 'طراحی وبسایت',
    }
    context.update(get_language_context(request))
    return render(request, 'main/web_design.html', context)


def mobile_app(request):
    """صفحه طراحی اپلیکیشن موبایل"""
    services = Service.objects.filter(service_type='mobile_app', active=True)
    projects = Project.objects.filter(project_type='mobile', active=True).order_by('-created_at')[:6]
    
    context = {
        'services': services,
        'projects': projects,
        'page_title': 'طراحی اپلیکیشن موبایل',
    }
    context.update(get_language_context(request))
    return render(request, 'main/mobile_app.html', context)


def ecommerce(request):
    """صفحه فروشگاه اینترنتی"""
    services = Service.objects.filter(service_type='ecommerce', active=True)
    projects = Project.objects.filter(project_type='ecommerce', active=True).order_by('-created_at')[:6]
    packages = Package.objects.filter(
        Q(package_type='commercial') | Q(package_type='professional'),
        active=True
    ).order_by('order')
    
    context = {
        'services': services,
        'projects': projects,
        'packages': packages,
        'page_title': 'فروشگاه اینترنتی',
    }
    context.update(get_language_context(request))
    return render(request, 'main/ecommerce.html', context)


def seo_services(request):
    """صفحه خدمات سئو"""
    services = Service.objects.filter(service_type='seo', active=True)
    
    context = {
        'services': services,
        'page_title': 'سئو و بهینه‌سازی',
    }
    context.update(get_language_context(request))
    return render(request, 'main/seo.html', context)


def hosting_services(request):
    """صفحه خدمات هاستینگ"""
    services = Service.objects.filter(service_type='hosting', active=True)
    
    context = {
        'services': services,
        'page_title': 'هاستینگ و دامنه',
    }
    context.update(get_language_context(request))
    return render(request, 'main/hosting.html', context)


def ui_ux_design(request):
    """صفحه طراحی UI/UX"""
    services = Service.objects.filter(service_type='ui_ux', active=True)
    projects = Project.objects.filter(active=True).order_by('-created_at')[:6]
    
    context = {
        'services': services,
        'projects': projects,
        'page_title': 'طراحی UI/UX',
    }
    context.update(get_language_context(request))
    return render(request, 'main/ui_ux.html', context)


def packages_list(request):
    """لیست پکیج‌ها"""
    packages = Package.objects.filter(active=True).order_by('order')
    context = {
        'packages': packages,
    }
    context.update(get_language_context(request))
    return render(request, 'main/packages.html', context)


def about(request):
    """صفحه درباره ما"""
    certificates = Certificate.objects.filter(active=True).order_by('order')
    testimonials = Testimonial.objects.filter(active=True).order_by('order')[:6]
    
    context = {
        'certificates': certificates,
        'testimonials': testimonials,
    }
    context.update(get_language_context(request))
    return render(request, 'main/about.html', context)


def projects_list(request):
    """لیست پروژه‌ها"""
    projects = Project.objects.filter(active=True).order_by('-created_at')
    videos = ProjectVideo.objects.filter(active=True).order_by('order')
    
    # Pagination
    paginator = Paginator(projects, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'projects': page_obj,
        'videos': videos,
    }
    context.update(get_language_context(request))
    return render(request, 'main/projects.html', context)


def project_detail(request, slug):
    """جزئیات پروژه"""
    project = get_object_or_404(Project, slug=slug, active=True)
    related_projects = Project.objects.filter(
        active=True,
        project_type=project.project_type
    ).exclude(id=project.id)[:3]
    
    context = {
        'project': project,
        'related_projects': related_projects,
    }
    context.update(get_language_context(request))
    return render(request, 'main/project_detail.html', context)


def resume(request):
    """صفحه رزومه"""
    certificates = Certificate.objects.filter(active=True).order_by('order')
    context = {
        'certificates': certificates,
    }
    context.update(get_language_context(request))
    return render(request, 'main/resume.html', context)


def team(request):
    """صفحه تیم"""
    team_members = TeamMember.objects.filter(active=True).order_by('order', 'created_at')
    context = {
        'team_members': team_members,
    }
    context.update(get_language_context(request))
    return render(request, 'main/team.html', context)


def contact(request):
    """صفحه تماس"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_message = form.save(commit=False)
            # Get IP address and user agent
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                contact_message.ip_address = x_forwarded_for.split(',')[0]
            else:
                contact_message.ip_address = request.META.get('REMOTE_ADDR')
            contact_message.user_agent = request.META.get('HTTP_USER_AGENT', '')
            contact_message.save()
            messages.success(request, 'پیام شما با موفقیت ارسال شد. به زودی با شما تماس خواهیم گرفت.')
            return redirect('contact')
    else:
        form = ContactForm()
    
    context = {
        'form': form,
    }
    context.update(get_language_context(request))
    return render(request, 'main/contact.html', context)


def quote_request(request):
    """درخواست قیمت"""
    if request.method == 'POST':
        form = QuoteRequestForm(request.POST)
        if form.is_valid():
            quote = form.save()
            messages.success(request, 'درخواست شما با موفقیت ثبت شد. به زودی با شما تماس خواهیم گرفت.')
            return redirect('quote_request')
    else:
        form = QuoteRequestForm()
    
    packages = Package.objects.filter(active=True).order_by('order')
    
    context = {
        'form': form,
        'packages': packages,
    }
    context.update(get_language_context(request))
    return render(request, 'main/quote_request.html', context)


def blog_list(request):
    """لیست وبلاگ"""
    posts = BlogPost.objects.filter(published=True).order_by('-published_at')
    
    # Search
    search_query = request.GET.get('search', '')
    if search_query:
        posts = posts.filter(
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(posts, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'posts': page_obj,
        'search_query': search_query,
    }
    context.update(get_language_context(request))
    return render(request, 'main/blog.html', context)


def blog_detail(request, slug):
    """جزئیات پست وبلاگ"""
    post = get_object_or_404(BlogPost, slug=slug, published=True)
    
    # Increase views
    post.views += 1
    post.save(update_fields=['views'])
    
    # Related posts
    related_posts = BlogPost.objects.filter(
        published=True
    ).exclude(id=post.id)[:3]
    
    context = {
        'post': post,
        'related_posts': related_posts,
    }
    context.update(get_language_context(request))
    return render(request, 'main/blog_detail.html', context)


def register(request):
    """ثبت‌نام کاربر"""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'ثبت‌نام با موفقیت انجام شد!')
            return redirect('index')
    else:
        form = UserRegistrationForm()
    
    context = {
        'form': form,
    }
    context.update(get_language_context(request))
    return render(request, 'main/register.html', context)


def user_login(request):
    """ورود کاربر"""
    if request.method == 'POST':
        from django.contrib.auth import authenticate
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.POST.get('next') or request.GET.get('next') or request.META.get('HTTP_REFERER') or 'index'
            # Avoid redirect loop back to login
            if not next_url or 'login' in str(next_url):
                next_url = 'index'
            return redirect(next_url)
        else:
            messages.error(request, 'نام کاربری یا رمز عبور اشتباه است.')
    
    context = {}
    context.update(get_language_context(request))
    return render(request, 'main/login.html', context)


@login_required
def dashboard(request):
    """داشبورد کاربر — اطلاعات و فعالیت‌ها"""
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        profile = None
    context = {'profile': profile}
    context.update(get_language_context(request))
    return render(request, 'main/dashboard.html', context)


@login_required
def user_logout(request):
    """خروج کاربر"""
    logout(request)
    messages.success(request, 'با موفقیت خارج شدید.')
    return redirect('index')


def set_language(request, lang_code):
    """تغییر زبان — Switch site language and persist in session/cookie."""
    from django.conf import settings
    from django.utils import translation
    from django.urls import translate_url

    if lang_code in ['tr', 'en', 'fa', 'ar']:
        translation.activate(lang_code)
        # Use Django's LANGUAGE_SESSION_KEY (default: '_language') so LocaleMiddleware picks it up
        session_key = getattr(settings, 'LANGUAGE_SESSION_KEY', '_language')
        if hasattr(request, 'session'):
            request.session[session_key] = lang_code
        request.LANGUAGE_CODE = lang_code

        referer = request.META.get('HTTP_REFERER')
        next_url = request.GET.get('next') or referer or '/'
        try:
            next_url = translate_url(next_url, lang_code) or next_url
        except Exception:
            pass
        response = redirect(next_url)
        response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang_code, max_age=365 * 24 * 60 * 60)
        return response
    return redirect('index')
