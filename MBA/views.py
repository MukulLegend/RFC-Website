import logging

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_POST

from .forms import (ChangePasswordForm, ContactForm, RegisterForm,
                    RegisterModelForm, UserProfileForm)
from .models import Announcement, Match, Player, Register

logger = logging.getLogger(__name__)

CLUB_SYSTEM_PROMPT = (
    "You are the friendly assistant for Ramos Football Club (RFC). The club began as 21-FC, "
    "founded by Mukul, Varun and Roshan, and was renamed after the Spanish defender Sergio Ramos. "
    "Its values are teamwork, discipline, perseverance and sportsmanship, with structured training "
    "programmes for players. Answer questions about football, training, fitness and the club clearly "
    "and concisely. If you don't know a club-specific detail (fees, timings, trial dates), say so and "
    "suggest the visitor use the Contact page. Politely decline requests unrelated to football or the club."
)


# ----------------------------------------------------------------- public pages
def Home(request):
    now = timezone.now()
    context = {
        "username": request.user.username if request.user.is_authenticated else "",
        "next_match": Match.objects.filter(date__gte=now).order_by("date").first(),
        "latest_news": Announcement.objects.filter(is_published=True)[:3],
    }
    return render(request, "home.html", context)


def About(request):
    return render(request, "about.html")


def squad(request):
    players = Player.objects.filter(is_active=True)
    groups = [(label, players.filter(position=code)) for code, label in Player.POSITIONS]
    groups = [(f"{label}s", qs) for label, qs in groups if qs.exists()]
    return render(request, "squad.html", {"groups": groups, "has_players": players.exists()})


def matches(request):
    now = timezone.now()
    context = {
        "upcoming": Match.objects.filter(date__gte=now).order_by("date"),
        "results": Match.objects.filter(date__lt=now).order_by("-date")[:20],
    }
    return render(request, "matches.html", context)


def news(request):
    return render(request, "news.html", {"items": Announcement.objects.filter(is_published=True)})


def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thanks! Your message has been sent. We'll get back to you soon.")
            return redirect("contact")
    else:
        form = ContactForm()
    return render(request, "contact.html", {"form": form})


def healthz(request):
    return HttpResponse("ok")


# ------------------------------------------------------------------ accounts
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        contact_form = RegisterModelForm(request.POST)
        if form.is_valid() and contact_form.is_valid():
            user = form.save()
            Register.objects.create(user=user, contact_no=contact_form.cleaned_data.get("contact_no"))
            login(request, user, backend="django.contrib.auth.backends.ModelBackend")
            return redirect("home")
    else:
        form = RegisterForm()
        contact_form = RegisterModelForm()
    return render(request, "register.html", {"form": form, "contact_form": contact_form})


def Login1(request):
    if request.method == "POST":
        user = authenticate(request, username=request.POST.get("username"),
                            password=request.POST.get("password"))
        if user is not None:
            login(request, user)
            next_url = request.GET.get("next", "")
            if next_url.startswith("/") and not next_url.startswith("//"):
                return redirect(next_url)
            return redirect("home")
        messages.error(request, "Invalid username or password.")
    return render(request, "login.html")


def logout_view(request):
    logout(request)
    return redirect("login")


@login_required(login_url="login")
def change_password(request):
    if request.method == "POST":
        form = ChangePasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Your password was successfully updated!")
            return redirect("dashboard")
        messages.error(request, "Please correct the error below.")
    else:
        form = ChangePasswordForm(user=request.user)
    return render(request, "change_password.html", {"form": form})


@login_required(login_url="login")
def dashboard(request):
    user = request.user
    reg, _ = Register.objects.get_or_create(user=user)
    if request.method == "POST":
        user_form = UserProfileForm(request.POST, instance=user)
        register_form = RegisterModelForm(request.POST, instance=reg)
        if user_form.is_valid() and register_form.is_valid():
            user_form.save()
            register_form.save()
            messages.success(request, "Your profile has been updated successfully.")
            return redirect("dashboard")
        messages.error(request, "Please correct the errors below.")
    else:
        user_form = UserProfileForm(instance=user)
        register_form = RegisterModelForm(instance=reg)
    return render(request, "dashboard.html", {
        "user_form": user_form,
        "register_form": register_form,
        "username": user.username,
    })


# ------------------------------------------------------------------ AI chat
@login_required(login_url="login")
@ensure_csrf_cookie
def chat(request):
    return render(request, "chat.html")


@login_required(login_url="login")
@require_POST
def chat_api(request):
    """Members-only AI chat. CSRF-protected, rate-limited, key read from environment."""
    import json

    if not settings.OPENAI_API_KEY:
        return JsonResponse({"error": "The AI assistant isn't configured yet."}, status=503)

    try:
        user_message = json.loads(request.body).get("message", "").strip()
    except (ValueError, AttributeError):
        return JsonResponse({"error": "Invalid request."}, status=400)
    if not user_message:
        return JsonResponse({"error": "Empty message."}, status=400)
    user_message = user_message[:1000]

    # simple per-user limit so nobody can drain your OpenAI credit
    key = f"chat-count-{request.user.pk}"
    used = cache.get(key, 0)
    if used >= settings.CHAT_MESSAGES_PER_HOUR:
        return JsonResponse({"error": "You've reached the hourly chat limit. Please try again later."}, status=429)
    cache.set(key, used + 1, timeout=3600)

    try:
        from openai import OpenAI

        client = OpenAI(api_key=settings.OPENAI_API_KEY)
        response = client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[
                {"role": "system", "content": CLUB_SYSTEM_PROMPT},
                {"role": "user", "content": user_message},
            ],
            max_tokens=300,
            temperature=0.7,
        )
        reply = (response.choices[0].message.content or "").strip()
        if not reply:
            return JsonResponse({"error": "No reply from the assistant."}, status=502)
        return JsonResponse({"reply": reply})
    except Exception:
        logger.exception("chat_api failed")  # details go to the server log, not the visitor
        return JsonResponse({"error": "Sorry, the assistant is unavailable right now."}, status=502)
