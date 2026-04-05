from __future__ import annotations

import os
import re
import shutil
import uuid
from datetime import date, datetime
from pathlib import Path

import django
import orjson

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tac_hydro.settings")
django.setup()

from django.conf import settings  # noqa: E402

from about_us.models import (  # noqa: E402
    AboutPageSection,
    CorePrinciple,
    CorePrinciplesIntro,
    TeamCategory,
    TeamMember,
    TeamMemberCategory,
)
from contact_us.models import (  # noqa: E402
    InitiateSynergySection,
    JobCategory,
    JobPosting,
    PartnershipRoadmapSection,
    PartnershipRoadmapStep,
)
from galleries.models import GalleryCategory, GalleryImage, GallerySubcategory  # noqa: E402
from home.models import (  # noqa: E402
    Banner,
    News,
    NewsCategory,
    SiteSettings,
    ValuedPartner,
)
from projects.models import (  # noqa: E402
    Project,
    ProjectScope,
    ProjectScopeImage,
    ProjectScopeMembership,
)
from services.models import ExpertiseCategory, ExpertiseItem, ServiceSector  # noqa: E402

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
MEDIA_ROOT = Path(settings.MEDIA_ROOT)


def load_json(name: str):
    with open(DATA_DIR / name) as f:
        return orjson.loads(f.read())


def copy_to_media(source_path: str | None, upload_to: str) -> str | None:
    if not source_path:
        return None
    source = BASE_DIR / source_path
    if not source.exists():
        return None
    dest_dir = MEDIA_ROOT / upload_to
    dest_dir.mkdir(parents=True, exist_ok=True)
    ext = source.suffix.lower()
    new_name = f"{uuid.uuid4().hex}{ext}"
    dest_path = dest_dir / new_name
    shutil.copy2(source, dest_path)
    return f"{upload_to}/{new_name}"


def parse_news_date(value: str):
    cleaned = " ".join(value.strip().split())
    for fmt in ("%b %d, %Y", "%B %d, %Y"):
        try:
            return datetime.strptime(cleaned.title(), fmt).date()
        except ValueError:
            continue
    return date.today()


def parse_capacity(value: str):
    match = re.search(r"([0-9]+(?:\.[0-9]+)?)\s*([A-Za-z]+)", value)
    if not match:
        return 0.0, "MW"
    return float(match.group(1)), match.group(2).upper()


def upsert_site_settings():
    data = load_json("site_settings.json")
    instance = SiteSettings.objects.first()
    if not instance:
        instance = SiteSettings(company_name=data.get("company_name", ""))
    instance.company_name = data.get("company_name", instance.company_name)
    instance.tagline = data.get("tagline", instance.tagline)
    instance.address = data.get("address", instance.address)
    instance.phone = data.get("phone", instance.phone)
    instance.contact_email = data.get("contact_email", instance.contact_email)
    instance.collaboration_email = data.get("collaboration_email", instance.collaboration_email)
    instance.business_hours = data.get("business_hours", instance.business_hours)
    instance.facebook_url = data.get("facebook_url", instance.facebook_url)
    instance.linkedin_url = data.get("linkedin_url", instance.linkedin_url)
    instance.map_embed_url = data.get("map_embed_url", instance.map_embed_url)
    instance.organization_chart_image = copy_to_media(data.get("organization_chart_image"), "home/organization")
    instance.founded_year = data.get("founded_year", instance.founded_year)
    instance.save()


def load_banner():
    data = load_json("banner.json")
    Banner.objects.update_or_create(
        headline=data.get("headline", ""),
        defaults={
            "subheadline": data.get("subheadline", ""),
            "background_image": copy_to_media(data.get("background_image"), "home/banners"),
            "typewriter_words": data.get("typewriter_words", []),
        },
    )


def load_valued_partners():
    data = load_json("valued_partners.json")
    for item in data:
        ValuedPartner.objects.update_or_create(
            name=item.get("name", ""),
            defaults={
                "logo": copy_to_media(item.get("logo"), "home/partners"),
                "order": item.get("order", 0),
            },
        )


def load_news():
    data = load_json("news.json")
    for item in data:
        category_name = item.get("category", "")
        category, _ = NewsCategory.objects.update_or_create(name=category_name, defaults={"order": 0})
        news_date = parse_news_date(item.get("date", ""))
        News.objects.update_or_create(
            title=item.get("title", ""),
            defaults={
                "news_category": category,
                "image": copy_to_media(item.get("image"), "home/news"),
                "news_date": news_date,
                "published_at": datetime.utcnow(),
                "summary": item.get("description", ""),
                "content_html": item.get("content", ""),
                "is_published": True,
            },
        )


def load_about_sections():
    sections = load_json("about_page_sections.json")
    for section in sections:
        AboutPageSection.objects.update_or_create(
            section_key=section.get("section_key", ""),
            defaults={
                "title": section.get("title", ""),
                "content_html": section.get("content_html", ""),
                "image": copy_to_media(section.get("image"), "about_us/sections"),
            },
        )


