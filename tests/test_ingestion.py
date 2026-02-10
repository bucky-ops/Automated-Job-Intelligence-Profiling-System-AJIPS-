"""Unit tests for ingestion service with SSRF protections."""

import pytest
from unittest.mock import patch, MagicMock
import urllib.parse

from ajips.app.services.ingestion import (
    fetch_job_posting,
    _is_safe_url,
    ALLOWED_NETLOCS,
)


def test_is_safe_url_allowed_schemes():
    # Accept http and https, reject others
    assert _is_safe_url("https://example.com")
    assert _is_safe_url("http://example.com")
    assert not _is_safe_url("ftp://example.com")
    assert not _is_safe_url("mailto:test@example.com")
    assert not _is_safe_url("file:///etc/passwd")


def test_is_safe_url_bad_parsing():
    assert not _is_safe_url("")
    assert not _is_safe_url("not a url")
    assert not _is_safe_url("http:/missing-slash.com")


def test_is_safe_url_private_ips():
    # Disallow private, loopback, and link-local IPs
    assert not _is_safe_url("http://127.0.0.1")
    assert not _is_safe_url("http://10.0.0.1")
    assert not _is_safe_url("http://192.168.1.1")
    assert not _is_safe_url("http://169.254.169.254")
    assert not _is_safe_url("http://[::1]")  # IPv6 loopback
    # Allow public IPs (if not restrict-by-allowlist)
    assert _is_safe_url("http://1.2.3.4")
    assert _is_safe_url("http://2606:4700:4700::1111")  # Cloudflare public IPv6


def test_is_safe_url_allowlist():
    # Test with explicit allowlist
    assert _is_safe_url("https://sub.example.com", allowed_netlocs=["example.com"])
    assert not _is_safe_url("https://other.com", allowed_netlocs=["example.com"])


@patch("ajips.app.services.ingestion.requests.get")
@patch("ajips.app.services.ingestion._is_safe_url")
def test_fetch_job_posting_valid_url(mock_is_safe, mock_get):
    mock_is_safe.return_value = True
    mock_response = MagicMock()
    mock_response.raise_for_status = MagicMock()
    mock_response.text = "<html><body><h1>Job Title</h1><p>desc</p></body></html>"
    mock_get.return_value = mock_response
    result = fetch_job_posting("https://example.com/job")
    assert result == "Job Title desc"
    mock_get.assert_called_once_with("https://example.com/job", timeout_s=10)


def test_fetch_job_posting_unsafe_url():
    with pytest.raises(ValueError, match="not allowed or is potentially unsafe"):
        fetch_job_posting("http://127.0.0.1/local")


@patch("ajips.app.services.ingestion.requests.get")
@patch("ajips.app.services.ingestion._is_safe_url")
def test_fetch_job_posting_http_error(mock_is_safe, mock_get):
    from requests.exceptions import HTTPError

    mock_is_safe.return_value = True
    mock_get.side_effect = HTTPError("404 Not Found")
    with pytest.raises(HTTPError):
        fetch_job_posting("https://example.com/notfound")


@patch("ajips.app.services.ingestion.requests.get")
@patch("ajips.app.services.ingestion._is_safe_url")
def test_fetch_job_posting_empty_content(mock_is_safe, mock_get):
    mock_is_safe.return_value = True
    mock_response = MagicMock()
    mock_response.raise_for_status = MagicMock()
    mock_response.text = "<html></html>"
    mock_get.return_value = mock_response
    result = fetch_job_posting("https://example.com/empty")
    assert result is None
