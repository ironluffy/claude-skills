#!/usr/bin/env python3
"""
Task Decomposition Analyzer

Decompose high-level tasks into actionable, testifiable subtasks with comprehensive analysis.

Usage:
    python analyze_task.py "<task description>" [options]

Examples:
    python analyze_task.py "Implement user authentication"
    python analyze_task.py "Refactor payment processing" --project backend
    python analyze_task.py "Add dark mode" --export-linear --team-id TEAM123
    python analyze_task.py "..." --graph dependencies.dot --risk-matrix risks.md

Options:
    --project NAME          Project context (frontend, backend, mobile, etc.)
    --complexity LEVEL      Estimated complexity (low, medium, high)
    --export-linear         Export subtasks to Linear
    --team-id ID            Linear team ID for export
    --parent-id ID          Linear parent issue ID
    --export-github         Export to GitHub issues
    --repo OWNER/REPO       GitHub repository
    --graph FILE            Generate dependency graph (DOT format)
    --risk-matrix FILE      Generate risk matrix markdown
    --output FILE           Save decomposition to file
    --format FORMAT         Output format (markdown, json, yaml)
"""

import sys
import json
import argparse
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
from enum import Enum


class Priority(Enum):
    P0 = "Critical Path"
    P1 = "Important"
    P2 = "Nice to Have"


