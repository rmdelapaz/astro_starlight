#!/usr/bin/env python3
"""Apply the shared Astro course shell without rewriting tutorial content."""

from pathlib import Path
import re
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent

PAGES = [
    ("astro_starlight_basic_html_tutorial.html", "Astro + Starlight Basics", "Start Here"),
    ("astro_starlight_full_site_setup_tutorial.html", "Full Site Setup", "Start Here"),
    ("astro_starlight_intermediate_advanced_tutorial.html", "Intermediate & Advanced Astro", "Start Here"),
    ("yaml_tutorial_guide.html", "YAML Guide", "Core Writing Tools"),
    ("markdown_mdx_tutorial_guide.html", "Markdown & MDX Guide", "Core Writing Tools"),
    ("starlight_project_structure_sidebar_navigation_tutorial.html", "Project Structure & Navigation", "Project Structure"),
    ("starlight_homepage_landing_page_tutorial.html", "Homepages & Landing Pages", "Project Structure"),
    ("starlight_search_metadata_tutorial.html", "Search & Metadata", "Project Structure"),
    ("starlight_custom_components_markdown_mdx_tutorial.html", "Custom MDX Components", "Components & Customization"),
    ("starlight_customizing_overriding_components_tutorial.html", "Overriding Starlight Components", "Components & Customization"),
    ("starlight_styling_theme_customization_tutorial.html", "Styling & Theme Customization", "Components & Customization"),
    ("astro_starlight_plugins_tutorial.html", "Starlight Plugins", "Components & Customization"),
    ("astro_content_collections_schemas_tutorial.html", "Content Collections & Schemas", "Content Architecture"),
    ("astro_starlight_tags_categories_filtering_tutorial.html", "Tags, Categories & Filtering", "Content Architecture"),
    ("astro_dynamic_routes_collection_indexes_tutorial.html", "Dynamic Routes & Indexes", "Content Architecture"),
    ("astro_starlight_asset_management_tutorial.html", "Asset Management", "Assets & Features"),
    ("astro_starlight_mermaid_diagrams_tutorial.html", "Mermaid Diagrams", "Assets & Features"),
    ("astro_starlight_accessibility_checklist_tutorial.html", "Accessibility Checklist", "Assets & Features"),
    ("astro_starlight_i18n_multilingual_tutorial.html", "Internationalization", "Assets & Features"),
    ("starlight_lesson_library_site_tutorial.html", "Lesson Library Capstone", "Capstone Projects"),
    ("starlight_world_bible_site_tutorial.html", "World Bible Capstone", "Capstone Projects"),
    ("astro_starlight_world_factbook_world_bible_tutorial.html", "World Factbook to World Bible", "Capstone Projects"),
    ("astro_starlight_rpg_character_sheet_system_tutorial.html", "RPG Character Sheet System", "Capstone Projects"),
    ("vercel_basic_how_to_tutorial.html", "Vercel Basics", "Deployment"),
    ("astro_starlight_deployment_workflow_tutorial.html", "Deployment Workflow", "Deployment"),
    ("astro_starlight_troubleshooting_build_errors_tutorial.html", "Troubleshooting Build Errors", "Deployment"),
]

LOOKUP = {name: (title, group, i) for i, (name, title, group) in enumerate(PAGES)}


def slug(text, used):
    value = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-") or "section"
    base, n = value, 2
    while value in used:
        value = f"{base}-{n}"
        n += 1
    used.add(value)
    return value


def fragment(html):
    return BeautifulSoup(html, "html.parser")


