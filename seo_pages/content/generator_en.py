from __future__ import annotations

import random
from typing import Dict, List, Tuple

from django.utils import timezone

from ..models import SeoPage
from ..silo_config import SERVICE_SILO_MAP
from .utils import MetaPack, cta_box, faq, h2, h3, make_meta, p, ul, word_count_from_html, clamp_text

# IMPORTANT (validation): Non-pricing pages must NOT use in content_html:
# EN: price, pricing, cost, package — use neutral wording (e.g. rates, scope, budget).

def _service_name(page: SeoPage) -> str:
    return page.service.en_name


def _service_base(page: SeoPage) -> str:
    return page.service.en_base_path


def _pillar_url(page: SeoPage) -> str:
    return f"/en/{_service_base(page)}/"


def _web_design_pillar_en(page: SeoPage) -> Dict:
    """Custom SEO pillar content for Web Design (EN) — professional, Istanbul-based, conversion-focused."""
    body: List[str] = []

    body.append(
        p(
            "A website today is not just about design. It must be fast, SEO optimized, mobile responsive, and built for conversions. "
            "At Angraweb, we develop scalable, high-performance websites and custom web applications tailored for modern businesses."
        )
    )

    body.append(h2("Why Professional Web Design Matters"))
    body.append(
        ul(
            [
                "SEO optimized website structure",
                "Responsive web design",
                "Core Web Vitals optimization",
                "Conversion-focused UX design",
                "Scalable backend architecture",
            ]
        )
    )
    body.append(
        p(
            "Google ranks performance, usability, and technical structure — not just visuals."
        )
    )

    body.append(h2("Our Web Development Process"))
    body.append(h3("Strategy & Planning"))
    body.append(p("Market research, competitor analysis, and conversion mapping."))
    body.append(h3("UI/UX Design"))
    body.append(p("User-centered design, intuitive navigation, and brand consistency."))
    body.append(h3("Custom Web Development"))
    body.append(
        ul(
            [
                f"Django web development — {{{{ link:/en/web-design/django-web-development/ }}}}",
                "Secure backend systems",
                "API integrations",
                "Custom modules",
            ]
        )
    )
    body.append(h3("SEO & Performance Optimization"))
    body.append(
        ul(
            [
                "Technical SEO setup",
                "Structured data (Schema)",
                "Speed optimization",
                "Core Web Vitals improvement",
            ]
        )
    )

    body.append(h2("Types of Websites We Build"))
    body.append(
        ul(
            [
                "Corporate websites",
                "E-commerce platforms",
                "Custom web applications",
                "Landing pages",
                "SaaS platforms",
            ]
        )
    )
    body.append(
        p(
            "Every successful project starts with defining scope and business goals. "
            f"See {{{{ link:{_guide_url(page)} }}}} for a practical workflow."
        )
    )

    body.append(h2("Istanbul-Based, Globally Focused"))
    body.append(
        p(
            "We are based in Istanbul and work with international clients across Europe and beyond. "
            "Our focus is performance-driven, SEO-ready web solutions."
        )
    )
    body.append(
        p(
            f"Local presence: {{{{ link:/en/web-design/web-design-company-istanbul/ }}}}"
        )
    )

    body.append(h2("What Affects Website Development Budget?"))
    body.append(
        ul(
            [
                "Project scope",
                "Custom features",
                "Integration complexity",
                "SEO requirements",
                "Timeline",
            ]
        )
    )
    body.append(
        p(
            "Request a consultation to get a tailored proposal. "
            f"Rates: {{{{ link:{_pricing_url(page)} }}}} · {{{{ link:{_quote_url(page)} }}}}"
        )
    )

    body.append(h2("Quick links"))
    body.append(
        ul(
            [
                f"Rates & scope: {{{{ link:{_pricing_url(page)} }}}}",
                f"Workflow: {{{{ link:{_guide_url(page)} }}}}",
                f"Request a quote: {{{{ link:{_quote_url(page)} }}}}",
            ]
        )
    )

    cluster_urls = _cluster_urls_for_service(page)
    if cluster_urls:
        body.append(h3("Topics"))
        body.append(ul([f"{{{{ link:{u} }}}}" for u in cluster_urls]))

    body.append(
        cta_box(
            "Get a Quote",
            "Ready to scale your business online? Let's build a high-performance website that converts.",
            _quote_url(page),
            "Request a scoped quote.",
            strong=True,
        )
    )

    content_html = "\n".join(body)

    faq_pairs = [
        ("How does the web design process work?", "Discovery, strategy, design, development, QA, and launch — with clear deliverables at each step."),
        ("What affects delivery timeline?", "Scope, integrations, content readiness, and approval speed. A clear scope keeps timelines predictable."),
        ("Do you provide post-launch support?", "Yes. We offer maintenance, monitoring, and iterative improvements."),
        ("What do I need for an initial quote?", "Goals, key pages/features, integrations, and a rough timeline target."),
        ("Do you work with clients outside Turkey?", "Yes. We work with international clients; communication and delivery are remote-friendly."),
        ("Why choose Django for web development?", "Django suits projects that need custom modules, roles, integrations, and scale. Secure and maintainable."),
    ]
    faq_json = faq(faq_pairs)

    meta_title = "Professional Web Design & Custom Development | Istanbul"
    meta_description = (
        "Istanbul-based web design and development: fast, SEO-optimized, mobile-responsive sites. "
        "Core Web Vitals, technical SEO, and conversion-focused UX."
    )
    meta_title = clamp_text(meta_title, 60)
    meta_description = clamp_text(meta_description, 160)

    return {
        "title": "Professional Web Design & Custom Development",
        "meta_title": meta_title,
        "meta_description": meta_description,
        "content_html": content_html,
        "faq_json": faq_json,
        "published_at": timezone.now(),
    }


