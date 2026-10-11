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


def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Saves the lead into the database table
        Inquiry.objects.create(name=name, phone=phone, email=email, message=message)

        messages.success(request,
                         "Thank you! Your inquiry has been received. Our advisory team will contact you shortly.")
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