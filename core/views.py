from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from .models import Project, Lease, ProjectImage, ProjectFeature, LeaseImage, LeaseFeature, Inquiry
from .forms import ProjectForm, LeaseForm, ProjectImageFormSet, ProjectFeatureFormSet, LeaseImageFormSet, \
    LeaseFeatureFormSet


def home(request):
    featured_projects = Project.objects.all().order_by('-created_at')[:4]
    available_leases = Lease.objects.filter(is_available=True).order_by('-created_at')[:5]
    return render(request, 'core/index.html', {
        'featured_projects': featured_projects,
        'available_leases': available_leases
    })


def services_view(request):
    return render(request, 'core/services.html')


def projects_view(request):
    projects = Project.objects.all().order_by('-created_at')
    return render(request, 'core/projects.html', {'projects': projects})


def project_detail_view(request, pk):
    project = get_object_or_404(Project, pk=pk)
    return render(request, 'core/project_detail.html', {'project': project})


def lease_detail_view(request, pk):
    lease = get_object_or_404(Lease, pk=pk)
    return render(request, 'core/lease_detail.html', {'lease': lease})


def leases_view(request):
    leases = Lease.objects.filter(is_available=True).order_by('-created_at')

    # Filter Logic
    location = request.GET.get('location')
    beds = request.GET.get('beds')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    project_id = request.GET.get('project')

    if location:
        leases = leases.filter(location__icontains=location)
    if beds and beds.isdigit():
        leases = leases.filter(bedrooms__gte=int(beds))
    if min_price and min_price.isdigit():
        leases = leases.filter(rent_price__gte=int(min_price))
    if max_price and max_price.isdigit():
        leases = leases.filter(rent_price__lte=int(max_price))
    if project_id and project_id.isdigit():
        leases = leases.filter(project_id=int(project_id))

    locations = Lease.objects.filter(is_available=True).values_list('location', flat=True).distinct()
    projects = Project.objects.all()

    context = {
        'leases': leases,
        'locations': locations,
        'projects': projects,
    }
    return render(request, 'core/leases.html', context)


def about_view(request):
    random_gallery = Project.objects.exclude(image='').order_by('?')[:6]
    return render(request, 'core/about.html', {
        'random_gallery': random_gallery
    })


import re
import time
from django.core.cache import cache

def get_client_ip(request):
    """Extracts the real visitor IP behind Cloudflare and Nginx."""
    cf_ip = request.META.get('HTTP_CF_CONNECTING_IP')
    if cf_ip:
        return cf_ip
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR', '0.0.0.0')


def contact_view(request):
    if request.method == 'POST':
        name = (request.POST.get('name') or '').strip()
        phone = (request.POST.get('phone') or '').strip()
        email = (request.POST.get('email') or '').strip()
        message = (request.POST.get('message') or '').strip()

        # Anti-spam fields
        honeypot = request.POST.get('company_website', '')
        form_load_time = request.POST.get('form_load_time', '')
        human_token = request.POST.get('human_token', '')

        fake_success_msg = "Thank you! Your inquiry has been received. Our advisory team will contact you shortly."

        # 1. HONEYPOT TRAP: If the hidden field has any text, it is a bot
        if honeypot:
            messages.success(request, fake_success_msg)
            return redirect('contact')

        # 2. JAVASCRIPT & SPEED TRAP: Require valid JS token and >= 3 seconds fill time
        try:
            load_ts = int(form_load_time)
            elapsed = time.time() - load_ts
            expected_token = f"edrak_verified_{form_load_time}"
            if human_token != expected_token or elapsed < 3 or elapsed > 86400:
                messages.success(request, fake_success_msg)
                return redirect('contact')
        except (ValueError, TypeError):
            messages.success(request, fake_success_msg)
            return redirect('contact')

        # 3. LINK & SPAM KEYWORD FILTER: Real property clients don't send URLs or SEO pitches
        combined_text = f"{name} {message}".lower()
        spam_patterns = [
            r'http://', r'https://', r'www\.', r'\[url', r'<a\s+href',
            r'crypto', r'bitcoin', r'casino', r'seo\s', r'backlink',
            r'viagra', r'telegram', r'whatsapp\s+marketing', r'web\s+traffic'
        ]
        if any(re.search(pattern, combined_text) for pattern in spam_patterns):
            messages.success(request, fake_success_msg)
            return redirect('contact')

        # 4. PHONE SANITY CHECK: Must contain at least 7 digits and no random words
        digits_only = re.sub(r'\D', '', phone)
        if len(digits_only) < 7 or len(digits_only) > 15 or re.search(r'[a-zA-Z]', phone):
            messages.error(request, "Please enter a valid phone number.")
            return redirect('contact')

        # 5. IP RATE LIMITING: Max 2 inquiries per IP every 15 minutes (900 seconds)
        client_ip = get_client_ip(request)
        cache_key = f"edrak_contact_rate_{client_ip}"
        submissions = cache.get(cache_key, 0)
        if submissions >= 2:
            messages.error(request, "You have recently submitted an inquiry. Our team will reach out shortly.")
            return redirect('contact')
        cache.set(cache_key, submissions + 1, timeout=900)

        # Passed all 5 security checks -> Save genuine lead to database
        Inquiry.objects.create(name=name, phone=phone, email=email, message=message)

        messages.success(request, fake_success_msg)
        return redirect('contact')

    return render(request, 'core/contact.html')


