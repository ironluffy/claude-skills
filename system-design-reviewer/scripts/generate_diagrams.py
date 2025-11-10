#!/usr/bin/env python3
"""
Diagram Generator - Generate Mermaid and ASCII diagrams from source code
Part of system-design-reviewer skill for Claude Skills

Refactored to use professional logging.
"""

import os
import re
import sys
from pathlib import Path

# Add shared directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'shared'))
from logger import Logger


class DiagramGenerator:
    """Generate architecture diagrams in multiple formats"""

    def __init__(self, project_path):
        self.project_path = Path(project_path)
        self.logger = Logger()

    def generate_all(self):
        """Generate all diagram types"""
        self.logger.info("Generating all diagram types...")

        diagrams = {
            "architecture_mermaid": self.generate_architecture_mermaid(),
            "architecture_ascii": self.generate_architecture_ascii(),
            "sequence_mermaid": self.generate_sequence_mermaid(),
            "sequence_ascii": self.generate_sequence_ascii(),
            "er_mermaid": self.generate_er_mermaid(),
            "er_ascii": self.generate_er_ascii()
        }

        self.logger.success(f"Generated {len(diagrams)} diagram types")
        return diagrams

    def generate_architecture_mermaid(self):
        """Generate Mermaid architecture diagram"""
        components = self._detect_components()

        diagram = ["graph TB"]

        # Add component nodes
        for component in components:
            diagram.append(f"    {component['id']}[{component['name']}]")

        # Add relationships (simplified)
        if len(components) >= 3:
            diagram.append(f"    {components[0]['id']} -->|HTTPS| {components[1]['id']}")
            diagram.append(f"    {components[1]['id']} -->|API Call| {components[2]['id']}")
            if len(components) >= 4:
                diagram.append(f"    {components[2]['id']} -->|Query| {components[3]['id']}")

        return "\n".join(diagram)

    def generate_architecture_ascii(self):
        """Generate ASCII architecture diagram"""
        components = self._detect_components()

        lines = []
        for i, component in enumerate(components[:4]):
            # Box
            name = component['name']
            width = max(len(name) + 4, 14)
            lines.append("┌" + "─" * width + "┐")
            lines.append("│" + name.center(width) + "│")
            lines.append("└" + "─" * width + "┘")

            # Arrow (except for last component)
            if i < len(components) - 1 and i < 3:
                lines.append("       │")
                lines.append("       ▼")

        return "\n".join(lines)

    def generate_sequence_mermaid(self):
        """Generate Mermaid sequence diagram"""
        return """sequenceDiagram
    participant C as Client
    participant A as API
    participant B as Backend
    participant D as Database

    C->>A: POST /api/endpoint
    A->>B: Process request
    B->>D: Query data
    D-->>B: Return results
    B-->>A: Response
    A-->>C: 200 OK"""

    def generate_sequence_ascii(self):
        """Generate ASCII sequence diagram"""
        return """Client    API      Backend    Database
  │       │         │          │
  ├──Request──────>│          │
  │       ├─Process──────>│    │
  │       │         ├─Query────>│
  │       │         │<──Data────┤
  │       │<──Response────┤     │
  │<──200 OK───────┤      │     │"""

    def generate_er_mermaid(self):
        """Generate Mermaid ER diagram"""
        tables = self._detect_database_tables()

        diagram = ["erDiagram"]

        # Add relationships (simplified)
        if len(tables) >= 2:
            diagram.append(f"    {tables[0].upper()} ||--o{{ {tables[1].upper()} : has")

        # Add table definitions
        for table in tables[:3]:
            diagram.append(f"    {table.upper()} {{")
            diagram.append("        int id PK")
            diagram.append(f"        string {table}_data")
            diagram.append("        timestamp created_at")
            diagram.append("    }")

        return "\n".join(diagram)

    def generate_er_ascii(self):
        """Generate ASCII ER diagram"""
        tables = self._detect_database_tables()

        lines = []
        for table in tables[:3]:
            name = table.upper()
            lines.append("┌──────────────────┐")
            lines.append(f"│ {name.ljust(16)} │")
            lines.append("├──────────────────┤")
            lines.append("│ id (PK)          │")
            lines.append(f"│ {table}_data      │")
            lines.append("│ created_at       │")
            lines.append("└──────────────────┘")
            if table != tables[min(2, len(tables)-1)]:
                lines.append("         │ 1:N")
                lines.append("         ▼")

        return "\n".join(lines)

    def _detect_components(self):
        """Detect system components from project structure"""
        components = []

        # Common component patterns
        patterns = {
            "client": ["frontend", "client", "ui", "web"],
            "api": ["api", "gateway", "router"],
            "backend": ["backend", "server", "service", "app"],
            "database": ["database", "db", "postgres", "mysql", "mongo"],
            "cache": ["cache", "redis", "memcached"],
            "queue": ["queue", "kafka", "rabbitmq", "sqs"]
        }

        # Scan project structure
        try:
            for root, dirs, files in os.walk(self.project_path):
                for dir_name in dirs:
                    dir_lower = dir_name.lower()
                    for comp_type, keywords in patterns.items():
                        if any(keyword in dir_lower for keyword in keywords):
                            components.append({
                                "id": comp_type.title(),
                                "name": dir_name.title(),
                                "type": comp_type
                            })
                            break
        except Exception as e:
            self.logger.debug(f"Error scanning components: {e}")

        # Default components if none detected
        if not components:
            components = [
                {"id": "Client", "name": "Web Client", "type": "client"},
                {"id": "API", "name": "API Gateway", "type": "api"},
                {"id": "Backend", "name": "Backend Service", "type": "backend"},
                {"id": "DB", "name": "Database", "type": "database"}
            ]

        return components[:6]  # Limit to 6 components

    def _detect_database_tables(self):
        """Detect database tables from schema files"""
        tables = []

        # Common schema file patterns
        schema_patterns = ["*.sql", "schema.py", "models.py", "*.prisma"]

        try:
            for pattern in schema_patterns:
                for schema_file in self.project_path.rglob(pattern):
                    try:
                        content = schema_file.read_text()
                        # Look for CREATE TABLE or model definitions
                        table_matches = re.findall(r'CREATE TABLE (\w+)|class (\w+)\(.*Model\)', content, re.IGNORECASE)
                        for match in table_matches:
                            table_name = match[0] or match[1]
                            if table_name and table_name.lower() not in ['model', 'base']:
                                tables.append(table_name.lower())
                    except Exception:
                        continue
        except Exception as e:
            self.logger.debug(f"Error detecting tables: {e}")

        # Default tables if none detected
        if not tables:
            tables = ["users", "sessions", "products"]

        return list(set(tables))[:5]  # Unique, limit to 5


if __name__ == "__main__":
    if len(sys.argv) < 2:
        logger = Logger()
        logger.error("Usage: python3 generate_diagrams.py <project_path>")
        sys.exit(1)

    generator = DiagramGenerator(sys.argv[1])
    diagrams = generator.generate_all()

    print("=== Architecture (Mermaid) ===")
    print(diagrams["architecture_mermaid"])
    print("\n=== Architecture (ASCII) ===")
    print(diagrams["architecture_ascii"])