def load_core_principles():
    intro = load_json("core_principles_intro.json")
    CorePrinciplesIntro.objects.update_or_create(
        title=intro.get("title", ""),
        defaults={
            "content_html": intro.get("content_html", ""),
            "image": copy_to_media(intro.get("image"), "about_us/core_principles"),
            "image_caption_title": intro.get("image_caption_title", ""),
            "image_caption_subtitle": intro.get("image_caption_subtitle", ""),
        },
    )

    principles = load_json("core_principles.json")
    for item in principles:
        CorePrinciple.objects.update_or_create(
            title=item.get("title", ""),
            defaults={
                "description": item.get("description", ""),
                "icon_key": item.get("icon", ""),
                "color_class": item.get("color", ""),
                "order": item.get("order", 0),
            },
        )


CATEGORY_ORDER = {
    "Board of Directors": 1,
    "Department Leads": 2,
    "Design Leads": 3,
    "Engineering Professionals": 4,
    "Independent Consultants": 5,
}


def load_team():
    members = load_json("team.json")

    for category_name, order in CATEGORY_ORDER.items():
        TeamCategory.objects.update_or_create(
            name=category_name,
            defaults={"order": order},
        )

    for item in members:
        category_name = item.get("category", "")
        category = TeamCategory.objects.filter(name=category_name).first()
        if not category:
            continue

        member, created = TeamMember.objects.get_or_create(
            name=item.get("name", ""),
            education=item.get("education", ""),
            defaults={
                "bio": item.get("bio", ""),
                "photo": copy_to_media(item.get("photo"), "about_us/team/photo"),
                "profile_photo": copy_to_media(
                    item.get("profile_photo"),
                    "about_us/team/profile_photo",
                ),
                "is_active": True,
            },
        )

        if not created and not member.photo:
            member.photo = copy_to_media(item.get("photo"), "about_us/team/photo")
            member.save()

        if not created and not member.profile_photo:
            member.profile_photo = copy_to_media(
                item.get("profile_photo"),
                "about_us/team/profile_photo",
            )
            member.save()

        existing_category = TeamMemberCategory.objects.filter(
            team_member=member,
            category=category,
        ).exists()

        if not existing_category:
            category_order = CATEGORY_ORDER.get(category_name, 0)
            TeamMemberCategory.objects.create(
                team_member=member,
                category=category,
                technical_expertise=item.get("technical_expertise", ""),
                role=item.get("role", ""),
                order=category_order,
            )


def load_services():
    expertise_data = load_json("expertise.json")
    scope_names = {
        "Detailed Feasibility Study",
        "Detailed Engineering Design",
        "Construction Supervision",
        "Due Diligence Appraisal",
        "Progress Monitoring and Bill Vetting",
    }
    for idx, category_data in enumerate(expertise_data):
        category = ExpertiseCategory.objects.update_or_create(
            title=category_data.get("title", ""),
            defaults={
                "icon_key": category_data.get("icon", ""),
                "order": idx,
                "theme_color": category_data.get("themeColor", ""),
            },
        )[0]
        for item_idx, item_title in enumerate(category_data.get("items", [])):
            scope_name = None
            if item_title in scope_names:
                scope_name = item_title
            elif item_title == "Construction Supervision and Quality Control":
                scope_name = "Construction Supervision"
            project_scope = None
            if scope_name:
                project_scope, _ = ProjectScope.objects.update_or_create(name=scope_name, defaults={"order": 0})
            ExpertiseItem.objects.update_or_create(
                category=category,
                title=item_title,
                defaults={
                    "project_scope": project_scope,
                    "order": item_idx,
                },
            )

    sectors = load_json("service_sectors.json")
    for idx, sector in enumerate(sectors):
        ServiceSector.objects.update_or_create(
            title=sector.get("title", ""),
            defaults={
                "image": copy_to_media(sector.get("image"), "services/sectors"),
                "description": sector.get("description", ""),
                "order": idx,
            },
        )


SCOPE_ORDER = {
    "Detailed Feasibility Study": 1,
    "Detailed Engineering Design": 2,
    "Construction Supervision": 3,
    "Due Diligence Appraisal": 4,
    "Progress Monitoring and Bill Vetting": 5,
}