def _cluster_corporate_website_en(page: SeoPage) -> Dict:
    """Custom cluster: Corporate Website Development — commercial investigation + service authority. 900–1200 words."""
    body: List[str] = []

    body.append(h2("What Is a Corporate Website?"))
    body.append(
        p(
            "A corporate website is your business’s digital front door: it builds trust, reinforces authority, and supports brand positioning. "
            "It goes beyond static information—a professional, responsive corporate site turns visitors into leads and supports both local and international reach. "
            "For B2B firms, agencies, and growing companies, it is the foundation of a credible online presence."
        )
    )
    body.append(
        p(
            f"For the full service framework, see {{{{ link:{_pillar_url(page)} }}}}."
        )
    )
    body.append(
        p(
            "When structured correctly, the site delivers both reputation and measurable outcomes: form submissions, contact requests, and core analytics in one place."
        )
    )

    body.append(h2("Why SEO-Friendly Corporate Web Design Matters"))
    body.append(
        p(
            "SEO-friendly corporate web design combines visibility with usability. Technical SEO (meta structure, sitemaps, canonicals), Core Web Vitals for fast loading, "
            "responsive design, and clear user experience directly affect search rankings and conversion. Structured data (Schema) enables rich snippets in search results."
        )
    )
    body.append(
        p(
            "Search engines use page speed, mobile fit, and content structure as ranking signals. "
            "A solid technical foundation is therefore essential for long-term organic traffic."
        )
    )
    body.append(
        ul(
            [
                "Technical SEO: heading hierarchy, internal linking, indexability",
                "Core Web Vitals: LCP, FID, CLS-focused performance",
                "Structured data: Organization, FAQ, Breadcrumb markup",
                "Responsive design: consistent experience across devices",
                "User experience: readability, CTA placement, form flows",
            ]
        )
    )

    body.append(h2("Corporate Website Development in Istanbul"))
    body.append(
        p(
            "We are an Istanbul-based team serving both local and international clients. Our corporate website projects range from Turkey-focused businesses to European and global brands. "
            "Communication and delivery are remote-friendly; on-site discovery workshops in Istanbul can be arranged when needed."
        )
    )
    body.append(
        p(
            "For businesses looking for \"Istanbul web design company\" or local SEO, we keep site structure and contact details consistent and easy to find. "
            f"Local presence and approach: {{{{ link:/en/web-design/web-design-company-istanbul/ }}}}"
        )
    )

    body.append(h2("Our Development Process"))
    body.append(
        p(
            "Delivery follows a clear sequence: strategy and discovery, information architecture and page plan, UI/UX design (mobile-first), "
            "custom development (Django when scalability or security is a priority), then QA and launch. Each phase has defined deliverables and acceptance criteria."
        )
    )
    body.append(
        ul(
            [
                "Strategy: target audience, competitors, conversion points",
                "Information architecture: page hierarchy, navigation, content plan",
                "UI/UX design: component library, responsive layouts",
                "Custom development: performance, technical SEO, HTTPS; Django for scalable backends when required",
                "QA and launch: Core Web Vitals, form and link checks",
            ]
        )
    )
    body.append(
        p(
            f"For deeper integrations or custom modules, {{{{ link:/en/web-design/custom-web-development/ }}}} is a better fit."
        )
    )
    body.append(
        p(
            "Custom modules, CRM integration, multi-language or role-based access often require a dedicated development approach rather than a fixed page set."
        )
    )

    body.append(h2("Who Needs a Corporate Website?"))
    body.append(
        p(
            "Corporate website development suits B2B companies, agencies, consultants, and growing businesses that want to strengthen brand perception, generate leads, "
            "and present a single, professional digital presence."
        )
    )
    body.append(
        ul(
            [
                "SMEs and companies targeting local or national markets",
                "B2B sales and corporate communications",
                "Agencies and consulting firms",
                "Scale-ups and growth-stage ventures",
            ]
        )
    )

    body.append(h2("Business Impact"))
    body.append(
        p(
            "Return on investment becomes measurable through trust, lead generation, and brand positioning. "
            "Analytics and conversion tracking clarify which pages and CTAs drive results."
        )
    )
    body.append(
        ul(
            [
                "Authority: consistent brand voice and secure (HTTPS) infrastructure",
                "Lead generation: forms, WhatsApp, and CTA-driven conversion points",
                "Scalability: structure that supports content and feature growth",
                "Analytics-driven optimization: data to improve performance and conversions",
            ]
        )
    )

    body.append(h2("Related pages"))
    body.append(
        ul(
            [
                f"{{{{ link:{_pillar_url(page)} }}}}",
                f"{{{{ link:{_pricing_url(page)} }}}}",
                f"{{{{ link:{_guide_url(page)} }}}}",
                f"{{{{ link:/en/web-design/custom-web-development/ }}}}",
                f"{{{{ link:/en/web-design/web-design-company-istanbul/ }}}}",
            ]
        )
    )

    body.append(h2("Must-haves for a corporate website"))
    body.append(
        p(
            "A professional corporate site is built on fast loading, responsive layout, clear contact paths, and at least one conversion form or call-to-action. "
            "HTTPS for security, basic contrast and font choices for accessibility, and a small set of clear CTAs support trust and conversion."
        )
    )
    body.append(
        ul(
            [
                "Speed and Core Web Vitals compliance",
                "Responsive pages across devices",
                "Contact form and/or WhatsApp / click-to-call",
                "HTTPS and up-to-date security",
                "Basic analytics and conversion tracking",
            ]
        )
    )

    body.append(
        cta_box(
            "Get a Quote",
            "Share your goals for a corporate website; we’ll propose a scoped plan and next steps.",
            _quote_url(page),
            "Open the quote request page.",
            strong=True,
        )
    )

    content_html = "\n".join(body)

    faq_pairs = [
        (
            "How long does corporate website delivery take?",
            "It depends on scope (number of pages, content, integrations) and approval speed. Clear acceptance criteria make timelines predictable.",
        ),
        (
            "What does SEO-friendly corporate website mean?",
            "Technical SEO (meta, sitemap, schema, speed), mobile responsiveness, and content architecture so the site is visible in search and user-focused.",
        ),
        (
            "Do you work with clients outside Istanbul?",
            "Yes. We work with international clients; communication and delivery are remote-friendly. On-site workshops in Istanbul can be arranged when useful.",
        ),
        (
            "What’s the difference between a corporate site and custom development?",
            "A corporate site usually has a fixed set of pages and basic forms/lead flows. For CRM/ERP integration, custom modules, or multi-language/multi-branch needs, custom web development is more appropriate.",
        ),
        (
            "Do you offer maintenance after launch?",
            "Yes. We offer maintenance and support for updates, security, and performance improvements.",
        ),
        (
            "What do you need to provide a quote?",
            "Goals, target audience, reference sites, and desired pages/flows are enough. We respond quickly to a short brief.",
        ),
    ]
    faq_json = faq(faq_pairs)

    meta_title = "Corporate Website Development | Professional & SEO-Ready"
    meta_description = (
        "Istanbul-based corporate web design: SEO-friendly, responsive, conversion-focused. "
        "Professional business websites and local presence."
    )
    meta_title = clamp_text(meta_title, 60)
    meta_description = clamp_text(meta_description, 160)

    return {
        "title": "Corporate Website Development — Professional & SEO-Ready Solutions",
        "meta_title": meta_title,
        "meta_description": meta_description,
        "content_html": content_html,
        "faq_json": faq_json,
        "published_at": timezone.now(),
    }


