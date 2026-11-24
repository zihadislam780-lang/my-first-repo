from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import *
from .forms import *


def registration(request):
    context = {}
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            context = {'error': 'Password and Confirm Password does not match'}
        elif User.objects.filter(username=username).exists():
            context = {'error': 'Username already exists'}
        else:
            User.objects.create_user(username=username, email=email, password=password)
            return redirect('login')

    return render(request, 'registration.html', context)


def login_view(request):
    context = {}
    if request.method == "POST":
        identifier = request.POST.get('username')
        password = request.POST.get('password')

        if identifier and '@' in identifier:
            u = User.objects.filter(email=identifier).first()
            if u:
                identifier = u.username

        user = authenticate(request, username=identifier, password=password)
        if user:
            login(request, user)
            return redirect('home')
        context = {'error': 'Invalid Credentials'}

    return render(request, 'login.html', context)


def logout_view(request):
    if request.method == "POST":
        logout(request)
    return redirect('home')




def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Apnar message pathano hoyeche!")
            return redirect('contact')
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})


def home(request):
    profile = None
    skills = []
    if request.user.is_authenticated:
        profile = Profile.objects.filter(user=request.user).first()
        skills = Skill.objects.filter(user=request.user)
    return render(request, 'home.html', {'profile': profile, 'skills': skills})


def cv(request):
    if not request.user.is_authenticated:
        return redirect('login')

    context = {
        'profile': Profile.objects.filter(user=request.user).first(),
        'skills': Skill.objects.filter(user=request.user),
        'experiences': Experience.objects.filter(user=request.user),
        'educations': Education.objects.filter(user=request.user),
        'projects': Project.objects.filter(user=request.user),
    }
    return render(request, 'cv.html', context)


def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')

    profile = Profile.objects.filter(user=request.user).first()

    if request.method == "POST":
        form_type = request.POST.get('form_type')

        if form_type == 'profile':
            name = request.POST.get('name')
            bio = request.POST.get('bio')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            photo = request.FILES.get('photo')

            if profile is None:
                profile = Profile(user=request.user)
            profile.name = name
            profile.bio = bio
            profile.email = email
            profile.phone = phone
            if photo:
                profile.photo = photo
            profile.save()

        elif form_type == 'skill':
            Skill.objects.create(
                user=request.user,
                name=request.POST.get('name'),
                level=request.POST.get('level'),
            )

        elif form_type == 'experience':
            Experience.objects.create(
                user=request.user,
                company=request.POST.get('company'),
                role=request.POST.get('role'),
                start_date=request.POST.get('start_date'),
                end_date=request.POST.get('end_date') or None,
                description=request.POST.get('description'),
            )

        elif form_type == 'education':
            Education.objects.create(
                user=request.user,
                institute=request.POST.get('institute'),
                degree=request.POST.get('degree'),
                year=request.POST.get('year'),
            )

        elif form_type == 'project':
            Project.objects.create(
                user=request.user,
                title=request.POST.get('title'),
                description=request.POST.get('description'),
                link=request.POST.get('link'),
            )

        return redirect('dashboard')

    context = {
        'profile': profile,
        'skills': Skill.objects.filter(user=request.user),
        'experiences': Experience.objects.filter(user=request.user),
        'educations': Education.objects.filter(user=request.user),
        'projects': Project.objects.filter(user=request.user),
    }
    return render(request, 'dashboard.html', context)


# ---------- Skill ----------
def update_skill(request, id):
    if not request.user.is_authenticated:
        return redirect('login')
    skill = Skill.objects.get(id=id, user=request.user)
    if request.method == "POST":
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = SkillForm(instance=skill)
    return render(request, 'update.html', {'form': form, 'title': 'Update Skill'})


def delete_skill(request, id):
    if not request.user.is_authenticated:
        return redirect('login')
    skill = Skill.objects.get(id=id, user=request.user)
    skill.delete()
    return redirect('dashboard')


# ---------- Experience ----------
def update_experience(request, id):
    if not request.user.is_authenticated:
        return redirect('login')
    experience = Experience.objects.get(id=id, user=request.user)
    if request.method == "POST":
        form = ExperienceForm(request.POST, instance=experience)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ExperienceForm(instance=experience)
    return render(request, 'update.html', {'form': form, 'title': 'Update Experience'})


def delete_experience(request, id):
    if not request.user.is_authenticated:
        return redirect('login')
    experience = Experience.objects.get(id=id, user=request.user)
    experience.delete()
    return redirect('dashboard')


# ---------- Education ----------
def update_education(request, id):
    if not request.user.is_authenticated:
        return redirect('login')
    education = Education.objects.get(id=id, user=request.user)
    if request.method == "POST":
        form = EducationForm(request.POST, instance=education)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = EducationForm(instance=education)
    return render(request, 'update.html', {'form': form, 'title': 'Update Education'})


def delete_education(request, id):
    if not request.user.is_authenticated:
        return redirect('login')
    education = Education.objects.get(id=id, user=request.user)
    education.delete()
    return redirect('dashboard')


# ---------- Project ----------
def update_project(request, id):
    if not request.user.is_authenticated:
        return redirect('login')
    project = Project.objects.get(id=id, user=request.user)
    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ProjectForm(instance=project)
    return render(request, 'update.html', {'form': form, 'title': 'Update Project'})


def delete_project(request, id):
    if not request.user.is_authenticated:
        return redirect('login')
    project = Project.objects.get(id=id, user=request.user)
    project.delete()
    return redirect('dashboard')