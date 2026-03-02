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


def _ecommerce_pillar_en(page: SeoPage) -> Dict:
    """Custom SEO pillar for E-Commerce Development (EN) — scalable, SEO-driven, no pricing triggers."""
    body: List[str] = []

    body.append(h2("Overview"))
    body.append(
        p(
            "E-commerce development is not just building an online store. Without a clear goal and technical strategy, most platforms slow down as they grow."
        )
    )
    body.append(
        p(
            "This page outlines a structured approach to: custom e-commerce development, B2B and B2C platforms, SEO-optimized e-commerce systems, scalable online store architecture."
        )
    )
    body.append(
        ul(
            [
                "custom e-commerce development",
                "B2B and B2C platforms",
                "SEO-optimized e-commerce systems",
                "scalable online store architecture",
            ]
        )
    )
    body.append(
        p(
            f"Rates & scope: {{{{ link:{_pricing_url(page)} }}}}. Workflow: {{{{ link:{_guide_url(page)} }}}}. Request a quote: {{{{ link:{_quote_url(page)} }}}}."
        )
    )

    body.append(h2("The Right Framework for Every E-Commerce Project"))
    body.append(
        p(
            "Successful projects follow this structure: Goal → User → Information Architecture → Design → Development → Testing → Launch → Measurement. Skipping steps creates long-term technical debt."
        )
    )

    body.append(h3("1) Define the Business Goal"))
    body.append(
        p(
            "Is the objective: Increase sales? Enter a new market? Build a B2B wholesale system? Improve operational efficiency? Architecture depends on clarity."
        )
    )

    body.append(h3("2) Scope Definition"))
    body.append(
        p(
            "Critical elements include: product management system, payment gateway integration, shipping & logistics integration, ERP/CRM integration, campaign & discount modules, multi-language / multi-currency, technical SEO foundation. Unclear scope = delayed delivery."
        )
    )

    body.append(h2("Development Process"))
    body.append(h3("Discovery"))
    body.append(
        p(
            "Goal analysis, competitor research, user flow mapping."
        )
    )
    body.append(h3("Design"))
    body.append(
        p(
            "Conversion-focused UX, mobile optimization, checkout flow optimization."
        )
    )
    body.append(h3("Development"))
    body.append(
        p(
            "Scalable backend, performance-optimized frontend, secure payment systems, structured SEO architecture."
        )
    )
    body.append(h3("Testing & Launch"))
    body.append(
        p(
            "Speed testing, checkout testing, analytics setup, monitoring."
        )
    )

    body.append(h2("SEO-First E-Commerce Architecture"))
    body.append(
        p(
            "E-commerce visibility depends on: Core Web Vitals, structured product data, optimized category architecture, internal linking strategy, technical performance. SEO is a structural decision, not an add-on."
        )
    )

    body.append(h2("Custom vs Ready-Made Platforms"))
    body.append(
        p(
            "Ready systems are faster initially but may limit scalability. Custom e-commerce solutions: allow full control; support complex B2B models; scale efficiently; reduce long-term technical constraints. The decision should align with growth strategy."
        )
    )

    body.append(h2("Launch & Sustainability"))
    body.append(
        p(
            "Post-launch includes: analytics tracking, conversion optimization, error monitoring, security updates, backup systems, performance scaling. Unmeasured platforms don't grow."
        )
    )

    body.append(
        cta_box(
            "Share your goals",
            "We'll build a clear roadmap aligned with your business. Get an E-Commerce Development quote.",
            _quote_url(page),
            "Get an E-Commerce Development Quote",
            strong=True,
        )
    )

    content_html = "\n".join(body)
    faq_pairs = [
        ("How long does e-commerce development take?", "Depends on scope, integrations, and customization."),
        ("Do you provide post-launch support?", "Ongoing monitoring and maintenance are essential for growing platforms."),
    ]
    faq_json = faq(faq_pairs)

    meta_title = "E-Commerce Development | Custom & Scalable E-Commerce Solutions"
    meta_description = (
        "Professional e-commerce development: custom e-commerce software, B2B & B2C platforms, SEO-optimized and performance-driven architecture designed to scale."
    )
    meta_title = clamp_text(meta_title, 60)
    meta_description = clamp_text(meta_description, 160)

    return {
        "title": "E-Commerce Development — Scalable and SEO-Driven Architecture",
        "meta_title": meta_title,
        "meta_description": meta_description,
        "content_html": content_html,
        "faq_json": faq_json,
        "published_at": timezone.now(),
    }


def _mobile_app_pillar_en(page: SeoPage) -> Dict:
    """Custom SEO pillar for Mobile App Development (EN) — scalable, high-performance, no pricing triggers."""
    body: List[str] = []

    body.append(h2("What Is Mobile App Development?"))
    body.append(
        p(
            "Mobile app development is not just coding an application. It is the strategic combination of: user experience design, performance optimization, secure backend architecture, scalable infrastructure, and business goal alignment. A successful app must deliver speed, reliability, and measurable growth."
        )
    )
    body.append(
        p(
            f"Workflow: {{{{ link:{_guide_url(page)} }}}}. Request a quote: {{{{ link:{_quote_url(page)} }}}}."
        )
    )

    body.append(h2("Why Professional Development Matters"))
    body.append(
        p(
            "Users expect: instant load time, smooth navigation, no crashes, secure transactions. Without proper architecture, apps fail quickly in competitive markets."
        )
    )

    body.append(h2("Android & iOS App Development Approaches"))
    body.append(h3("Native Development"))
    body.append(
        p(
            "Kotlin (Android), Swift (iOS). Highest performance and platform-specific experience."
        )
    )
    body.append(h3("Cross-Platform Development"))
    body.append(
        p(
            "Flutter, React Native. Faster deployment with shared codebase."
        )
    )
    body.append(h3("Backend & API Integration"))
    body.append(
        ul(
            [
                "Secure authentication",
                "Payment systems",
                "Push notifications",
                "Analytics integration",
                "Cloud infrastructure",
            ]
        )
    )
    body.append(
        p(
            "Strong backend equals scalable growth."
        )
    )

    body.append(h2("Our Development Process"))
    body.append(h3("Strategy & Planning"))
    body.append(
        p(
            "Market research, feature mapping, monetization model."
        )
    )
    body.append(h3("UX/UI Design"))
    body.append(
        p(
            "User flows, wireframes, prototyping."
        )
    )
    body.append(h3("Development"))
    body.append(
        p(
            "Frontend implementation + backend API."
        )
    )
    body.append(h3("Testing & QA"))
    body.append(
        p(
            "Device testing, performance analysis, store compliance."
        )
    )
    body.append(h3("Launch & Optimization"))
    body.append(
        p(
            "App Store submission, ASO, analytics tracking."
        )
    )

    body.append(h2("Performance & Security"))
    body.append(
        p(
            "Professional apps include: optimized data handling, encrypted communication, secure authentication, scalable server infrastructure. Security builds trust."
        )
    )

    body.append(h2("Who Is It For?"))
    body.append(
        ul(
            [
                "E-commerce businesses",
                "SaaS platforms",
                "Logistics & delivery systems",
                "Education apps",
                "Fintech startups",
            ]
        )
    )
    body.append(
        p(
            "Mobile apps drive direct engagement and retention."
        )
    )

    body.append(h2("Final Thoughts"))
    body.append(
        p(
            "Mobile app development requires more than coding — it demands architecture, performance engineering, and user-centered thinking. Built correctly, it becomes a scalable growth engine."
        )
    )

    body.append(h2("Related topics"))
    body.append(
        p(
            f"Workflow: {{{{ link:{_guide_url(page)} }}}}. Quote: {{{{ link:{_quote_url(page)} }}}}."
        )
    )
    cluster_urls = _cluster_urls_for_service(page)
    if cluster_urls:
        body.append(ul([f"{{{{ link:{u} }}}}" for u in cluster_urls[:10]]))

    body.append(
        cta_box(
            "Get a Quote",
            "Share your mobile app goals; we'll outline scope and a clear plan.",
            _quote_url(page),
            "Go to quote form.",
            strong=True,
        )
    )

    content_html = "\n".join(body)
    faq_pairs = [
        ("How long does mobile app development take?", "Depends on scope, features, and platform requirements."),
        ("Can Android and iOS be developed together?", "Yes, via native or cross-platform approaches."),
        ("Do you provide post-launch support?", "Yes, maintenance and updates are planned."),
        ("What impacts App Store ranking?", "ASO, performance, reviews, retention rate."),
        ("Is backend development necessary?", "For most scalable applications, yes."),
    ]
    faq_json = faq(faq_pairs)

    meta_title = "Mobile App Development | Android & iOS Scalable Solutions"
    meta_description = (
        "Professional mobile app development for Android and iOS. High-performance, secure, and scalable applications built for growth."
    )
    meta_title = clamp_text(meta_title, 60)
    meta_description = clamp_text(meta_description, 160)

    return {
        "title": "Mobile App Development — Scalable & High-Performance Solutions",
        "meta_title": meta_title,
        "meta_description": meta_description,
        "content_html": content_html,
        "faq_json": faq_json,
        "published_at": timezone.now(),
    }


def _cluster_android_app_development_en(page: SeoPage) -> Dict:
    """Custom cluster: Android App Development — device diversity, performance, security. No pricing triggers."""
    body: List[str] = []

    body.append(h2("Overview"))
    body.append(
        p(
            "Android development is fundamentally shaped by device diversity and real-world performance constraints. A successful Android app must run smoothly not only on flagship devices but also on mid-range and low-end phones — under varying network conditions."
        )
    )
    body.append(
        p(
            "This page explains the practical framework behind building Android apps that are: fast and responsive, secure by design, scalable for growth, ready for Play Store release, measurable through analytics."
        )
    )
    body.append(
        p(
            f"Service overview: {{{{ link:{_pillar_url(page)} }}}}. Workflow: {{{{ link:{_guide_url(page)} }}}}."
        )
    )

    body.append(h2("Common Android Development Challenges (and What Matters)"))
    body.append(h3("1) Device Diversity & Compatibility"))
    body.append(
        p(
            "Android runs across countless device types, screen sizes, chipsets, and OS versions. That means your app must be engineered to handle:"
        )
    )
    body.append(
        ul(
            [
                "responsive UI across screen sizes",
                "stable behavior on different Android versions",
                "performance constraints (low RAM / low CPU)",
                "manufacturer-specific quirks",
                "a realistic device testing strategy",
            ]
        )
    )
    body.append(h3("2) Performance & Responsiveness"))
    body.append(
        p(
            "Users don't tolerate slow apps. Performance is not \"nice to have\" — it directly impacts retention. Key performance factors:"
        )
    )
    body.append(
        ul(
            [
                "cold start / launch time",
                "smooth scrolling on lists and feeds",
                "efficient network usage and fewer API calls",
                "smart caching for data and media",
                "resilience under weak connectivity (offline-first thinking)",
            ]
        )
    )
    body.append(h3("3) Security & Data Protection"))
    body.append(
        p(
            "Security is more than login. Android apps often fail due to weak token handling or unsafe data storage. A professional security baseline includes:"
        )
    )
    body.append(
        ul(
            [
                "secure authentication and token lifecycle",
                "server-side validation for API requests",
                "safe local storage practices",
                "abuse prevention and rate limiting",
                "preventing sensitive data leaks in logs/crash reports",
            ]
        )
    )

    body.append(h2("Recommended Delivery Process"))
    body.append(h3("1) Discovery & Goals"))
    body.append(
        ul(
            [
                "define the primary outcome (sales, leads, operations)",
                "map critical user journeys",
                "align on MVP vs phased roadmap",
            ]
        )
    )
    body.append(p("<strong>Output:</strong> scope draft + priorities + measurable goals"))
    body.append(h3("2) Planning & Architecture"))
    body.append(
        p(
            "Architecture choices drive performance and maintainability. Plan should define: navigation and information architecture, API contracts and error handling strategy, push notifications and background tasks approach, analytics event plan (what to measure and why)."
        )
    )
    body.append(p("<strong>Output:</strong> technical plan + delivery criteria"))
    body.append(h3("3) Design & Development"))
    body.append(
        ul(
            [
                "UX clarity, simple navigation, strong CTAs",
                "performance-driven implementation",
                "maintainable code structure for future iterations",
            ]
        )
    )
    body.append(p("<strong>Output:</strong> working build + testable release candidate"))
    body.append(h3("4) Testing & Launch"))
    body.append(
        p(
            "Launching on Android is an engineering phase: device coverage testing, crash/ANR risk reduction, Play Store compliance checks, release notes and rollout plan."
        )
    )
    body.append(p("<strong>Output:</strong> launch checklist + monitoring plan"))

    body.append(h2("Deliverables You Should Expect"))
    body.append(
        p(
            "For a clear project outcome, deliverables must be tangible: phased release roadmap, testing strategy (device list + critical flows), analytics measurement plan, post-launch iteration framework (first 30 days)."
        )
    )

    body.append(h2("When to Choose an Android-Focused Approach"))
    body.append(
        ul(
            [
                "your goals are measurable",
                "user flows are clear",
                "you want phased delivery instead of chaos",
                "performance and security are top priorities",
            ]
        )
    )
    body.append(
        p(
            "Android success is not \"ship fast\" — it's build sustainable."
        )
    )

    body.append(h2("Post-Launch: Monitoring & Iteration"))
    body.append(
        p(
            "Launch is the beginning. Strong Android products establish: crash monitoring, performance tracking, user feedback loops, continuous improvements and updates."
        )
    )
    body.append(
        p(
            "This improves stability, trust, and retention over time."
        )
    )

    body.append(
        cta_box(
            "Share your Android app goal in 2–3 sentences",
            "We'll define the scope, split it into phases, and build a reliable execution plan. Go to the quote page.",
            _quote_url(page),
            "Go to the quote page.",
            strong=True,
        )
    )

    content_html = "\n".join(body)
    faq_pairs = [
        ("What's the first step in Android app development?", "Define goals and critical user flows, then lock scope in writing."),
        ("Where does Android performance break most often?", "App launch time, list scrolling, inefficient network calls, and poor caching."),
        ("How do you handle device diversity?", "By setting a target device/OS matrix and building a realistic test strategy."),
        ("What's the minimum security baseline?", "Secure auth, safe token handling, server-side validation, and protected local storage."),
        ("What causes launch issues on Google Play?", "Permissions, policy compliance, high crash/ANR rate, and missing release checklist items."),
        ("What should you track after launch?", "Crashes, session duration, key conversion flows, retention, and performance metrics."),
    ]
    faq_json = faq(faq_pairs)

    meta_title = "Android App Development | Performance, Security & Scalability"
    meta_description = (
        "Android app development built for device diversity, speed, and reliability. Secure architecture, Play Store readiness, analytics-driven iteration."
    )
    meta_title = clamp_text(meta_title, 60)
    meta_description = clamp_text(meta_description, 160)

    return {
        "title": "Android App Development — Reliable Performance Across Device Diversity",
        "meta_title": meta_title,
        "meta_description": meta_description,
        "content_html": content_html,
        "faq_json": faq_json,
        "published_at": timezone.now(),
    }