def _cluster_agency_vs_freelancer_en(page: SeoPage) -> Dict:
    """Custom cluster: Web Design Agency vs Freelancer — long-form SEO. No pricing triggers in body."""
    body: List[str] = []

    body.append(
        p(
            "When building a professional website, one of the most common questions is: should you hire a web design agency or a freelancer? "
            "The decision impacts SEO performance, scalability, technical structure, and long-term growth."
        )
    )
    body.append(
        p(
            "In competitive markets, an SEO-optimized website requires more than visual design. It requires: technical SEO setup, structured data (schema markup), "
            "internal linking architecture, Core Web Vitals optimization, responsive web design, and scalable backend development. "
            f"For the full framework, see {{{{ link:{_pillar_url(page)} }}}}."
        )
    )

    body.append(h2("What Is a Web Design Agency?"))
    body.append(
        p(
            "A web design agency operates with a team structure: UI/UX designers, developers, SEO specialists, project managers. "
            "This structure allows: strategic planning, technical performance optimization, SEO-driven architecture, and scalable systems."
        )
    )

    body.append(h2("What Is a Freelancer?"))
    body.append(
        p(
            "A freelance web developer handles the project independently. Freelancers are often suitable for: small business websites, landing pages, limited-scope projects. "
            "However, advanced technical SEO and scalability may depend entirely on individual expertise."
        )
    )
    body.append(
        p(
            f"Details on working with a freelancer: {{{{ link:/en/web-design/hire-web-developer/ }}}}."
        )
    )

    body.append(h2("SEO Perspective: Agency vs Freelancer"))
    body.append(
        p(
            "Search engines rank websites based on: page speed, Core Web Vitals, structured content, clean semantic HTML, internal linking structure, mobile usability. "
            "Agencies often implement full technical SEO frameworks. Freelancers may or may not specialize in advanced SEO infrastructure."
        )
    )

    body.append(h2("Performance & Core Web Vitals"))
    body.append(
        p(
            "Performance metrics matter: Largest Contentful Paint, Interaction latency, Layout stability, Mobile responsiveness. "
            "Agencies typically optimize: image compression, caching strategy, server configuration, database queries, asset management. "
            "Freelancer projects may vary by individual expertise."
        )
    )

    body.append(h2("Scalability & Custom Development"))
    body.append(
        p(
            "If your business plans to grow, you may require: API integrations, CRM systems, custom modules, multi-language support, advanced analytics. "
            f"Custom web development using frameworks like Django allows full control over technical structure and SEO flexibility: {{{{ link:/en/web-design/custom-web-development/ }}}}."
        )
    )

    body.append(h2("When to Choose a Freelancer"))
    body.append(
        ul(
            [
                "Small websites",
                "Limited functionality",
                "Quick launch",
                "Low technical complexity",
            ]
        )
    )

    body.append(h2("When to Choose an Agency"))
    body.append(
        ul(
            [
                "SEO-focused growth",
                "Corporate websites",
                "E-commerce platforms",
                "Custom web applications",
                "Long-term digital strategy",
            ]
        )
    )

    body.append(h2("Final Thoughts"))
    body.append(
        p(
            "A freelancer offers flexibility. An agency offers structure, scalability, and integrated expertise. "
            "If your goal is search visibility, performance, and long-term digital growth, a structured and SEO-driven approach is critical."
        )
    )

    body.append(h2("Related pages"))
    body.append(
        ul(
            [
                f"{{{{ link:{_pillar_url(page)} }}}}",
                f"{{{{ link:{_guide_url(page)} }}}}",
                f"{{{{ link:{_quote_url(page)} }}}}",
                f"{{{{ link:/en/web-design/hire-web-developer/ }}}}",
                f"{{{{ link:/en/web-design/web-development-company/ }}}}",
                f"{{{{ link:/en/web-design/web-design-company-istanbul/ }}}}",
            ]
        )
    )
    body.append(
        cta_box(
            "Get a Quote",
            "Share your goals; we'll help you choose between an agency or freelancer approach and propose a scoped plan.",
            _quote_url(page),
            "Open the quote request page.",
            strong=True,
        )
    )

    content_html = "\n".join(body)

    faq_pairs = [
        ("What's the main difference between an agency and a freelancer?", "An agency provides team structure, process, and reporting; a freelancer offers single-point, flexible communication. For strong SEO and scale, an agency is often a better fit."),
        ("For SEO, should I choose an agency or a freelancer?", "Technical SEO, Core Web Vitals, and internal linking strategy benefit from team expertise. In competitive markets, an agency approach is usually safer."),
        ("When is a freelancer enough?", "For a single landing page, a simple corporate site, or low integration needs, a freelancer can be sufficient."),
        ("What should I look for when choosing an agency in Istanbul?", "Evaluate expertise, process transparency, SEO approach, and scalability plan."),
        ("What if my project grows later?", "If you need multi-language, CRM, or custom modules, a modular architecture and agency or team model are more sustainable."),
        ("What do you need to provide a quote?", "Share your goals, scope, and preference (agency / freelancer / undecided); we'll respond with a clear proposal."),
    ]
    faq_json = faq(faq_pairs)

    meta_title = "Web Design Agency vs Freelancer | Which Is Better for SEO?"
    meta_description = (
        "Web design agency vs freelancer comparison. Technical SEO, performance, scalability and long-term digital growth explained."
    )
    meta_title = clamp_text(meta_title, 60)
    meta_description = clamp_text(meta_description, 160)

    return {
        "title": "Web Design Agency vs Freelancer: Which Is the Right Choice?",
        "meta_title": meta_title,
        "meta_description": meta_description,
        "content_html": content_html,
        "faq_json": faq_json,
        "published_at": timezone.now(),
    }


def _cluster_django_vs_php_en(page: SeoPage) -> Dict:
    """Custom cluster: Django vs PHP — technical comparison + authority. No pricing triggers."""
    body: List[str] = []

    body.append(
        p(
            "When choosing a backend technology for web development, Django and PHP are often compared. "
            "Both are powerful, but their architectural philosophy, security model, and SEO control differ significantly."
        )
    )
    body.append(
        p(
            f"For the full service structure, see {{{{ link:{_pillar_url(page)} }}}}."
        )
    )

    body.append(h2("What Is Django?"))
    body.append(
        p(
            "Django is a Python-based web framework designed for scalability, security, and clean architecture."
        )
    )
    body.append(
        ul(
            [
                "Structured project architecture",
                "Built-in admin system",
                "ORM for database abstraction",
                "Built-in security protections",
                "Clean URL routing",
                "Modular application design",
            ]
        )
    )
    body.append(
        p(
            "Django is commonly used for custom web development and scalable web applications."
        )
    )

    body.append(h2("What Is PHP?"))
    body.append(
        p(
            "PHP is a server-side scripting language widely used in web development. "
            "It powers many CMS platforms and frameworks."
        )
    )
    body.append(
        p(
            "Advantages: large ecosystem, flexible hosting options, easy for small projects. "
            "However, without structured frameworks, maintainability may vary."
        )
    )

    body.append(h2("Architecture Comparison"))
    body.append(
        p(
            "Django enforces: organized app structure, clear separation of concerns, reusable modules. "
            "PHP structure depends heavily on the chosen framework or developer discipline."
        )
    )

    body.append(h2("Security"))
    body.append(
        p(
            "Django includes built-in protection for: CSRF, XSS, SQL injection, secure session handling. "
            "Security is critical for SEO because compromised websites lose search trust."
        )
    )

    body.append(h2("SEO Infrastructure"))
    body.append(
        p(
            "Django allows: full URL control, dynamic sitemap generation, canonical management, structured data implementation, clean semantic templates. "
            "For SEO-driven websites, backend control matters."
        )
    )

    body.append(h2("Scalability"))
    body.append(
        p(
            "Django is highly suitable for: custom web applications, corporate websites, multi-language platforms, API integrations, high-traffic projects."
        )
    )
    body.append(
        p(
            f"Custom web development with Django: {{{{ link:/en/web-design/custom-web-development/ }}}}. "
            f"Django web development overview: {{{{ link:/en/web-design/django-web-development/ }}}}."
        )
    )

    body.append(h2("Final Thoughts"))
    body.append(
        p(
            "Django provides a structured, secure, and scalable foundation for modern web development. "
            "For projects requiring long-term growth, technical SEO flexibility, and modular architecture, Django offers a strong advantage."
        )
    )

    body.append(h2("Related pages"))
    body.append(
        ul(
            [
                f"{{{{ link:{_pillar_url(page)} }}}}",
                f"{{{{ link:{_guide_url(page)} }}}}",
                f"{{{{ link:{_quote_url(page)} }}}}",
                f"{{{{ link:/en/web-design/django-web-development/ }}}}",
                f"{{{{ link:/en/web-design/custom-web-development/ }}}}",
            ]
        )
    )
    body.append(
        cta_box(
            "Get a Quote",
            "Share your goals and scope; we'll help you choose between Django and PHP and propose a scoped plan.",
            _quote_url(page),
            "Open the quote request page.",
            strong=True,
        )
    )

    content_html = "\n".join(body)
    faq_pairs = [
        ("What's the main difference between Django and PHP?", "Django is a structured framework with built-in security and architecture; PHP is a language whose structure depends on the framework or project."),
        ("Which is better for SEO?", "Django offers direct control over URLs, sitemaps, and structured data. With PHP, the CMS or framework in use determines SEO capabilities."),
        ("When should I choose Django?", "For corporate sites, custom applications, multi-language setups, high traffic, and API-heavy projects, Django is a strong fit."),
        ("When is PHP enough?", "For simple content sites, small-scale projects, and quick launches, PHP is widely used."),
        ("Is there a security difference?", "Django ships with CSRF, XSS, and SQL injection protections. In PHP, security depends on developer practice and the framework used."),
        ("What do I need to provide for a quote?", "Goals, scope (pages/features), technical constraints, and preference (Django / PHP / undecided) are enough."),
    ]
    faq_json = faq(faq_pairs)

    meta_title = "Django vs PHP | Technical Comparison for Web Development"
    meta_description = (
        "Django vs PHP comparison focusing on security, scalability, SEO structure and performance architecture."
    )
    meta_title = clamp_text(meta_title, 60)
    meta_description = clamp_text(meta_description, 160)

    return {
        "title": "Django vs PHP — Which Framework Is More Scalable?",
        "meta_title": meta_title,
        "meta_description": meta_description,
        "content_html": content_html,
        "faq_json": faq_json,
        "published_at": timezone.now(),
    }


