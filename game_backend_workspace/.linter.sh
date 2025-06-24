#!/bin/bash
cd /home/kavia/workspace/code-generation/tictactoe-connect-68731-2267312d/game_backend_workspace/game_backend
source venv/bin/activate
flake8 .
LINT_EXIT_CODE=$?
if [ $LINT_EXIT_CODE -ne 0 ]; then
  exit 1
fi