def _cluster_ios_app_development_en(page: SeoPage) -> Dict:
    """Custom cluster: iOS App Development — App Store ready, stable, scalable. No pricing triggers."""
    body: List[str] = []

    body.append(h2("Overview"))
    body.append(
        p(
            "Shipping an iOS app is not just \"building screens.\" Real outcomes come from combining App Store readiness, iOS UX standards, stability, performance, and post-launch iteration."
        )
    )
    body.append(
        p(
            "This page explains a practical iOS delivery framework with clear process steps, deliverables, and acceptance criteria. "
            f"Service overview: {{{{ link:{_pillar_url(page)} }}}}. Workflow: {{{{ link:{_guide_url(page)} }}}}."
        )
    )

    body.append(h2("Common Needs We Solve"))
    body.append(h3("1) App Store Readiness (Planned Early)"))
    body.append(
        p(
            "App Store submission shouldn't be a last-minute surprise. Typical areas include: guideline-friendly user flows, permission messaging and privacy approach (user trust), release notes, screenshots, submission checklist, testing workflow (TestFlight, scenario coverage)."
        )
    )
    body.append(p("<strong>Goal:</strong> turn \"review uncertainty\" into a predictable checklist-driven launch."))
    body.append(h3("2) iOS Design Standards (UI/UX)"))
    body.append(
        p(
            "iOS users expect consistency. That means: clear navigation patterns, clean forms and CTAs, consistent typography and spacing, accessibility basics (readability, tap targets)."
        )
    )
    body.append(p("<strong>Goal:</strong> remove friction and guide users to the key action."))
    body.append(h3("3) Stability, Performance, and Sustainability"))
    body.append(
        p(
            "Even with a controlled ecosystem, quality requires: crash monitoring and logging strategy, performance targets for critical flows, network resilience (retry, offline tolerance when relevant), small iterations after launch."
        )
    )
    body.append(p("<strong>Goal:</strong> \"measurably reliable\" — not just \"it works on my phone.\""))

    body.append(h2("Recommended iOS Delivery Process"))
    body.append(h3("1) Discovery & Goals"))
    body.append(
        ul(
            [
                "define users and the problem",
                "map critical flows (signup, booking, checkout, messaging)",
                "set measurable metrics (activation, retention, conversion steps)",
            ]
        )
    )
    body.append(p("<strong>Deliverable:</strong> goals + scope skeleton + key decisions"))
    body.append(h3("2) Planning: Delivery Criteria & Priorities"))
    body.append(
        ul(
            [
                "MVP scope (v1) + phased roadmap",
                "define \"must-have\" screens and flows",
                "analytics event plan (what to measure)",
            ]
        )
    )
    body.append(p("<strong>Deliverable:</strong> phased plan + acceptance criteria"))
    body.append(h3("3) Design & Development"))
    body.append(
        ul(
            [
                "iOS-consistent UI system and components",
                "secure session handling (auth/token; role-based needs if required)",
                "performance-driven data flow",
            ]
        )
    )
    body.append(p("<strong>Deliverable:</strong> testable build + critical flows complete"))
    body.append(h3("4) Testing & Launch"))
    body.append(
        ul(
            [
                "scenario-based QA",
                "TestFlight distribution + feedback loop",
                "launch checklist + monitoring plan",
            ]
        )
    )
    body.append(p("<strong>Deliverable:</strong> launch-ready build + monitoring setup"))

    body.append(h2("Deliverables"))
    body.append(
        p(
            "A strong iOS release includes more than the binary: App Store submission checklist, release notes template, testing plan (critical scenarios + OS coverage), monitoring plan (crashes + core user actions)."
        )
    )

    body.append(h2("When This Approach Fits Best"))
    body.append(
        p(
            "This framework is ideal when:"
        )
    )
    body.append(
        ul(
            [
                "App Store readiness must be smooth",
                "stability and UX are brand-critical",
                "growth is planned through post-launch iteration",
                "you want measurable scope discipline",
            ]
        )
    )

    body.append(
        cta_box(
            "Share your goal and critical flows",
            "We'll clarify scope and turn it into a practical iOS delivery plan. Go to the quote page.",
            _quote_url(page),
            "Go to the quote page.",
            strong=True,
        )
    )

    content_html = "\n".join(body)
    faq_pairs = [
        ("What's the first step in iOS app development?", "Define the user goal and critical flows, then lock an MVP scope in writing."),
        ("Why plan for App Store submission early?", "Permissions, privacy approach, UI standards, and submission requirements can impact timelines if handled late."),
        ("Why do iOS UX standards matter?", "Consistency improves trust, reduces friction, and increases conversion on key actions."),
        ("What is TestFlight used for?", "Controlled pre-release distribution, feedback collection, and stability improvements."),
        ("What should you focus on after launch?", "Crash rate, performance of critical flows, and activation/retention metrics."),
        ("How do you manage scope changes?", "Through phased planning and acceptance criteria (must-have / priority / optional)."),
    ]
    faq_json = faq(faq_pairs)

    meta_title = "iOS App Development | App Store Ready & Scalable Delivery"
    meta_description = (
        "iOS app development focused on App Store requirements, iOS design standards, stability, performance, and measurable delivery criteria for sustainable growth."
    )
    meta_title = clamp_text(meta_title, 60)
    meta_description = clamp_text(meta_description, 160)

    return {
        "title": "iOS App Development — App Store Ready, Stable, and Scalable Products",
        "meta_title": meta_title,
        "meta_description": meta_description,
        "content_html": content_html,
        "faq_json": faq_json,
        "published_at": timezone.now(),
    }


def _cluster_istanbul_service_en(page: SeoPage) -> Dict:
    """Custom cluster: Mobile App Development in Istanbul — local competition, fast communication, on-site. No pricing triggers."""
    body: List[str] = []

    body.append(h2("Overview"))
    body.append(
        p(
            "Building a mobile app in Istanbul is not only engineering — it's managing dense competition, fast decision cycles, and real operational needs."
        )
    )
    body.append(
        p(
            "This page explains how we structure Istanbul-based mobile projects around a clear framework: goal → scope → acceptance criteria → launch → measurement → iteration. "
            f"Service overview: {{{{ link:{_pillar_url(page)} }}}}. Workflow: {{{{ link:{_guide_url(page)} }}}}."
        )
    )

    body.append(h2("Common Needs in Istanbul Projects"))
    body.append(h3("1) Local Competition: \"Similar apps already exist\""))
    body.append(
        p(
            "In many Istanbul markets (restaurants, beauty, services, real estate, education, logistics), apps look similar. Winning is not about adding more features — it's about reducing friction. What works: define the value proposition in one sentence; pick 2–3 critical flows (booking, ordering, signup, quote request); prioritize clarity and speed over feature overload; focus on activation and repeat usage in v1."
        )
    )
    body.append(h3("2) Fast Communication Expectations"))
    body.append(
        p(
            "Fast communication is good — but it must not turn into chaotic scope changes. How we keep it controlled: weekly short status updates + a clear priority list; a written \"done\" definition (acceptance criteria); every change request tied to a phase plan; one decision owner to avoid confusion."
        )
    )
    body.append(h3("3) On-Site Meetings (When Needed)"))
    body.append(
        p(
            "In-person meetings can accelerate alignment — only if they follow a clear agenda. Efficient meeting template: goal + users + critical flows; scope boundaries (in / out); delivery criteria + testing/launch plan; written summary and next actions."
        )
    )

    body.append(h2("Recommended Process (Istanbul-Oriented)"))
    body.append(h3("1) Discovery & Goals"))
    body.append(
        ul(
            [
                "define the local audience segment (district/area/service region)",
                "map user motivation and urgency",
                "select critical flows + success metrics",
            ]
        )
    )
    body.append(p("<strong>Deliverable:</strong> goals + scope draft + decision notes"))
    body.append(h3("2) Planning: Priorities & Acceptance Criteria"))
    body.append(
        ul(
            [
                "MVP (v1) and phase roadmap",
                "must-have screens and flows",
                "measurement plan (events to track)",
            ]
        )
    )
    body.append(p("<strong>Deliverable:</strong> phased plan + acceptance criteria"))
    body.append(h3("3) Design & Development"))
    body.append(
        ul(
            [
                "mobile-first UX and clear CTAs",
                "stability and performance targets",
                "feedback loop design (support, reviews, in-app signals)",
            ]
        )
    )
    body.append(p("<strong>Deliverable:</strong> testable build with core flows completed"))
    body.append(h3("4) Testing & Launch"))
    body.append(
        ul(
            [
                "scenario-based testing for critical flows",
                "launch checklist + monitoring plan",
            ]
        )
    )
    body.append(p("<strong>Deliverable:</strong> launch-ready build + monitoring baseline"))

    body.append(h2("Deliverables (Specific to Istanbul Service)"))
    body.append(
        p(
            "local-focused scope framework (goal/scope/criteria clarity); industry examples (critical flow templates for common business types); communication plan (meeting rhythm, reporting format, decision structure)."
        )
    )

    body.append(h2("Post-Launch Sustainability"))
    body.append(
        p(
            "In competitive markets, launch is the start. The first 30 days should focus on: friction points in key flows; stability and performance; user feedback loops; small, high-impact iterations."
        )
    )

    body.append(
        cta_box(
            "Share your goal and your Istanbul audience segment",
            "We'll turn it into a clear scope and a practical delivery plan. Go to the quote page.",
            _quote_url(page),
            "Go to the quote page.",
            strong=True,
        )
    )

    content_html = "\n".join(body)
    faq_pairs = [
        ("What's the first step for an Istanbul-based mobile app project?", "Define the local audience segment and select 2–3 critical flows."),
        ("How do you compete in a crowded market?", "By reducing friction: fast onboarding, clear CTAs, and simple repeat usage loops."),
        ("Are on-site meetings required?", "Sometimes — especially for operational businesses — but only with a strict agenda and written outcomes."),
        ("Can fast communication hurt delivery?", "Yes, if unmanaged. We prevent chaos with weekly summaries, priorities, and acceptance criteria."),
        ("What matters most after launch?", "Critical flow performance, stability, and user behavior-driven iteration."),
        ("How do you handle scope changes?", "With a phased roadmap: must-have / priority / optional."),
    ]
    faq_json = faq(faq_pairs)

    meta_title = "Mobile App Development in Istanbul | Local Competition Ready Delivery"
    meta_description = (
        "Istanbul-focused mobile app development: local competition, fast communication, on-site meetings, clear scope, measurable deliverables, launch monitoring, and iteration."
    )
    meta_title = clamp_text(meta_title, 60)
    meta_description = clamp_text(meta_description, 160)

    return {
        "title": "Mobile App Development in Istanbul — A Local-Competition, Metrics-Driven Approach",
        "meta_title": meta_title,
        "meta_description": meta_description,
        "content_html": content_html,
        "faq_json": faq_json,
        "published_at": timezone.now(),
    }


def _cluster_mobile_app_freelancer_en(page: SeoPage) -> Dict:
    """Custom cluster: Mobile App Freelancer — reduce risk, delivery checklist. No pricing triggers."""
    body: List[str] = []

    body.append(h2("Overview"))
    body.append(
        p(
            "Hiring a mobile app freelancer can be a fast path to launch — or a risky shortcut if the project depends on a single person without structure."
        )
    )
    body.append(
        p(
            "This page helps you make freelancer work reliable by focusing on scope clarity, acceptance criteria, testing, launch discipline, and ownership of deliverables. "
            f"Service overview: {{{{ link:{_pillar_url(page)} }}}}. Workflow: {{{{ link:{_guide_url(page)} }}}}."
        )
    )

    body.append(h2("Common Challenges"))
    body.append(h3("1) Single-Person Team Risk"))
    body.append(
        p(
            "The biggest risk is not talent — it's dependency: availability issues (busy, sick, travel); knowledge locked in one place; weak testing and documentation → launch problems."
        )
    )
    body.append(
        p(
            "<strong>Principle:</strong> Build a system, not a dependency: written scope, repo structure, test plan, launch checklist."
        )
    )
    body.append(h3("2) Process Gaps"))
    body.append(
        p(
            "Mobile apps require more than coding: device/OS fragmentation, store requirements, stability and performance, analytics and events. Without a process, \"it works on my phone\" becomes a disaster."
        )
    )

    body.append(h2("Recommended Process (Freelancer-Proof)"))
    body.append(h3("1) Discovery & Goals"))
    body.append(
        p(
            "Ask these key questions: What is the main goal? (booking, ordering, membership, tracking) What are the top 2–3 critical flows? What screens are must-have in v1? Which integrations are required? (auth, notifications, maps, payments) How will success be measured? (activation, retention, conversions)"
        )
    )
    body.append(p("<strong>Deliverable:</strong> a one-page goal + scope summary"))
    body.append(h3("2) Planning: Priorities & Acceptance Criteria"))
    body.append(
        ul(
            [
                "MVP (v1) + phase roadmap",
                "acceptance criteria per feature",
                "change request discipline",
            ]
        )
    )
    body.append(p("<strong>Deliverable:</strong> scope list + acceptance criteria"))
    body.append(h3("3) Design & Development"))
    body.append(
        ul(
            [
                "clear UX flows (Figma or written flows)",
                "code standards, branching",
                "crash logging + basic analytics events",
            ]
        )
    )
    body.append(p("<strong>Deliverable:</strong> testable build with core flows working"))
    body.append(h3("4) Testing & Launch"))
    body.append(
        ul(
            [
                "device matrix",
                "release checklist",
                "monitoring baseline (crashes, performance, key events)",
            ]
        )
    )
    body.append(p("<strong>Deliverable:</strong> launch-ready build + monitoring plan"))

    body.append(h2("How to Choose a Freelancer (Selection Criteria)"))
    body.append(h3("Strong technical signals"))
    body.append(
        ul(
            [
                "has delivered similar apps (ideally published on stores)",
                "can explain tech choices clearly",
                "understands release and versioning",
                "can discuss performance and stability",
            ]
        )
    )
    body.append(h3("Strong process signals"))
    body.append(
        ul(
            [
                "insists on written scope",
                "proposes weekly reporting rhythm",
                "explains testing and launch plan",
                "offers a risk plan for single-person delivery",
            ]
        )
    )
    body.append(h3("Red flags"))
    body.append(
        ul(
            [
                "\"I can do everything\" but refuses scope clarity",
                "ignores testing",
                "messy repo / no documentation",
                "underestimates store requirements",
            ]
        )
    )

    body.append(h2("Delivery Checklist (Use This to Avoid Pain)"))
    body.append(p("<strong>Must-have deliverables:</strong>"))
    body.append(
        ul(
            [
                "source code + repo access (not tied to one account)",
                "setup/build documentation (README)",
                "release notes (done / pending)",
                "monitoring setup (crash logging, basic events)",
                "test scenarios for critical flows",
                "launch checklist",
            ]
        )
    )
    body.append(
        p(
            "<strong>High-value extras:</strong> simple architecture overview; feature map; technical debt notes for future improvements."
        )
    )

    body.append(h2("When a Freelancer Is a Good Fit"))
    body.append(
        p(
            "scope is clear and not overly complex; you want a focused MVP; you can manage risk with structure."
        )
    )
    body.append(h2("When It's Risky"))
    body.append(
        p(
            "heavy integrations and complex permissions; tight timelines without a backup plan; long-term iteration depends on one person."
        )
    )

    body.append(h2("Post-Launch Sustainability"))
    body.append(
        p(
            "Sustainability is not \"launched and done.\" You need: crash monitoring, performance tracking, user behavior insights, small, fast iterations."
        )
    )

    body.append(
        cta_box(
            "If you want to work with a freelancer",
            "Start by locking scope and acceptance criteria in writing — then build with a clean delivery system. Go to the quote page.",
            _quote_url(page),
            "Go to the quote page.",
            strong=True,
        )
    )

    content_html = "\n".join(body)
    faq_pairs = [
        ("What's the first step when hiring a mobile app freelancer?", "Define critical flows and document scope with acceptance criteria."),
        ("How do I reduce single-person risk?", "Own the repo access, require documentation, testing plan, and a launch checklist."),
        ("What's the best signal of a strong freelancer?", "A proven store delivery + a clear process (scope, testing, reporting)."),
        ("What happens when scope changes?", "Handle changes through a phased roadmap: must-have / priority / optional."),
        ("What must be included in delivery?", "Repo, README, release notes, test scenarios, monitoring setup."),
        ("What matters most after launch?", "Stability, performance, and behavior-driven iteration."),
    ]
    faq_json = faq(faq_pairs)

    meta_title = "Mobile App Freelancer | How to Choose + Delivery Checklist"
    meta_description = (
        "Guide to working with a mobile app freelancer: single-person risk, process management, selection criteria, delivery checklist, testing and launch plan, sustainability after release."
    )
    meta_title = clamp_text(meta_title, 60)
    meta_description = clamp_text(meta_description, 160)

    return {
        "title": "Working with a Mobile App Freelancer — A Practical Guide to Reduce Risk and Secure Delivery",
        "meta_title": meta_title,
        "meta_description": meta_description,
        "content_html": content_html,
        "faq_json": faq_json,
        "published_at": timezone.now(),
    }


