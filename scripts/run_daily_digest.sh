#!/bin/bash
# Daily Digest wrapper for cron
# venv 활성화 + 작업 디렉토리 설정 + 스크립트 실행

cd /home/ubuntu/investing-agent/scripts
source /home/ubuntu/investing-agent/venv/bin/activate

# Claude Code 구독 인증 토큰 (.env → 환경변수)
# claude CLI 는 .env 를 자동으로 읽지 않으므로 여기서 넘겨준다
if [ -f /home/ubuntu/investing-agent/.env ]; then
  export CLAUDE_CODE_OAUTH_TOKEN=$(grep "^CLAUDE_CODE_OAUTH_TOKEN=" /home/ubuntu/investing-agent/.env | cut -d= -f2- | tr -d '"'"'"' \r')
fi

LOG_DIR=/home/ubuntu/investing-agent/logs
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/daily_digest_$(date +%Y%m%d).log"

# 오래된 것부터 정리 (디스크 6.8GB 뿐이라 무한 적재 금지)
find "$LOG_DIR" -name 'daily_digest_*.log' -mtime +14 -delete 2>/dev/null
find /home/ubuntu/investing-agent/digests/dry-run -type f -mtime +14 -delete 2>/dev/null

echo "=== $(date '+%Y-%m-%d %H:%M:%S') Daily Digest 시작 ===" >> "$LOG_FILE"

python3 daily_digest.py >> "$LOG_FILE" 2>&1
EXIT_CODE=$?

echo "=== $(date '+%Y-%m-%d %H:%M:%S') Daily Digest 종료 (exit: $EXIT_CODE) ===" >> "$LOG_FILE"

exit $EXIT_CODE
