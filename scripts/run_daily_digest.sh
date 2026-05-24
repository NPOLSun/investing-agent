#!/bin/bash
# Daily Digest wrapper for cron
# venv 활성화 + 작업 디렉토리 설정 + 스크립트 실행

cd /home/ubuntu/investing-agent/scripts
source /home/ubuntu/investing-agent/venv/bin/activate

# 로그 파일에 기록
LOG_DIR=/home/ubuntu/investing-agent/logs
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/daily_digest_$(date +%Y%m%d).log"

echo "=== $(date '+%Y-%m-%d %H:%M:%S') Daily Digest 시작 ===" >> "$LOG_FILE"

python3 daily_digest.py >> "$LOG_FILE" 2>&1
EXIT_CODE=$?

echo "=== $(date '+%Y-%m-%d %H:%M:%S') Daily Digest 종료 (exit: $EXIT_CODE) ===" >> "$LOG_FILE"

exit $EXIT_CODE
