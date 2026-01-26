from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.utils import translation
from django.utils.translation import gettext as _
from django.contrib.auth.models import User
from django_ratelimit.decorators import ratelimit
from django_ratelimit.exceptions import Ratelimited
from .models import (
    Service, Package, Project, ProjectVideo, Certificate,
    ContactMessage, QuoteRequest, BlogPost, Testimonial, SiteSetting, TeamMember, UserProfile, FAQ, NewsletterSubscriber,
    ProcessStep, CaseStudy, TimelineEvent, Skill
)
from .forms import ContactForm, QuoteRequestForm, UserRegistrationForm, NewsletterForm


def get_language_context(request):
    """دریافت زبان فعلی و تنظیمات مربوطه — از session/cookie می‌خواند و activate می‌کند"""
    from django.conf import settings
    from django.utils import translation
    
    # اول از session بخوان (که set_language می‌نویسد)
    session_key = getattr(settings, 'LANGUAGE_SESSION_KEY', '_language')
    lang = None
    if hasattr(request, 'session'):
        lang = request.session.get(session_key)
    
    # اگر session نبود، از cookie بخوان
    if not lang:
        cookie_name = getattr(settings, 'LANGUAGE_COOKIE_NAME', 'django_language')
        lang = request.COOKIES.get(cookie_name)
    
    # اگر هیچکدام نبود، از translation.get_language() (که middleware set کرده)
    if not lang:
        lang = translation.get_language()
    
    # اگر هنوز نبود، default
    if not lang or lang not in ['tr', 'en', 'fa', 'ar']:
        lang = 'tr'
    
    # اطمینان از activate شدن زبان برای این درخواست (برای {% trans %} در template)
    if lang and lang in ['tr', 'en', 'fa', 'ar']:
        translation.activate(lang)
    
    # دیباگ: چک کن که زبان درست خوانده شده
    if settings.DEBUG:
        session_lang = request.session.get(session_key) if hasattr(request, 'session') else None
        cookie_lang = request.COOKIES.get(getattr(settings, 'LANGUAGE_COOKIE_NAME', 'django_language'))
        print(f"[get_language_context] Session: {session_lang}, Cookie: {cookie_lang}, Final: {lang}")
    
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
    
    # Statistics
    total_projects = Project.objects.filter(active=True).count()
    total_clients = Testimonial.objects.filter(active=True).values('name').distinct().count()
    total_blog_posts = BlogPost.objects.filter(published=True).count()
    
    context = {
        'services': services,
        'packages': packages,
        'projects': projects,
        'testimonials': testimonials,
        'blog_posts': blog_posts,
        'total_projects': total_projects,
        'total_clients': total_clients,
        'total_blog_posts': total_blog_posts,
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


def packages_compare(request):
    """مقایسه پکیج‌ها"""
    packages = Package.objects.filter(active=True).order_by('order')
    
    # Get all unique features across all packages
    all_features = set()
    for package in packages:
        for feature in package.features.all():
            all_features.add(feature.title)
    
    # Create a dictionary for quick lookup: package_id -> {feature_title: included}
    # Use 'yes', 'no', or None for better template handling
    package_features_dict = {}
    for package in packages:
        package_features_dict[package.id] = {}
        for feature in package.features.all():
            if feature.included:
                package_features_dict[package.id][feature.title] = 'yes'
            else:
                package_features_dict[package.id][feature.title] = 'no'
    
    context = {
        'packages': packages,
        'all_features': sorted(all_features),
        'package_features_dict': package_features_dict,
    }
    context.update(get_language_context(request))
    return render(request, 'main/packages_compare.html', context)


def about(request):
    """صفحه درباره ما"""
    certificates = Certificate.objects.filter(active=True).order_by('order')
    testimonials = Testimonial.objects.filter(active=True).order_by('order')[:6]
    timeline_events = TimelineEvent.objects.filter(active=True).order_by('-date', 'order')
    skills = Skill.objects.filter(active=True).order_by('order')
    
    # Group skills by category
    skills_by_category = {}
    for skill in skills:
        if skill.category not in skills_by_category:
            skills_by_category[skill.category] = []
        skills_by_category[skill.category].append(skill)
    
    context = {
        'certificates': certificates,
        'testimonials': testimonials,
        'timeline_events': timeline_events,
        'skills': skills,
        'skills_by_category': skills_by_category,
    }
    context.update(get_language_context(request))
    return render(request, 'main/about.html', context)


def projects_list(request):
    """لیست پروژه‌ها"""
    projects = Project.objects.filter(active=True)
    videos = ProjectVideo.objects.filter(active=True).order_by('order')
    
    # Filters
    project_type = request.GET.get('type', '')
    technology = request.GET.get('tech', '')
    
    if project_type:
        projects = projects.filter(project_type=project_type)
    
    if technology:
        projects = projects.filter(technologies__icontains=technology)
    
    projects = projects.order_by('-created_at')
    
    # Get unique project types and technologies for filters
    all_types = Project.PROJECT_TYPES
    all_technologies = set()
    for project in Project.objects.filter(active=True):
        if project.technologies:
            for tech in project.get_technologies_list():
                all_technologies.add(tech)
    
    # Pagination
    paginator = Paginator(projects, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'projects': page_obj,
        'videos': videos,
        'all_types': all_types,
        'all_technologies': sorted(all_technologies),
        'selected_type': project_type,
        'selected_tech': technology,
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


@ratelimit(key='ip', rate='5/m', method='POST', block=True)
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


@ratelimit(key='ip', rate='3/m', method='POST', block=True)
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


def _normalize_phone(s):
    return ''.join(c for c in (s or '') if c.isdigit())


def user_login(request):
    """ورود با شماره تلفن و رمز عبور — خطا به زبان فعلی"""
    if request.method == 'POST':
        phone_raw = (request.POST.get('phone') or '').strip()
        password = request.POST.get('password', '')
        key = _normalize_phone(phone_raw)
        user = None
        if key:
            for p in UserProfile.objects.exclude(phone=''):
                if _normalize_phone(p.phone) == key and p.user.check_password(password):
                    user = p.user
                    break
        if not user and phone_raw:
            u = User.objects.filter(username=phone_raw.strip()).first()
            if u and u.check_password(password):
                user = u
        if user:
            login(request, user)
            next_url = request.POST.get('next') or request.GET.get('next') or request.META.get('HTTP_REFERER') or 'index'
            if not next_url or 'login' in str(next_url):
                next_url = 'index'
            return redirect(next_url)
        messages.error(request, _('Invalid phone number or password.'))
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


def testimonials_list(request):
    """لیست نظرات مشتریان"""
    testimonials = Testimonial.objects.filter(active=True).order_by('order', '-created_at')
    
    context = {
        'testimonials': testimonials,
    }
    context.update(get_language_context(request))
    return render(request, 'main/testimonials.html', context)


def faq_list(request):
    """صفحه سوالات متداول"""
    category = request.GET.get('category', '')
    search_query = request.GET.get('search', '')
    
    faqs = FAQ.objects.filter(active=True)
    
    if category:
        faqs = faqs.filter(category=category)
    
    if search_query:
        faqs = faqs.filter(
            Q(question__icontains=search_query) |
            Q(answer__icontains=search_query)
        )
    
    faqs = faqs.order_by('order', 'created_at')
    
    # Group by category
    faqs_by_category = {}
    for faq in faqs:
        if faq.category not in faqs_by_category:
            faqs_by_category[faq.category] = []
        faqs_by_category[faq.category].append(faq)
    
    context = {
        'faqs': faqs,
        'faqs_by_category': faqs_by_category,
        'selected_category': category,
        'search_query': search_query,
        'categories': FAQ.CATEGORY_CHOICES,
    }
    context.update(get_language_context(request))
    return render(request, 'main/faq.html', context)


@ratelimit(key='ip', rate='3/m', method='POST', block=True)
def newsletter_subscribe(request):
    """ثبت‌نام در خبرنامه"""
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            subscriber = form.save(commit=False)
            # Get IP address
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                subscriber.ip_address = x_forwarded_for.split(',')[0]
            else:
                subscriber.ip_address = request.META.get('REMOTE_ADDR')
            
            # Check if already exists
            existing = NewsletterSubscriber.objects.filter(email=subscriber.email).first()
            if existing:
                if existing.subscribed:
                    messages.info(request, _('You are already subscribed to our newsletter.'))
                else:
                    existing.subscribed = True
                    existing.unsubscribed_at = None
                    existing.name = subscriber.name
                    existing.save()
                    messages.success(request, _('Welcome back! You have been resubscribed to our newsletter.'))
            else:
                subscriber.save()
                messages.success(request, _('Thank you for subscribing to our newsletter!'))
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'message': str(messages.get_messages(request))})
            return redirect(request.META.get('HTTP_REFERER', 'index'))
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'errors': form.errors})
            messages.error(request, _('Please check your email address and try again.'))
    
    return redirect('index')


