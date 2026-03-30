# TAC Hydro Backend Design Notes

## Overview
This document captures the backend data model and app layout derived from the
current frontend repo. Apps are aligned with top-level UI navigation (Home,
About Us, Services, Projects, Galleries, Contact Us) while keeping data models
close to the frontend content structure.

## Frontend Sources (for reference)
- News/articles: `src/data/newsData.ts`, `src/routes/News/NewsDetail.tsx`
- Projects: `src/routes/Projects/data/projectData.ts`, `src/routes/Projects/sections/ProjectSection.tsx`,
  map pins in `src/routes/Home/sections/MapSection.tsx`
- Team: `src/routes/AboutUs/data/teamData.ts`, `src/routes/AboutUs/sections/TeamSection.tsx`
- Careers: `src/routes/ContactUs/data/careerData.ts`, `src/routes/ContactUs/sections/CurrentVacancySection.tsx`
- Core principles: `src/data/corePrinciples.ts`
- Services: `src/components/sections/ExpertiseAndServicesSection.tsx`,
  sectors in `src/components/sections/SectorsOfServicesSection.tsx`
- Galleries: `src/routes/Galleries/sections/GallerySection.tsx`
- Contact/footer: `src/routes/ContactUs/sections/ContactDetailsSection.tsx`,
  `src/components/sections/FooterSection.tsx`

## Suggested Django Apps and Models

### home
- SiteSettings:
  company_name, tagline, address, phone, contact_email, collaboration_email,
  business_hours, facebook_url, linkedin_url, map_embed_url,
  organization_chart_image
- Banner: headline, subheadline, background_image, typewriter_words (JSON)
- ValuedPartner: name, logo, order
- NewsCategory: name, order
- News:
  title, slug, news_category (FK), image, news_date, published_at, summary,
  content_html, is_published, created_at, updated_at
- NewsAttachment: news (FK), file, title

### about_us
- AboutPageSection: section_key, title, content_html, image
- CorePrinciplesIntro:
  title, content_html, image, image_caption_title, image_caption_subtitle
- CorePrinciple: title, description, icon_key, color_class, order
- TeamCategory: name, order
- TeamMember:
  name, education, bio, photo, is_active
- TeamMemberCategory:
  team_member (FK), category (FK), position, order

### services
- ExpertiseCategory: title, icon_key, order, theme_color
- ExpertiseItem: category (FK), title, project_scope (FK nullable), order
- ServiceSector: title, image, description, order

### projects
- ProjectScope: name, order
- Project:
  title, status (choices), installed_capacity (float),
  installed_capacity_unit, latitude, longitude, description,
  technical_highlights (JSON)
- ProjectScopeMembership:
  project (FK), project_scope (FK), role
- ProjectScopeImage:
  project_scope_membership (FK), image, alt_text, order

### galleries
- GalleryCategory: name, order
- GallerySubcategory: category (FK), name, order
- GalleryImage: gallery_subcategory (FK), image, order

### contact_us
- CollaborativeAdvantageSection: title, subtitle
- CollaborativeAdvantageItem:
  section (FK), title, description, icon_key, order
- PartnershipRoadmapSection: title, subtitle
- PartnershipRoadmapStep:
  section (FK), milestone, title, description, icon_key, order
- CollaborativeEcosystemSection: title, subtitle
- CollaborativeEcosystemItem:
  section (FK), title, description, icon_key, order
- InitiateSynergySection: title, description, cta_text, cta_note
- JobCategory: name, order
- JobPosting:
  title, category (FK), type (choices), location, description,
  responsibilities (JSON), qualifications (JSON), is_open, published_at
- JobApplication:
  job (FK), first_name, middle_name, last_name, gender, phone, email,
  degree, grade, year_completed, specialization, college, abilities,
  software_proficiency, employment_status, experience_sector,
  years_experience, joining_date, expected_salary, cv_file, cover_letter_file,
  submitted_at, status

## Key Design Notes
- Use `slug` fields only where a public detail route is required
  (news articles).
- Keep explicit `order` fields to preserve display order from the frontend.
- Store news content as HTML (`content_html`) if the frontend will render as-is;
  otherwise store Markdown and render safely server-side.
- News articles should default to ordering by `news_date` descending, then
  `title` ascending.
- Store coordinates as float fields for map pins (lat/long from projects).
- Store project technical highlights as JSON to mirror the frontend map
  (use an ordered list if display order must be stable).
- Limit project scope images to a maximum of 4 per project+scope.

## Minimal API Shape (optional)
- `GET /api/home/settings/`
- `GET /api/home/valued-partners/`
- `GET /api/home/news/` (list), `GET /api/home/news/{slug}/` (detail)
- `GET /api/about-us/sections/`
- `GET /api/about-us/core-principles/`
- `GET /api/about-us/team/`
- `GET /api/services/`, `GET /api/sectors/`
- `GET /api/projects/` (filter by scope), `GET /api/projects/{id}/`
- `GET /api/galleries/` (filter by category)
- `GET /api/contact-us/collaborative-advantage/`
- `GET /api/contact-us/partnership-roadmap/`
- `GET /api/contact-us/collaborative-ecosystem/`
- `GET /api/contact-us/initiate-synergy/`
- `GET /api/contact-us/jobs/` (filter by type/category), `POST /api/contact-us/jobs/{id}/apply/`
