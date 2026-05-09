#!/bin/bash

# Sync agent files to GitHub repository
# Usage: sync-to-github [agent1 agent2 ...]

set -e

# Get the agent names from arguments
AGENTS=("$@")

if [ ${#AGENTS[@]} -eq 0 ]; then
    echo "Usage: sync-to-github [agent1 agent2 ...]"
    echo "Available agents: kodee emma govy"
    exit 1
fi

# Check if agents repo exists
if [ ! -d "agents" ]; then
    echo "Error: agents repository not found"
    echo "Clone it first: git clone https://github.com/4hfaisal/agents.git"
    exit 1
fi

cd agents

for AGENT in "${AGENTS[@]}"; do
    AGENT=$(echo "$AGENT" | tr '[:upper:]' '[:lower:]')
    
    case $AGENT in
        kodee|kodeespark|emma|govy)
            echo "Syncing $AGENT to GitHub..."
            
            # Create agent directory if it doesn't exist
            mkdir -p "$AGENT"
            
            # Copy files from workspace
            if [ "$AGENT" = "kodee" ]; then
                cp ../openclaw.json "$AGENT/"
            fi
            cp ../SOUL.md "$AGENT/"
            cp ../TOOLS.md "$AGENT/"
            cp ../USER.md "$AGENT/"
            
            # Add to git
            git add "$AGENT/"
            
            echo "✓ $AGENT files copied"
            ;;
        all)
            # Sync all agents
            echo "Syncing all agents to GitHub..."
            
            # Kodee gets openclaw.json
            mkdir -p kodee
            cp ../openclaw.json kodee/
            cp ../SOUL.md kodee/
            cp ../TOOLS.md kodee/
            cp ../USER.md kodee/
            git add kodee/
            
            # Other agents
            for OTHER_AGENT in emma govy; do
                mkdir -p "$OTHER_AGENT"
                cp ../SOUL.md "$OTHER_AGENT/"
                cp ../TOOLS.md "$OTHER_AGENT/"
                cp ../USER.md "$OTHER_AGENT/"
                git add "$OTHER_AGENT/"
            done
            
            echo "✓ All agents synced"
            break
            ;;
        *)
            echo "Unknown agent: $AGENT"
            echo "Available agents: kodee emma govy"
            ;;
    esac
done

# Commit and push
if git diff-index --quiet HEAD --; then
    echo "No changes to commit"
else
    git commit -m "Sync agent files: ${AGENTS[*]}"
    git push
    echo "✓ Changes committed and pushed to GitHub"
fi