def how_it_works(request):
    """صفحه فرآیند کار"""
    steps = ProcessStep.objects.filter(active=True).order_by('order', 'step_number')
    
    context = {
        'steps': steps,
    }
    context.update(get_language_context(request))
    return render(request, 'main/how_it_works.html', context)


def case_studies_list(request):
    """لیست مطالعات موردی"""
    case_studies = CaseStudy.objects.filter(active=True).order_by('order', '-created_at')
    
    # Filter by industry if provided
    industry = request.GET.get('industry', '')
    if industry:
        case_studies = case_studies.filter(client_industry__icontains=industry)
    
    # Pagination
    paginator = Paginator(case_studies, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'case_studies': page_obj,
        'selected_industry': industry,
    }
    context.update(get_language_context(request))
    return render(request, 'main/case_studies.html', context)


def case_study_detail(request, slug):
    """جزئیات مطالعه موردی"""
    case_study = get_object_or_404(CaseStudy, slug=slug, active=True)
    related_cases = CaseStudy.objects.filter(
        active=True
    ).exclude(id=case_study.id)[:3]
    
    context = {
        'case_study': case_study,
        'related_cases': related_cases,
    }
    context.update(get_language_context(request))
    return render(request, 'main/case_study_detail.html', context)


def price_calculator(request):
    """ماشین حساب قیمت پروژه"""
    context = {}
    context.update(get_language_context(request))
    return render(request, 'main/calculator.html', context)