def load_projects():
    projects = load_json("projects.json")
    for item in projects:
        installed_capacity, installed_unit = parse_capacity(item.get("installedCapacity", "0 MW"))
        status = item.get("status", "")
        latitude, longitude = item.get("location", [0.0, 0.0])
        project = Project.objects.filter(
            title=item.get("title", ""),
            installed_capacity=installed_capacity,
            installed_capacity_unit=installed_unit,
            latitude=latitude,
            longitude=longitude,
            status=status,
        ).first()
        if not project:
            project = Project(
                title=item.get("title", ""),
                status=status,
                installed_capacity=installed_capacity,
                installed_capacity_unit=installed_unit,
                latitude=latitude,
                longitude=longitude,
                description=item.get("description", ""),
                technical_highlights=item.get("technicalHighlights", {}),
            )
        else:
            project.description = item.get("description", "")
            project.technical_highlights = item.get("technicalHighlights", {})
        project.save()

        scope_order = SCOPE_ORDER.get(item.get("scope", ""), 0)
        scope, _ = ProjectScope.objects.update_or_create(name=item.get("scope", ""), defaults={"order": scope_order})
        membership, _ = ProjectScopeMembership.objects.update_or_create(
            project=project,
            project_scope=scope,
            defaults={"role": item.get("role", "")},
        )

        for idx, image_path in enumerate(item.get("images", [])[:4]):
            stored_path = copy_to_media(image_path, "projects/scopes")
            if stored_path:
                ProjectScopeImage.objects.update_or_create(
                    project_scope_membership=membership,
                    order=idx,
                    defaults={
                        "image": stored_path,
                        "alt_text": "",
                    },
                )


def load_galleries():
    data = load_json("gallery.json")
    category_order = 0
    for category_name, subcategories in data.items():
        category, _ = GalleryCategory.objects.update_or_create(name=category_name, defaults={"order": category_order})
        category_order += 1

        subcategory_order = 0
        for subcategory_name, images in subcategories.items():
            subcategory, _ = GallerySubcategory.objects.update_or_create(
                category=category, name=subcategory_name, defaults={"order": subcategory_order}
            )
            subcategory_order += 1
            for idx, image_path in enumerate(images):
                stored_path = copy_to_media(image_path, "galleries/images")
                if stored_path:
                    GalleryImage.objects.update_or_create(
                        gallery_subcategory=subcategory,
                        order=idx,
                        defaults={"image": stored_path},
                    )


def load_contact_us():
    data = load_json("collaboration_sections.json")

    roadmap = data.get("partnership_roadmap", {})
    roadmap_section, _ = PartnershipRoadmapSection.objects.update_or_create(
        title=roadmap.get("title", ""),
        defaults={"subtitle": roadmap.get("subtitle", "")},
    )
    for item in roadmap.get("steps", []):
        PartnershipRoadmapStep.objects.update_or_create(
            section=roadmap_section,
            milestone=item.get("milestone", ""),
            title=item.get("title", ""),
            defaults={
                "description": item.get("description", ""),
                "icon_key": item.get("icon_key", ""),
                "order": item.get("order", 0),
            },
        )

    synergy = data.get("initiate_synergy", {})
    InitiateSynergySection.objects.update_or_create(
        title=synergy.get("title", ""),
        defaults={
            "description": synergy.get("description", ""),
            "cta_text": synergy.get("cta_text", ""),
            "cta_note": synergy.get("cta_note", ""),
        },
    )

    careers = load_json("careers.json")
    for job in careers:
        category, _ = JobCategory.objects.update_or_create(name=job.get("category", ""), defaults={"order": 0})
        JobPosting.objects.update_or_create(
            title=job.get("title", ""),
            category=category,
            defaults={
                "type": job.get("type", ""),
                "location": job.get("location", ""),
                "description": job.get("description", ""),
                "responsibilities": job.get("responsibilities", []),
                "qualifications": job.get("qualifications", []),
                "is_open": True,
                "published_at": None,
            },
        )

    roadmap = data.get("partnership_roadmap", {})
    roadmap_section, _ = PartnershipRoadmapSection.objects.update_or_create(
        title=roadmap.get("title", ""),
        defaults={"subtitle": roadmap.get("subtitle", "")},
    )
    for item in roadmap.get("steps", []):
        PartnershipRoadmapStep.objects.update_or_create(
            section=roadmap_section,
            milestone=item.get("milestone", ""),
            title=item.get("title", ""),
            defaults={
                "description": item.get("description", ""),
                "icon_key": item.get("icon_key", ""),
                "order": item.get("order", 0),
            },
        )

    synergy = data.get("initiate_synergy", {})
    InitiateSynergySection.objects.update_or_create(
        title=synergy.get("title", ""),
        defaults={
            "description": synergy.get("description", ""),
            "cta_text": synergy.get("cta_text", ""),
            "cta_note": synergy.get("cta_note", ""),
        },
    )

    careers = load_json("careers.json")
    for job in careers:
        category, _ = JobCategory.objects.update_or_create(name=job.get("category", ""), defaults={"order": 0})
        JobPosting.objects.update_or_create(
            title=job.get("title", ""),
            category=category,
            defaults={
                "type": job.get("type", ""),
                "location": job.get("location", ""),
                "description": job.get("description", ""),
                "responsibilities": job.get("responsibilities", []),
                "qualifications": job.get("qualifications", []),
                "is_open": True,
                "published_at": None,
            },
        )


def main():
    upsert_site_settings()
    load_banner()
    load_valued_partners()
    load_news()
    load_about_sections()
    load_core_principles()
    load_team()
    load_services()
    load_projects()
    load_galleries()
    load_contact_us()
    print("Data load complete.")


if __name__ == "__main__":
    main()
