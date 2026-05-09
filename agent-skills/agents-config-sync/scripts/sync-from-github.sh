#!/bin/bash

# Sync agent files from GitHub repository
# Usage: sync-from-github [agent1 agent2 ...]

set -e

# Get the agent names from arguments
AGENTS=("$@")

if [ ${#AGENTS[@]} -eq 0 ]; then
    echo "Usage: sync-from-github [agent1 agent2 ...]"
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

# Pull latest changes from GitHub
echo "Pulling latest changes from GitHub..."
git pull

for AGENT in "${AGENTS[@]}"; do
    AGENT=$(echo "$AGENT" | tr '[:upper:]' '[:lower:]')
    
    case $AGENT in
        kodee|kodeespark|emma|govy)
            echo "Syncing $AGENT from GitHub..."
            
            # Check if agent directory exists in repo
            if [ ! -d "$AGENT" ]; then
                echo "Warning: $AGENT directory not found in repository"
                continue
            fi
            
            # Copy files from repo to workspace
            if [ "$AGENT" = "kodee" ] && [ -f "$AGENT/openclaw.json" ]; then
                cp "$AGENT/openclaw.json" ../
            fi
            
            if [ -f "$AGENT/SOUL.md" ]; then
                cp "$AGENT/SOUL.md" ../
            fi
            
            if [ -f "$AGENT/TOOLS.md" ]; then
                cp "$AGENT/TOOLS.md" ../
            fi
            
            if [ -f "$AGENT/USER.md" ]; then
                cp "$AGENT/USER.md" ../
            fi
            
            echo "✓ $AGENT files synced from GitHub"
            ;;
        all)
            # Sync all agents
            echo "Syncing all agents from GitHub..."
            
            for AGENT_DIR in kodee emma govy; do
                if [ -d "$AGENT_DIR" ]; then
                    echo "Syncing $AGENT_DIR..."
                    
                    if [ "$AGENT_DIR" = "kodee" ] && [ -f "$AGENT_DIR/openclaw.json" ]; then
                        cp "$AGENT_DIR/openclaw.json" ../
                    fi
                    
                    [ -f "$AGENT_DIR/SOUL.md" ] && cp "$AGENT_DIR/SOUL.md" ../
                    [ -f "$AGENT_DIR/TOOLS.md" ] && cp "$AGENT_DIR/TOOLS.md" ../
                    [ -f "$AGENT_DIR/USER.md" ] && cp "$AGENT_DIR/USER.md" ../
                fi
            done
            
            echo "✓ All agents synced from GitHub"
            break
            ;;
        *)
            echo "Unknown agent: $AGENT"
            echo "Available agents: kodee emma govy"
            ;;
    esac
done