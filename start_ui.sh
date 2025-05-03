#!/usr/bin/env bash
#
# Starts the background agent and then launches
# the Streamlit UI.  When you close Streamlit,
# the agent is cleaned up automatically.

set -e            # exit on first error
set -o pipefail   # catch piped-command errors

# 1) spawn the agent in the background
python3 ./ui/agent_tools.py &
AGENT_PID=$!

# 2) run the Streamlit app in the foreground
streamlit run ./ui/chatbot_st.py

# 3) once Streamlit exits, stop the agent
kill "$AGENT_PID" 2>/dev/null || true