def technology_stack(request):
    """صفحه Technology Stack"""
    context = {}
    context.update(get_language_context(request))
    return render(request, 'main/technology_stack.html', context)


def set_language(request, lang_code):
    """سوئیچ زبان — ذخیره در session و cookie. بدون translate_url چون با prefix_default_language=False مسیر /en/... وجود ندارد."""
    from django.conf import settings
    from django.utils import translation

    if lang_code not in ['tr', 'en', 'fa', 'ar']:
        return redirect('index')

    # ذخیره در session
    session_key = getattr(settings, 'LANGUAGE_SESSION_KEY', '_language')
    if hasattr(request, 'session'):
        request.session[session_key] = lang_code
        request.session.modified = True
        # اطمینان از save شدن session
        try:
            request.session.save()
        except Exception as e:
            # در صورت خطا، لاگ کن (فقط در DEBUG)
            if settings.DEBUG:
                print(f"[set_language] Session save error: {e}")

    # activate برای درخواست فعلی (اختیاری — middleware بعد از redirect می‌خواند)
    translation.activate(lang_code)

    next_url = (request.GET.get('next') or request.META.get('HTTP_REFERER') or '').strip()
    if not next_url or '/lang/' in next_url:
        next_url = '/'
    # فقط مسیرهای همون سایت (شروع با /) یا آدرس همین دامنه
    if next_url.startswith('//') or (next_url.startswith('http') and request.get_host() not in next_url):
        next_url = '/'

    response = redirect(next_url)
    # ذخیره در cookie
    cookie_name = getattr(settings, 'LANGUAGE_COOKIE_NAME', 'django_language')
    response.set_cookie(cookie_name, lang_code, max_age=365 * 24 * 60 * 60, path='/', samesite='Lax')
    
    # دیباگ: چک کن که session set شده
    if settings.DEBUG and hasattr(request, 'session'):
        saved_lang = request.session.get(session_key)
        print(f"[set_language] Set language to: {lang_code}, Session now has: {saved_lang}")
    
    return response
