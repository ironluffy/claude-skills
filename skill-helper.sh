#!/bin/bash
#
# Universal Claude Skills Helper Script
#
# Quick access to common skill operations
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

function print_header() {
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}  Universal Claude Skills - Helper Script${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
}

function show_help() {
    print_header
    echo "Usage: ./skill-helper.sh <command> [options]"
    echo ""
    echo "Commands:"
    echo ""
    echo "  ${GREEN}Skill Creation:${NC}"
    echo "    create <name> \"<description>\"  Create a new skill"
    echo "    validate <skill-name>          Validate a skill"
    echo "    list                           List all skills"
    echo ""
    echo "  ${GREEN}Task Decomposition:${NC}"
    echo "    decompose \"<task>\"             Decompose a task"
    echo "    decompose-example              Show example decomposition"
    echo ""
    echo "  ${GREEN}Issue Management:${NC}"
    echo "    block <issue-id> \"<reason>\"   Report a blocker"
    echo "    split <issue-id>               Split an issue"
    echo "    query \"<filter>\"               Query issues"
    echo ""
    echo "  ${GREEN}Utilities:${NC}"
    echo "    test-all                       Test all skills"
    echo "    install                        Show installation instructions"
    echo "    examples                       Show usage examples"
    echo ""
    echo "Examples:"
    echo "  ./skill-helper.sh create my-skill \"Analyze code quality\""
    echo "  ./skill-helper.sh validate my-skill"
    echo "  ./skill-helper.sh decompose \"Implement authentication\""
    echo "  ./skill-helper.sh block TEAM-123 \"Waiting for design\""
    echo ""
}

function create_skill() {
    local name="$1"
    local description="$2"

    if [[ -z "$name" ]] || [[ -z "$description" ]]; then
        echo -e "${RED}Error: Name and description required${NC}"
        echo "Usage: ./skill-helper.sh create <name> \"<description>\""
        exit 1
    fi

    echo -e "${BLUE}Creating skill: ${name}${NC}"
    python3 "$SCRIPT_DIR/skill-creator/scripts/init_skill.py" "$name" "$description"
}

function validate_skill() {
    local skill="$1"

    if [[ -z "$skill" ]]; then
        echo -e "${RED}Error: Skill name required${NC}"
        echo "Usage: ./skill-helper.sh validate <skill-name>"
        exit 1
    fi

    echo -e "${BLUE}Validating skill: ${skill}${NC}"
    python3 "$SCRIPT_DIR/skill-creator/scripts/package_skill.py" "$skill"
}

function list_skills() {
    print_header
    echo -e "${GREEN}Available Skills:${NC}"
    echo ""

    for skill_dir in "$SCRIPT_DIR"/*/; do
        if [[ -f "${skill_dir}SKILL.md" ]]; then
            skill_name=$(basename "$skill_dir")
            # Extract description from SKILL.md
            description=$(grep "^description:" "${skill_dir}SKILL.md" | cut -d':' -f2- | xargs)
            echo -e "  ${BLUE}${skill_name}${NC}"
            echo "    ${description}"
            echo ""
        fi
    done
}

function decompose_task() {
    local task="$1"

    if [[ -z "$task" ]]; then
        echo -e "${RED}Error: Task description required${NC}"
        echo "Usage: ./skill-helper.sh decompose \"<task>\""
        exit 1
    fi

    echo -e "${BLUE}Decomposing task: ${task}${NC}"
    python3 "$SCRIPT_DIR/task-decomposer/scripts/analyze_task.py" "$task"
}

function decompose_example() {
    echo -e "${BLUE}Running example task decomposition...${NC}"
    echo ""
    python3 "$SCRIPT_DIR/task-decomposer/scripts/analyze_task.py" \
        "Implement user authentication system" \
        --project backend
}

function report_blocker() {
    local issue="$1"
    local reason="$2"

    if [[ -z "$issue" ]] || [[ -z "$reason" ]]; then
        echo -e "${RED}Error: Issue ID and reason required${NC}"
        echo "Usage: ./skill-helper.sh block <issue-id> \"<reason>\""
        exit 1
    fi

    echo -e "${BLUE}Reporting blocker on ${issue}${NC}"
    python3 "$SCRIPT_DIR/issue-manager/scripts/issue_operations.py" \
        report-blocker \
        --issue "$issue" \
        --blocked-by "$reason" \
        --dry-run
}

function split_issue() {
    local issue="$1"

    if [[ -z "$issue" ]]; then
        echo -e "${RED}Error: Issue ID required${NC}"
        echo "Usage: ./skill-helper.sh split <issue-id>"
        exit 1
    fi

    echo -e "${BLUE}Splitting issue: ${issue}${NC}"
    python3 "$SCRIPT_DIR/issue-manager/scripts/issue_operations.py" \
        split-issue \
        --issue "$issue" \
        --num-subtasks 4 \
        --dry-run
}

function query_issues() {
    local filter="$1"

    if [[ -z "$filter" ]]; then
        echo -e "${RED}Error: Filter required${NC}"
        echo "Usage: ./skill-helper.sh query \"<filter>\""
        exit 1
    fi

    echo -e "${BLUE}Querying issues: ${filter}${NC}"
    python3 "$SCRIPT_DIR/issue-manager/scripts/issue_operations.py" \
        query \
        --filter "$filter"
}

function test_all_skills() {
    print_header
    echo -e "${GREEN}Testing all skills...${NC}"
    echo ""

    for skill_dir in "$SCRIPT_DIR"/*/; do
        if [[ -f "${skill_dir}SKILL.md" ]]; then
            skill_name=$(basename "$skill_dir")
            echo -e "${BLUE}Testing: ${skill_name}${NC}"
            python3 "$SCRIPT_DIR/skill-creator/scripts/package_skill.py" "$skill_name" || true
            echo ""
        fi
    done
}

