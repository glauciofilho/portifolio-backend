from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.db.models import Count
from .models import Project, ProjectAccess, File
from .utils import get_client_ip, get_user_agent, get_country_from_ip

def project_list(request):
    lang = request.GET.get("lang", "pt")

    projects = []
    for p in Project.objects.all():
        projects.append({
            "id": p.id,
            "name": p.name_pt if lang == "pt" else p.name_en,
            "summary": p.summary_pt if lang == "pt" else p.summary_en,
            "created_at": p.created_at,
        })

    return JsonResponse(projects, safe=False)

def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    lang = request.GET.get("lang", "pt")

    ip = get_client_ip(request)

    ProjectAccess.objects.create(
        project=project,
        ip_address=ip,
        user_agent=get_user_agent(request),
        country=get_country_from_ip(ip)
    )

    stacks = [
        {
            "id": link.stack.id,
            "name": link.stack.name,
            "badge_url": link.stack.badge_url
        }
        for link in project.stack_links.select_related("stack")
    ]

    files = [
        {
            "id": f.id,
            "path": f.path
        }
        for f in project.files.all()
    ]

    data = {
        "project": {
            "id": project.id,
            "name": project.name_pt if lang == "pt" else project.name_en,
            "summary": project.summary_pt if lang == "pt" else project.summary_en,
            "created_at": project.created_at,
        },
        "stacks": stacks,
        "files": files
    }

    return JsonResponse(data)

def file_detail(request, id_project, id_file):
    lang = request.GET.get("lang", "pt")

    file = get_object_or_404(
        File,
        id=id_file,
        project_id=id_project
    )

    data = {
        "id": file.id,
        "path": file.path,
        "content": file.content_pt if lang == "pt" else file.content_en
    }

    return JsonResponse(data)


def analytics(request):
    data = {
        "total_accesses": ProjectAccess.objects.count(),
        "projects": list(
            Project.objects.annotate(
                total=Count("accesses")
            ).values("id", "name_en", "total")
        ),
        "countries": list(
            ProjectAccess.objects.values("country")
            .annotate(total=Count("id"))
            .order_by("-total")
        )
    }

    return JsonResponse(data)