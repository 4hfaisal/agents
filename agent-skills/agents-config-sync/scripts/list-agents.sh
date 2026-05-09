#!/bin/bash

# List available agents in the repository

echo "Available agents in repository:"
echo ""

if [ -d "agents" ]; then
    cd agents
    
    echo "Local agents:"
    ls -1d */ 2>/dev/null | sed 's/\///g' | grep -v "^\." || echo "No agents found"
    echo ""
    
    echo "GitHub repository: https://github.com/4hfaisal/agents"
    echo ""
    
    echo "Agent folders contain:"
    echo "- SOUL.md (agent identity)"
    echo "- TOOLS.md (tool configurations)"
    echo "- USER.md (user information)"
    echo "- openclaw.json (Kodee only - main configuration)"
    
else
    echo "Agents repository not found locally"
    echo "Clone it: git clone https://github.com/4hfaisal/agents.git"
fi