def _cluster_how_to_build_mobile_app_en(page: SeoPage) -> Dict:
    """Custom cluster: How to Build a Mobile App — step-by-step process guide. No pricing triggers."""
    body: List[str] = []

    body.append(h2("Overview"))
    body.append(
        p(
            "Building a mobile app is not just coding. A successful mobile app: starts with clear goals, defines scope properly, focuses on UX, uses the right technology, is tested thoroughly, is monitored after launch."
        )
    )
    body.append(
        p(
            "This guide explains the complete mobile app development process in a structured and professional way. "
            f"Service overview: {{{{ link:{_pillar_url(page)} }}}}. Workflow: {{{{ link:{_guide_url(page)} }}}}."
        )
    )

    body.append(h2("1) Define the Idea and Goals"))
    body.append(
        p(
            "Most mobile apps fail due to strategy, not code. Key questions: What problem does it solve? Who is the target user? What are the 2–3 critical flows? What features are mandatory in v1? How will success be measured? Without this clarity, development becomes chaotic."
        )
    )

    body.append(h2("2) Define Scope and MVP"))
    body.append(
        p(
            "Biggest mistake: building everything at once. Correct method: Must-have (MVP), Priority, Optional (Phase 2). Each feature needs measurable acceptance criteria."
        )
    )

    body.append(h2("3) UX/UI Design"))
    body.append(
        p(
            "Mobile UX requires: thumb-friendly layout, intuitive navigation, clear hierarchy, proper error states, loading states, empty states. Design is experience architecture."
        )
    )

    body.append(h2("4) Choose the Right Technology"))
    body.append(
        ul(
            [
                "Native Android",
                "Native iOS",
                "Cross-platform (Flutter, React Native)",
                "Backend/API architecture",
            ]
        )
    )
    body.append(p("Technology must align with scalability and performance goals."))

    body.append(h2("5) Development Phase"))
    body.append(
        p(
            "Key technical considerations: clean architecture, version control, API security, performance optimization, crash logging, analytics planning. \"Working\" is not enough. It must be stable."
        )
    )

    body.append(h2("6) Testing Phase"))
    body.append(
        p(
            "Professional apps require: functional testing, user flow testing, device compatibility, performance checks, security review. Testing protects reputation."
        )
    )

    body.append(h2("7) Publishing"))
    body.append(
        p(
            "Publishing includes: store compliance, privacy policy, screenshots, release notes, approval process. Launch is the beginning, not the end."
        )
    )

    body.append(h2("8) Post-Launch Optimization"))
    body.append(
        p(
            "After release: monitor crashes, track performance, analyze user behavior, iterate quickly. The first 30 days are critical."
        )
    )

    body.append(
        cta_box(
            "Ready to build a mobile app?",
            "Start by defining goals and scope — then we'll turn it into a clear delivery plan. Go to the quote page.",
            _quote_url(page),
            "Go to the quote page.",
            strong=True,
        )
    )

    content_html = "\n".join(body)
    faq_pairs = [
        ("How long does it take to build a mobile app?", "Depends on scope and integrations."),
        ("What is MVP?", "Minimum viable product — the first functional release."),
        ("Should I build Android or iOS first?", "Based on target audience analysis."),
        ("Is post-launch work necessary?", "Yes. Optimization is essential."),
    ]
    faq_json = faq(faq_pairs)

    meta_title = "How to Build a Mobile App — Step-by-Step Development Guide"
    meta_description = (
        "How to build a mobile app from idea to launch. Step-by-step mobile app development process, MVP strategy, testing, publishing and optimization guide."
    )
    meta_title = clamp_text(meta_title, 60)
    meta_description = clamp_text(meta_description, 160)

    return {
        "title": "How to Build a Mobile App — From Idea to Launch",
        "meta_title": meta_title,
        "meta_description": meta_description,
        "content_html": content_html,
        "faq_json": faq_json,
        "published_at": timezone.now(),
    }


def _cluster_what_is_a_mobile_app_en(page: SeoPage) -> Dict:
    """Custom cluster: What Is a Mobile App? — types, use cases, how to decide. No pricing triggers."""
    body: List[str] = []

    body.append(h2("Overview"))
    body.append(
        p(
            "A mobile app is software designed for smartphones and tablets to help users complete tasks quickly and repeatedly. But \"mobile app\" is not one single format. In practice, it can mean: native iOS and Android apps; cross-platform apps built from one codebase; web solutions that behave like apps (PWA); business apps that streamline operations and workflows."
        )
    )
    body.append(
        p(
            "This page helps you answer the real question: Do you actually need a mobile app? "
            f"Service overview: {{{{ link:{_pillar_url(page)} }}}}. Workflow: {{{{ link:{_guide_url(page)} }}}}."
        )
    )

    body.append(h2("What Does a Mobile App Improve?"))
    body.append(
        p(
            "Mobile apps are strongest when they create continuous user touchpoints: push notifications to increase return visits; device features (camera, location, biometrics) to speed up flows; smoother repeat actions (one-tap journeys); better stability in weak network situations; measurement and iteration based on user behavior. A mobile app wins when speed, repeat usage, and engagement matter."
        )
    )

    body.append(h2("Types of Mobile Apps"))
    body.append(h3("1) Native Apps (iOS / Android)"))
    body.append(
        p(
            "Built specifically for each platform. Best for: high performance requirements; heavy device integrations; products where the app is the core experience."
        )
    )
    body.append(h3("2) Cross-Platform Apps (Flutter / React Native)"))
    body.append(
        p(
            "One codebase targeting both platforms. Best for: faster launch cycles; consistent experience across platforms; MVP and first releases with planned iterations."
        )
    )
    body.append(h3("3) PWA (Progressive Web App)"))
    body.append(
        p(
            "Web-based experience that feels like an app. Best for: content-focused products; simpler user flows; reducing app store dependency. The right choice depends on the use case, not the trend."
        )
    )

    body.append(h2("How to Choose the Right Use Case"))
    body.append(
        p(
            "Ask these 3 questions: How often will users repeat the core action weekly? Does mobile create a clear speed advantage? Do you need notifications or device features? If at least two are \"yes,\" mobile is a strong candidate."
        )
    )

    body.append(h2("Target Audience: B2C vs B2B"))
    body.append(h3("B2C"))
    body.append(
        p(
            "Focus: UX, onboarding, retention, speed. Examples: e-commerce, booking, delivery, content platforms."
        )
    )
    body.append(h3("B2B"))
    body.append(
        p(
            "Focus: roles, workflows, reporting, integrations. Examples: field team apps, internal CRM companion apps, inventory and order tracking, operational tools."
        )
    )

    body.append(h2("Practical Examples"))
    body.append(
        ul(
            [
                "booking apps: repeatable flows + convenience",
                "delivery tracking: location + real-time status + notifications",
                "loyalty apps: campaigns + notifications + account journeys",
                "operations apps: role-based access + reporting + process consistency",
            ]
        )
    )

    body.append(h2("Recommended Process (High-Level)"))
    body.append(
        p(
            "Successful teams follow a consistent sequence: Discovery → Scope → UX/UI → Development → Testing → Publishing → Measurement & Iteration. Breaking this order usually leads to delays and rework."
        )
    )

    body.append(h2("Must-Haves for Quality"))
    body.append(
        ul(
            [
                "clear information architecture",
                "performance targets",
                "secure authentication and access control",
                "crash logging + core analytics events",
                "post-launch improvement plan",
            ]
        )
    )

    body.append(
        cta_box(
            "Have a mobile app idea?",
            "Start by clarifying the right use case and target audience. A clear plan reduces surprises and makes growth easier. Go to the quote page.",
            _quote_url(page),
            "Go to the quote page.",
            strong=True,
        )
    )

    content_html = "\n".join(body)
    faq_pairs = [
        ("What is the difference between a mobile app and a website?", "Apps leverage notifications and device features; websites are easier to access instantly and are strong for content."),
        ("Do all businesses need a mobile app?", "No. If repeat actions and device features are not essential, web/PWA can be a better fit."),
        ("Native vs cross-platform — what should I choose?", "Native for maximum performance; cross-platform for speed and shared product experience."),
        ("What is a PWA?", "A web-based app-like experience with some limitations depending on device/platform."),
        ("What is the first step to start?", "Define the target user and the 2–3 critical user journeys."),
        ("Is post-launch work necessary?", "Yes. Measurement and iteration are how apps improve and grow."),
    ]
    faq_json = faq(faq_pairs)

    meta_title = "What Is a Mobile App? Types, Use Cases, and Real Examples"
    meta_description = (
        "What is a mobile app? Learn mobile app types (native, cross-platform, PWA), when you actually need one, target audience logic, and practical examples."
    )
    meta_title = clamp_text(meta_title, 60)
    meta_description = clamp_text(meta_description, 160)

    return {
        "title": "What Is a Mobile App? — Types, Use Cases, and How to Decide",
        "meta_title": meta_title,
        "meta_description": meta_description,
        "content_html": content_html,
        "faq_json": faq_json,
        "published_at": timezone.now(),
    }


def _cluster_custom_mobile_app_en(page: SeoPage) -> Dict:
    """Custom cluster: Custom Mobile App — product-led, scalable, sustainable development. No pricing triggers."""
    body: List[str] = []

    body.append(h2("Overview"))
    body.append(
        p(
            "A custom mobile app is built around your business goals and user journeys, not around a generic template. The goal isn't just to \"publish an app.\" The goal is to deliver a product that: can evolve over time; is measurable and improvable; stays stable as features grow; supports integrations and real workflows."
        )
    )
    body.append(
        p(
            "This approach is ideal for both B2C and B2B products where mobile is a strategic channel — not a side project. "
            f"Service overview: {{{{ link:{_pillar_url(page)} }}}}. Workflow: {{{{ link:{_guide_url(page)} }}}}."
        )
    )

    body.append(h2("Most Common Needs"))
    body.append(h3("1) Alignment with business goals"))
    body.append(
        p(
            "A strong app is designed for a measurable outcome, such as: increasing bookings or orders; reducing operational time; improving repeat usage (retention); lowering support workload with self-service flows."
        )
    )
    body.append(h3("2) Long-term product iteration"))
    body.append(
        p(
            "Custom apps are not \"one-and-done.\" As the product grows, you'll need: new journeys and modules; performance optimization; stronger security and permissions; continuous improvements driven by data. That's why roadmap + architecture + analytics are planned from day one."
        )
    )

    body.append(h2("When Should You Choose a Custom Mobile App?"))
    body.append(
        p(
            "Custom development is the right call if you need 2–3 of the following: non-standard workflows tailored to your business; integrations (CRM/ERP/payment/logistics); multiple roles and permissions; device-driven flows (camera, QR, location, notifications); a long-term product roadmap with future expansions."
        )
    )
    body.append(
        ul(
            [
                "Non-standard workflows tailored to your business",
                "Integrations (CRM/ERP/payment/logistics)",
                "Multiple roles and permissions",
                "Device-driven flows (camera, QR, location, notifications)",
                "Long-term product roadmap with future expansions",
            ]
        )
    )

    body.append(h2("Recommended Process"))
    body.append(
        p(
            "1) Discovery & goals: define success metrics (conversion, retention, task time), map users and scenarios, clarify constraints and risks. 2) Planning: scope + acceptance criteria — define MVP scope, phase breakdown (Phase 1 / Phase 2), clear \"done\" definitions. 3) Execution: UX/UI + engineering — information architecture and screen hierarchy, design system / components, API integrations and data modeling. 4) Testing & release: scenario-based testing, performance checks, release checklist + monitoring setup."
        )
    )

    body.append(h2("Deliverables"))
    body.append(h3("Product Roadmap"))
    body.append(
        p(
            "A roadmap answers the real question: What ships first, what comes next, and why? It typically includes: MVP scope; phased feature plan; measurement plan; dependencies and risks."
        )
    )
    body.append(h3("Technical Architecture"))
    body.append(
        p(
            "Architecture supports long-term delivery by clarifying: backend structure and API contracts; authentication and authorization; security and data handling; analytics and crash monitoring; versioning and release strategy."
        )
    )

    body.append(h2("Quality Standards That Actually Matter"))
    body.append(
        ul(
            [
                "Performance: fast startup, smooth navigation",
                "Security: token handling, role-based access, safe storage",
                "Measurement: events, funnels, retention tracking",
                "Maintainability: clean standards, documentation, monitoring",
                "Sustainability: update-ready structure and stable releases",
            ]
        )
    )
    body.append(p("Quality is not a \"final checklist.\" It's a discipline across the full delivery cycle."))

    body.append(h2("Release and Sustainability"))
    body.append(
        p(
            "Publishing is the start of the feedback loop. The first 30 days usually focus on: measuring user behavior; identifying friction points; improving via small, fast iterations. This ties growth to real data instead of assumptions."
        )
    )

    body.append(
        cta_box(
            "Planning a custom mobile app?",
            "The first step is to clarify scope and set up the roadmap correctly. Share your goals and priorities; we'll work out a plan that fits. Go to the quote page.",
            _quote_url(page),
            "Go to the quote page.",
            strong=True,
        )
    )

    content_html = "\n".join(body)
    faq_pairs = [
        ("What's the difference between a custom app and a ready-made solution?", "Custom apps are tailored to your workflows and scale over time; ready-made tools are limited to standard flows."),
        ("What is an MVP and why is it important?", "An MVP launches the critical journeys first and validates direction quickly. Future phases are planned based on data."),
        ("Why does architecture matter so much?", "Architecture impacts performance, security, and long-term maintenance. Weak architecture becomes expensive as the product grows."),
        ("Do I really need analytics?", "Yes. Without metrics like retention and conversion, improvements become guesswork."),
        ("What should I prepare before starting?", "Your goal, target users, 2–3 key journeys, and any integration requirements."),
    ]
    faq_json = faq(faq_pairs)

    meta_title = "Custom Mobile App Development | Scalable, Product-Led Delivery"
    meta_description = (
        "Custom mobile app development explained: when to choose it, product roadmap, technical architecture, long-term iteration, and a process built for sustainable growth."
    )
    meta_title = clamp_text(meta_title, 60)
    meta_description = clamp_text(meta_description, 160)

    return {
        "title": "Custom Mobile App — Product-Led, Scalable, and Sustainable Development",
        "meta_title": meta_title,
        "meta_description": meta_description,
        "content_html": content_html,
        "faq_json": faq_json,
        "published_at": timezone.now(),
    }


