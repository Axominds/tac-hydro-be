from datetime import datetime
from django.db.models import Sum
from django_bolt.views import APIView

from about_us.models import TeamMember
from home.models import SiteSettings, ValuedPartner
from projects.models import Project


def round_down_to_5(value):
    return value
    if value is None:
        return None
    return (value // 5) * 5


class StatsView(APIView):
    async def get(self, request):
        projects_count = await Project.objects.all().acount()
        mw_capacity_result = await Project.objects.aaggregate(total=Sum("installed_capacity"))
        mw_capacity = mw_capacity_result.get("total", 0)

        clients_count = await ValuedPartner.objects.all().acount()

        team_members_count = await TeamMember.objects.filter(is_active=True).acount()

        site_settings = await SiteSettings.objects.afirst()
        if site_settings:
            years = datetime.now().year - site_settings.founded_year
        else:
            years = None

        return {
            "mw_capacity": round_down_to_5(round(mw_capacity, 2)),
            "projects_count": round_down_to_5(projects_count),
            "clients_count": round_down_to_5(clients_count),
            "team_members_count": round_down_to_5(team_members_count),
            "years": round_down_to_5(years),
        }
