#!/usr/bin/env python3
"""
Security Analyzer - Detect security vulnerabilities and gaps
Part of system-design-reviewer skill for Claude Skills

Refactored to use BaseAnalyzer and shared utilities.
"""

import re
from pathlib import Path

from analyzer_base import BaseAnalyzer
from constants import (
    SECRET_PATTERNS,
    SECURITY_INDICATORS,
    CODE_EXTENSIONS
)


class SecurityAnalyzer(BaseAnalyzer):
    """Analyze security vulnerabilities and best practices"""

    def analyze(self):
        """Run security analysis"""
        self._log_analysis_start("Security")

        results = {
            "critical_count": 0,
            "high_count": 0,
            "medium_count": 0,
            "strengths": [],
            "critical_issues": [],
            "high_issues": [],
            "medium_issues": []
        }

        # Find strengths
        results["strengths"] = self._find_strengths()

        # Find vulnerabilities
        critical, high, medium = self._find_vulnerabilities()
        results["critical_issues"] = critical
        results["high_issues"] = high
        results["medium_issues"] = medium

        results["critical_count"] = len(critical)
        results["high_count"] = len(high)
        results["medium_count"] = len(medium)

        self._log_analysis_complete(results)

        return results

    def _find_strengths(self):
        """Find security strengths"""
        strengths = []

        # Check for HTTPS
        if self._uses_https():
            strengths.append("Using HTTPS for secure communication")

        # Check for password hashing
        if self._uses_password_hashing():
            strengths.append("Using secure password hashing (bcrypt/argon2)")

        # Check for input validation
        if self._has_input_validation():
            strengths.append("Input validation detected on API endpoints")

        return strengths or ["Basic security measures in place"]

    def _find_vulnerabilities(self):
        """Find security vulnerabilities"""
        critical_issues = []
        high_issues = []
        medium_issues = []

        # Check for hardcoded secrets
        secrets = self._find_hardcoded_secrets()
        for secret in secrets:
            critical_issues.append(self._create_issue(
                title=f"Hardcoded {secret['type']} in source code",
                impact=f"{secret['type'].title()} exposure in version control",
                recommendation="Move to environment variables or secret management",
                effort="1 hour",
                file=secret["file"],
                risk=f"{secret['type'].title()} exposure in version control"
            ))

        # Check for rate limiting
        if not self._has_rate_limiting():
            high_issues.append(self._create_issue(
                title="No rate limiting on authentication endpoints",
                impact="Brute force attacks possible",
                recommendation="Add rate limiting (10-100 requests/minute)",
                effort="2 hours",
                risk="Brute force attacks possible"
            ))

        # Check for SQL injection protection
        if not self._has_sql_protection():
            high_issues.append(self._create_issue(
                title="Potential SQL injection vulnerabilities",
                impact="Database compromise through malicious queries",
                recommendation="Use parameterized queries/ORM everywhere",
                effort="4 hours",
                risk="Database compromise through malicious queries"
            ))

        # Check for security headers
        if not self._has_security_headers():
            medium_issues.append(self._create_issue(
                title="Missing security headers",
                impact="XSS, clickjacking vulnerabilities",
                recommendation="Add CSP, X-Frame-Options, HSTS headers",
                effort="1 hour",
                risk="XSS, clickjacking vulnerabilities"
            ))

        # Check for CSRF protection
        if not self._has_csrf_protection():
            medium_issues.append(self._create_issue(
                title="No CSRF protection detected",
                impact="Cross-site request forgery attacks",
                recommendation="Implement CSRF tokens for state-changing operations",
                effort="2 hours",
                risk="Cross-site request forgery attacks"
            ))

        return critical_issues, high_issues, medium_issues

    def _find_hardcoded_secrets(self):
        """Find hardcoded secrets in source code"""
        secrets = []

        # Scan code files
        code_files = self._get_code_files(CODE_EXTENSIONS)

        for code_file in code_files:
            content = self._read_file_safe(code_file)
            if not content:
                continue

            for secret_type, pattern in SECRET_PATTERNS.items():
                matches = re.findall(pattern, content)
                if matches:
                    # Check if it looks like a real secret (not placeholder)
                    for match in matches:
                        value = match[1] if isinstance(match, tuple) else match
                        if self._looks_like_real_secret(value):
                            secrets.append({
                                "type": secret_type,
                                "file": str(code_file.relative_to(self.project_path)),
                                "value_preview": value[:10] + "..."
                            })
                            break  # One finding per file is enough

        return secrets

    def _looks_like_real_secret(self, value):
        """Check if value looks like a real secret (not placeholder)"""
        # Common placeholder patterns
        placeholders = ['xxx', 'yyy', 'your', 'example', 'test', 'dummy', 'placeholder', 'changeme']
        value_lower = value.lower()

        # If it contains placeholder text, it's likely not real
        if any(placeholder in value_lower for placeholder in placeholders):
            return False

        # If it's all the same character, it's likely a placeholder
        if len(set(value)) <= 2:
            return False

        return True

    def _uses_https(self):
        """Check if HTTPS is used"""
        return self._contains_technology(SECURITY_INDICATORS['https'])

    def _uses_password_hashing(self):
        """Check for secure password hashing"""
        return self._contains_technology(SECURITY_INDICATORS['password_hashing'])

    def _has_input_validation(self):
        """Check for input validation"""
        return self._contains_technology(SECURITY_INDICATORS['input_validation'])

    def _has_rate_limiting(self):
        """Check for rate limiting"""
        return self._contains_technology(SECURITY_INDICATORS['rate_limiting'])

    def _has_sql_protection(self):
        """Check for SQL injection protection"""
        # Look for ORM usage or parameterized queries
        orm_patterns = ['sqlalchemy', 'sequelize', 'hibernate', 'activerecord', 'prisma', 'typeorm']
        param_patterns = [r'\?', r':\w+', r'\$\d+', 'prepared.statement']

        code_files = self._get_code_files()

        for file_path in code_files:
            content = self._read_file_safe(file_path)
            if content:
                content_lower = content.lower()
                if any(orm in content_lower for orm in orm_patterns):
                    return True
                if any(re.search(pattern, content) for pattern in param_patterns):
                    return True

        return False

    def _has_security_headers(self):
        """Check for security headers"""
        return self._contains_technology(SECURITY_INDICATORS['security_headers'])

    def _has_csrf_protection(self):
        """Check for CSRF protection"""
        return self._contains_technology(SECURITY_INDICATORS['csrf'])


if __name__ == "__main__":
    import sys
    import json

    if len(sys.argv) < 2:
        print("Usage: python3 security_analyzer.py <project_path>")
        sys.exit(1)

    analyzer = SecurityAnalyzer(sys.argv[1])
    results = analyzer.analyze()
    print(json.dumps(results, indent=2))