function show_install() {
    print_header
    echo -e "${GREEN}Installation Instructions:${NC}"
    echo ""
    echo "1. Clone or download this repository"
    echo ""
    echo "2. Install in Claude Code:"
    echo "   ${BLUE}/plugin marketplace add ironluffy/claude-skills${NC}"
    echo "   ${BLUE}/plugin install universal-claude-skills${NC}"
    echo ""
    echo "3. Or use skills directly:"
    echo "   ${BLUE}cd skill-creator/scripts${NC}"
    echo "   ${BLUE}./init_skill.py my-skill \"Description\"${NC}"
    echo ""
    echo "4. Platform integrations:"
    echo "   ${BLUE}export LINEAR_API_KEY=\"your-key\"${NC}"
    echo "   ${BLUE}export GITHUB_TOKEN=\"your-token\"${NC}"
    echo ""
}

function show_examples() {
    print_header
    echo -e "${GREEN}Usage Examples:${NC}"
    echo ""
    echo "Create a new skill:"
    echo "  ${BLUE}./skill-helper.sh create pdf-analyzer \"Analyze PDF documents\"${NC}"
    echo ""
    echo "Decompose a task:"
    echo "  ${BLUE}./skill-helper.sh decompose \"Build REST API for orders\"${NC}"
    echo ""
    echo "Report a blocker:"
    echo "  ${BLUE}./skill-helper.sh block TEAM-123 \"Waiting for API design\"${NC}"
    echo ""
    echo "Split an issue:"
    echo "  ${BLUE}./skill-helper.sh split TEAM-456${NC}"
    echo ""
    echo "Validate a skill:"
    echo "  ${BLUE}./skill-helper.sh validate my-skill${NC}"
    echo ""
}

# Main command dispatcher
case "${1:-}" in
    create)
        create_skill "$2" "$3"
        ;;
    validate)
        validate_skill "$2"
        ;;
    list)
        list_skills
        ;;
    decompose)
        if [[ "$2" == "example" ]]; then
            decompose_example
        else
            decompose_task "$2"
        fi
        ;;
    decompose-example)
        decompose_example
        ;;
    block)
        report_blocker "$2" "$3"
        ;;
    split)
        split_issue "$2"
        ;;
    query)
        query_issues "$2"
        ;;
    test-all)
        test_all_skills
        ;;
    install)
        show_install
        ;;
    examples)
        show_examples
        ;;
    help|--help|-h|"")
        show_help
        ;;
    *)
        echo -e "${RED}Unknown command: $1${NC}"
        echo ""
        show_help
        exit 1
        ;;
esac