def _cluster_android_or_ios_en(page: SeoPage) -> Dict:
    """Custom cluster: Android or iOS? — platform selection guide. No pricing triggers."""
    body: List[str] = []

    body.append(h2("Overview"))
    body.append(
        p(
            "\"Android vs iOS\" is not a tech debate — it's a product strategy decision. The right choice depends on your audience, launch plan, core user flows, and how you plan to iterate after release."
        )
    )
    body.append(
        p(
            "This page gives you a practical framework to decide with clear criteria, not guesses. "
            f"Service overview: {{{{ link:{_pillar_url(page)} }}}}. Workflow: {{{{ link:{_guide_url(page)} }}}}."
        )
    )

    body.append(h2("The Most Common Decision Drivers"))
    body.append(h3("1) Audience & Usage Behavior"))
    body.append(
        p(
            "Platform choice starts with your users: are they mass-market or niche? is this a daily habit product or an occasional utility? do you expect usage on many device types (Android diversity) or a more controlled ecosystem (iOS)? Key question: What device profile dominates your target segment?"
        )
    )
    body.append(h3("2) Time-to-Market & Learning Loop"))
    body.append(
        p(
            "If the goal is fast validation, starting with one platform often makes sense: MVP → measure real behavior → iterate; phased roadmap (v1 single platform, v2 second platform); priorities evolve based on data, not assumptions. Key question: What is the one behavior you want to validate first?"
        )
    )
    body.append(h3("3) Product Complexity & Technical Risk"))
    body.append(
        p(
            "Some features introduce different levels of complexity across platforms: real-time flows, heavy media, offline scenarios; background tasks, notifications; hardware-related features (camera, location, sensors). Key question: Does your core flow require equal stability across both platforms from day one?"
        )
    )

    body.append(h2("Practical Differences That Actually Matter"))
    body.append(h3("Android: Strengths"))
    body.append(
        ul(
            [
                "broad ecosystem → strong reach potential",
                "flexible UI and device support",
                "scalable with the right architecture",
            ]
        )
    )
    body.append(p("Trade-off: device diversity requires a serious testing and performance plan."))
    body.append(h3("iOS: Strengths"))
    body.append(
        ul(
            [
                "controlled hardware/OS landscape → stability is easier to manage",
                "consistent UX expectations",
                "often a clean iteration loop for certain products",
            ]
        )
    )
    body.append(p("Trade-off: audience alignment matters; reach expectations must be realistic."))

    body.append(h2("Recommended Process for Platform Decision"))
    body.append(h3("1) Discovery & Goals"))
    body.append(
        ul(
            [
                "define the user and the problem",
                "map critical flows (signup, booking, checkout, messaging)",
                "choose measurable metrics (activation, retention, conversion steps)",
            ]
        )
    )
    body.append(p("<strong>Output:</strong> decision criteria + MVP goal"))
    body.append(h3("2) Planning: Priorities & Delivery Criteria"))
    body.append(
        ul(
            [
                "single platform or dual platform?",
                "phased roadmap (v1, v1.1, v2)",
                "analytics event plan (what to track and why)",
            ]
        )
    )
    body.append(p("<strong>Output:</strong> roadmap + scope boundaries"))
    body.append(h3("3) Design & Development"))
    body.append(
        ul(
            [
                "mobile-first UX with clear CTAs",
                "performance-driven data flow",
                "security baseline (auth/token, data protection)",
            ]
        )
    )
    body.append(p("<strong>Output:</strong> testable build"))
    body.append(h3("4) Testing & Launch"))
    body.append(
        p(
            "device/OS coverage strategy, crash monitoring setup + release checklist, post-launch iteration loop."
        )
    )
    body.append(p("<strong>Output:</strong> monitoring plan + improvement backlog"))

    body.append(h2("Deliverables"))
    body.append(
        p(
            "A real \"platform selection guide\" should produce tangible outputs: platform decision document (why, assumptions, risk plan), MVP scope + phased roadmap, testing strategy (Android device matrix / iOS OS coverage), measurement plan (events + conversion steps)."
        )
    )

    body.append(h2("When This Approach Is the Right Fit"))
    body.append(
        p(
            "Use this framework when:"
        )
    )
    body.append(
        ul(
            [
                "your goals are measurable",
                "you want scope discipline",
                "you plan to grow through iteration after launch",
                "you want visibility into risks early",
            ]
        )
    )

    body.append(
        cta_box(
            "Share your audience and product goal",
            "We'll clarify the platform decision and turn it into a practical delivery plan. Go to the quote page.",
            _quote_url(page),
            "Go to the quote page.",
            strong=True,
        )
    )

    content_html = "\n".join(body)
    faq_pairs = [
        ("What's the first step to choose between Android and iOS?", "Define the audience and the core user flow, then set measurable goals."),
        ("Is starting with one platform a good idea?", "Yes — especially for MVPs where you want faster learning and iteration."),
        ("What's the biggest Android risk?", "Underestimating device diversity, testing scope, and performance optimization."),
        ("Why can iOS be more predictable?", "The ecosystem is more controlled, which often improves stability and test planning."),
        ("Does platform choice affect organic growth directly?", "Not directly — but performance, UX, and measurement strongly affect retention and growth."),
        ("What should you focus on after launch?", "Crash rate, activation steps, retention, and performance of critical flows."),
    ]
    faq_json = faq(faq_pairs)

    meta_title = "Android or iOS? | Platform Selection Guide for Mobile Apps"
    meta_description = (
        "Android or iOS? Choose the right platform based on audience, product goals, performance constraints, launch strategy, and sustainable development."
    )
    meta_title = clamp_text(meta_title, 60)
    meta_description = clamp_text(meta_description, 160)

    return {
        "title": "Android or iOS? — Choose the Right Platform Based on Your Goal",
        "meta_title": meta_title,
        "meta_description": meta_description,
        "content_html": content_html,
        "faq_json": faq_json,
        "published_at": timezone.now(),
    }


def _cluster_b2b_ecommerce_en(page: SeoPage) -> Dict:
    """Custom cluster: B2B E-Commerce — wholesale, dealer, quote, ERP. No pricing triggers (use rates/tiers)."""
    body: List[str] = []

    body.append(h2("Overview"))
    body.append(
        p(
            "B2B e-commerce differs significantly from traditional online stores. The target audience is not end users, but dealers, distributors, and corporate buyers."
        )
    )
    body.append(
        p(
            "Therefore, the system must support: customer-specific rates and tiers, quotation workflows, account-based purchasing, approval processes, ERP integration. Standard B2C platforms often fail to handle this complexity."
        )
    )
    body.append(
        p(
            f"Service overview: {{{{ link:{_pillar_url(page)} }}}}. Workflow: {{{{ link:{_guide_url(page)} }}}}. Request a quote: {{{{ link:{_quote_url(page)} }}}}."
        )
    )

    body.append(h2("Key B2B Features"))
    body.append(h3("Tiered Rates"))
    body.append(p("Different rate rules per customer or group."))
    body.append(h3("RFQ (Request for Quote)"))
    body.append(p("Quote-based purchasing instead of direct checkout."))
    body.append(h3("Account & Credit Management"))
    body.append(p("Deferred payments and balance tracking."))
    body.append(h3("Multi-Level Approval"))
    body.append(p("Internal purchasing authorization flow."))
    body.append(h3("ERP / CRM Integration"))
    body.append(p("Inventory and invoice synchronization."))

    body.append(h2("Development Approach"))
    body.append(
        ul(
            [
                "Business model analysis",
                "Role-based system architecture",
                "Scalable backend design",
                "Secure authentication & permissions",
                "Integration testing",
            ]
        )
    )

    body.append(h2("SEO in B2B Platforms"))
    body.append(
        p(
            "B2B platforms can generate organic traffic through: technical product pages, structured category architecture, industry-focused keywords, content-driven SEO strategy. SEO is a long-term competitive advantage."
        )
    )

    body.append(h2("Custom vs Ready-Made B2B Platforms"))
    body.append(
        p(
            "Ready systems may limit: rate and tier logic, workflow customization, performance scaling. Custom B2B e-commerce solutions: handle complex rate structures; scale with order volume; integrate deeply with ERP systems. For enterprise models, custom architecture is often preferred."
        )
    )

    body.append(h2("Post-Launch Sustainability"))
    body.append(
        ul(
            [
                "Order volume monitoring",
                "Infrastructure scaling",
                "Security hardening",
                "Backup strategy",
                "Performance optimization",
            ]
        )
    )
    body.append(p("B2B systems must grow with the business."))

    body.append(
        cta_box(
            "Define your B2B sales structure",
            "We'll design a scalable e-commerce architecture tailored to your model. Get a B2B E-Commerce quote.",
            _quote_url(page),
            "Get a B2B E-Commerce Quote",
            strong=True,
        )
    )

    content_html = "\n".join(body)
    faq_pairs = [
        ("How long does B2B e-commerce development take?", "Depends on integration scope and complexity of rate and approval workflows."),
        ("Is a ready-made platform enough?", "For simple models sometimes; for complex dealer structures, custom software is usually required."),
        ("Can you integrate with our ERP?", "Yes, with proper scoping and planning."),
    ]
    faq_json = faq(faq_pairs)

    meta_title = "B2B E-Commerce Development | Wholesale & Dealer Management System"
    meta_description = (
        "Custom B2B e-commerce development with tiered rates, quote workflows, account management, and ERP integration. Scalable enterprise solutions."
    )
    meta_title = clamp_text(meta_title, 60)
    meta_description = clamp_text(meta_description, 160)

    return {
        "title": "B2B E-Commerce — Scalable Infrastructure for Wholesale & Dealer Systems",
        "meta_title": meta_title,
        "meta_description": meta_description,
        "content_html": content_html,
        "faq_json": faq_json,
        "published_at": timezone.now(),
    }