# ==========================================
# CUSTOM EDRAK ADMIN DASHBOARD
# ==========================================
@staff_member_required
def custom_admin_dashboard(request):
    projects = Project.objects.all().order_by('-created_at')
    leases = Lease.objects.all().order_by('-created_at')

    # Inquiry Filter Logic
    inquiry_status = request.GET.get('inquiry_status', 'all')
    inquiries = Inquiry.objects.all().order_by('-created_at')

    if inquiry_status == 'resolved':
        inquiries = inquiries.filter(is_resolved=True)
    elif inquiry_status == 'unresolved':
        inquiries = inquiries.filter(is_resolved=False)

    return render(request, 'core/admin_dashboard.html', {
        'projects': projects,
        'leases': leases,
        'inquiries': inquiries,
        'inquiry_status': inquiry_status
    })


@staff_member_required
def inquiry_action_view(request):
    """Handles both single inline actions and bulk checkbox actions."""
    if request.method == 'POST':

        # --- SINGLE INLINE ACTIONS ---
        if 'single_resolve' in request.POST:
            Inquiry.objects.filter(id=request.POST.get('single_resolve')).update(is_resolved=True)
            messages.success(request, "Inquiry marked as resolved.")
            return redirect('custom_admin')

        if 'single_unresolve' in request.POST:
            Inquiry.objects.filter(id=request.POST.get('single_unresolve')).update(is_resolved=False)
            messages.success(request, "Inquiry reverted to unresolved.")
            return redirect('custom_admin')

        if 'single_delete' in request.POST:
            Inquiry.objects.filter(id=request.POST.get('single_delete')).delete()
            messages.success(request, "Inquiry deleted.")
            return redirect('custom_admin')

        if 'single_note' in request.POST:
            inq_id = request.POST.get('single_note')
            note_value = request.POST.get(f'note_{inq_id}')
            Inquiry.objects.filter(id=inq_id).update(admin_note=note_value)
            messages.success(request, "Internal note saved.")
            return redirect('custom_admin')

        # --- BULK ACTIONS (CHECKBOXES) ---
        action = request.POST.get('bulk_action')
        selected_ids = request.POST.getlist('inquiry_ids')

        if action == 'delete' and selected_ids:
            Inquiry.objects.filter(id__in=selected_ids).delete()
            messages.success(request, "Selected inquiries deleted.")
        elif action == 'resolve' and selected_ids:
            Inquiry.objects.filter(id__in=selected_ids).update(is_resolved=True)
            messages.success(request, "Selected inquiries marked as resolved.")
        elif action == 'unresolve' and selected_ids:
            Inquiry.objects.filter(id__in=selected_ids).update(is_resolved=False)
            messages.success(request, "Selected inquiries marked as unresolved.")
        elif action == 'save_notes':
            for key, value in request.POST.items():
                if key.startswith('note_'):
                    inq_id = key.split('_')[1]
                    Inquiry.objects.filter(id=inq_id).update(admin_note=value)
            messages.success(request, "All internal notes updated.")

    return redirect('custom_admin')


@staff_member_required
def item_form_view(request, item_type, pk=None):
    if item_type == 'project':
        ModelClass, FormClass = Project, ProjectForm
        ImageFormSet, FeatureFormSet = ProjectImageFormSet, ProjectFeatureFormSet
    else:
        ModelClass, FormClass = Lease, LeaseForm
        ImageFormSet, FeatureFormSet = LeaseImageFormSet, LeaseFeatureFormSet

    instance = get_object_or_404(ModelClass, pk=pk) if pk else None

    if request.method == 'POST':
        form = FormClass(request.POST, request.FILES, instance=instance)
        image_formset = ImageFormSet(request.POST, request.FILES, instance=instance)
        feature_formset = FeatureFormSet(request.POST, instance=instance)

        if form.is_valid() and image_formset.is_valid() and feature_formset.is_valid():
            saved_instance = form.save()
            image_formset.instance = saved_instance
            image_formset.save()
            feature_formset.instance = saved_instance
            feature_formset.save()
            return redirect('custom_admin')
    else:
        form = FormClass(instance=instance)
        image_formset = ImageFormSet(instance=instance)
        feature_formset = FeatureFormSet(instance=instance)

    return render(request, 'core/admin_form.html', {
        'form': form, 'image_formset': image_formset, 'feature_formset': feature_formset,
        'item_type': item_type, 'instance': instance
    })


@staff_member_required
def item_delete_view(request, item_type, pk):
    ModelClass = Project if item_type == 'project' else Lease
    instance = get_object_or_404(ModelClass, pk=pk)
    if request.method == 'POST':
        instance.delete()
    return redirect('custom_admin')


from .models import Project, Lease


def why_edrak(request):
    projects = Project.objects.all()
    leases = Lease.objects.select_related('project').all()[:6]

    # Extract unique statuses from backend projects for dynamic filter buttons
    project_statuses = Project.objects.values_list('status', flat=True).distinct()

    context = {
        'projects': projects,
        'leases': leases,
        'project_statuses': project_statuses,
        'total_projects': projects.count(),
        'total_leases': Lease.objects.count(),
    }
    return render(request, 'core/why_edrak.html', context)