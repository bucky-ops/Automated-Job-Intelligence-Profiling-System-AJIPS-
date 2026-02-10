from __future__ import annotations

import re
from collections import Counter
from typing import Dict, List, Set

# Comprehensive skill database organized by category
SKILL_DATABASE = {
    # Programming Languages
    "languages": {
        "python",
        "java",
        "javascript",
        "typescript",
        "c++",
        "c#",
        "go",
        "golang",
        "rust",
        "ruby",
        "php",
        "swift",
        "kotlin",
        "scala",
        "r",
        "matlab",
        "perl",
        "shell",
        "bash",
        "powershell",
        "vba",
    },
    # Web Frameworks & Libraries
    "web_frameworks": {
        "react",
        "angular",
        "vue",
        "vue.js",
        "next.js",
        "nuxt",
        "svelte",
        "django",
        "flask",
        "fastapi",
        "express",
        "express.js",
        "node.js",
        "spring",
        "spring boot",
        "asp.net",
        ".net",
        "laravel",
        "rails",
        "jquery",
        "bootstrap",
        "tailwind",
        "material-ui",
        "redux",
    },
    # Databases
    "databases": {
        "postgresql",
        "postgres",
        "mysql",
        "mongodb",
        "redis",
        "cassandra",
        "dynamodb",
        "elasticsearch",
        "oracle",
        "sql server",
        "mariadb",
        "sqlite",
        "neo4j",
        "couchdb",
        "influxdb",
        "timescaledb",
    },
    # Cloud Platforms
    "cloud": {
        "aws",
        "amazon web services",
        "azure",
        "gcp",
        "google cloud",
        "heroku",
        "digitalocean",
        "linode",
        "cloudflare",
        "vercel",
        "netlify",
        "firebase",
        "supabase",
    },
    # DevOps & Infrastructure
    "devops": {
        "docker",
        "kubernetes",
        "k8s",
        "terraform",
        "ansible",
        "jenkins",
        "gitlab ci",
        "github actions",
        "circleci",
        "travis ci",
        "helm",
        "vagrant",
        "puppet",
        "chef",
        "nginx",
        "apache",
        "prometheus",
        "grafana",
        "datadog",
        "new relic",
        "splunk",
    },
    # Data & Analytics
    "data_tools": {
        "spark",
        "apache spark",
        "hadoop",
        "airflow",
        "kafka",
        "flink",
        "tableau",
        "power bi",
        "looker",
        "dbt",
        "snowflake",
        "databricks",
        "pandas",
        "numpy",
        "scikit-learn",
        "tensorflow",
        "pytorch",
        "keras",
    },
    # Version Control & Collaboration
    "tools": {
        "git",
        "github",
        "gitlab",
        "bitbucket",
        "jira",
        "confluence",
        "slack",
        "trello",
        "asana",
        "notion",
        "figma",
        "sketch",
    },
    # Methodologies & Practices
    "methodologies": {
        "agile",
        "scrum",
        "kanban",
        "devops",
        "ci/cd",
        "tdd",
        "bdd",
        "microservices",
        "rest",
        "restful",
        "graphql",
        "api",
        "soap",
        "oauth",
        "jwt",
        "saml",
        "sso",
    },
    # Soft Skills
    "soft_skills": {
        "leadership",
        "communication",
        "teamwork",
        "problem-solving",
        "analytical",
        "critical thinking",
        "collaboration",
        "mentoring",
        "presentation",
        "documentation",
        "project management",
    },
}

# Multi-word skills that need special handling
MULTI_WORD_SKILLS = {
    "machine learning",
    "deep learning",
    "natural language processing",
    "computer vision",
    "data science",
    "software engineering",
    "web development",
    "mobile development",
    "full stack",
    "front end",
    "back end",
    "backend",
    "frontend",
    "cloud computing",
    "big data",
    "artificial intelligence",
    "version control",
    "continuous integration",
    "continuous deployment",
    "test driven development",
    "object oriented",
    "functional programming",
    "responsive design",
    "user experience",
    "user interface",
    "ui/ux",
    "rest api",
    "microservices architecture",
}