def _cluster_react_native_vs_native_en(page: SeoPage) -> Dict:
    """Custom cluster: React Native or Native? — decision matrix, scenarios, process. No pricing triggers."""
    body: List[str] = []

    body.append(h2("Overview"))
    body.append(
        p(
            "Choosing between React Native and Native (Swift/Kotlin) is not about \"which is better.\" It’s about your goals, constraints, and product requirements."
        )
    )
    body.append(
        p(
            "This page helps you make a clear, measurable decision based on performance needs, budget, and delivery speed—so the outcome stays sustainable long-term. "
            f"Service overview: {{{{ link:{_pillar_url(page)} }}}}. Workflow: {{{{ link:{_guide_url(page)} }}}}."
        )
    )

    body.append(h2("Common decision drivers"))
    body.append(h3("Performance"))
    body.append(
        ul(
            [
                "smooth scrolling lists and feeds",
                "stable UX on low-end devices",
                "heavy animations, camera, background processing",
            ]
        )
    )

    body.append(h3("Budget"))
    body.append(
        ul(
            [
                "one cross-platform team vs two native teams",
                "long-term maintenance effort",
                "keeping spend under control as the product scales",
            ]
        )
    )

    body.append(h3("Time"))
    body.append(
        ul(
            [
                "faster MVP release",
                "iteration speed after launch",
                "store processes and testing cycles",
            ]
        )
    )

    body.append(h2("What is React Native vs Native?"))
    body.append(
        p(
            "React Native: One codebase for iOS + Android—great for fast MVPs and efficient iteration when scoped correctly."
        )
    )
    body.append(
        p(
            "Native: Separate iOS (Swift) and Android (Kotlin) apps—best for maximum performance and deepest platform control."
        )
    )

    body.append(h2("Decision matrix (quick guide)"))
    body.append(
        p(
            "This is not a one-size-fits-all answer, but a practical frame to speed up the right decision."
        )
    )
    body.append(h3("React Native is usually a strong fit if"))
    body.append(
        ul(
            [
                "you need to ship an MVP fast",
                "your app is mostly standard product flows",
                "you want one team to deliver on both platforms",
                "frequent iteration is part of the roadmap",
                "budget efficiency matters",
            ]
        )
    )
    body.append(h3("Native is usually a better fit if"))
    body.append(
        ul(
            [
                "top-tier performance is the #1 requirement",
                "your app is heavy on camera/AR/ML/video processing",
                "deep low-level hardware integrations are needed",
                "you need platform-perfect native UX in fine detail",
                "you plan separate platform-specific roadmaps",
            ]
        )
    )

    body.append(h2("Scenario-based recommendations"))
    body.append(h3("E-commerce / booking / catalog apps"))
    body.append(
        p(
            "Typical flows: listing, detail, cart, checkout, profile. React Native is often ideal here thanks to speed and long-term maintainability."
        )
    )
    body.append(h3("Social feed / messaging products"))
    body.append(
        p(
            "Key factors: smooth scrolling, media handling, notifications, offline behavior. React Native can work well—if performance targets are defined and engineered early. For very heavy real-time media, Native may be safer."
        )
    )
    body.append(h3("Camera / AR / filters / ML-heavy apps"))
    body.append(
        p(
            "When device hardware, low-level access, and high FPS are critical, Native is usually the more reliable option."
        )
    )
    body.append(h3("Internal enterprise apps / CRM / field operations"))
    body.append(
        p(
            "Where forms, workflows, and integrations dominate, React Native is often the most efficient approach (faster delivery, simpler maintenance)."
        )
    )

    body.append(h2("Recommended process"))
    body.append(
        p(
            "A structured decision and delivery flow typically looks like this: Discovery & goals (critical flows, screen-level performance targets); Planning (MVP scope, acceptance criteria, risk management); Implementation (architecture, performance discipline, analytics); Testing & release (device coverage, monitoring, rollout strategy)."
        )
    )

    body.append(h2("Deliverables"))
    body.append(
        ul(
            [
                "Decision matrix document: goals, constraints, screen-level requirements, recommended approach",
                "Scenario-based plan: MVP + phase roadmap, scope boundaries (“what’s out”)",
            ]
        )
    )

    body.append(
        cta_box(
            "Share your goal and constraints",
            "You don’t need endless meetings to decide. A clear brief is enough to recommend the right approach and delivery plan. Go to the quote page.",
            _quote_url(page),
            "Go to the quote page.",
            strong=True,
        )
    )

    content_html = "\n".join(body)
    faq_pairs = [
        (
            "Is React Native fast enough?",
            "For many product apps, yes—when performance expectations are defined and engineered early.",
        ),
        (
            "Is Native always better?",
            "Not always. Native gives more control, but can increase delivery time and required effort.",
        ),
        (
            "What’s the first step?",
            "Clarify goals and priorities, then write the MVP scope in a short brief.",
        ),
    ]
    faq_json = faq(faq_pairs)

    meta_title = "React Native or Native? | Performance, Budget, and Time Comparison"
    meta_description = (
        "React Native vs Native: how to choose the right approach. Decision matrix, scenario-based recommendations, and a structured process to align performance, budget, and delivery timeline."
    )
    meta_title = clamp_text(meta_title, 60)
    meta_description = clamp_text(meta_description, 160)

    return {
        "title": "React Native or Native? — How to Choose the Right Approach",
        "meta_title": meta_title,
        "meta_description": meta_description,
        "content_html": content_html,
        "faq_json": faq_json,
        "published_at": timezone.now(),
    }


def _cluster_corporate_website_en(page: SeoPage) -> Dict:
    """Custom cluster: Corporate Website Development — strategic planning guide, decision-stage. No pricing triggers."""
    body: List[str] = []

    body.append(h2("Why a Corporate Website Is Not Just a Website"))
    body.append(
        p(
            "Many companies treat corporate website development as a design project. In reality, it is infrastructure."
        )
    )
    body.append(
        p(
            "A poorly structured website: fails to rank, fails to convert, fails to scale, creates technical debt. "
            "A properly engineered website: builds authority, generates organic traffic, improves lead quality, supports long-term growth."
        )
    )
    body.append(
        p(
            f"For the full service framework, see {{{{ link:{_pillar_url(page)} }}}}."
        )
    )

    body.append(h2("Critical Questions Before Development"))
    body.append(
        p(
            "What is the primary goal? Lead generation? Brand positioning? International visibility? Investor credibility? Strategy defines structure."
        )
    )
    body.append(
        p(
            "Who is the target audience? B2B decision makers? End users? Technical teams? "
            "User intent shapes content hierarchy and conversion flow."
        )
    )
    body.append(
        p(
            "SEO must be engineered from the beginning. SEO is not an add-on. It requires: structured URL hierarchy, internal linking architecture, "
            "schema implementation, Core Web Vitals optimization, clean semantic markup. Technical decisions determine long-term visibility."
        )
    )

    body.append(h2("Must-Have Technical Foundations"))
    body.append(
        ul(
            [
                "SEO-friendly architecture",
                "Server-side rendering",
                "Mobile-first responsiveness",
                "Structured data",
                "Secure backend",
                "Optimized loading speed",
            ]
        )
    )

    body.append(h2("Custom Development vs Template Systems"))
    body.append(
        p(
            "Template systems offer speed. Custom development offers control. Control means: clean architecture, flexible data modeling, "
            "scalable systems, full SEO optimization. For long-term digital growth, backend flexibility becomes critical."
        )
    )
    body.append(
        p(
            f"For deeper control and scalability: {{{{ link:/en/web-design/custom-web-development/ }}}}."
        )
    )

    body.append(h2("Common Mistakes in Corporate Website Projects"))
    body.append(
        ul(
            [
                "Treating it as a visual project only",
                "Ignoring technical SEO",
                "Not planning internal structure",
                "Neglecting performance metrics",
                "Underestimating security",
            ]
        )
    )

    body.append(h2("Long-Term Value"))
    body.append(
        p(
            "Corporate website development is not a short-term task. It is the digital backbone of the organization. "
            "Strategic architecture determines whether your platform scales or stagnates."
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
                f"{{{{ link:/en/web-design/web-design-company-istanbul/ }}}}",
            ]
        )
    )
    body.append(
        cta_box(
            "Get a Quote",
            "Share your goals and target audience; we'll propose a strategic plan and next steps.",
            _quote_url(page),
            "Open the quote request page.",
            strong=True,
        )
    )

    content_html = "\n".join(body)
    faq_pairs = [
        ("What should I plan before corporate website development?", "Goals, target audience, technical SEO foundations, and process steps should be clear from the start."),
        ("Why plan SEO from the beginning?", "URL structure, internal linking, and schema must be built in from day one; adding later creates technical debt and lost visibility."),
        ("Template or custom development?", "Templates offer speed; custom offers control, scalability, and full SEO flexibility for long-term growth."),
        ("What are common mistakes?", "Treating it as design-only, ignoring technical SEO, skipping performance and security planning."),
        ("How is long-term value measured?", "Organic traffic, authority, lead quality, and scalable architecture define real value."),
        ("What do you need to provide a quote?", "Goals, target audience, reference sites, and priorities are enough."),
    ]
    faq_json = faq(faq_pairs)

    meta_title = "Corporate Website Development | Strategic Planning Guide"
    meta_description = (
        "Planning a corporate website? Learn what truly matters: SEO architecture, performance, scalability and long-term digital growth."
    )
    meta_title = clamp_text(meta_title, 60)
    meta_description = clamp_text(meta_description, 160)

    return {
        "title": "Corporate Website Development — A Strategic Investment",
        "meta_title": meta_title,
        "meta_description": meta_description,
        "content_html": content_html,
        "faq_json": faq_json,
        "published_at": timezone.now(),
    }


def _cluster_web_design_istanbul_en(page: SeoPage) -> Dict:
    """Custom cluster: Web Design in Istanbul — local SEO, competitive market, technical depth. No pricing triggers."""
    body: List[str] = []

    body.append(h2("Competing in Istanbul's Digital Landscape"))
    body.append(
        p(
            "Istanbul is one of the most competitive digital markets in the region. Businesses targeting the same keywords compete aggressively for visibility."
        )
    )
    body.append(
        p(
            "In this environment: weak technical SEO fails, slow websites lose traffic, poor structure reduces authority, generic design does not convert. "
            "Web design in Istanbul is not just about building a website — it is about engineering competitive advantage."
        )
    )
    body.append(
        p(
            f"For the full service framework, see {{{{ link:{_pillar_url(page)} }}}}."
        )
    )

    body.append(h2("Why Strategy Matters More in Istanbul"))
    body.append(
        p(
            "Local competition includes: established agencies, high-authority domains, businesses investing in content marketing, companies optimizing performance aggressively. "
            "Without structured architecture, ranking becomes extremely difficult."
        )
    )

    body.append(h2("Local SEO Beyond Keywords"))
    body.append(
        p(
            "Ranking in Istanbul requires: location-structured URL hierarchy, internal linking architecture, technical crawl efficiency, mobile performance optimization, structured data implementation. "
            "Local visibility depends on technical clarity."
        )
    )

    body.append(h2("Common Mistakes in Istanbul-Based Projects"))
    body.append(
        ul(
            [
                "Treating the website as a visual asset only",
                "Ignoring backend scalability",
                "Not planning internal content structure",
                "Overlooking performance metrics",
                "Underestimating competition",
            ]
        )
    )

    body.append(h2("Performance as a Competitive Advantage"))
    body.append(
        p(
            "Mobile traffic dominates in urban markets like Istanbul. Fast loading speed and clean backend architecture directly influence: bounce rate, engagement, search ranking, conversion performance."
        )
    )

    body.append(h2("Scalable Development for Growing Businesses"))
    body.append(
        p(
            "Businesses in Istanbul evolve quickly. Your infrastructure must support: API integrations, CRM connections, multi-language content, structured growth, high-traffic capacity. "
            "Scalable backend architecture ensures long-term stability."
        )
    )
    body.append(
        p(
            f"Custom web development: {{{{ link:/en/web-design/custom-web-development/ }}}}. "
            f"Corporate website planning: {{{{ link:/en/web-design/corporate-website-development/ }}}}."
        )
    )

    body.append(h2("Final Thoughts"))
    body.append(
        p(
            "Web design in Istanbul requires more than aesthetics. It requires strategic planning, technical SEO discipline, and scalable architecture built for competition. "
            "In high-density markets, precision matters."
        )
    )

    body.append(h2("Related pages"))
    body.append(
        ul(
            [
                f"{{{{ link:{_pillar_url(page)} }}}}",
                f"{{{{ link:{_guide_url(page)} }}}}",
                f"{{{{ link:{_quote_url(page)} }}}}",
                f"{{{{ link:/en/web-design/corporate-website-development/ }}}}",
                f"{{{{ link:/en/web-design/custom-web-development/ }}}}",
            ]
        )
    )
    body.append(
        cta_box(
            "Get a Quote",
            "Share your goals and market; we'll propose a strategy and scope built for Istanbul's competitive landscape.",
            _quote_url(page),
            "Open the quote request page.",
            strong=True,
        )
    )

    content_html = "\n".join(body)
    faq_pairs = [
        ("Why is web design in Istanbul different?", "Local competition is intense; technical errors and slow sites quickly hurt rankings. Strategic planning and technical SEO are essential."),
        ("What does local SEO require?", "Location-structured URLs, topic clusters, mobile performance, structured data, and internal linking must be planned from the start."),
        ("What are common mistakes?", "Focusing on design and leaving SEO for later, not testing performance, underestimating technical infrastructure."),
        ("Why is performance critical?", "Mobile usage is high in Istanbul; slow sites lose conversions and drop in rankings."),
        ("Why does scalability matter?", "As the business grows, integration, API, and multi-language needs arise; infrastructure must be planned accordingly."),
        ("What do you need for a quote?", "Goals, target audience, sector, and competitor examples are enough."),
    ]
    faq_json = faq(faq_pairs)

    meta_title = "Web Design in Istanbul | Competing in a High-Competition Market"
    meta_description = (
        "Professional web design and development services in Istanbul. SEO-focused, performance-driven and built for competitive markets."
    )
    meta_title = clamp_text(meta_title, 60)
    meta_description = clamp_text(meta_description, 160)

    return {
        "title": "Web Design & Development in Istanbul — Built for Competitive Markets",
        "meta_title": meta_title,
        "meta_description": meta_description,
        "content_html": content_html,
        "faq_json": faq_json,
        "published_at": timezone.now(),
    }


def _cluster_custom_web_development_en(page: SeoPage) -> Dict:
    """Custom cluster: Custom Web Development — scalable, SEO-ready, performance-driven. No pricing triggers."""
    body: List[str] = []

    body.append(h2("What Is Custom Web Development?"))
    body.append(
        p(
            "Custom web development refers to building a website or web application from the ground up, tailored specifically to business goals, workflows, and scalability needs."
        )
    )
    body.append(
        p(
            "Unlike template-based systems, custom development offers: full architectural control, flexible data modeling, advanced SEO configuration, high performance optimization, integration freedom. It is engineered, not assembled."
        )
    )
    body.append(
        p(
            f"For the full service framework, see {{{{ link:{_pillar_url(page)} }}}}."
        )
    )

    body.append(h2("Why Businesses Choose Custom Development"))
    body.append(h2("Scalability"))
    body.append(
        p(
            "Growing companies require: multi-user role management, CRM integrations, API connections, custom modules, multi-language support. Template systems often limit scalability. Custom architecture supports growth."
        )
    )
    body.append(h2("Technical SEO Advantage"))
    body.append(
        p(
            "Custom web development allows: structured URL hierarchy, advanced internal linking, detailed schema markup, crawl optimization, speed engineering. SEO becomes part of the infrastructure."
        )
    )
    body.append(h2("Performance Optimization"))
    body.append(
        p(
            "Search engines reward speed. Custom-built platforms enable: optimized backend logic, efficient database queries, clean asset loading, Core Web Vitals improvement, mobile-first performance. Performance impacts both ranking and conversions."
        )
    )

    body.append(h2("Projects That Benefit from Custom Web Development"))
    body.append(
        ul(
            [
                "Corporate platforms",
                "SaaS applications",
                "Booking systems",
                "Dashboards",
                "B2B systems",
                "Integration-heavy platforms",
            ]
        )
    )
    body.append(
        p("When complexity increases, custom architecture becomes necessary.")
    )

    body.append(h2("Development Process"))
    body.append(
        ul(
            [
                "Strategy and technical analysis",
                "Information architecture planning",
                "UI/UX design",
                "Backend development (e.g., Django-based systems)",
                "API and integration setup",
                "Performance optimization",
                "QA and launch",
            ]
        )
    )
    body.append(p("Structured process reduces technical debt."))

    body.append(h2("Security & Data Protection"))
    body.append(
        p(
            "Custom platforms enable: role-based access control, secure authentication flows, HTTPS enforcement, backend hardening, structured data protection. Security is designed into the system."
        )
    )

    body.append(h2("Custom Development vs Templates"))
    body.append(
        p(
            "Templates offer speed. Custom development offers control. Control provides: SEO flexibility, performance tuning, integration scalability, long-term adaptability. For competitive industries, control becomes a strategic advantage."
        )
    )
    body.append(
        p(
            f"Comparison: {{{{ link:/en/web-design/custom-website-vs-template/ }}}}."
        )
    )

    body.append(h2("Final Thoughts"))
    body.append(
        p(
            "Custom web development is not just about building a website. It is about engineering a scalable, secure and SEO-ready digital infrastructure designed for long-term growth."
        )
    )

    body.append(h2("Related pages"))
    body.append(
        ul(
            [
                f"{{{{ link:{_pillar_url(page)} }}}}",
                f"{{{{ link:{_guide_url(page)} }}}}",
                f"{{{{ link:{_quote_url(page)} }}}}",
                f"{{{{ link:/en/web-design/corporate-website-development/ }}}}",
                f"{{{{ link:/en/web-design/django-web-development/ }}}}",
                f"{{{{ link:/en/web-design/custom-website-vs-template/ }}}}",
            ]
        )
    )
    body.append(
        cta_box(
            "Get a Quote",
            "Share your goals and technical requirements; we'll propose a scoped approach for your custom project.",
            _quote_url(page),
            "Open the quote request page.",
            strong=True,
        )
    )

    content_html = "\n".join(body)
    faq_pairs = [
        ("What is custom web development?", "Building a website or web application from the ground up, tailored to business goals and scalability needs; not template-based."),
        ("Why choose custom development?", "Scalability, technical SEO control, performance, and security; long-term flexibility and growth."),
        ("Which projects benefit?", "Corporate platforms, SaaS, booking systems, dashboards, B2B systems, integration-heavy platforms."),
        ("How does the process work?", "Strategy, information architecture, UI/UX, backend development, API and integrations, performance, QA and launch."),
        ("How is security handled?", "Role-based access, secure auth, HTTPS, backend hardening are designed into the architecture."),
        ("Custom vs templates?", "Templates for speed; custom for control, SEO depth, and long-term adaptability."),
    ]
    faq_json = faq(faq_pairs)

    meta_title = "Custom Web Development | Scalable & SEO-Ready Solutions"
    meta_description = (
        "Scalable, secure and SEO-optimized custom web development tailored for growing businesses and advanced digital platforms."
    )
    meta_title = clamp_text(meta_title, 60)
    meta_description = clamp_text(meta_description, 160)

    return {
        "title": "Custom Web Development — Scalable, Secure & Performance-Driven",
        "meta_title": meta_title,
        "meta_description": meta_description,
        "content_html": content_html,
        "faq_json": faq_json,
        "published_at": timezone.now(),
    }