def _cluster_django_web_development_en(page: SeoPage) -> Dict:
    """Custom cluster: Django Web Development — scalable, secure, SEO-optimized. No pricing triggers."""
    body: List[str] = []

    body.append(h2("Introduction: Why Backend Architecture Matters for SEO"))
    body.append(
        p(
            "In modern web development, frontend design alone does not determine ranking, performance, or scalability. "
            "Search engines evaluate: crawl efficiency, URL structure, rendering strategy, server response time, Core Web Vitals, structured data integrity, internal linking architecture. "
            "All of these depend heavily on backend architecture."
        )
    )
    body.append(
        p(
            "Django web development offers full control over these technical layers — making it ideal for businesses that rely on organic growth and long-term digital scalability. "
            f"For the full service structure, see {{{{ link:{_pillar_url(page)} }}}}."
        )
    )

    body.append(h2("What Makes Django Different?"))
    body.append(
        p(
            "Django is not just a programming framework. "
            "It is a structured architectural system built on Python that enforces clean code organization and security standards."
        )
    )
    body.append(
        ul(
            [
                "Modular app architecture",
                "Built-in ORM for optimized database queries",
                "Explicit URL routing control",
                "Secure authentication system",
                "Middleware-based request handling",
                "Clear separation between logic, presentation, and data",
            ]
        )
    )
    body.append(
        p(
            "This structured approach prevents technical debt — a common issue in loosely structured backend environments."
        )
    )

    body.append(h2("Technical SEO Advantages of Django"))
    body.append(
        p(
            "Most websites fail at SEO not because of content — but because of architecture. Django enables:"
        )
    )
    body.append(
        ul(
            [
                "Clean URL hierarchies: full control over routing ensures logical, keyword-aligned URL structures.",
                "Crawl budget optimization: efficient routing and query optimization reduce unnecessary crawl waste.",
                "Dynamic sitemap scaling: large content platforms (10k+ URLs) can generate structured sitemaps programmatically.",
                "Canonical and hreflang management: precise multi-language SEO control with structured template logic.",
                "Server-side rendering: search engines fully understand content without JS rendering delays.",
                "Structured data automation: schema markup can be injected dynamically based on content models.",
            ]
        )
    )

    body.append(h2("Performance Engineering with Django"))
    body.append(
        p(
            "Google ranking is heavily influenced by Core Web Vitals: Largest Contentful Paint (LCP), interaction responsiveness, layout stability. "
            "Django allows backend-level optimization such as: query optimization using select_related/prefetch_related, caching strategies (Redis, per-view cache), asset compression control, lazy loading strategies, middleware-level performance tuning. "
            "Because the backend is structured, performance bottlenecks are easier to identify and resolve."
        )
    )

    body.append(h2("Security as a Ranking and Trust Signal"))
    body.append(
        p(
            "Security affects both user trust and SEO stability. Django provides built-in protection against CSRF, XSS, SQL injection, session hijacking. "
            "Compromised sites lose search visibility. A secure framework protects long-term domain authority."
        )
    )

    body.append(h2("Scalability and Long-Term Growth"))
    body.append(
        p(
            "Businesses evolve. Websites must scale. Django supports: API-first architecture, multi-language systems, multi-tenant platforms, custom admin workflows, integration with CRM, ERP, payment systems, microservice expansion."
        )
    )
    body.append(
        p(
            "This flexibility makes Django suitable for: corporate websites, SaaS platforms, high-traffic content systems, custom web applications."
        )
    )

    body.append(h2("Django vs Template-Based Systems"))
    body.append(
        p(
            "Template-based systems often limit: URL control, database modeling, structured content flexibility, advanced SEO customization. "
            "Django eliminates these limitations by offering full backend ownership. "
            "For businesses prioritizing organic growth and technical performance, backend control becomes a competitive advantage."
        )
    )

    body.append(h2("When Django Web Development Is the Right Choice"))
    body.append(
        p(
            "Django is ideal when: technical SEO matters, long-term scalability is required, custom logic is needed, performance optimization is a priority, security cannot be compromised. "
            "It is not just about building pages — it is about engineering systems."
        )
    )

    body.append(h2("Final Thoughts"))
    body.append(
        p(
            "Django web development provides a structured, secure, and scalable foundation for modern digital platforms. "
            "If your growth strategy depends on organic traffic, performance stability, and architectural control, choosing the right backend framework is not a minor decision — it is a strategic one."
        )
    )

    body.append(h2("Related pages"))
    body.append(
        ul(
            [
                f"{{{{ link:{_pillar_url(page)} }}}}",
                f"{{{{ link:{_guide_url(page)} }}}}",
                f"{{{{ link:{_quote_url(page)} }}}}",
                f"{{{{ link:/en/web-design/custom-web-development/ }}}}",
                f"{{{{ link:/en/web-design/django-vs-php/ }}}}",
            ]
        )
    )
    body.append(
        cta_box(
            "Get a Quote",
            "Share your goals and technical requirements; we'll propose a Django-based architecture and scope.",
            _quote_url(page),
            "Open the quote request page.",
            strong=True,
        )
    )

    content_html = "\n".join(body)
    faq_pairs = [
        ("When should I choose Django web development?", "When technical SEO, scalability, custom logic, performance, and security are priorities."),
        ("How does Django help with SEO?", "Full URL control, sitemaps, canonical/hreflang, server-side rendering, and structured data are manageable at the backend level."),
        ("What about performance?", "Query optimization, caching, and middleware tuning help meet Core Web Vitals targets."),
        ("Is Django secure by default?", "Yes. CSRF, XSS, SQL injection, and session security are built in."),
        ("What types of projects fit Django?", "Corporate sites, SaaS, content platforms, and integration-heavy applications."),
        ("What do I need to provide for a quote?", "Goals, scope, and technical requirements are enough."),
    ]
    faq_json = faq(faq_pairs)

    meta_title = "Django Web Development | Scalable, Secure & SEO-Optimized Systems"
    meta_description = (
        "Enterprise-grade Django web development focused on scalability, technical SEO architecture, performance optimization and secure backend engineering."
    )
    meta_title = clamp_text(meta_title, 60)
    meta_description = clamp_text(meta_description, 160)

    return {
        "title": "Django Web Development — Engineering Scalable & SEO-Driven Platforms",
        "meta_title": meta_title,
        "meta_description": meta_description,
        "content_html": content_html,
        "faq_json": faq_json,
        "published_at": timezone.now(),
    }


