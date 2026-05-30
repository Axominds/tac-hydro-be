from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from about_us.models import TeamMember
from home.models import News, ValuedPartner
from projects.models import Project, ProjectScope, ProjectScopeMembership
from services.models import ExpertiseCategory, ServiceSector


class AdminDashboardStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        projects_count = Project.objects.count()

        scopes = ProjectScope.objects.all()
        projects_by_scope = {}
        for scope in scopes:
            count = (
                ProjectScopeMembership.objects.filter(project_scope=scope)
                .values("project")
                .distinct()
                .count()
            )
            projects_by_scope[scope.name] = count

        return Response(
            {
                "team_members_count": TeamMember.objects.filter(is_active=True).count(),
                "projects_count": projects_count,
                "projects_by_scope": projects_by_scope,
                "service_sectors_count": ServiceSector.objects.count(),
                "expertise_categories_count": ExpertiseCategory.objects.count(),
                "news_count": News.objects.count(),
                "partners_count": ValuedPartner.objects.count(),
            }
        )
