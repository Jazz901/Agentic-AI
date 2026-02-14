# utils/prompts.py
from __future__ import annotations


# ----------------------------
# System prompts (constants)
# ----------------------------

LINK_SYSTEM_PROMPT = """
You are provided with a list of links found on a webpage.
You are able to decide which of the links would be most relevant to include in a brochure about the company,
such as links to an About page, or a Company page, or Careers/Jobs pages.
You should respond in JSON as in this example:

{
    "links": [
        {"type": "about page", "url": "https://full.url/goes/here/about"},
        {"type": "careers page", "url": "https://another.full.url/careers"}
    ]
}
""".strip()


BROCHURE_SYSTEM_PROMPT = """
You are an assistant that analyzes the contents of several relevant pages from a company website
and creates a short brochure about the company for prospective customers, investors and recruits.
Respond in markdown without code blocks.
Include details of company culture, customers and careers/jobs if you have the information.
""".strip()


# ----------------------------
# Prompt builders
# ----------------------------

def build_links_user_prompt(url: str, links: list[str]) -> str:
    """
    Build the user prompt for link selection.
    Pass in links already scraped from the website.
    """
    header = f"""
Here is the list of links on the website {url} -
Please decide which of these are relevant web links for a brochure about the company,
respond with the full https URL in JSON format.
Do not include Terms of Service, Privacy, email links.

Links (some might be relative links):

""".lstrip()

    return header + "\n".join(links)


def build_brochure_user_prompt(company_name: str, url: str, site_text: str, max_chars: int = 5_000) -> str:
    """
    Build the user prompt for brochure generation.
    'site_text' should already contain the landing page + relevant pages content.
    """
    prompt = f"""
You are looking at a company called: {company_name}
Website: {url}

Here are the contents of its landing page and other relevant pages;
use this information to build a short brochure of the company in markdown without code blocks.

{site_text}
""".lstrip()

    return prompt[:max_chars]
