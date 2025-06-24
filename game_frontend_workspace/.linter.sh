#!/bin/bash
cd /home/kavia/workspace/code-generation/tictactoe-connect-68731-2267312d/game_frontend_workspace/game_frontend
npx eslint
ESLINT_EXIT_CODE=$?
npm run build
BUILD_EXIT_CODE=$?
if [ $ESLINT_EXIT_CODE -ne 0 ] || [ $BUILD_EXIT_CODE -ne 0 ]; then
   exit 1
fi