def modernize(path):
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    is_home = path.name == "index.html"
    info = LOOKUP.get(path.name)

    # Normalize shared head assets and metadata.
    for tag in soup.head.find_all(["link", "script"]):
        ref = tag.get("href") or tag.get("src") or ""
        if ref.endswith(("styles/main.css", "styles/styles.css", "styles/enhanced.css", "js/theme.js", "js/nav.js", "js/course.js", "js/clipboard.js")):
            tag.decompose()
    for meta in soup.head.find_all("meta", attrs={"name": "scaffold-version"}):
        meta.decompose()
    soup.head.append(fragment('<link rel="stylesheet" href="styles/main.css">').link)
    soup.head.append(fragment('<script src="js/course.js" defer></script>').script)
    desc = soup.find("meta", attrs={"name": "description"})
    if not desc:
        desc = soup.new_tag("meta")
        desc["name"] = "description"
        soup.head.append(desc)
    desc["content"] = "Learn Astro and Starlight through practical, project-focused tutorials." if is_home else (soup.find("h1").get_text(" ", strip=True) + " — Astro and Starlight course tutorial.")

    # Remove the old shared shell; keep all authored content.
    old_header = soup.find("header", attrs={"data-scaffold": "header"})
    if old_header:
        old_header.decompose()
    old_nav = soup.find("nav", attrs={"data-scaffold": "page-nav"})
    if old_nav:
        old_nav.decompose()
    for generated in soup.select(".skip-to-main, .main-nav, .breadcrumb, .toc-card, .lesson-nav, .site-footer"):
        generated.decompose()
    for footer in soup.body.find_all("footer", recursive=False):
        footer.decompose()

    shell = fragment('''
<a class="skip-to-main" href="#main-content">Skip to main content</a>
<nav class="main-nav" aria-label="Primary navigation">
  <div class="nav-container">
    <a class="nav-logo" href="index.html"><span aria-hidden="true">✦</span> Astro &amp; Starlight</a>
    <button class="mobile-menu-toggle" id="mobile-menu-toggle" aria-expanded="false" aria-controls="nav-links" aria-label="Open navigation">☰</button>
    <div class="nav-links" id="nav-links">
      <a href="index.html">Course Home</a>
      <a href="index.html#course-library">Course Library</a>
      <span class="nav-divider" aria-hidden="true"></span>
      <a href="https://rays-home.netlify.app/">Ray's House of Fun</a>
      <a href="https://rays-home.netlify.app/contact">Contact</a>
      <button class="theme-toggle" id="theme-toggle" aria-label="Switch color theme" title="Switch color theme">🌙</button>
    </div>
  </div>
</nav>''')
    for node in reversed(list(shell.contents)):
        soup.body.insert(0, node)

    main = soup.main
    main["id"] = "main-content"
    main["class"] = list(dict.fromkeys(main.get("class", []) + (["home-content"] if is_home else ["lesson-content"])))
    # The original home hero lived directly under <body>; bring it into main.
    if is_home:
        authored_header = soup.body.find("header", recursive=False)
        if authored_header:
            main.insert(0, authored_header.extract())

    # Breadcrumb sits outside main, matching the reference layout.
    current = "Home" if is_home else (info[0] if info else soup.title.get_text().split(" - ")[0])
    crumb = fragment('<nav class="breadcrumb" aria-label="Breadcrumb"><ol></ol></nav>').nav
    ol = crumb.ol
    if not is_home:
        li = soup.new_tag("li")
        a = soup.new_tag("a", href="index.html")
        a.string = "Home"
        li.append(a)
        ol.append(li)
        if info:
            li = soup.new_tag("li")
            a = soup.new_tag("a", href="index.html#course-library")
            a.string = info[1]
            li.append(a)
            ol.append(li)
    li = soup.new_tag("li")
    li["aria-current"] = "page"
    li.string = current
    ol.append(li)
    main.insert_before(crumb)

    # Add stable heading anchors and an automatic lesson TOC.
    used = {tag.get("id") for tag in main.find_all(id=True)}
    headings = main.find_all("h2")
    for heading in headings:
        if not heading.get("id"):
            heading["id"] = slug(heading.get_text(" ", strip=True), used)
    if not is_home and len(headings) >= 3:
        toc = fragment('<details class="toc-card" open><summary><span aria-hidden="true">☷</span> On this page <span class="toc-chevron" aria-hidden="true">⌄</span></summary><nav aria-label="Table of contents"><ol></ol></nav></details>').details
        for heading in headings:
            li = soup.new_tag("li")
            a = soup.new_tag("a", href="#" + heading["id"])
            a["class"] = "toc-link"
            a.string = heading.get_text(" ", strip=True)
            li.append(a)
            toc.ol.append(li)
        first_h1 = main.find("h1")
        if first_h1:
            first_h1.insert_after(toc)
        else:
            main.insert(0, toc)

    # Course navigation follows the learning path on the existing home page.
    if info:
        idx = info[2]
        nav = fragment('<nav class="lesson-nav" aria-label="Lesson navigation"></nav>').nav
        if idx:
            prev = PAGES[idx - 1]
            a = soup.new_tag("a", href=prev[0])
            a["class"] = "prev-lesson"
            a.string = "← " + prev[1]
            nav.append(a)
        a = soup.new_tag("a", href="index.html#course-library")
        a["class"] = "home-link"
        a.string = "Course Library"
        nav.append(a)
        if idx < len(PAGES) - 1:
            nxt = PAGES[idx + 1]
            a = soup.new_tag("a", href=nxt[0])
            a["class"] = "next-lesson"
            a.string = nxt[1] + " →"
            nav.append(a)
        main.append(nav)

    if is_home:
        first_section = main.find("section")
        if first_section:
            first_section["class"] = list(dict.fromkeys(first_section.get("class", []) + ["intro-card"]))
        library_heading = main.find("h2", string=lambda value: value and "Start Here" in value)
        if library_heading and library_heading.parent.name == "section":
            library_heading.parent["id"] = "course-library"
        for section in main.find_all("section"):
            if section.find("article"):
                section["class"] = list(dict.fromkeys(section.get("class", []) + ["module-section"]))

    if path.name == "vercel_basic_how_to_tutorial.html" and "End of tutorial." not in main.get_text(" ", strip=True):
        end_note = soup.new_tag("p")
        end_note["class"] = "end-note"
        end_note.string = "End of tutorial."
        main.append(end_note)

    footer = fragment('''<footer class="site-footer">
  <p><strong>Astro &amp; Starlight Course</strong> · Learn by building.</p>
  <div class="footer-links"><a href="index.html">Course Home</a><a href="https://rays-home.netlify.app/">Ray's House of Fun</a><a href="https://rays-home.netlify.app/contact">Contact</a><button id="print-button" type="button">Print Page</button></div>
  <p><small>© 2026 Ray de la Paz</small></p>
</footer>''').footer
    soup.body.append(footer)
    path.write_text(str(soup), encoding="utf-8")


for html_path in sorted(ROOT.glob("*.html")):
    modernize(html_path)
print(f"Modernized {len(list(ROOT.glob('*.html')))} HTML pages.")
