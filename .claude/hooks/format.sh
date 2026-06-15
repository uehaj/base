#!/usr/bin/env bash
# PostToolUse hook: 直前に編集/作成したファイルを言語に応じて自動整形する。
# 整形ツールやファイルが無ければ静かにスキップし、常に exit 0（編集操作をブロックしない）。
set -o pipefail

input="$(cat)"
# フックの標準入力JSON(tool_input.file_path)から対象ファイルを取り出す。
file="$(printf '%s' "$input" | python3 -c "import sys,json;print(json.load(sys.stdin).get('tool_input',{}).get('file_path',''))" 2>/dev/null)"

[ -z "$file" ] && exit 0
[ -f "$file" ] || exit 0

cd "${CLAUDE_PROJECT_DIR:-.}" 2>/dev/null || exit 0

case "$file" in
  *.py)
    uv run ruff format "$file" >/dev/null 2>&1
    uv run ruff check --fix "$file" >/dev/null 2>&1
    ;;
  *.js|*.jsx|*.ts|*.tsx|*.mjs|*.cjs|*.json|*.md|*.css|*.html|*.yml|*.yaml)
    pnpm exec prettier --write "$file" >/dev/null 2>&1
    ;;
esac

exit 0
