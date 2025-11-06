#!/usr/bin/env python3
"""
Security Analyzer - Detect security vulnerabilities and gaps
"""

import os
import re
from pathlib import Path


class SecurityAnalyzer:
    """Analyze security vulnerabilities and best practices"""

    def __init__(self, project_path):
        self.project_path = Path(project_path)

    def analyze(self):
        """Run security analysis"""
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
            critical_issues.append({
                "title": f"Hardcoded {secret['type']} in source code",
                "file": secret["file"],
                "risk": f"{secret['type'].title()} exposure in version control",
                "fix": "Move to environment variables or secret management",
                "effort": "1 hour"
            })

        # Check for rate limiting
        if not self._has_rate_limiting():
            high_issues.append({
                "title": "No rate limiting on authentication endpoints",
                "risk": "Brute force attacks possible",
                "fix": "Add rate limiting (10-100 requests/minute)",
                "effort": "2 hours"
            })

        # Check for SQL injection protection
        if not self._has_sql_protection():
            high_issues.append({
                "title": "Potential SQL injection vulnerabilities",
                "risk": "Database compromise through malicious queries",
                "fix": "Use parameterized queries/ORM everywhere",
                "effort": "4 hours"
            })

        # Check for security headers
        if not self._has_security_headers():
            medium_issues.append({
                "title": "Missing security headers",
                "risk": "XSS, clickjacking vulnerabilities",
                "fix": "Add CSP, X-Frame-Options, HSTS headers",
                "effort": "1 hour"
            })

        # Check for CSRF protection
        if not self._has_csrf_protection():
            medium_issues.append({
                "title": "No CSRF protection detected",
                "risk": "Cross-site request forgery attacks",
                "fix": "Implement CSRF tokens for state-changing operations",
                "effort": "2 hours"
            })

        return critical_issues, high_issues, medium_issues

    def _find_hardcoded_secrets(self):
        """Find hardcoded secrets in source code"""
        secrets = []

        # Secret patterns
        patterns = {
            "api_key": r'(?i)(api[_-]?key|apikey)\s*=\s*[\'"]([a-zA-Z0-9]{20,})[\'"]',
            "password": r'(?i)(password|passwd|pwd)\s*=\s*[\'"](?!{{)[^\'"]{8,}[\'"]',
            "token": r'(?i)(token|auth[_-]?token)\s*=\s*[\'"]([a-zA-Z0-9]{20,})[\'"]',
            "secret": r'(?i)(secret|secret[_-]?key)\s*=\s*[\'"]([a-zA-Z0-9]{20,})[\'"]'
        }

        # Scan code files
        code_extensions = ['.py', '.js', '.java', '.rb', '.php', '.go', '.ts', '.jsx', '.tsx']

        for code_file in self.project_path.rglob("*"):
            if code_file.suffix in code_extensions:
                # Skip test files and examples
                if 'test' in code_file.name.lower() or 'example' in code_file.name.lower():
                    continue

                try:
                    content = code_file.read_text()
                    for secret_type, pattern in patterns.items():
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
                except Exception:
                    continue

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
        for file in self.project_path.rglob("*"):
            if file.suffix in ['.py', '.js', '.java', '.conf', '.yml', '.yaml']:
                try:
                    content = file.read_text()
                    if re.search(r'https://', content, re.IGNORECASE):
                        return True
                except Exception:
                    continue
        return False

    def _uses_password_hashing(self):
        """Check for secure password hashing"""
        hash_libs = ['bcrypt', 'argon2', 'scrypt', 'pbkdf2']
        for file in self.project_path.rglob("*"):
            if file.suffix in ['.py', '.js', '.java', '.go']:
                try:
                    content = file.read_text().lower()
                    if any(lib in content for lib in hash_libs):
                        return True
                except Exception:
                    continue
        return False

    def _has_input_validation(self):
        """Check for input validation"""
        validation_patterns = ['validate', 'sanitize', 'validator', 'schema', 'joi', 'yup']
        for file in self.project_path.rglob("*"):
            if file.suffix in ['.py', '.js', '.java', '.go']:
                try:
                    content = file.read_text().lower()
                    if any(pattern in content for pattern in validation_patterns):
                        return True
                except Exception:
                    continue
        return False

    def _has_rate_limiting(self):
        """Check for rate limiting"""
        rate_limit_patterns = ['rate.limit', 'ratelimit', 'throttle', 'rate_limit']
        for file in self.project_path.rglob("*"):
            try:
                content = file.read_text().lower()
                if any(pattern in content for pattern in rate_limit_patterns):
                    return True
            except Exception:
                continue
        return False

    def _has_sql_protection(self):
        """Check for SQL injection protection"""
        # Look for ORM usage or parameterized queries
        orm_patterns = ['sqlalchemy', 'sequelize', 'hibernate', 'activerecord', 'prisma', 'typeorm']
        param_patterns = [r'\?', r':\w+', r'\$\d+', 'prepared.statement']

        for file in self.project_path.rglob("*"):
            if file.suffix in ['.py', '.js', '.java', '.go']:
                try:
                    content = file.read_text().lower()
                    if any(orm in content for orm in orm_patterns):
                        return True
                    if any(re.search(pattern, content) for pattern in param_patterns):
                        return True
                except Exception:
                    continue
        return False

    def _has_security_headers(self):
        """Check for security headers"""
        header_patterns = ['x-frame-options', 'content-security-policy', 'csp', 'hsts', 'strict-transport-security']
        for file in self.project_path.rglob("*"):
            try:
                content = file.read_text().lower()
                if any(header in content for header in header_patterns):
                    return True
            except Exception:
                continue
        return False

    def _has_csrf_protection(self):
        """Check for CSRF protection"""
        csrf_patterns = ['csrf', 'xsrf', 'cross.site.request']
        for file in self.project_path.rglob("*"):
            try:
                content = file.read_text().lower()
                if any(pattern.replace('.', r'[\s_-]?') in content for pattern in csrf_patterns):
                    return True
            except Exception:
                continue
        return False


if __name__ == "__main__":
    import sys
    import json

    if len(sys.argv) < 2:
        print("Usage: python3 security_analyzer.py <project_path>")
        sys.exit(1)

    analyzer = SecurityAnalyzer(sys.argv[1])
    results = analyzer.analyze()
    print(json.dumps(results, indent=2))
