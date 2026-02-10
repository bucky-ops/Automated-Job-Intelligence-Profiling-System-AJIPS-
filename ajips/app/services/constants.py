"""
Constants and patterns used across services.
Centralized location for magic strings and thresholds.
"""

from enum import Enum

# Regex Patterns
YEARS_PATTERN = r"(\d+)\+?\s*years?"
SALARY_PATTERN = r"\$[\d,]+(?:\s*[-–]\s*\$[\d,]+)?"
SALARY_K_PATTERN = r"[\d,]+(?:\s*[-–]\s*[\d,]+)?\s*(?:per\s+)?(?:year|annum|k)"
ENTRY_LEVEL_PATTERN = r"\b(entry.?level|junior|graduate)\b"
JOB_TITLE_PATTERN_1 = r"(?:position|role|title):\s*([^\n]+)"
JOB_TITLE_PATTERN_2 = r"(?:hiring|seeking|looking for)\s+(?:a\s+)?([^\n,]+?)(?:\s+to|\s+who|\s+with)"
JOB_TITLE_PATTERN_3 = r"^([A-Z][^\n]{10,60}?)(?:\s*[-–—]\s*|\n)"

# Experience Thresholds
MAX_REALISTIC_YEARS = 15
ENTRY_LEVEL_MAX_YEARS = 2
JUNIOR_MAX_YEARS = 3

# Technology age limits (in years)
TECH_AGE_LIMITS = {
    "next.js": 5,
    "nuxt": 5,
    "svelte": 5,
    "deno": 10,
    "rust": 15,
    "go": 13,
    "golang": 13,
    "kubernetes": 8,
    "k8s": 8,
}

# Cloud Providers
CLOUD_PROVIDERS = ("aws", "azure", "gcp", "google cloud", "cloudflare", "heroku", "vercel")

# Databases
COMMON_DATABASES = (
    "postgresql",
    "mysql",
    "mongodb",
    "redis",
    "oracle",
    "sql server",
    "cassandra",
    "dynamodb",
    "elasticsearch",
    "mariadb",
)

# Entry Level Keywords
ENTRY_LEVEL_KEYWORDS = {"entry-level", "junior", "graduate", "entry level"}
SENIOR_KEYWORDS = {"senior", "principal", "lead", "staff", "architect"}

# Keywords for feature detection
INTERVIEW_STAGES = {
    "phone": ["phone screen", "initial call", "screening call"],
    "technical": ["coding challenge", "technical assessment", "coding test", "technical interview"],
    "system_design": ["system design", "architecture", "design interview"],
    "behavioral": ["behavioral", "culture fit", "team lunch", "onsite"],
}

# Input Constraints
MAX_JOB_TEXT_LENGTH = 50000  # 50KB
MIN_JOB_TEXT_LENGTH = 50
MAX_RESUME_TEXT_LENGTH = 20000  # 20KB

# Response Caching
CACHE_TTL_SECONDS = 3600  # 1 hour
MAX_CACHE_SIZE = 1000  # Maximum cached URLs


class SeverityLevel(str, Enum):
    """Critique severity levels."""

    CRITICAL = "critical"
    WARNING = "warning"
    INFO = "info"