def _pricing_url(page: SeoPage) -> str:
    return f"/en/{_service_base(page)}/pricing/"


def _guide_url(page: SeoPage) -> str:
    return f"/en/{_service_base(page)}/guide/"


def _quote_url(page: SeoPage) -> str:
    return f"/en/{_service_base(page)}/get-quote/"


def _cluster_urls_for_service(page: SeoPage) -> List[str]:
    cfg = SERVICE_SILO_MAP.get(page.service.key, {}).get("en", {})
    base = _service_base(page)
    return [f"/en/{base}/{slug}/" for slug in cfg.get("clusters", [])]


def _topic_for_cluster_slug(service_key: str, slug: str) -> Tuple[str, List[str], List[str]]:
    mapping = {
        "web-design-services": ("Web Design Services", ["Brand consistency", "Conversion-focused pages", "Performance and accessibility"], ["IA and page structure", "Design system", "Reusable components", "Technical SEO baseline"]),
        "web-design-agency": ("Web Design Agency", ["Process transparency", "Delivery quality", "Long-term support"], ["Discovery workshop", "Sprint plan", "QA checklist"]),
        "web-development-company": ("Web Development Company", ["Engineering depth", "Stakeholder communication", "Reliable delivery"], ["Architecture plan", "Implementation roadmap", "Release process"]),
        "corporate-website-development": ("Corporate Website Development", ["Multiple stakeholders", "Content governance", "Security requirements"], ["Content model", "Roles/permissions", "Analytics foundation"]),
        "custom-web-development": ("Custom Web Development", ["Integrations", "Scalability", "Non-standard workflows"], ["Custom modules", "API integrations", "Monitoring"]),
        "django-web-development": ("Django Web Development", ["Secure foundations", "Maintainability", "Admin workflows"], ["App structure", "Permissions", "Admin CMS", "Deployment plan"]),
        "hire-web-developer": ("Hire a Web Developer", ["Skill verification", "Speed vs quality balance"], ["Interview checklist", "Trial sprint plan"]),
        "web-design-company-istanbul": ("Web Design Company in Istanbul", ["Local competition", "Fast communication"], ["Local-focused proposal", "Reference approach"]),
        "what-is-web-design": ("What Is Web Design?", ["Foundations", "Common misconceptions"], ["Core concepts", "Practical examples"]),
        "how-to-build-a-website": ("How to Build a Website", ["Scope clarity", "Content readiness"], ["Step-by-step workflow", "Risk checklist"]),
        "custom-website-vs-template": ("Custom Website vs Template", ["Budget vs flexibility", "Time-to-market"], ["Decision matrix", "Scenario guidance"]),
        "django-vs-php": ("Django vs PHP", ["Team skill set", "Security posture"], ["Comparison table", "Fit-by-project notes"]),
        "react-native-app-development": ("React Native App Development", ["Single codebase strategy", "Release velocity"], ["MVP plan", "Store readiness", "Telemetry"]),
        "android-app-development": ("Android App Development", ["Device fragmentation", "Performance"], ["Testing strategy", "Release plan"]),
        "ios-app-development": ("iOS App Development", ["App Store compliance", "UX patterns"], ["Submission checklist", "Versioning"]),
        "custom-mobile-app-development": ("Custom Mobile App Development", ["Business alignment", "Roadmap clarity"], ["Product roadmap", "Architecture"]),
        "mobile-app-development-company": ("Mobile App Development Company", ["Cross-functional delivery", "Quality assurance"], ["Team composition", "Delivery milestones"]),
        "what-is-mobile-app-development": ("What Is Mobile App Development?", ["Basic concepts", "Platform choices"], ["Definitions", "Examples"]),
        "hire-mobile-app-developer": ("Hire a Mobile App Developer", ["Role fit", "Delivery reliability"], ["Interview rubric", "Pilot sprint"]),
        "react-native-vs-native": ("React Native vs Native", ["Performance", "Budget", "Timeline"], ["Decision matrix", "Use-case mapping"]),
        "cross-platform-vs-native": ("Cross-Platform vs Native", ["Long-term maintenance", "Team structure"], ["Trade-off analysis", "Recommendation guide"]),
        "mobile-app-development-cost": ("Mobile App Development Scope", ["Scope creep risk", "Hidden complexity"], ["Scope drivers list", "Planning framework"]),
        "custom-ecommerce-development": ("Custom Ecommerce Development", ["Complex catalog rules", "Integrations"], ["Custom checkout", "Inventory sync"]),
        "ecommerce-development-company": ("Ecommerce Development Company", ["Delivery confidence", "Support model"], ["SLA approach", "Release cadence"]),
        "ecommerce-platform-development": ("Ecommerce Platform Development", ["Scalability", "Operational tooling"], ["Admin workflows", "Analytics"]),
        "b2b-ecommerce-development": ("B2B Ecommerce Development", ["Product lists", "Approvals"], ["Account features", "Approval flows"]),
        "b2c-ecommerce-website": ("B2C Ecommerce Website", ["Conversion rate", "Mobile UX"], ["One-page checkout", "Promotion slots"]),
        "what-is-ecommerce": ("What Is Ecommerce?", ["Getting started", "Key terms"], ["Concepts", "Starter checklist"]),
        "ecommerce-website-guide": ("Ecommerce Website Guide", ["Step order", "Launch readiness"], ["Process map", "Launch checklist"]),
        "ecommerce-website-cost": ("Ecommerce Website Scope", ["Scope drivers", "Scope clarity"], ["Budget framework", "Planning checklist"]),
        "ecommerce-pricing": ("Ecommerce Scope & Tiers", ["Tier approach", "Scope tiers"], ["Tier definitions", "Trade-offs"]),
        "custom-vs-template-ecommerce": ("Custom vs Template Ecommerce", ["Speed vs flexibility", "Total investment"], ["Decision matrix", "Scenario fit"]),
        "technical-seo-services": ("Technical SEO Services", ["Crawl efficiency", "Indexation health"], ["Fix list", "Monitoring plan"]),
        "on-page-seo-services": ("On-Page SEO Services", ["Content structure", "Internal linking"], ["Template rules", "Content briefs"]),
        "seo-consultancy": ("SEO Consultancy", ["Prioritization", "Reporting"], ["Roadmap", "Monthly reporting"]),
        "seo-pricing": ("SEO Scope & Tiers", ["Scope tiers", "Retainer planning"], ["Tier approach", "Scope framework"]),
        "seo-cost": ("SEO Scope & Planning", ["Expectations", "Trade-offs"], ["Scope drivers", "Planning model"]),
        "what-is-seo": ("What Is SEO?", ["Core concepts", "How it works"], ["Definitions", "Examples"]),
        "how-seo-works": ("How SEO Works", ["Ranking factors", "Practical workflow"], ["Process outline", "Checklist"]),
        "hire-seo-expert": ("Hire an SEO Expert", ["Skill verification", "Strategy fit"], ["Interview checklist", "Pilot plan"]),
        "seo-audit": ("SEO Audit", ["Issue discovery", "Quick wins"], ["Audit report", "Priority list"]),
        "seo-for-django-sites": ("SEO for Django Sites", ["Rendering and performance", "Routing and canonicals"], ["Technical checklist", "Implementation plan"]),
        "web-hosting-services": ("Web Hosting Services", ["Reliability", "Security"], ["Backups", "Monitoring"]),
        "vps-hosting": ("VPS Hosting", ["Resource sizing", "Ops overhead"], ["Setup plan", "Hardening"]),
        "dedicated-server-hosting": ("Dedicated Server Hosting", ["Performance", "Budget control"], ["Sizing guide", "SLA"]),
        "cloud-hosting": ("Cloud Hosting", ["Elastic scaling", "Resilience"], ["Automation", "Redundancy"]),
        "django-hosting": ("Django Hosting", ["Deployment stability", "Security"], ["Release pipeline", "Ops checklist"]),
        "domain-registration": ("Domain Registration", ["Right domain choice", "DNS management"], ["Registration steps", "DNS checklist"]),
        "ssl-certificate": ("SSL Certificate", ["Browser trust", "TLS configuration"], ["Setup steps", "Renewal plan"]),
        "linux-server-setup": ("Linux Server Setup", ["Hardening", "Performance"], ["Setup checklist", "Security baseline"]),
        "web-hosting-pricing": ("Web Hosting Plans", ["Plan comparison", "Hidden limits"], ["Selection factors", "Selection guide"]),
        "vps-hosting-cost": ("VPS Hosting Plans", ["Sizing accuracy", "Budget planning"], ["Scope drivers", "Example tiers"]),
        "ui-ux-design-services": ("UI/UX Design Services", ["User clarity", "Design consistency"], ["Design system", "Prototype"]),
        "user-experience-design": ("User Experience Design", ["Research", "Journey clarity"], ["User flows", "Testing plan"]),
        "user-interface-design": ("User Interface Design", ["Component consistency", "Accessibility"], ["Component library", "Style guide"]),
        "what-is-ui-ux": ("What Is UI/UX?", ["Basic definitions", "Common pitfalls"], ["Concepts", "Examples"]),
        "figma-design": ("Figma Design", ["Collaboration", "Version control"], ["Component sets", "Documentation"]),
        "wireframe-design": ("Wireframe Design", ["Fast validation", "IA clarity"], ["Wireframes", "Flow map"]),
        "prototype-design": ("Prototype Design", ["Testability", "Stakeholder alignment"], ["Interactive prototype", "Handoff notes"]),
        "mobile-app-ui-design": ("Mobile App UI Design", ["Platform patterns", "Usability"], ["Screen set", "Prototype"]),
        "ui-ux-pricing": ("UI/UX Scope & Tiers", ["Scope tiers", "Deliverables"], ["Tier definitions", "Scope checklist"]),
        "ux-research": ("UX Research", ["Insights", "Decision support"], ["Interviews", "Analysis"]),
    }
    if slug in mapping:
        return mapping[slug]
    title = " ".join([w.capitalize() for w in (slug or "").replace("-", " ").split()])
    return (title, ["Scope clarity", "Delivery reliability", "Quality control"], ["Plan", "Implementation", "Acceptance criteria"])


