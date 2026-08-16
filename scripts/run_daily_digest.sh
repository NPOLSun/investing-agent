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

# 최신 코드·설정으로 돌린다.
# 봇이 EC2 에서 쓰는 경로는 스스로 pull 하지만, PC 에서 푸시한 변경은
# 여기서 당기지 않으면 cron 이 옛 코드로 돌고, 끝에 붙는 상태 push 도
# 원격이 앞서 있어 실패한다. 실패해도 다이제스트는 계속 진행한다.
cd /home/ubuntu/investing-agent
git pull --ff-only origin main 2>&1 | tail -2
cd /home/ubuntu/investing-agent/scripts

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

# 실패하면 알린다.
# 성공하면 다이제스트가 오지만 죽으면 아무것도 안 온다 — 그러면 '신호 없는 조용한 날' 과
# '스크립트가 죽은 날' 이 구분되지 않는다. 다이제스트 자체가 미점검과 이상없음을
# 엄격히 구분하는데, 파이프라인 레벨에서 그게 무너지면 의미가 없다.
if [ "$EXIT_CODE" -ne 0 ]; then
  ENV_FILE=/home/ubuntu/investing-agent/.env
  BOT_TOKEN=$(grep "^TELEGRAM_BOT_TOKEN=" "$ENV_FILE" | cut -d= -f2- | tr -d '"'"'"' \r')
  CHAT_ID=$(grep "^TELEGRAM_CHAT_ID=" "$ENV_FILE" | cut -d= -f2- | tr -d '"'"'"' \r')
  if [ -n "$BOT_TOKEN" ] && [ -n "$CHAT_ID" ]; then
    curl -s -o /dev/null --max-time 20 \
      -d chat_id="$CHAT_ID" \
      --data-urlencode "text=⚠️ 일간 다이제스트 실패 (exit $EXIT_CODE)
$(date '+%Y-%m-%d %H:%M') KST

로그 마지막 부분:
$(tail -c 800 "$LOG_FILE")" \
      "https://api.telegram.org/bot$BOT_TOKEN/sendMessage"
  fi
fi

exit $EXIT_CODE
