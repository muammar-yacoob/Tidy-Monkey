#!/bin/bash
# Linting script for TidyMonkey Blender addon

echo "🔍 Running Python linting checks..."
echo ""

# Check if in virtual environment
if [ -z "$VIRTUAL_ENV" ]; then
    echo "⚠️  Warning: Not in a virtual environment"
    echo "   Consider running: python3 -m venv .venv && source .venv/bin/activate"
    echo ""
fi

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

errors=0

# 1. Check Python syntax
echo "1️⃣  Checking Python syntax..."
if python3 -m py_compile __init__.py src/**/*.py 2>/dev/null; then
    echo -e "${GREEN}✓ Syntax check passed${NC}"
else
    echo -e "${RED}✗ Syntax errors found${NC}"
    python3 -m py_compile __init__.py src/**/*.py
    ((errors++))
fi
echo ""

# 2. Run flake8
echo "2️⃣  Running flake8..."
if command -v flake8 &> /dev/null; then
    if flake8 . --count --show-source --statistics; then
        echo -e "${GREEN}✓ Flake8 passed${NC}"
    else
        echo -e "${YELLOW}⚠ Flake8 found issues${NC}"
        ((errors++))
    fi
else
    echo -e "${YELLOW}⚠ flake8 not installed. Install with: pip install -r dev-requirements.txt${NC}"
fi
echo ""

# 3. Run pylint
echo "3️⃣  Running pylint..."
if command -v pylint &> /dev/null; then
    if pylint __init__.py src/ --rcfile=pyproject.toml 2>/dev/null; then
        echo -e "${GREEN}✓ Pylint passed${NC}"
    else
        echo -e "${YELLOW}⚠ Pylint found issues${NC}"
    fi
else
    echo -e "${YELLOW}⚠ pylint not installed. Install with: pip install -r dev-requirements.txt${NC}"
fi
echo ""

# 4. Run mypy
echo "4️⃣  Running mypy type checking..."
if command -v mypy &> /dev/null; then
    if mypy src/ --config-file=pyproject.toml 2>/dev/null; then
        echo -e "${GREEN}✓ Type checking passed${NC}"
    else
        echo -e "${YELLOW}⚠ Type checking found issues${NC}"
    fi
else
    echo -e "${YELLOW}⚠ mypy not installed. Install with: pip install -r dev-requirements.txt${NC}"
fi
echo ""

# Summary
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if [ $errors -eq 0 ]; then
    echo -e "${GREEN}✓ All critical checks passed!${NC}"
    exit 0
else
    echo -e "${RED}✗ Found $errors critical issue(s)${NC}"
    exit 1
fi
