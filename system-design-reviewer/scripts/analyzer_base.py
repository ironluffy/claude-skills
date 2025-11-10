"""
Analyzer Base - Abstract base class for all analyzers
Part of system-design-reviewer skill for Claude Skills

Provides common functionality and interface for all analyzer types.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, List, Optional, Set
import sys
import os

# Add shared directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'shared'))
from logger import Logger

from constants import (
    CODE_EXTENSIONS,
    CONFIG_EXTENSIONS,
    SKIP_PATTERNS,
    MAX_FILE_SIZE
)


class BaseAnalyzer(ABC):
    """Abstract base class for all system design analyzers

    All analyzer classes should inherit from this and implement
    the required abstract methods.

    Attributes:
        project_path: Path to project being analyzed
        logger: Logger instance for console output
    """

    def __init__(self, project_path: str):
        """Initialize analyzer

        Args:
            project_path: Path to project directory
        """
        self.project_path = Path(project_path)
        self.logger = Logger()

        # Validate project path
        if not self.project_path.exists():
            raise ValueError(f"Project path does not exist: {project_path}")
        if not self.project_path.is_dir():
            raise ValueError(f"Project path is not a directory: {project_path}")

    @abstractmethod
    def analyze(self) -> Dict:
        """Run the analysis

        Returns:
            Dict: Analysis results with standardized structure
        """
        pass

    @abstractmethod
    def _find_strengths(self) -> List[str]:
        """Find positive aspects of the system

        Returns:
            List[str]: List of strength descriptions
        """
        pass

    # =============================================================================
    # COMMON HELPER METHODS
    # =============================================================================

    def _get_code_files(self, extensions: Optional[List[str]] = None) -> List[Path]:
        """Get all code files in project

        Args:
            extensions: File extensions to include (default: CODE_EXTENSIONS)

        Returns:
            List[Path]: List of code file paths
        """
        if extensions is None:
            extensions = CODE_EXTENSIONS

        files = []
        for ext in extensions:
            for file_path in self.project_path.rglob(f"*{ext}"):
                if self._should_skip_file(file_path):
                    continue
                if file_path.stat().st_size > MAX_FILE_SIZE:
                    self.logger.warning(f"Skipping large file: {file_path.name}")
                    continue
                files.append(file_path)

        return files

    def _get_config_files(self) -> List[Path]:
        """Get all configuration files in project

        Returns:
            List[Path]: List of config file paths
        """
        return self._get_files_by_extensions(CONFIG_EXTENSIONS)

    def _get_files_by_extensions(self, extensions: List[str]) -> List[Path]:
        """Get files matching specific extensions

        Args:
            extensions: List of file extensions (with dots)

        Returns:
            List[Path]: Matching file paths
        """
        files = []
        for ext in extensions:
            for file_path in self.project_path.rglob(f"*{ext}"):
                if self._should_skip_file(file_path):
                    continue
                files.append(file_path)

        return files

    def _should_skip_file(self, file_path: Path) -> bool:
        """Check if file should be skipped

        Args:
            file_path: Path to check

        Returns:
            bool: True if file should be skipped
        """
        # Skip directories
        if not file_path.is_file():
            return True

        # Check skip patterns
        path_str = str(file_path)
        for pattern in SKIP_PATTERNS:
            if pattern in path_str:
                return True

        # Skip test and example files for security scanning
        filename_lower = file_path.name.lower()
        if 'test' in filename_lower or 'example' in filename_lower or 'sample' in filename_lower:
            # Allow tests for architecture analysis, skip for security
            if isinstance(self, BaseAnalyzer) and 'Security' in self.__class__.__name__:
                return True

        return False

    def _read_file_safe(self, file_path: Path) -> Optional[str]:
        """Safely read file contents

        Args:
            file_path: Path to file

        Returns:
            Optional[str]: File contents or None if error
        """
        try:
            return file_path.read_text(encoding='utf-8', errors='ignore')
        except Exception as e:
            self.logger.debug(f"Could not read {file_path.name}: {e}")
            return None

    def _search_pattern_in_files(self, pattern: str, file_paths: Optional[List[Path]] = None) -> List[Dict]:
        """Search for pattern in files

        Args:
            pattern: String pattern to search for (case-insensitive)
            file_paths: Optional list of files to search (default: all code files)

        Returns:
            List[Dict]: List of matches with file path and context
        """
        import re

        if file_paths is None:
            file_paths = self._get_code_files()

        matches = []
        pattern_re = re.compile(pattern, re.IGNORECASE)

        for file_path in file_paths:
            content = self._read_file_safe(file_path)
            if not content:
                continue

            for line_num, line in enumerate(content.split('\n'), 1):
                if pattern_re.search(line):
                    matches.append({
                        'file': str(file_path.relative_to(self.project_path)),
                        'line': line_num,
                        'content': line.strip()
                    })

        return matches

    def _find_files_by_pattern(self, pattern: str) -> List[Path]:
        """Find files matching glob pattern

        Args:
            pattern: Glob pattern (e.g., "*controller*")

        Returns:
            List[Path]: Matching file paths
        """
        matches = []
        for file_path in self.project_path.rglob(pattern):
            if not self._should_skip_file(file_path):
                matches.append(file_path)

        return matches

    def _check_directory_exists(self, dir_names: List[str]) -> Dict[str, bool]:
        """Check if directories exist in project

        Args:
            dir_names: List of directory names to check

        Returns:
            Dict[str, bool]: Mapping of directory name to exists boolean
        """
        results = {}
        for dir_name in dir_names:
            results[dir_name] = any(self.project_path.rglob(f"*{dir_name}*"))

        return results

    def _contains_technology(self, tech_indicators: List[str], file_extensions: Optional[List[str]] = None) -> bool:
        """Check if project uses specific technology

        Args:
            tech_indicators: List of technology indicator strings
            file_extensions: Optional file extensions to search in

        Returns:
            bool: True if technology detected
        """
        files = self._get_files_by_extensions(file_extensions) if file_extensions else self._get_code_files()

        # Check filenames first
        for file_path in files:
            if any(indicator in file_path.name.lower() for indicator in tech_indicators):
                return True

        # Check file contents
        for file_path in files:
            content = self._read_file_safe(file_path)
            if content:
                content_lower = content.lower()
                if any(indicator in content_lower for indicator in tech_indicators):
                    return True

        return False

    # =============================================================================
    # RESULT FORMATTING
    # =============================================================================

    def _create_issue(
        self,
        title: str,
        impact: str,
        recommendation: str,
        effort: str,
        cost_impact: str = "None",
        file: Optional[str] = None,
        risk: Optional[str] = None
    ) -> Dict:
        """Create standardized issue dictionary

        Args:
            title: Issue title
            impact: Impact description
            recommendation: Recommendation description
            effort: Effort estimate
            cost_impact: Cost impact estimate
            file: Optional file path
            risk: Optional risk description (for security issues)

        Returns:
            Dict: Standardized issue dictionary
        """
        issue = {
            "title": title,
            "impact": impact,
            "recommendation": recommendation,
            "effort": effort,
            "cost_impact": cost_impact
        }

        if file:
            issue["file"] = file
        if risk:
            issue["risk"] = risk

        return issue

    def _log_analysis_start(self, analysis_type: str) -> None:
        """Log analysis start message

        Args:
            analysis_type: Type of analysis (e.g., "Security", "Performance")
        """
        self.logger.info(f"Starting {analysis_type} analysis...")
        self.logger.info(f"Project: {self.project_path}")

    def _log_analysis_complete(self, results: Dict) -> None:
        """Log analysis completion with summary

        Args:
            results: Analysis results dictionary
        """
        self.logger.success("Analysis complete!")

        # Try to extract counts
        total_issues = 0
        for key in results:
            if 'count' in key or '_issues' in key or '_impact' in key:
                value = results[key]
                if isinstance(value, int):
                    total_issues += value
                elif isinstance(value, list):
                    total_issues += len(value)

        if total_issues > 0:
            self.logger.info(f"Found {total_issues} items to review")