def _pick_sibling_clusters(page: SeoPage, n: int = 2) -> List[str]:
    cfg = SERVICE_SILO_MAP.get(page.service.key, {}).get("en", {})
    slugs = list(cfg.get("clusters", []))
    if page.slug not in slugs or len(slugs) < 2:
        return []
    idx = slugs.index(page.slug)
    picks = []
    for i in range(1, n + 1):
        picks.append(slugs[(idx + i) % len(slugs)])
    base = _service_base(page)
    return [f"/en/{base}/{s}/" for s in picks]


def _ensure_word_target(page: SeoPage, html: str, min_words: int, max_words: int, seed: str) -> str:
    rnd = random.Random(seed + ":pad")
    wc = word_count_from_html(html)
    if wc >= min_words:
        return html

    def chunk_delivery() -> str:
        return "\n".join(
            [
                h2("Delivery standards and acceptance criteria"),
                p(
                    "High-quality delivery starts with measurable acceptance criteria. When goals are translated into explicit checks—"
                    "flows, performance, accessibility, and security—teams make faster decisions and reduce rework."
                ),
                p(
                    "Acceptance criteria should guide implementation, not just final review. This keeps scope stable and makes timelines predictable."
                ),
                ul(
                    [
                        "Critical journeys: validated end-to-end",
                        "Performance: baseline targets and optimization plan",
                        "Content structure: consistent templates and hierarchy",
                        "Security: permissions and basic hardening",
                    ]
                ),
            ]
        )

    def chunk_ops() -> str:
        return "\n".join(
            [
                h2("Operating rhythm: communication and reporting"),
                p(
                    "A reliable operating rhythm reduces surprises. Weekly summaries, clear priorities, and written decisions help stakeholders stay aligned."
                ),
                p(
                    "We keep delivery transparent through milestones, a visible backlog, and explicit definitions of done."
                ),
                ul(
                    [
                        "Weekly update: shipped items and blockers",
                        "Next steps: this week / next week priorities",
                        "Risks: dependencies, content readiness, integration uncertainty",
                        "Definition of done: agreed acceptance checks",
                    ]
                ),
            ]
        )

    def chunk_ia() -> str:
        return "\n".join(
            [
                h2("Information architecture and internal linking"),
                p(
                    "A strong structure improves both usability and search visibility. A clear hub page connected to focused topic pages"
                    " creates a predictable path for users and crawlers."
                ),
                p(f"Use the overview at {{ link:{_pillar_url(page)} }} and the workflow at {{ link:{_guide_url(page)} }} to align the structure."),
                ul(
                    [
                        "Pillar → all cluster pages",
                        "Guide → 6–10 selected clusters",
                        "Cluster → pillar + relevant pages + 1–2 sibling topics",
                        "Quote → pillar and scope pages",
                    ]
                ),
            ]
        )

    def chunk_scope() -> str:
        return "\n".join(
            [
                h2("Scope definition: a practical method"),
                p(
                    "Scope is not only a list of features—it’s a boundary. Clear boundaries make estimates reliable and prevent uncontrolled expansion."
                ),
                p(
                    "A practical method is to split requirements into must-have, high-priority, and later-phase items, then attach acceptance checks to each."
                ),
                ul(
                    [
                        "Must-have: critical journeys and baseline functionality",
                        "High-priority: conversion and operational improvements",
                        "Later-phase: enhancements after validation",
                        "Acceptance: measurable checks per item",
                    ]
                ),
            ]
        )

    def chunk_release() -> str:
        return "\n".join(
            [
                h2("Release plan and sustainability"),
                p(
                    "Launch is the start of iteration, not the finish line. A release checklist, monitoring, and a feedback loop reduce risk in the first 30 days."
                ),
                p(
                    "Sustainability comes from operational basics: permissions, backups, performance monitoring, and a clear support path."
                ),
                ul(
                    [
                        "Checklist: critical flows, forms, redirects",
                        "Monitoring: error tracking and baseline metrics",
                        "Backups: schedule and rollback plan",
                        "Iteration: targeted improvements after launch",
                    ]
                ),
            ]
        )

    def chunk_pricing_only() -> str:
        return "\n".join(
            [
                h2("Pricing transparency: what you’re paying for"),
                p(
                    "Healthy pricing is a function of scope clarity. When deliverables are visible, it’s easier to understand what increases cost"
                    " and what can be deferred into later phases."
                ),
                p(
                    "We typically recommend MVP-first budgeting, then expanding in phases. This reduces risk and keeps estimates realistic."
                ),
                ul(
                    [
                        "Scope: modules, pages/screens, admin needs",
                        "Integrations: third-party APIs and data flows",
                        "Design depth: custom system vs adaptation",
                        "Quality work: QA depth, performance, security",
                    ]
                ),
            ]
        )

    chunks = [chunk_delivery(), chunk_ops(), chunk_ia(), chunk_scope(), chunk_release()]
    if page.page_type == SeoPage.TYPE_PRICING:
        chunks.insert(0, chunk_pricing_only())
    else:
        chunks.append(
            "\n".join(
                [
                    h2("Next step"),
                    p(
                        "To turn this into a practical plan, share a short brief with goals and priorities. We’ll propose a scoped approach and timeline."
                    ),
                    p(f"Start here: {{ link:{_quote_url(page)} }}"),
                ]
            )
        )

    blocks = [html]
    rnd.shuffle(chunks)
    i = 0
    while wc < min_words and i < 80:
        blocks.append(chunks[i % len(chunks)])
        wc = word_count_from_html("\n".join(blocks))
        i += 1
    return "\n".join(blocks)