class RiskLevel(Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


@dataclass
class SubTask:
    """Represents a decomposed subtask."""
    id: int
    title: str
    description: str
    priority: Priority
    estimate_hours: float
    labels: List[str]
    dependencies: List[int]
    acceptance_criteria: List[str]
    testing_criteria: List[str]
    expected_outputs: List[str]
    risks: List[Dict[str, str]]

    def to_markdown(self) -> str:
        """Convert subtask to markdown format."""
        deps = f"#{', #'.join(map(str, self.dependencies))}" if self.dependencies else "None"

        md = f"""### {self.id}. {self.title}
**Priority:** {self.priority.name} ({self.priority.value})
**Estimate:** {self.estimate_hours} hours
**Labels:** {', '.join(self.labels)}
**Dependencies:** {deps}

**Description:**
{self.description}

**Acceptance Criteria:**
{self._format_checklist(self.acceptance_criteria)}

**Testing:**
{self._format_checklist(self.testing_criteria)}

**Expected Outputs:**
{self._format_list(self.expected_outputs)}

**Risks:**
{self._format_risks()}
"""
        return md

    def _format_checklist(self, items: List[str]) -> str:
        """Format items as checklist."""
        return '\n'.join(f"- [ ] {item}" for item in items)

    def _format_list(self, items: List[str]) -> str:
        """Format items as bulleted list."""
        return '\n'.join(f"- {item}" for item in items)

    def _format_risks(self) -> str:
        """Format risk list."""
        if not self.risks:
            return "- None"
        return '\n'.join(
            f"- {risk['level']}: {risk['description']} (mitigation: {risk['mitigation']})"
            for risk in self.risks
        )


@dataclass
class Decomposition:
    """Complete task decomposition."""
    original_task: str
    rationale: str
    as_is_state: str
    to_be_state: str
    gap_analysis: str
    subtasks: List[SubTask]
    overall_risks: List[Dict[str, str]]

    def to_markdown(self) -> str:
        """Convert decomposition to markdown."""
        md = f"""# Task Decomposition: {self.original_task}

## Rationale

{self.rationale}

## State Analysis

**As-Is (Current State):**
{self.as_is_state}

**To-Be (Desired State):**
{self.to_be_state}

**Gap Analysis:**
{self.gap_analysis}

## Subtasks

{self._format_subtasks()}

## Overall Risk Assessment

{self._format_overall_risks()}

## Dependency Summary

{self._format_dependencies()}

## Estimation Summary

- Total subtasks: {len(self.subtasks)}
- Total estimated time: {sum(st.estimate_hours for st in self.subtasks)} hours
- Critical path items: {len([st for st in self.subtasks if st.priority == Priority.P0])}
"""
        return md

    def _format_subtasks(self) -> str:
        """Format all subtasks."""
        return '\n---\n\n'.join(st.to_markdown() for st in self.subtasks)

    def _format_overall_risks(self) -> str:
        """Format overall risks by level."""
        high = [r for r in self.overall_risks if r['level'] == 'HIGH']
        medium = [r for r in self.overall_risks if r['level'] == 'MEDIUM']
        low = [r for r in self.overall_risks if r['level'] == 'LOW']

        sections = []
        if high:
            sections.append("### HIGH Risk\n" + '\n\n'.join(
                f"**{r['name']}**\n"
                f"- Impact: {r['impact']}\n"
                f"- Probability: {r['probability']}\n"
                f"- Mitigation: {r['mitigation']}\n"
                f"- Owner: {r['owner']}"
                for r in high
            ))

        if medium:
            sections.append("### MEDIUM Risk\n" + '\n\n'.join(
                f"**{r['name']}**\n"
                f"- Impact: {r['impact']}\n"
                f"- Probability: {r['probability']}\n"
                f"- Mitigation: {r['mitigation']}\n"
                f"- Owner: {r['owner']}"
                for r in medium
            ))

        if low:
            sections.append("### LOW Risk\n" + '\n\n'.join(
                f"**{r['name']}**\n"
                f"- Impact: {r['impact']}\n"
                f"- Probability: {r['probability']}\n"
                f"- Mitigation: {r['mitigation']}\n"
                f"- Owner: {r['owner']}"
                for r in low
            ))

        return '\n\n'.join(sections)

    def _format_dependencies(self) -> str:
        """Format dependency summary."""
        lines = []
        for st in self.subtasks:
            if st.dependencies:
                deps = ', '.join(f"#{d}" for d in st.dependencies)
                lines.append(f"- Subtask #{st.id} depends on: {deps}")
            else:
                lines.append(f"- Subtask #{st.id} has no dependencies (can start immediately)")
        return '\n'.join(lines)


def analyze_task(task: str, project: str = None, complexity: str = "medium") -> Decomposition:
    """
    Analyze task and generate decomposition.

    This is a template/example implementation. In production, this would use
    LLM or more sophisticated analysis.
    """

    # Example decomposition (would be AI-generated in production)
    subtasks = [
        SubTask(
            id=1,
            title="Analyze requirements and design approach",
            description="Review requirements, research best practices, and design solution architecture.",
            priority=Priority.P0,
            estimate_hours=2.0,
            labels=["planning", "research"],
            dependencies=[],
            acceptance_criteria=[
                "Requirements documented",
                "Technical approach defined",
                "Architecture diagram created"
            ],
            testing_criteria=[
                "Review with stakeholders",
                "Validate approach with team"
            ],
            expected_outputs=[
                "Requirements document",
                "Architecture diagram",
                "Technical design doc"
            ],
            risks=[]
        ),
        SubTask(
            id=2,
            title="Implement core functionality",
            description=f"Build the main components for: {task}",
            priority=Priority.P0,
            estimate_hours=4.0,
            labels=[project] if project else ["development"],
            dependencies=[1],
            acceptance_criteria=[
                "Core logic implemented",
                "Unit tests written (>80% coverage)",
                "Code reviewed"
            ],
            testing_criteria=[
                "Run unit tests",
                "Test edge cases",
                "Verify error handling"
            ],
            expected_outputs=[
                "Source code",
                "Unit tests",
                "API documentation"
            ],
            risks=[
                {
                    "level": "MEDIUM",
                    "description": "Complexity underestimated",
                    "mitigation": "Buffer time allocated, incremental approach"
                }
            ]
        ),
        SubTask(
            id=3,
            title="Integration testing and validation",
            description="Test integration with existing systems and validate functionality.",
            priority=Priority.P1,
            estimate_hours=2.0,
            labels=["testing", "integration"],
            dependencies=[2],
            acceptance_criteria=[
                "Integration tests pass",
                "End-to-end scenarios validated",
                "Performance benchmarks met"
            ],
            testing_criteria=[
                "Run integration test suite",
                "Test in staging environment",
                "Performance testing"
            ],
            expected_outputs=[
                "Integration test results",
                "Test coverage report",
                "Performance metrics"
            ],
            risks=[]
        )
    ]

    decomposition = Decomposition(
        original_task=task,
        rationale=f"Task decomposed into {len(subtasks)} subtasks to enable parallel work, "
                   "clear testing criteria, and manageable scope per work item.",
        as_is_state="Current system does not have this functionality.",
        to_be_state=f"System will have: {task}",
        gap_analysis="Need to implement, test, and integrate new functionality.",
        subtasks=subtasks,
        overall_risks=[
            {
                "level": "MEDIUM",
                "name": "Scope creep",
                "impact": "Timeline delay",
                "probability": "Medium",
                "mitigation": "Clear requirements, regular review",
                "owner": "Project Manager"
            }
        ]
    )

    return decomposition


def export_to_linear(decomposition: Decomposition, team_id: str, parent_id: str = None):
    """Export decomposition to Linear (placeholder)."""
    print(f"\n📤 Exporting to Linear team: {team_id}")
    if parent_id:
        print(f"   Parent issue: {parent_id}")

    print("\nThis would create Linear issues via API:")
    for st in decomposition.subtasks:
        print(f"  - {st.title} ({st.estimate_hours}h)")

    print("\n⚠️  Linear API integration not implemented in this template.")
    print("   See references/linear-integration.md for implementation guide.")


def export_to_github(decomposition: Decomposition, repo: str):
    """Export decomposition to GitHub (placeholder)."""
    print(f"\n📤 Exporting to GitHub repo: {repo}")

    print("\nThis would create GitHub issues via API:")
    for st in decomposition.subtasks:
        print(f"  - {st.title} ({', '.join(st.labels)})")

    print("\n⚠️  GitHub API integration not implemented in this template.")
    print("   Implement using PyGithub library.")


def generate_dependency_graph(decomposition: Decomposition, output_file: str):
    """Generate DOT format dependency graph."""
    lines = ["digraph dependencies {"]
    lines.append('  rankdir=TB;')
    lines.append('  node [shape=box, style=rounded];')

    for st in decomposition.subtasks:
        label = f"{st.id}. {st.title}\\n{st.estimate_hours}h"
        color = "red" if st.priority == Priority.P0 else "orange" if st.priority == Priority.P1 else "lightblue"
        lines.append(f'  {st.id} [label="{label}", fillcolor={color}, style="filled,rounded"];')

    for st in decomposition.subtasks:
        for dep in st.dependencies:
            lines.append(f'  {dep} -> {st.id};')

    lines.append("}")

    with open(output_file, 'w') as f:
        f.write('\n'.join(lines))

    print(f"\n✓ Dependency graph saved to: {output_file}")
    print(f"  Generate PNG: dot -Tpng {output_file} -o dependencies.png")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Decompose tasks into actionable subtasks")
    parser.add_argument("task", help="Task description to decompose")
    parser.add_argument("--project", help="Project context")
    parser.add_argument("--complexity", choices=["low", "medium", "high"], default="medium")
    parser.add_argument("--export-linear", action="store_true")
    parser.add_argument("--team-id", help="Linear team ID")
    parser.add_argument("--parent-id", help="Linear parent issue ID")
    parser.add_argument("--export-github", action="store_true")
    parser.add_argument("--repo", help="GitHub repository (owner/repo)")
    parser.add_argument("--graph", help="Generate dependency graph to file")
    parser.add_argument("--output", help="Save output to file")
    parser.add_argument("--format", choices=["markdown", "json", "yaml"], default="markdown")

    args = parser.parse_args()

    # Analyze task
    print(f"Analyzing task: {args.task}\n")
    decomposition = analyze_task(args.task, args.project, args.complexity)

    # Generate output
    if args.format == "markdown":
        output = decomposition.to_markdown()
    elif args.format == "json":
        output = json.dumps(asdict(decomposition), indent=2, default=str)
    else:  # yaml
        import yaml
        output = yaml.dump(asdict(decomposition), default_flow_style=False)

    # Save or print
    if args.output:
        with open(args.output, 'w') as f:
            f.write(output)
        print(f"✓ Decomposition saved to: {args.output}")
    else:
        print(output)

    # Generate graph
    if args.graph:
        generate_dependency_graph(decomposition, args.graph)

    # Export to Linear
    if args.export_linear:
        if not args.team_id:
            print("Error: --team-id required for Linear export")
            sys.exit(1)
        export_to_linear(decomposition, args.team_id, args.parent_id)

    # Export to GitHub
    if args.export_github:
        if not args.repo:
            print("Error: --repo required for GitHub export")
            sys.exit(1)
        export_to_github(decomposition, args.repo)


if __name__ == "__main__":
    main()
