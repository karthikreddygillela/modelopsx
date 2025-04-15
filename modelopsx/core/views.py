from django.shortcuts import render

def main_dashboard(request):
    context = {
        'errors': {
            'cloud': 5,
            'private_ai': 5,
            'genai': 15,
        },
        'deployments': ['CHG1023564', 'CHG123456789'],
        'upcoming_deployments': ['CHG03578942', 'CHG9542365'],
        'knowledge_base': ['Splunk Setup', 'GCP Project Naming', 'GenAI Rate Limits']
    }
    return render(request, 'core/main_dashboard.html', context)

from django.shortcuts import render, redirect
from .models import UseCase
from .forms import UseCaseForm
from django.db.models import Q

def usecase_list(request):
    search_query = request.GET.get('q', '')
    usecases = UseCase.objects.filter(status='deployed')  # only approved

    if search_query:
        usecases = usecases.filter(
            Q(name__icontains=search_query)
        )

    context = {
        'usecases': usecases,
        'search_query': search_query
    }
    return render(request, 'core/usecase_list.html', context)


def usecase_create(request):
    if request.method == 'POST':
        form = UseCaseForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('usecase_list')
    else:
        form = UseCaseForm()
    return render(request, 'core/usecase_create.html', {'form': form})

from django.shortcuts import render
from .models import HubCategory, HubLink

from django.shortcuts import render, redirect, get_object_or_404
from .models import HubLink, HubCategory
from django.db.models import Q

def hub_view(request):
    category_filter = request.GET.get('category')
    search_query = request.GET.get('q', '')

    categories = HubCategory.objects.all()
    links = HubLink.objects.all()

    if category_filter:
        links = links.filter(category__name=category_filter)

    if search_query:
        links = links.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    recommended_links = []
    if request.user.is_authenticated:
        recommended_links = HubUserActivity.objects.filter(user=request.user)\
            .order_by('-access_count')\
            .values_list('link', flat=True)[:5]
        recommended_links = HubLink.objects.filter(id__in=recommended_links)

    context = {
        'categories': categories,
        'links': links,
        'recommended_links': recommended_links,
        'selected_category': category_filter,
        'search_query': search_query,
    }
    return render(request, 'core/hub_view.html', context)


from .models import HubLink, HubUserActivity
from django.utils.timezone import now

def hub_redirect(request, pk):
    link = get_object_or_404(HubLink, pk=pk)

    if request.user.is_authenticated:
        activity, created = HubUserActivity.objects.get_or_create(
            user=request.user,
            link=link
        )
        activity.access_count += 1
        activity.last_accessed = now()
        activity.save()

    return redirect(link.url)

from django.shortcuts import render, get_object_or_404
from .models import ServerHost

def server_list(request):
    servers = ServerHost.objects.all()
    return render(request, 'core/server_list.html', {'servers': servers})



from django.shortcuts import render, get_object_or_404
from .models import ServerHost
from .ssh_service import ssh_to_jumpbox  # updated function name to match reality

def shell_terminal(request, pk):
    server = get_object_or_404(ServerHost, pk=pk)
    output = ""

    if request.method == "POST":
        cmd = request.POST.get("command")

        jumpbox = {
            'ip': server.jumpbox_ip_or_hostname,
            'username': server.username,
            'auth_type': server.auth_type,
            'pem_file': server.pem_file.file.read().decode() if server.auth_type == 'pem' else None,
            'password': server.password,
        }

        output = ssh_to_jumpbox(jumpbox, cmd)

    return render(request, 'core/terminal.html', {'server': server, 'output': output})


def interactive_shell(request):
    return render(request, 'core/live_terminal.html')