def _cluster_custom_website_vs_template_en(page: SeoPage) -> Dict:
    """Custom cluster: Custom vs Template — comparison, no pricing triggers."""
    body: List[str] = []

    body.append(h2("Introduction"))
    body.append(
        p(
            "One of the most common questions in web development: Should I choose a template-based website or invest in custom development? "
            "This decision directly impacts: SEO performance, page speed, security, scalability, long-term digital growth."
        )
    )
    body.append(
        p(
            f"We compare both approaches strategically. Full framework: {{{{ link:{_pillar_url(page)} }}}}."
        )
    )

    body.append(h2("What Is a Template Website?"))
    body.append(
        p(
            "Template websites are built using platforms like WordPress, Wix, Shopify, or pre-built themes."
        )
    )
    body.append(p("Advantages:"))
    body.append(
        ul(
            [
                "Fast setup",
                "Lower upfront investment",
                "Minimal technical complexity",
                "Suitable for small projects",
            ]
        )
    )
    body.append(p("Limitations:"))
    body.append(
        ul(
            [
                "Restricted customization",
                "Plugin dependency",
                "Performance overhead",
                "Limited technical SEO flexibility",
            ]
        )
    )
    body.append(p("Templates are ideal for simple use cases."))

    body.append(h2("What Is Custom Web Development?"))
    body.append(
        p(
            "Custom web development involves building the platform from scratch using frameworks like Django, Laravel, Node.js, or custom backend architecture."
        )
    )
    body.append(p("Advantages:"))
    body.append(
        ul(
            [
                "Full architectural control",
                "Optimized performance",
                "Advanced SEO structure",
                "Integration flexibility",
                "Long-term scalability",
            ]
        )
    )
    body.append(
        p(
            f"It is engineered to grow with the business. Details: {{{{ link:/en/web-design/custom-web-development/ }}}}."
        )
    )

    body.append(h2("SEO Comparison"))
    body.append(
        p(
            "Template websites: Limited URL structure control; plugin-heavy architecture; potential Core Web Vitals issues; constrained technical SEO adjustments."
        )
    )
    body.append(
        p(
            "Custom development: Structured internal linking; clean URL hierarchy; full schema markup control; optimized crawl efficiency; performance engineering. For competitive SEO, custom development provides stronger control."
        )
    )

    body.append(h2("Performance & Speed"))
    body.append(
        p(
            "Search engines prioritize: page speed, mobile responsiveness, Core Web Vitals, server response time. Template systems may include: excessive scripts, unused CSS/JS, shared hosting bottlenecks. Custom-built platforms allow precise optimization."
        )
    )

    body.append(h2("Security"))
    body.append(
        p(
            "Template ecosystems can face: plugin vulnerabilities, update conflicts, exploitable extensions. Custom systems allow: role-based access control, secure authentication flows, backend hardening, controlled attack surface. Security becomes part of the architecture."
        )
    )

    body.append(h2("Scalability"))
    body.append(
        p(
            "If your roadmap includes: multi-user dashboards, CRM integration, payment systems, API architecture, SaaS features — custom development is usually the sustainable path."
        )
    )

    body.append(h2("Strategic Perspective"))
    body.append(
        p(
            "Templates solve \"today's problem.\" Custom development builds \"tomorrow's infrastructure.\" Your decision should align with long-term growth goals."
        )
    )

    body.append(h2("Final Thoughts"))
    body.append(
        p(
            "There is no universal winner. But for businesses prioritizing SEO performance, scalability, and technical control, custom web development often delivers stronger long-term value."
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
                f"{{{{ link:/en/web-design/django-web-development/ }}}}",
            ]
        )
    )
    body.append(
        cta_box(
            "Get a Quote",
            "Decide together whether template or custom fits your goals; we'll propose the right scope.",
            _quote_url(page),
            "Open the quote request page.",
            strong=True,
        )
    )

    content_html = "\n".join(body)
    faq_pairs = [
        ("What is a template website?", "Built on WordPress, Wix, Shopify or themes; fast setup, limited customization and technical SEO."),
        ("What is custom web development?", "Platform built from scratch with full control; scalable, SEO-optimized, integration-ready."),
        ("SEO: template vs custom?", "Custom allows full URL, schema, internal linking and performance control; templates are more constrained."),
        ("When is a template a good fit?", "Small business, simple brochure site, short-term need, no technical integrations."),
        ("When is custom development better?", "Growth goals, SEO priority, performance critical, integrations or system infrastructure planned."),
        ("How do I decide?", "Clarify goals and vision; use the quote form to get a scoped recommendation."),
    ]
    faq_json = faq(faq_pairs)

    meta_title = "Custom Website vs Template Website | Which Is Better?"
    meta_description = (
        "Custom development or template website? Compare SEO, performance, scalability, security, and long-term growth potential."
    )
    meta_title = clamp_text(meta_title, 60)
    meta_description = clamp_text(meta_description, 160)

    return {
        "title": "Custom Website vs Template Website — How to Choose the Right Approach",
        "meta_title": meta_title,
        "meta_description": meta_description,
        "content_html": content_html,
        "faq_json": faq_json,
        "published_at": timezone.now(),
    }


def _cluster_hire_web_developer_en(page: SeoPage) -> Dict:
    """Custom cluster: Working with a Freelancer — advantages, risks, when to choose. No pricing triggers."""
    body: List[str] = []

    body.append(h2("What Does Working with a Freelancer Mean?"))
    body.append(
        p(
            "Hiring a freelance web developer means collaborating with an independent professional on a project basis. Common benefits include: flexible communication, lower initial investment, faster project start."
        )
    )
    body.append(
        p(
            "However, modern web development requires more than design. It involves SEO structure, performance optimization, scalability, and long-term maintenance."
        )
    )
    body.append(
        p(
            f"Full framework: {{{{ link:{_pillar_url(page)} }}}}. Agency comparison: {{{{ link:/en/web-design/web-design-agency/ }}}}."
        )
    )

    body.append(h2("Advantages of Hiring a Freelancer"))
    body.append(
        ul(
            [
                "Flexibility: Decision-making can be faster.",
                "Lower entry budget: Suitable for small or early-stage projects.",
                "Direct communication: You work directly with the developer.",
            ]
        )
    )
    body.append(
        p("For simple landing pages or MVP projects, freelancers can be effective.")
    )

    body.append(h2("Risks of Working with a Freelancer"))
    body.append(
        ul(
            [
                "Scalability issues: As your business grows, project complexity may exceed individual capacity.",
                "Technical SEO limitations: Not all freelancers specialize in technical SEO architecture.",
                "Performance optimization: Core Web Vitals and backend performance tuning may be overlooked.",
                "Long-term support: Ongoing maintenance and structured support may be limited.",
            ]
        )
    )

    body.append(h2("Freelancer vs Agency — How to Decide?"))
    body.append(
        p(
            "Consider: Is your project long-term? Do you need integrations or custom development? Is SEO a core growth strategy? Do you require ongoing support? Strategic digital investments usually require structured development processes."
        )
    )
    body.append(
        p(
            f"Detailed comparison: {{{{ link:/en/web-design/web-design-agency/ }}}}."
        )
    )

    body.append(h2("SEO & Technical Infrastructure Perspective"))
    body.append(
        p(
            "A professionally built website includes: structured data (schema markup), clean internal linking architecture, Core Web Vitals optimization, secure hosting configuration, long-term scalability planning. Make sure these elements are clearly defined before hiring."
        )
    )

    body.append(h2("When Is a Freelancer the Right Choice?"))
    body.append(
        ul(
            [
                "Simple landing pages",
                "Personal portfolio sites",
                "Small informational websites",
                "Early-stage MVPs",
            ]
        )
    )

    body.append(h2("When Should You Choose a Structured Team?"))
    body.append(
        ul(
            [
                "Corporate websites",
                "E-commerce platforms",
                "Custom web applications",
                "Competitive SEO-driven industries",
                "Long-term digital growth strategies",
            ]
        )
    )
    body.append(
        p(
            f"Custom development: {{{{ link:/en/web-design/custom-web-development/ }}}}."
        )
    )

    body.append(h2("Final Thoughts"))
    body.append(
        p(
            "Hiring a freelancer is not wrong. Choosing the wrong structure for your project is. Web development is a strategic investment. The right decision depends on your growth goals."
        )
    )

    body.append(h2("Related pages"))
    body.append(
        ul(
            [
                f"{{{{ link:{_pillar_url(page)} }}}}",
                f"{{{{ link:{_guide_url(page)} }}}}",
                f"{{{{ link:{_quote_url(page)} }}}}",
                f"{{{{ link:/en/web-design/web-design-agency/ }}}}",
                f"{{{{ link:/en/web-design/custom-web-development/ }}}}",
            ]
        )
    )
    body.append(
        cta_box(
            "Get a Quote",
            "Decide together whether freelancer or agency fits your goals; we'll recommend the right model.",
            _quote_url(page),
            "Open the quote request page.",
            strong=True,
        )
    )

    content_html = "\n".join(body)
    faq_pairs = [
        ("What does working with a freelancer mean?", "Collaborating with an independent developer on a project basis; flexible communication, lower entry budget, faster start."),
        ("What are the advantages?", "Flexibility, lower entry budget, direct communication; suitable for landing pages, portfolios, MVPs."),
        ("What are the risks?", "Scalability, technical SEO gaps, performance optimization and long-term support may be limited."),
        ("Freelancer or agency?", "Long-term, integration-heavy, SEO-driven projects favor agency; simple short-term projects may suit a freelancer."),
        ("When is a freelancer enough?", "Landing pages, portfolio sites, small brochure sites, early-stage MVPs."),
        ("What do you need for a quote?", "Goals, scope, and preference (freelancer or agency) are enough."),
    ]
    faq_json = faq(faq_pairs)

    meta_title = "Working with a Freelancer | Web Development Pros & Cons"
    meta_description = (
        "Should you hire a freelance web developer? Advantages, risks, scalability, and SEO considerations explained for modern businesses."
    )
    meta_title = clamp_text(meta_title, 60)
    meta_description = clamp_text(meta_description, 160)

    return {
        "title": "Working with a Freelancer — Advantages and Risks in Web Development",
        "meta_title": meta_title,
        "meta_description": meta_description,
        "content_html": content_html,
        "faq_json": faq_json,
        "published_at": timezone.now(),
    }


def _cluster_what_is_web_design_en(page: SeoPage) -> Dict:
    """Custom cluster: What Is Web Design? — high-value, trend keywords. No new page links, no pricing triggers."""
    body: List[str] = []

    body.append(h2("What Is Web Design?"))
    body.append(
        p(
            "Web design is the process of planning and implementing the visual layout, user interface (UI), user experience (UX), and technical foundation of a website. It is not only visual mockups; it is the combination of text, imagery, navigation, and interaction elements aligned with business goals and the target audience."
        )
    )
    body.append(
        p(
            "Modern web design includes desktop and mobile compatibility (responsive design), accessibility, page speed, and search engine alignment (SEO). Professional web design covers all of these."
        )
    )
    body.append(
        p(
            f"Service overview: {{{{ link:{_pillar_url(page)} }}}}. Process guide: {{{{ link:{_guide_url(page)} }}}}."
        )
    )

    body.append(h2("What Does Web Design Include?"))
    body.append(
        ul(
            [
                "Information architecture and page hierarchy",
                "Visual design and typography",
                "User flows and conversion-focused layout (CTAs)",
                "Mobile-responsive structure",
                "Technical SEO foundation (URLs, headings, meta)",
                "Performance and speed optimization",
            ]
        )
    )

    body.append(h2("Why Does Web Design Matter?"))
    body.append(
        p(
            "Your website is your brand's digital face. Visitors react to page speed, structure, and trust within seconds. Poor design or slow pages increase bounce rate; good design strengthens conversion and brand perception."
        )
    )
    body.append(
        p(
            "Search engines also evaluate user experience and technical structure. Clean code, fast loading, and logical content hierarchy affect ranking."
        )
    )

    body.append(h2("Web Design and SEO"))
    body.append(
        p(
            "SEO-friendly web design means planning heading hierarchy (H1–H2–H3), meaningful URL structure, mobile compatibility, and Core Web Vitals from the start. Technical requirements should be considered during the design phase, not added afterward."
        )
    )

    body.append(h2("Who Is It For?"))
    body.append(
        p(
            "Corporate sites, e-commerce, consulting and agencies, portfolio sites, landing pages, and SaaS products all rely on web design. Scope varies by audience and business model."
        )
    )

    body.append(h2("Final Thoughts"))
    body.append(
        p(
            "What is web design? It is a strategic and technical whole, not only visuals. With the right planning, both user experience and search visibility are strengthened."
        )
    )

    body.append(h2("Related pages"))
    body.append(
        ul(
            [
                f"{{{{ link:{_pillar_url(page)} }}}}",
                f"{{{{ link:{_guide_url(page)} }}}}",
                f"{{{{ link:{_quote_url(page)} }}}}",
            ]
        )
    )
    body.append(
        cta_box(
            "Get a Quote",
            "Share your goals for web design; we'll propose the right scope.",
            _quote_url(page),
            "Open the quote request page.",
            strong=True,
        )
    )

    content_html = "\n".join(body)
    faq_pairs = [
        ("What is web design?", "The process of planning and implementing a site's visual layout, UI/UX, and technical foundation aligned with business goals."),
        ("What does it include?", "Information architecture, visual design, user flows, responsive layout, technical SEO, and performance optimization."),
        ("Why does it matter?", "Your site is your digital face; speed, structure, and trust drive both users and search engines."),
        ("How does it relate to SEO?", "Heading hierarchy, URL structure, mobile fit, and Core Web Vitals should be planned in the design phase."),
        ("Who is it for?", "Corporate, e-commerce, consulting, agencies, portfolios, landing pages, and SaaS."),
        ("What do you need for a quote?", "Goals, target audience, and project scope are enough."),
    ]
    faq_json = faq(faq_pairs)

    meta_title = "What Is Web Design? | Professional Web Design Guide"
    meta_description = (
        "What is web design? UI, UX, responsive design, and SEO-friendly websites explained. Modern web design guide."
    )
    meta_title = clamp_text(meta_title, 60)
    meta_description = clamp_text(meta_description, 160)

    return {
        "title": "What Is Web Design? — Definition, Scope & Modern Approach",
        "meta_title": meta_title,
        "meta_description": meta_description,
        "content_html": content_html,
        "faq_json": faq_json,
        "published_at": timezone.now(),
    }


