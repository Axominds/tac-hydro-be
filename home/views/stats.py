from datetime import datetime

from django.db.models import Sum
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from about_us.models import TeamMember
from home.models import SiteSettings, ValuedPartner
from projects.models import Project


class StatsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        projects_count = Project.objects.count()
        mw_capacity_result = Project.objects.aggregate(total=Sum("installed_capacity"))
        mw_capacity = mw_capacity_result.get("total", 0) or 0

        clients_count = ValuedPartner.objects.count()

        team_members_count = TeamMember.objects.filter(is_active=True).count()

        site_settings = SiteSettings.objects.first()
        if site_settings:
            years = datetime.now().year - site_settings.founded_year
        else:
            years = None

        return Response(
            {
                "mw_capacity": round(mw_capacity, 2),
                "projects_count": projects_count,
                "clients_count": clients_count,
                "team_members_count": team_members_count,
                "years": years,
            }
        )