def generate_en(page: SeoPage) -> Dict:
    svc = _service_name(page)
    seed = f"en:{page.service.key}:{page.page_type}:{page.slug}"

    if page.page_type == SeoPage.TYPE_PILLAR:
        if page.service.key == "web-design":
            return _web_design_pillar_en(page)
        title = svc
        meta = make_meta(
            title=title,
            meta_title=f"{svc} | B2B Delivery Approach",
            meta_description=f"{svc} for companies that need a clear process, measurable outcomes, and reliable delivery. Explore approach, deliverables, and next steps.",
        )
        body: List[str] = []
        body.append(h2("How we structure delivery"))
        body.append(
            p(
                "We treat delivery as a system: goals → scope → architecture → design → implementation → QA → release. "
                "Clear milestones and acceptance criteria keep work predictable."
            )
        )
        body.append(h2("What you get"))
        body.append(
            ul(
                [
                    "Discovery and scope definition",
                    "Technical plan and delivery milestones",
                    "Quality assurance and release checklist",
                    "Optional support and iteration after launch",
                ]
            )
        )
        body.append(h2("Start here"))
        body.append(
            ul(
                [
                    f"Pricing details: {{ link:{_pricing_url(page)} }}",
                    f"Implementation guide: {{ link:{_guide_url(page)} }}",
                    f"Request a quote: {{ link:{_quote_url(page)} }}",
                ]
            )
        )
        cluster_urls = _cluster_urls_for_service(page)
        if cluster_urls:
            body.append(h3("Topics"))
            body.append(ul([f"{{{{ link:{u} }}}}" for u in cluster_urls]))

        body.append(
            cta_box(
                "Plan the next step",
                "Share your goals and constraints. We’ll propose a practical scope and timeline.",
                _quote_url(page),
                "Open the quote request page.",
                strong=True,
            )
        )

        content_html = "\n".join(body)
        faq_json = faq(
            [
                (f"How does {svc} typically start?", "With discovery: goals, constraints, stakeholders, and scope. Then we align on milestones and acceptance criteria."),
                ("What affects timeline most?", "Scope clarity, integration complexity, content readiness, and review/approval speed."),
                ("Do you provide post-launch support?", "Yes. We can structure support as a monthly iteration plan with monitoring and improvements."),
                ("How do you manage changes?", "We evaluate changes in writing, estimate impact, and align before implementation."),
                ("What do you need for an initial quote?", "Goals, key pages/features, integrations, and a rough timeline target."),
                ("Can you work with internal teams?", "Yes. We can integrate with your stakeholders and delivery workflow."),
            ]
        )
        content_html = _ensure_word_target(page, content_html, 2000, 2500, seed)
        return {
            "title": meta.title,
            "meta_title": meta.meta_title,
            "meta_description": meta.meta_description,
            "content_html": content_html,
            "faq_json": faq_json[:8],
            "published_at": timezone.now(),
        }

    if page.page_type == SeoPage.TYPE_PRICING:
        title = f"{svc} Pricing"
        meta = make_meta(
            title=title,
            meta_title=f"{svc} Pricing | Scope & Tiers",
            meta_description=f"{svc} pricing depends on scope, integrations, design depth, and delivery timeline. Review cost drivers and how to plan a realistic budget.",
        )
        body: List[str] = []
        body.append(h2("Pricing model"))
        body.append(
            p(
                "Pricing is driven by scope and delivery requirements. This page focuses on cost drivers and budget planning—"
                "not education or implementation details."
            )
        )
        body.append(h2("Primary cost drivers"))
        body.append(
            ul(
                [
                    "Scope: pages/screens, modules, admin needs",
                    "Integrations: payments, CRM/ERP, third-party APIs",
                    "Design depth: template adaptation vs custom system",
                    "Quality: QA depth, performance work, security hardening",
                    "Support: monitoring and iteration after launch",
                ]
            )
        )
        body.append(h2("How to budget without overpaying"))
        body.append(
            p(
                "Define an MVP scope first, then expand in phases. This approach reduces risk and helps you validate outcomes early."
            )
        )
        body.append(h2("Request a scoped quote"))
        body.append(
            cta_box(
                "Get a quote",
                "Share your scope and priorities. We’ll come back with a clear plan and a realistic estimate.",
                _quote_url(page),
                "Open the quote request page.",
                strong=True,
            )
        )
        content_html = "\n".join(body)
        faq_json = faq(
            [
                ("Do you offer fixed pricing?", "We can offer fixed pricing when scope and acceptance criteria are clearly defined."),
                ("Is support included?", "Support can be included or offered as a separate monthly plan depending on needs."),
                ("How do you handle changes?", "We estimate impact and align before proceeding, keeping scope controlled."),
                ("Can you work within a budget cap?", "Yes. We can propose an MVP and phased roadmap to fit constraints."),
                ("What’s the fastest way to get a quote?", "Send goals, must-have features, integrations, and timeline expectations."),
                ("Do you provide tiered options?", "Yes. We can propose tiers based on scope depth and delivery speed."),
            ]
        )
        content_html = _ensure_word_target(page, content_html, 1500, 2000, seed)
        return {
            "title": meta.title,
            "meta_title": meta.meta_title,
            "meta_description": meta.meta_description,
            "content_html": content_html,
            "faq_json": faq_json[:8],
            "published_at": timezone.now(),
        }

    if page.page_type == SeoPage.TYPE_GUIDE:
        title = f"{svc} Guide"
        meta = make_meta(
            title=title,
            meta_title=f"{svc} Guide | Practical Workflow",
            meta_description=f"A practical {svc.lower()} guide covering scope, architecture, design, implementation, QA, and launch. Use checklists to keep delivery on track.",
        )
        body: List[str] = []
        body.append(h2("Who this guide is for"))
        body.append(p("This guide is for teams that want a clean process, clear ownership, and measurable outcomes."))
        body.append(h2("Step 1: Define outcomes and constraints"))
        body.append(ul(["Business outcome", "Users and journeys", "Constraints and dependencies"]))
        body.append(h2("Step 2: Architecture and content model"))
        body.append(p("A good structure prevents rework. Start with hierarchy, template types, and conversion points."))
        body.append(h2("Step 3: Design for clarity"))
        body.append(ul(["Consistency via components", "Accessibility", "Mobile-first patterns", "Performance awareness"]))
        body.append(h2("Step 4: Implement, QA, release"))
        body.append(ul(["Acceptance criteria", "QA checklist", "Performance checks", "Release and rollback plan"]))
        body.append(h2("Next step"))
        body.append(
            ul(
                [
                    f"Service overview: {{ link:{_pillar_url(page)} }}",
                    f"Pricing details: {{ link:{_pricing_url(page)} }}",
                    f"Request a quote: {{ link:{_quote_url(page)} }}",
                ]
            )
        )
        cluster_urls = _cluster_urls_for_service(page)[:10]
        if cluster_urls:
            body.append(h3("Recommended related topics"))
            body.append(ul([f"{{{{ link:{u} }}}}" for u in cluster_urls]))
        body.append(
            cta_box(
                "Turn this into your roadmap",
                "Share your current situation and goals. We’ll turn the guide into a scoped plan.",
                _quote_url(page),
                "Request a quote.",
                strong=True,
            )
        )
        content_html = "\n".join(body)
        faq_json = faq(
            [
                ("How do I define scope?", "Start with an MVP and write acceptance criteria. Then add phase 2/3 items separately."),
                ("When should content be prepared?", "As early as possible—before design is finalized, to avoid layout rework."),
                ("How do I prevent timeline slip?", "Keep scope controlled, set review SLAs, and maintain clear milestones."),
                ("Do I need a design system?", "For multi-page or evolving products, yes. It reduces inconsistency and rework."),
                ("What should happen after launch?", "Monitoring, user feedback collection, and iterative improvements."),
                ("Can you help scope the MVP?", "Yes—share goals and constraints and we’ll propose a practical MVP."),
            ]
        )
        content_html = _ensure_word_target(page, content_html, 1800, 2200, seed)
        return {
            "title": meta.title,
            "meta_title": meta.meta_title,
            "meta_description": meta.meta_description,
            "content_html": content_html,
            "faq_json": faq_json[:8],
            "published_at": timezone.now(),
        }

    if page.page_type == SeoPage.TYPE_QUOTE:
        title = f"Get a Quote for {svc}"
        meta = make_meta(
            title=title,
            meta_title=f"Get a Quote | {svc}",
            meta_description=f"Request a scoped quote for {svc.lower()}. Share goals and priorities to receive a clear plan, timeline, and delivery milestones.",
        )
        body: List[str] = []
        body.append(h2("What happens after you submit"))
        body.append(
            ul(
                [
                    "We review your brief and clarify key questions",
                    "We propose scope, milestones, and assumptions",
                    "You receive a structured quote with timeline options",
                ]
            )
        )
        body.append(h2("What to include in your brief"))
        body.append(ul(["Outcome and target users", "Must-have features/pages", "Integrations", "Timeline constraints", "Reference examples"]))
        body.append(h2("Helpful pages"))
        body.append(ul([f"{{{{ link:{_pricing_url(page)} }}}}", f"{{{{ link:{_guide_url(page)} }}}}"]))
        body.append(
            cta_box(
                "Request a quote",
                "Share your brief. We’ll respond with a clear scope and next steps.",
                _quote_url(page),
                "Open the quote request page.",
                strong=True,
            )
        )
        content_html = "\n".join(body)
        faq_json = faq(
            [
                ("How fast do you respond?", "Response time depends on brief completeness, but we aim to clarify scope quickly."),
                ("Do you offer different delivery timelines?", "Yes. We can propose options based on priorities and constraints."),
                ("Can you sign an NDA?", "Yes, NDAs and confidentiality terms can be arranged."),
                ("How do you handle scope changes?", "We document changes, estimate impact, and align before proceeding."),
                ("Do you support ongoing iteration?", "Yes. We can provide a monthly iteration and monitoring plan."),
            ]
        )
        content_html = _ensure_word_target(page, content_html, 800, 1200, seed)
        return {
            "title": meta.title,
            "meta_title": meta.meta_title,
            "meta_description": meta.meta_description,
            "content_html": content_html,
            "faq_json": faq_json[:8],
            "published_at": timezone.now(),
        }

    # -------------------------------------------------------------------------
    # Custom cluster: Corporate Website Development (EN)
    # -------------------------------------------------------------------------
    if page.page_type == SeoPage.TYPE_CLUSTER and page.service.key == "web-design" and page.slug == "corporate-website-development":
        return _cluster_corporate_website_en(page)

    # -------------------------------------------------------------------------
    # Custom cluster: Agency vs Freelancer (EN)
    # -------------------------------------------------------------------------
    if page.page_type == SeoPage.TYPE_CLUSTER and page.service.key == "web-design" and page.slug == "web-design-agency":
        return _cluster_agency_vs_freelancer_en(page)

    # -------------------------------------------------------------------------
    # Custom cluster: Django vs PHP (EN)
    # -------------------------------------------------------------------------
    if page.page_type == SeoPage.TYPE_CLUSTER and page.service.key == "web-design" and page.slug == "django-vs-php":
        return _cluster_django_vs_php_en(page)

    # -------------------------------------------------------------------------
    # Custom cluster: Django Web Development (EN)
    # -------------------------------------------------------------------------
    if page.page_type == SeoPage.TYPE_CLUSTER and page.service.key == "web-design" and page.slug == "django-web-development":
        return _cluster_django_web_development_en(page)

    # CLUSTER
    topic_title, pain_points, deliverables = _topic_for_cluster_slug(page.service.key, page.slug)
    title = topic_title
    meta = make_meta(
        title=title,
        meta_title=f"{topic_title} | {svc}",
        meta_description=f"An overview of {topic_title.lower()} covering scope, delivery approach, and expected deliverables. See next steps and request a scoped quote.",
    )
    body: List[str] = []
    body.append(h2("Summary"))
    body.append(
        p(
            f"{topic_title} works best when goals and acceptance criteria are explicit. "
            f"For the full service structure, see {{ link:{_pillar_url(page)} }}."
        )
    )
    body.append(h2("Common requirements"))
    body.append(ul(pain_points))
    body.append(h2("Delivery approach"))
    body.append(
        ul(
            [
                "Discovery and scope definition",
                "Architecture and implementation plan",
                "Build and QA with measurable criteria",
                "Release, monitoring, and iteration",
            ]
        )
    )
    body.append(h2("Deliverables"))
    body.append(ul(deliverables))
    body.append(h2("Related pages"))
    siblings = _pick_sibling_clusters(page, n=2)
    links = [f"{{{{ link:{_guide_url(page)} }}}}", f"{{{{ link:{_pricing_url(page)} }}}}", f"{{{{ link:{_quote_url(page)} }}}}"]
    links.extend([f"{{{{ link:{u} }}}}" for u in siblings])
    body.append(ul(links))
    body.append(
        cta_box(
            "Get a scoped quote",
            "Share goals and constraints. We’ll propose scope, milestones, and timeline options.",
            _quote_url(page),
            "Request a quote.",
            strong=True,
        )
    )
    content_html = "\n".join(body)
    faq_json = faq(
        [
            (f"What’s the first step for {topic_title.lower()}?", "Clarify outcomes, scope, and acceptance criteria before implementation."),
            ("What affects delivery time?", "Scope size, integration complexity, and review cycles."),
            ("Do you include pricing here?", "No. Pricing intent is handled only on pricing pages."),
            ("How do I request a quote?", "Provide goals, must-haves, integrations, and timeline constraints."),
            ("Can you work in phases?", "Yes. MVP-first and phased delivery is often the safest approach."),
        ]
    )
    content_html = _ensure_word_target(page, content_html, 1200, 1800, seed)
    return {
        "title": meta.title,
        "meta_title": meta.meta_title,
        "meta_description": meta.meta_description,
        "content_html": content_html,
        "faq_json": faq_json[:8],
        "published_at": timezone.now(),
    }