def _cluster_how_to_build_a_website_en(page: SeoPage) -> Dict:
    """Custom cluster: How to Build a Website — step-by-step, high-value. No new page links, no pricing triggers."""
    body: List[str] = []

    body.append(h2("How to Build a Website?"))
    body.append(
        p(
            "Building a website is a structured process: goal setting, planning, design, development, testing, and launch. The right steps reduce technical debt and strengthen both user experience and search engine alignment."
        )
    )
    body.append(
        p(
            f"Service overview: {{{{ link:{_pillar_url(page)} }}}}. Step-by-step guide: {{{{ link:{_guide_url(page)} }}}}."
        )
    )

    body.append(h2("Step-by-Step Website Building Process"))
    body.append(
        ul(
            [
                "Discovery and goal analysis: Define purpose, target audience, and competitors.",
                "Information architecture: Plan page structure, navigation, and content hierarchy.",
                "UI/UX design: Wireframes and design sign-off; mobile compatibility.",
                "Development: Coding, integrations, technical SEO foundation.",
                "Test and performance: Speed, security, and cross-browser checks.",
                "Launch and monitoring: Go live, sitemap, analytics, and maintenance plan.",
            ]
        )
    )

    body.append(h2("Common Mistakes"))
    body.append(
        p(
            "Starting without clear goals, leaving SEO for later, neglecting mobile experience, and separating content plan from development are common. A process-driven approach reduces these risks."
        )
    )

    body.append(h2("What to Prepare Before Starting"))
    body.append(
        ul(
            [
                "Clear business goal and target audience definition",
                "Basic content outline (copy, imagery needs)",
                "Competitor and reference site examples",
                "Domain and hosting preference (if any)",
            ]
        )
    )

    body.append(h2("Final Thoughts"))
    body.append(
        p(
            "How to build a website? Through a planned process and the right steps. Once discovery, design, development, and test are complete, you have a solid foundation for both users and search engines."
        )
    )

    body.append(h2("Related pages"))
    body.append(
        ul(
            [
                f"{{{{ link:{_pillar_url(page)} }}}}",
                f"{{{{ link:{_guide_url(page)} }}}}",
                f"{{{{ link:{_quote_url(page)} }}}}",
            ]
        )
    )
    body.append(
        cta_box(
            "Get a Quote",
            "Share your website project goals; we'll outline the right steps and scope.",
            _quote_url(page),
            "Open the quote request page.",
            strong=True,
        )
    )

    content_html = "\n".join(body)
    faq_pairs = [
        ("How to build a website?", "A planned process: goal analysis, information architecture, design, development, test, and launch."),
        ("What is the first step?", "Discovery and goal analysis; define purpose, audience, and competitors."),
        ("What are common mistakes?", "Starting without clear goals, leaving SEO for later, neglecting mobile experience."),
        ("What to prepare before starting?", "Business goal, target audience, content outline, reference examples, domain/hosting preference."),
        ("How long does the process take?", "Depends on scope; clear scope and approval cycles define the timeline."),
        ("What do you need for a quote?", "Goals, scope, and content needs are enough."),
    ]
    faq_json = faq(faq_pairs)

    meta_title = "How to Build a Website? | Step-by-Step Guide"
    meta_description = (
        "How to build a website? Discovery, design, development, test, and launch. Professional website building guide."
    )
    meta_title = clamp_text(meta_title, 60)
    meta_description = clamp_text(meta_description, 160)

    return {
        "title": "How to Build a Website? — Step-by-Step Guide",
        "meta_title": meta_title,
        "meta_description": meta_description,
        "content_html": content_html,
        "faq_json": faq_json,
        "published_at": timezone.now(),
    }


def _cluster_professional_web_design_en(page: SeoPage) -> Dict:
    """Custom cluster: Professional Web Design — SEO, performance, conversion. No pricing triggers."""
    body: List[str] = []

    body.append(h2("What Is Professional Web Design?"))
    body.append(
        p(
            "Professional web design is more than visual design. It integrates: technical SEO, performance optimization, responsive architecture, security, conversion strategy. A modern website must be engineered for search visibility and business growth."
        )
    )
    body.append(
        p(
            f"Full framework: {{{{ link:{_pillar_url(page)} }}}}."
        )
    )

    body.append(h2("Why It Matters"))
    body.append(
        p(
            "Search engines evaluate: Core Web Vitals, page speed, mobile responsiveness, internal linking structure, technical SEO foundation. Without professional architecture, competitive rankings are difficult."
        )
    )

    body.append(h2("SEO-Optimized Architecture"))
    body.append(
        ul(
            [
                "Structured heading hierarchy",
                "Clean URL structure",
                "Schema markup integration",
                "Crawl efficiency",
                "Canonical and indexing control",
            ]
        )
    )
    body.append(p("SEO should be foundational, not reactive."))

    body.append(h2("Performance & Scalability"))
    body.append(
        p(
            "High-performance web design ensures: optimized media, efficient backend architecture, fast server response, mobile-first implementation. Speed directly affects ranking and conversions."
        )
    )

    body.append(h2("Conversion-Focused UX"))
    body.append(
        p(
            "Professional design aligns with business goals: clear call-to-actions, logical navigation, trust-building layout, strategic lead capture. The objective is measurable growth."
        )
    )

    body.append(h2("Related pages"))
    body.append(
        ul(
            [
                f"{{{{ link:{_pillar_url(page)} }}}}",
                f"{{{{ link:{_guide_url(page)} }}}}",
                f"{{{{ link:{_quote_url(page)} }}}}",
                f"{{{{ link:/en/web-design/corporate-website-development/ }}}}",
                f"{{{{ link:/en/web-design/custom-web-development/ }}}}",
            ]
        )
    )
    body.append(
        cta_box(
            "Get a Quote",
            "Share your goals for a professional web design; we'll propose the right scope.",
            _quote_url(page),
            "Open the quote request page.",
            strong=True,
        )
    )

    content_html = "\n".join(body)
    faq_pairs = [
        ("What is professional web design?", "Integration of technical SEO, performance, responsive architecture, security and conversion strategy — engineered for visibility and growth."),
        ("Why does it matter?", "Search engines rank on Core Web Vitals, speed, mobile experience and technical SEO; amateur setups don't scale in competitive sectors."),
        ("How is SEO planned?", "Heading hierarchy, schema, URL structure, crawl efficiency and canonical control are set from the start."),
        ("Why is performance critical?", "Speed affects both ranking and conversion; optimized assets and backend are essential."),
        ("Who is it for?", "Corporate, e-commerce, consulting, agencies, SaaS and competitive industries."),
        ("What do you need for a quote?", "Goals, target audience and sector are enough."),
    ]
    faq_json = faq(faq_pairs)

    meta_title = "Professional Web Design | SEO-Optimized & High-Performance"
    meta_description = (
        "Professional web design services focused on SEO, performance, responsiveness, and conversion optimization for scalable digital growth."
    )
    meta_title = clamp_text(meta_title, 60)
    meta_description = clamp_text(meta_description, 160)

    return {
        "title": "Professional Web Design — SEO & Performance-Driven Solutions",
        "meta_title": meta_title,
        "meta_description": meta_description,
        "content_html": content_html,
        "faq_json": faq_json,
        "published_at": timezone.now(),
    }


def _cluster_web_developer_istanbul_en(page: SeoPage) -> Dict:
    """Custom cluster: Web Developer in Istanbul — local + hiring intent. No pricing triggers."""
    body: List[str] = []

    body.append(h2("Choosing the Right Web Developer in Istanbul"))
    body.append(
        p(
            "Selecting a web developer requires evaluating: technical SEO expertise, performance optimization, backend architecture, security implementation, long-term support. In competitive markets, technical quality defines success."
        )
    )
    body.append(
        p(
            f"Full framework: {{{{ link:{_pillar_url(page)} }}}}. Local presence: {{{{ link:/en/web-design/web-design-company-istanbul/ }}}}."
        )
    )

    body.append(h2("Why Professional Development Matters"))
    body.append(
        p(
            "A skilled web developer ensures: SEO-friendly coding standards, Core Web Vitals optimization, secure infrastructure, clean internal linking, scalable system design."
        )
    )

    body.append(h2("Freelancer or Structured Team?"))
    body.append(
        p(
            "Freelancers may suit small projects. Growth-oriented businesses benefit from structured development processes."
        )
    )
    body.append(
        p(
            f"Comparison: {{{{ link:/en/web-design/web-design-agency/ }}}}, {{{{ link:/en/web-design/hire-web-developer/ }}}}."
        )
    )

    body.append(h2("Suitable For"))
    body.append(
        ul(
            [
                "Corporate websites",
                "Custom web applications",
                "E-commerce platforms",
                "SEO-driven industries",
            ]
        )
    )
    body.append(
        p(
            f"Custom development: {{{{ link:/en/web-design/custom-web-development/ }}}}."
        )
    )

    body.append(h2("Final Thoughts"))
    body.append(
        p(
            "When choosing a web developer in Istanbul, evaluate technical foundation, SEO alignment and scalability together. The right choice supports long-term digital success."
        )
    )

    body.append(h2("Related pages"))
    body.append(
        ul(
            [
                f"{{{{ link:{_pillar_url(page)} }}}}",
                f"{{{{ link:{_guide_url(page)} }}}}",
                f"{{{{ link:{_quote_url(page)} }}}}",
                f"{{{{ link:/en/web-design/web-design-company-istanbul/ }}}}",
                f"{{{{ link:/en/web-design/custom-web-development/ }}}}",
            ]
        )
    )
    body.append(
        cta_box(
            "Get a Quote",
            "Share your goals for a web developer in Istanbul; we'll propose the right scope.",
            _quote_url(page),
            "Open the quote request page.",
            strong=True,
        )
    )

    content_html = "\n".join(body)
    faq_pairs = [
        ("What to look for when choosing a web developer in Istanbul?", "Technical SEO, performance, backend architecture, security and long-term support."),
        ("Why choose a professional developer?", "SEO-friendly code, Core Web Vitals, scalable architecture and secure infrastructure."),
        ("Freelancer or team?", "Freelancers for small projects; structured teams for growth-oriented and corporate projects."),
        ("Suitable for which projects?", "Corporate sites, custom apps, e-commerce, SEO-driven and integration-heavy platforms."),
        ("What do you need for a quote?", "Goals, scope and technical requirements are enough."),
    ]
    faq_json = faq(faq_pairs)

    meta_title = "Web Developer in Istanbul | SEO & Scalable Solutions"
    meta_description = (
        "Looking for a web developer in Istanbul? SEO-ready, high-performance, and scalable web development for modern businesses."
    )
    meta_title = clamp_text(meta_title, 60)
    meta_description = clamp_text(meta_description, 160)

    return {
        "title": "Web Developer in Istanbul — Professional & Scalable Web Solutions",
        "meta_title": meta_title,
        "meta_description": meta_description,
        "content_html": content_html,
        "faq_json": faq_json,
        "published_at": timezone.now(),
    }