# Create a flat set of all skills for quick lookup
ALL_SKILLS: Set[str] = set()
for category_skills in SKILL_DATABASE.values():
    ALL_SKILLS.update(category_skills)
ALL_SKILLS.update(MULTI_WORD_SKILLS)


def extract_skills(text: str) -> List[str]:
    """
    Extract technical and soft skills from job posting text.
    Uses pattern matching for both single-word and multi-word skills.
    """
    text_lower = text.lower()
    found_skills: Dict[str, int] = {}

    # Extract multi-word skills first (to avoid partial matches)
    for skill in MULTI_WORD_SKILLS:
        # Use word boundaries for better matching
        pattern = r"\b" + re.escape(skill) + r"\b"
        matches = len(re.findall(pattern, text_lower))
        if matches > 0:
            found_skills[skill] = matches

    # Extract single-word skills
    # Tokenize while preserving some punctuation patterns
    tokens = re.findall(r"\b[\w+#.-]+\b", text_lower)

    for token in tokens:
        # Clean token
        cleaned = token.strip(".,;:()[]{}")
        if cleaned in ALL_SKILLS and cleaned not in found_skills:
            found_skills[cleaned] = tokens.count(token)

    # Sort by frequency and return
    sorted_skills = sorted(found_skills.items(), key=lambda x: x[1], reverse=True)
    return [skill for skill, _ in sorted_skills]


def categorize_skills(skills: List[str]) -> Dict[str, List[str]]:
    """
    Categorize extracted skills into their respective domains.
    """
    categorized = {category: [] for category in SKILL_DATABASE.keys()}
    categorized["other"] = []

    for skill in skills:
        categorized_flag = False
        for category, category_skills in SKILL_DATABASE.items():
            if skill in category_skills:
                categorized[category].append(skill)
                categorized_flag = True
                break

        if not categorized_flag and skill in MULTI_WORD_SKILLS:
            # Categorize multi-word skills based on keywords
            if any(kw in skill for kw in ["data", "analytics", "ml", "ai"]):
                categorized["data_tools"].append(skill)
            elif any(kw in skill for kw in ["web", "front", "back", "full"]):
                categorized["web_frameworks"].append(skill)
            else:
                categorized["methodologies"].append(skill)
        elif not categorized_flag:
            categorized["other"].append(skill)

    # Remove empty categories
    return {k: v for k, v in categorized.items() if v}


def extract_experience_level(text: str) -> str:
    """
    Extract experience level from job posting.
    """
    text_lower = text.lower()

    if re.search(r"\b(entry.?level|junior|graduate|0-2 years)\b", text_lower):
        return "Entry Level"
    elif re.search(r"\b(mid.?level|intermediate|2-5 years|3-5 years)\b", text_lower):
        return "Mid Level"
    elif re.search(r"\b(senior|lead|5\+ years|7\+ years)\b", text_lower):
        return "Senior Level"
    elif re.search(r"\b(principal|staff|architect|10\+ years)\b", text_lower):
        return "Principal/Staff Level"
    elif re.search(r"\b(director|vp|head of|chief)\b", text_lower):
        return "Leadership"

    return "Not Specified"


def extract_education_requirements(text: str) -> List[str]:
    """
    Extract education requirements from job posting.
    """
    requirements = []
    text_lower = text.lower()

    if re.search(r"\b(bachelor|bs|ba|b\.s\.|b\.a\.)\b", text_lower):
        requirements.append("Bachelor's Degree")
    if re.search(r"\b(master|ms|ma|m\.s\.|m\.a\.|mba)\b", text_lower):
        requirements.append("Master's Degree")
    if re.search(r"\b(phd|ph\.d\.|doctorate)\b", text_lower):
        requirements.append("PhD")
    if re.search(
        r"\b(certification|certifications|certified|certificate)\b", text_lower
    ):
        requirements.append("Professional Certification")

    return requirements if requirements else ["Not Specified"]
