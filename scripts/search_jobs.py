#!/usr/bin/env python3
"""Search RemoteOK, Remotive, Jobicy, and Arbeitnow (public JSON APIs) for jobs
matching keywords.

These 4 sources are hardcoded here directly — profile/job_sources.md is a
separate reference document, not something this script reads. Everything else
(LinkedIn, Indeed, local/regional job boards, staffing agencies, etc.) doesn't
have a public search API and is checked manually / via WebSearch instead.

Usage:
    python3 search_jobs.py
    python3 search_jobs.py --keywords "kubernetes,devops,sre"
"""
import argparse
import json
import re
import urllib.request

# EXAMPLE keywords only — replace with terms relevant to YOUR field.
# Deliberately specific phrases/terms only — matched against title + tags,
# never the free-text description (which is full of generic boilerplate like
# "our network of clients" or perk copy that produces false positives).
DEFAULT_KEYWORDS = [
    "your role title", "another role title", "core skill or tool",
]

HEADERS = {"User-Agent": "Mozilla/5.0 (job-search-script; personal use)"}


def fetch_json(url: str):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.load(resp)


def matches(text: str, keywords: list[str]) -> bool:
    text = text.lower()
    return any(re.search(r"\b" + re.escape(k) + r"\b", text) for k in keywords)


def search_remoteok(keywords: list[str]):
    data = fetch_json("https://remoteok.com/api")
    results = []
    for job in data:
        if "position" not in job:
            continue  # first entry is a legal notice, not a job
        # Title only: RemoteOK tags are single loose words (e.g. "cloud",
        # "engineer" as separate tags) — joining them can accidentally spell
        # out a multi-word keyword phrase that has nothing to do with the role.
        if matches(job.get("position", ""), keywords):
            results.append({
                "source": "RemoteOK",
                "title": job.get("position"),
                "company": job.get("company"),
                "location": job.get("location") or "Remote",
                "url": job.get("url") or job.get("apply_url"),
            })
    return results


def search_jobicy(keywords: list[str], tags=("network", "security", "cloud")):
    # tags default is a tech-focused EXAMPLE — Jobicy only accepts its own
    # predefined tag values (check jobicy.com for the current list), swap
    # these for whichever tags match your field.
    results = []
    seen_ids = set()
    for tag in tags:
        data = fetch_json(f"https://jobicy.com/api/v2/remote-jobs?count=20&tag={tag}")
        for job in data.get("jobs", []):
            if job["id"] in seen_ids:
                continue
            if matches(job.get("jobTitle", ""), keywords):
                seen_ids.add(job["id"])
                results.append({
                    "source": "Jobicy",
                    "title": job.get("jobTitle"),
                    "company": job.get("companyName"),
                    "location": job.get("jobGeo") or "Remote",
                    "url": job.get("url"),
                })
    return results


def search_arbeitnow(keywords: list[str]):
    data = fetch_json("https://www.arbeitnow.com/api/job-board-api")
    results = []
    for job in data.get("data", []):
        if matches(job.get("title", ""), keywords):
            results.append({
                "source": "Arbeitnow",
                "title": job.get("title"),
                "company": job.get("company_name"),
                "location": job.get("location") or ("Remote" if job.get("remote") else ""),
                "url": job.get("url"),
            })
    return results


def search_remotive(keywords: list[str], categories=("devops-sysadmin", "software-dev")):
    # categories default is a tech-focused EXAMPLE — Remotive only accepts its
    # own predefined category slugs (check remotive.com/api for the current
    # list), swap these for whichever categories match your field.
    results = []
    seen_ids = set()
    for category in categories:
        data = fetch_json(f"https://remotive.com/api/remote-jobs?category={category}&limit=200")
        for job in data.get("jobs", []):
            if job["id"] in seen_ids:
                continue
            # Title only: some listings (staffing agencies like Lemon.io) tag
            # posts with a generic catch-all list of dozens of technologies
            # unrelated to the actual role, which pollutes tag-based matching.
            if matches(job.get("title", ""), keywords):
                seen_ids.add(job["id"])
                results.append({
                    "source": "Remotive",
                    "title": job.get("title"),
                    "company": job.get("company_name"),
                    "location": job.get("candidate_required_location") or "Remote",
                    "url": job.get("url"),
                })
    return results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--keywords", help="comma-separated keywords, overrides defaults")
    args = parser.parse_args()

    keywords = [k.strip().lower() for k in args.keywords.split(",")] if args.keywords else DEFAULT_KEYWORDS

    print(f"Buscando con keywords: {', '.join(keywords)}\n")

    all_results = []
    try:
        all_results += search_remoteok(keywords)
    except Exception as e:
        print(f"[RemoteOK] error: {e}")

    try:
        all_results += search_remotive(keywords)
    except Exception as e:
        print(f"[Remotive] error: {e}")

    try:
        all_results += search_jobicy(keywords)
    except Exception as e:
        print(f"[Jobicy] error: {e}")

    try:
        all_results += search_arbeitnow(keywords)
    except Exception as e:
        print(f"[Arbeitnow] error: {e}")

    if not all_results:
        print("Sin resultados con esas keywords.")
        return

    for r in all_results:
        print(f"[{r['source']}] {r['title']} — {r['company']} ({r['location']})")
        print(f"  {r['url']}\n")

    print(f"Total: {len(all_results)} resultados")


if __name__ == "__main__":
    main()