def _cluster_web_design_company_en(page: SeoPage) -> Dict:
    """Custom cluster: Web Design Company — professional, SEO-focused, scalable. No pricing triggers."""
    body: List[str] = []

    body.append(h2("Choosing the Right Web Design Company Matters"))
    body.append(
        p(
            "Selecting a web design company is not a cosmetic decision. It determines: search visibility, technical performance, scalability, security stability, long-term digital growth."
        )
    )
    body.append(
        p(
            "A poorly structured project creates technical debt. A well-engineered website builds digital authority. "
            f"For the full service framework, see {{{{ link:{_pillar_url(page)} }}}}."
        )
    )

    body.append(h2("What Defines a Professional Web Development Company?"))
    body.append(
        p(
            "A professional web development company focuses on:"
        )
    )
    body.append(
        ul(
            [
                "Technical SEO architecture: clean URL hierarchy, internal linking strategy, structured data implementation, canonical management, crawl optimization. SEO must be engineered from the start.",
                "Performance optimization: Core Web Vitals, asset loading, database queries, backend efficiency, mobile responsiveness. Performance impacts both ranking and conversions.",
                "Scalable architecture: API integrations, CRM systems, custom modules, multi-language support, flexible backend systems. Scalable development reduces the need for rebuilds.",
            ]
        )
    )

    body.append(h2("Web Design Company vs Freelancer"))
    body.append(
        p(
            "A structured company typically provides: team-based expertise, process transparency, technical specialization, strategic planning. Scalability and long-term support become easier."
        )
    )
    body.append(
        p(
            f"Details: {{{{ link:/en/web-design/web-design-agency/ }}}}."
        )
    )

    body.append(h2("Custom Development vs Template Systems"))
    body.append(
        p(
            "Template systems offer speed. Custom development offers control. Control enables: advanced SEO customization, structured architecture, data modeling flexibility, performance tuning. For competitive markets, control becomes a strategic asset."
        )
    )
    body.append(
        p(
            f"Custom web development: {{{{ link:/en/web-design/custom-web-development/ }}}}."
        )
    )

    body.append(h2("Final Thoughts"))
    body.append(
        p(
            "A web design company should not just build websites. It should engineer scalable, secure, and SEO-ready digital platforms that support long-term growth."
        )
    )

    body.append(h2("Related pages"))
    body.append(
        ul(
            [
                f"{{{{ link:{_pillar_url(page)} }}}}",
                f"{{{{ link:{_guide_url(page)} }}}}",
                f"{{{{ link:{_quote_url(page)} }}}}",
                f"{{{{ link:/en/web-design/corporate-website-development/ }}}}",
                f"{{{{ link:/en/web-design/custom-web-development/ }}}}",
            ]
        )
    )
    body.append(
        cta_box(
            "Get a Quote",
            "Share your goals and technical expectations; we'll propose a scoped approach and next steps.",
            _quote_url(page),
            "Open the quote request page.",
            strong=True,
        )
    )

    content_html = "\n".join(body)
    faq_pairs = [
        ("What should I look for in a web design company?", "Reference projects, technical approach, SEO strategy, process transparency, and performance testing."),
        ("What makes a professional company different?", "They plan technical SEO, performance, and scalable architecture from the start; SEO is not an add-on."),
        ("Template or custom development?", "Depends on goals and scalability needs; custom development offers more long-term control."),
        ("Why does company structure matter?", "Team expertise, process, and strategic planning make scalability and long-term support easier."),
        ("What do you need for a quote?", "Goals, target audience, reference projects, and technical expectations are enough."),
    ]
    faq_json = faq(faq_pairs)

    meta_title = "Web Design Company | Professional & SEO-Focused Development"
    meta_description = (
        "Professional web design company delivering scalable, SEO-optimized and performance-driven web solutions."
    )
    meta_title = clamp_text(meta_title, 60)
    meta_description = clamp_text(meta_description, 160)

    return {
        "title": "Web Design Company — Engineering Performance & Digital Growth",
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
        "professional-web-design": ("Professional Web Design", ["Brand consistency", "Usability", "Performance"], ["Design system", "Component library", "Performance optimization"]),
        "web-developer-istanbul": ("Web Developer in Istanbul", ["Technical verification", "Reference evaluation"], ["Evaluation criteria", "Sample delivery process"]),
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
        if page.service.key == "ecommerce-development":
            return _ecommerce_pillar_en(page)
        if page.service.key == "mobile-app-development":
            return _mobile_app_pillar_en(page)
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
                    f"Rates & scope: {{ link:{_pricing_url(page)} }}",
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
                    f"Rates & scope: {{ link:{_pricing_url(page)} }}",
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
    # Custom cluster: React Native App Development (EN) — mobile-app-development
    # -------------------------------------------------------------------------
    if page.page_type == SeoPage.TYPE_CLUSTER and page.service.key == "mobile-app-development" and page.slug == "react-native-app-development":
        return _cluster_react_native_app_development_en(page)

    # -------------------------------------------------------------------------
    # Custom cluster: Corporate Website Development (EN)
    # -------------------------------------------------------------------------
    if page.page_type == SeoPage.TYPE_CLUSTER and page.service.key == "web-design" and page.slug == "corporate-website-development":
        return _cluster_corporate_website_en(page)

    # -------------------------------------------------------------------------
    # Custom cluster: Web Design in Istanbul (EN)
    # -------------------------------------------------------------------------
    if page.page_type == SeoPage.TYPE_CLUSTER and page.service.key == "web-design" and page.slug == "web-design-company-istanbul":
        return _cluster_web_design_istanbul_en(page)

    # -------------------------------------------------------------------------
    # Custom cluster: Professional Web Design (EN)
    # -------------------------------------------------------------------------
    if page.page_type == SeoPage.TYPE_CLUSTER and page.service.key == "web-design" and page.slug == "professional-web-design":
        return _cluster_professional_web_design_en(page)

    # -------------------------------------------------------------------------
    # Custom cluster: Custom Web Development (EN)
    # -------------------------------------------------------------------------
    if page.page_type == SeoPage.TYPE_CLUSTER and page.service.key == "web-design" and page.slug == "custom-web-development":
        return _cluster_custom_web_development_en(page)

    # -------------------------------------------------------------------------
    # Custom cluster: Web Design Company (EN) — slug: web-development-company
    # -------------------------------------------------------------------------
    if page.page_type == SeoPage.TYPE_CLUSTER and page.service.key == "web-design" and page.slug == "web-development-company":
        return _cluster_web_design_company_en(page)

    # -------------------------------------------------------------------------
    # Custom cluster: Web Developer in Istanbul (EN)
    # -------------------------------------------------------------------------
    if page.page_type == SeoPage.TYPE_CLUSTER and page.service.key == "web-design" and page.slug == "web-developer-istanbul":
        return _cluster_web_developer_istanbul_en(page)

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

    # -------------------------------------------------------------------------
    # Custom cluster: Custom Website vs Template (EN)
    # -------------------------------------------------------------------------
    if page.page_type == SeoPage.TYPE_CLUSTER and page.service.key == "web-design" and page.slug == "custom-website-vs-template":
        return _cluster_custom_website_vs_template_en(page)

    # -------------------------------------------------------------------------
    # Custom cluster: Working with a Freelancer (EN) — slug: hire-web-developer
    # -------------------------------------------------------------------------
    if page.page_type == SeoPage.TYPE_CLUSTER and page.service.key == "web-design" and page.slug == "hire-web-developer":
        return _cluster_hire_web_developer_en(page)

    # -------------------------------------------------------------------------
    # Custom cluster: What Is Web Design? (EN)
    # -------------------------------------------------------------------------
    if page.page_type == SeoPage.TYPE_CLUSTER and page.service.key == "web-design" and page.slug == "what-is-web-design":
        return _cluster_what_is_web_design_en(page)

    # -------------------------------------------------------------------------
    # Custom cluster: How to Build a Website (EN)
    # -------------------------------------------------------------------------
    if page.page_type == SeoPage.TYPE_CLUSTER and page.service.key == "web-design" and page.slug == "how-to-build-a-website":
        return _cluster_how_to_build_a_website_en(page)

    # -------------------------------------------------------------------------
    # Custom cluster: Android App Development (EN) — mobile-app-development
    # -------------------------------------------------------------------------
    if page.page_type == SeoPage.TYPE_CLUSTER and page.service.key == "mobile-app-development" and page.slug == "android-app-development":
        return _cluster_android_app_development_en(page)

    # -------------------------------------------------------------------------
    # Custom cluster: iOS App Development (EN) — mobile-app-development
    # -------------------------------------------------------------------------
    if page.page_type == SeoPage.TYPE_CLUSTER and page.service.key == "mobile-app-development" and page.slug == "ios-app-development":
        return _cluster_ios_app_development_en(page)

    # -------------------------------------------------------------------------
    # Custom cluster: Mobile App Development in Istanbul (EN) — mobile-app-development
    # -------------------------------------------------------------------------
    if page.page_type == SeoPage.TYPE_CLUSTER and page.service.key == "mobile-app-development" and page.slug == "istanbul-service":
        return _cluster_istanbul_service_en(page)

    # -------------------------------------------------------------------------
    # Custom cluster: Mobile App Freelancer (EN) — mobile-app-development
    # -------------------------------------------------------------------------
    if page.page_type == SeoPage.TYPE_CLUSTER and page.service.key == "mobile-app-development" and page.slug == "mobile-app-freelancer":
        return _cluster_mobile_app_freelancer_en(page)

    # -------------------------------------------------------------------------
    # Custom cluster: How to Build a Mobile App (EN) — mobile-app-development
    # -------------------------------------------------------------------------
    if page.page_type == SeoPage.TYPE_CLUSTER and page.service.key == "mobile-app-development" and page.slug == "how-to-build-a-mobile-app":
        return _cluster_how_to_build_mobile_app_en(page)

    # -------------------------------------------------------------------------
    # Custom cluster: What Is a Mobile App? (EN) — mobile-app-development
    # -------------------------------------------------------------------------
    if page.page_type == SeoPage.TYPE_CLUSTER and page.service.key == "mobile-app-development" and page.slug == "what-is-a-mobile-app":
        return _cluster_what_is_a_mobile_app_en(page)

    # -------------------------------------------------------------------------
    # Custom cluster: Custom Mobile App (EN) — mobile-app-development
    # -------------------------------------------------------------------------
    if page.page_type == SeoPage.TYPE_CLUSTER and page.service.key == "mobile-app-development" and page.slug == "custom-mobile-app-development":
        return _cluster_custom_mobile_app_en(page)

    # -------------------------------------------------------------------------
    # Custom cluster: Android or iOS? (EN) — mobile-app-development
    # -------------------------------------------------------------------------
    if page.page_type == SeoPage.TYPE_CLUSTER and page.service.key == "mobile-app-development" and page.slug == "android-or-ios":
        return _cluster_android_or_ios_en(page)

    # -------------------------------------------------------------------------
    # Custom cluster: React Native or Native? (EN) — mobile-app-development
    # -------------------------------------------------------------------------
    if page.page_type == SeoPage.TYPE_CLUSTER and page.service.key == "mobile-app-development" and page.slug == "react-native-vs-native":
        return _cluster_react_native_vs_native_en(page)

    # -------------------------------------------------------------------------
    # Custom cluster: B2B E-Commerce (EN) — ecommerce-development
    # -------------------------------------------------------------------------
    if page.page_type == SeoPage.TYPE_CLUSTER and page.service.key == "ecommerce-development" and page.slug == "b2b-ecommerce-development":
        return _cluster_b2b_ecommerce_en(page)

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
            ("Do you include rates here?", "No. Rates and scope are handled only on the rates & scope page."),
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


def _cluster_react_native_app_development_en(page: SeoPage) -> Dict:
    """Custom cluster: React Native App Development — one codebase for iOS + Android. No pricing triggers."""
    body: List[str] = []

    body.append(h2("Overview"))
    body.append(
        p(
            "React Native is a strong approach for building iOS and Android with a single codebase. When done right, it helps you ship an MVP faster, iterate quickly, and keep long-term maintenance more efficient."
        )
    )
    body.append(
        p(
            "The goal isn’t simply \"two platforms.\" The goal is a sustainable product with clear scope, performance targets, and a planned release process. "
            f"Service overview: {{{{ link:{_pillar_url(page)} }}}}. Workflow: {{{{ link:{_guide_url(page)} }}}}."
        )
    )

    body.append(h2("Common Needs"))
    body.append(h3("1) Speed with a single codebase"))
    body.append(
        p(
            "Teams often want to launch an MVP faster, manage both platforms with one team, and deliver features to iOS + Android simultaneously."
        )
    )
    body.append(
        ul(
            [
                "launch an MVP faster",
                "manage both platforms with one team",
                "deliver features to iOS + Android simultaneously",
            ]
        )
    )

    body.append(h3("2) Performance expectations"))
    body.append(
        p(
            "React Native can deliver great performance, but it’s not automatic. Without early decisions, you may face: laggy lists and feeds; slow UI on low-end devices; unnecessary re-renders and bundle bloat. That’s why we define critical screens and performance goals early."
        )
    )

    body.append(h3("3) Store release process"))
    body.append(
        p(
            "Even with one codebase, store releases are two separate ecosystems: App Store & Google Play requirements; testing and rollout strategy; versioning discipline; crash/ANR monitoring. Release checklist and monitoring are planned from day one."
        )
    )

    body.append(h2("When React Native Makes Sense"))
    body.append(
        p(
            "React Native is usually a good choice if: you need iOS + Android together; MVP speed and iteration matter; your app is mostly standard journeys and UI flows; you want sustainable maintenance with one team; you plan to grow with analytics-driven improvements."
        )
    )
    body.append(
        ul(
            [
                "you need iOS + Android together",
                "MVP speed and iteration matter",
                "your app is mostly standard journeys and UI flows",
                "you want sustainable maintenance with one team",
                "you plan to grow with analytics-driven improvements",
            ]
        )
    )

    body.append(h2("When Native May Be Better"))
    body.append(
        p(
            "Native can be a better fit when: you need extremely high FPS animations or game-like UI; heavy camera/AR/ML processing is core; deep low-level hardware integrations are required; top-tier performance is the most critical requirement. React Native is powerful—but not a one-size-fits-all solution."
        )
    )

    body.append(h2("Recommended Process"))
    body.append(
        p(
            "A practical delivery sequence looks like this: Discovery & goals (KPIs, journeys, critical screens); Planning (MVP scope, acceptance criteria, risks); Execution (design system, data flow, integrations, performance tuning); Testing & release (device coverage, monitoring, store readiness)."
        )
    )

    body.append(h2("Deliverables"))
    body.append(
        ul(
            [
                "MVP plan: phased scope + measurable acceptance criteria",
                "Store readiness: release checklist, notes, testing & rollout plan",
                "Analytics & measurement: funnels, retention events, crash/performance monitoring",
            ]
        )
    )

    body.append(h2("Quality Standards That Matter"))
    body.append(
        ul(
            [
                "performance: rendering discipline, list optimization, bundle control",
                "security: auth, token handling, secure storage",
                "consistency: iOS/Android UI differences managed intentionally",
                "maintainability: standards, documentation, versioning",
            ]
        )
    )

    body.append(
        cta_box(
            "Planning a React Native app?",
            "If you want to launch on both platforms, the first step is to clarify MVP scope and performance expectations. Share your goals and context; we’ll help you shape a realistic, sustainable plan. Go to the quote page.",
            _quote_url(page),
            "Go to the quote page.",
            strong=True,
        )
    )

    content_html = "\n".join(body)
    faq_pairs = [
        (
            "Can React Native build any app?",
            "Most product apps—yes. For heavy performance or deep device work, native may be the better fit.",
        ),
        (
            "Does one codebase mean identical UX on both platforms?",
            "Not automatically. Platform differences exist and should be handled intentionally in design and implementation.",
        ),
        (
            "Why is MVP planning so important?",
            "It helps you validate fast and scale based on real user data, not assumptions.",
        ),
        (
            "What should be planned for release?",
            "Store requirements, testing strategy, versioning, and monitoring should be set up early.",
        ),
    ]
    faq_json = faq(faq_pairs)

    meta_title = "React Native App Development | One Codebase for iOS + Android"
    meta_description = (
        "Build iOS and Android apps with a single React Native codebase. MVP planning, performance expectations, store release process, analytics, and sustainable delivery."
    )
    meta_title = clamp_text(meta_title, 60)
    meta_description = clamp_text(meta_description, 160)

    return {
        "title": "React Native App — One Codebase for iOS and Android",
        "meta_title": meta_title,
        "meta_description": meta_description,
        "content_html": content_html,
        "faq_json": faq_json,
        "published_at": timezone.now(),
    }

