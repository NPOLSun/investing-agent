# Step 3 — AWS EC2 인스턴스 생성 + SSH 접속

> 가장 어려운 단계. 30분~1시간.
> 본인이 Linux 환경 셋업 경험 있다 했으니 평균보다 수월할 수 있지만, AWS 콘솔 UI 가 복잡.

---

## 0. 작업 개요

이 단계에서 본인이 만들 것:

1. AWS 에서 **EC2 인스턴스** (가상 서버) 하나 생성
2. SSH key 다운로드 + Windows 에서 사용 준비
3. **방화벽 (Security Group)** 설정 — 본인 PC 에서 SSH 접속 가능하게
4. PowerShell 에서 EC2 에 SSH 접속

완료 시 본인은 *AWS 의 Ubuntu Linux 서버* 에 접속한 상태.

---

## 1. AWS 콘솔에서 EC2 시작 (5분)

### 1.1 AWS 콘솔 로그인
1. https://console.aws.amazon.com 접속·로그인
2. 우측 상단 region 확인: **"Asia Pacific (Seoul) ap-northeast-2"** 로 설정
   - 다른 region 이면 클릭해서 변경

### 1.2 EC2 서비스로 이동
1. 좌측 상단 "Services" → 검색 "EC2" → 클릭
2. 또는 직접 URL: https://ap-northeast-2.console.aws.amazon.com/ec2/

### 1.3 인스턴스 시작
1. EC2 대시보드에서 "Launch instance" 클릭 (주황색 버튼)

---

## 2. 인스턴스 설정 (10분)

### 2.1 Name (이름)
- **Name**: `investing-agent-v2` (또는 본인 원하는 이름)

### 2.2 Application and OS Images (Amazon Machine Image — AMI)
- "Quick Start" 탭에서 **Ubuntu** 선택
- "Amazon Machine Image (AMI)": 기본값 (Ubuntu Server 24.04 LTS 또는 22.04 LTS — 두 개 다 OK)
- **Architecture**: 64-bit (x86) — 기본값

### 2.3 Instance type (인스턴스 사양)
- **t3.small** 선택
  - 가격: 시간당 ~$0.026 USD = 월 약 $15~18 (서울 리전)
  - 메모리 2GB, vCPU 2
  - Track 1 일간만 작동 시 충분
- 만약 비용 더 줄이고 싶으면 **t3.micro** 도 가능 (메모리 1GB, ~$8/월) — 약간 좁지만 작동

### 2.4 Key pair (login) ★ 가장 중요
1. **"Create new key pair"** 클릭
2. **Key pair name**: `investing-agent-key` (또는 본인 원하는 이름)
3. **Key pair type**: RSA (기본값)
4. **Private key file format**: **.pem** 선택 (★ Windows 에서 PuTTY 안 쓰면 .pem 이 표준)
5. "Create key pair" 클릭
6. 자동으로 `investing-agent-key.pem` 파일 다운로드됨
7. **이 파일을 잃어버리면 EC2 접속 불가**. 안전한 위치에 보관:
   - 추천 위치: `C:\Users\본인\.ssh\investing-agent-key.pem`
   - `.ssh` 폴더 없으면 생성

### 2.5 Network settings (방화벽)
1. "Edit" 클릭 (오른쪽 상단)
2. **Allow SSH traffic from**: **My IP** 선택 (★ 본인 IP 만 접속 가능, 보안)
   - 또는 "Anywhere" 가능하나 보안 약함
3. 다른 항목 (HTTP/HTTPS) 은 체크 안 함 (필요 없음)

### 2.6 Configure storage (디스크)
- **8 GiB** 기본값 그대로 (충분)
- 또는 늘리고 싶으면 20 GiB (월 추가 $1~2)

### 2.7 Advanced details
- 건드릴 필요 없음. 기본값.

### 2.8 Summary 확인 + 시작
- 우측 "Summary" 패널 확인:
  - Number of instances: 1
  - OS: Ubuntu
  - Instance type: t3.small
  - Key pair: investing-agent-key
  - Network: SSH from My IP
- "Launch instance" 클릭 (주황색 버튼)

→ 1~2분 후 "Successfully initiated launch of instance" 메시지.

### 2.9 인스턴스 정보 확인
1. "View all instances" 클릭
2. 본인 인스턴스 (Name: investing-agent-v2) 상태 확인:
   - Instance state: **Running** (녹색)
   - Status check: 2/2 checks passed (약 2~3분 후)
3. **Public IPv4 address** 메모 (예: `13.124.XXX.XXX`)
   - ★ 이 IP 로 SSH 접속

- [ ] EC2 인스턴스 생성 완료
- [ ] .pem 파일 다운로드·안전한 위치 보관
- [ ] Public IPv4 주소 메모

---

## 3. .pem 파일 권한 설정 (5분)

Windows 에서 .pem 파일을 그대로 사용하면 SSH 가 "Permissions too open" 에러. 권한 제한 필수.

### 3.1 PowerShell 에서 권한 설정

PowerShell 열고 (관리자 권한 필요할 수 있음):

```powershell
# .pem 파일 위치로 이동
cd C:\Users\본인\.ssh

# 권한 제거 (Inherit 제거)
icacls investing-agent-key.pem /inheritance:r

# 본인 user 만 read 권한
icacls investing-agent-key.pem /grant:r "$($env:USERNAME):(R)"

# 다른 권한 모두 제거
icacls investing-agent-key.pem /remove "Authenticated Users"
icacls investing-agent-key.pem /remove "BUILTIN\Users"
icacls investing-agent-key.pem /remove "Everyone" 2>$null
```

→ 마지막 명령 일부는 "no such user" 에러 나올 수 있음 (정상, 무시).

### 3.2 권한 확인
```powershell
icacls investing-agent-key.pem
```

→ 출력에 본인 username 만 보이면 OK.

- [ ] .pem 파일 권한 제한 완료

---

## 4. SSH 로 EC2 접속 (5분)

### 4.1 PowerShell 에서 SSH 명령

```powershell
ssh -i C:\Users\본인\.ssh\investing-agent-key.pem ubuntu@13.124.XXX.XXX
```

- `-i ...pem` : 본인 SSH key 파일 위치
- `ubuntu@...` : Ubuntu 인스턴스 기본 사용자 이름은 `ubuntu`
- `13.124.XXX.XXX` : 본인 EC2 의 Public IPv4 (위 2.9 에서 메모한 값)

### 4.2 첫 접속 확인
첫 접속 시 다음과 같은 질문 나옴:
```
The authenticity of host '13.124.XXX.XXX' can't be established.
ECDSA key fingerprint is SHA256:XXXXXXXX
Are you sure you want to continue connecting (yes/no/[fingerprint])?
```

→ `yes` 입력 후 Enter.

### 4.3 접속 성공 화면
다음과 같이 출력되면 성공:
```
Welcome to Ubuntu 24.04 LTS (GNU/Linux 6.X.X-aws x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/pro

  System information as of XXX
  ...

ubuntu@ip-172-XX-XX-XXX:~$
```

→ 마지막 줄의 `ubuntu@...:~$` 가 **EC2 안의 프롬프트**. 본인이 이제 EC2 안에 있음.

- [ ] SSH 접속 성공

### 4.4 EC2 안에서 확인 명령
```bash
whoami
# 출력: ubuntu

pwd
# 출력: /home/ubuntu

uname -a
# 출력: Linux ip-172-XX-XX-XXX ... Ubuntu ...

df -h
# 출력: 디스크 용량 (8GiB)
```

- [ ] EC2 안에서 명령 실행 확인

### 4.5 접속 종료
나오는 명령:
```bash
exit
```

→ PowerShell 프롬프트로 돌아옴.

---

## 5. (선택, 권장) SSH 접속 단축키 설정

매번 긴 명령어 치는 게 번거로움. SSH config 파일로 단축 가능.

### 5.1 SSH config 파일 생성/편집

```powershell
notepad C:\Users\본인\.ssh\config
```

(파일 없으면 새로 생성 — 확장자 없음)

내용:
```
Host investing-agent
    HostName 13.124.XXX.XXX
    User ubuntu
    IdentityFile C:\Users\본인\.ssh\investing-agent-key.pem
```

→ 본인 IP·경로로 수정해서 저장.

### 5.2 단축 접속
이제부터는:
```powershell
ssh investing-agent
```

→ 한 줄로 접속.

- [ ] (선택) SSH config 설정

---

## 6. Step 3 완료 ✅

다음 모두 ✅ 되었으면 Step 4 진행 가능:

- [ ] EC2 인스턴스 생성·Running 확인
- [ ] .pem 파일 다운로드·권한 설정
- [ ] Public IPv4 주소 메모
- [ ] SSH 접속 성공 (`ubuntu@ip-...:~$` 프롬프트 확인)
- [ ] EC2 안에서 기본 명령 실행 확인
- [ ] (선택) SSH config 단축키

---

## 트러블슈팅

### "Permission denied (publickey)"
**원인**: SSH key 권한 또는 파일 경로 문제.

해결:
1. .pem 파일 경로 정확한지 확인
2. 위 3.1 의 권한 명령 다시 실행
3. EC2 인스턴스의 username 확인 (Ubuntu = `ubuntu`, Amazon Linux = `ec2-user`)

### "Connection timed out"
**원인**: Security Group (방화벽) 가 본인 IP 차단.

해결:
1. AWS 콘솔 → EC2 → Instances → 본인 인스턴스 클릭
2. "Security" 탭 → Security group 클릭
3. "Inbound rules" 확인:
   - Type: SSH, Port: 22
   - Source: 본인 현재 IP (`X.X.X.X/32`)
4. 본인 IP 가 바뀌었으면 (Wi-Fi 변경 등):
   - "Edit inbound rules" → SSH 룰의 Source 를 "My IP" 로 다시 선택 → Save
5. 다시 SSH 시도

### "Bad permissions" 또는 ".pem file UNPROTECTED"
**원인**: .pem 파일 권한 너무 광범위.

해결: 위 3.1 의 icacls 명령 다시 실행.

### EC2 인스턴스 Status check 가 0/2
**원인**: 인스턴스 부팅 중. 2~3분 더 기다리기.

### AWS 콘솔에서 "Insufficient capacity"
**원인**: 서울 리전 t3.small 일시 품절 (드뭄).

해결: 1~2시간 후 재시도, 또는 t3.micro 로 선택.

### 방금 만든 인스턴스가 안 보임
**원인**: Region 다를 가능성. 우측 상단 region 이 "서울" 인지 확인.

---

## ⚠️ 비용 주의

EC2 는 **인스턴스가 Running 상태인 시간만큼 과금**. 24/7 켜져 있으면 월 ~$15~18.

**비상 시 (시스템 작동 중단 원할 때)**:
1. AWS 콘솔 → EC2 → 인스턴스 우클릭 → "Stop instance" (재시작 가능)
2. 또는 "Terminate instance" (완전 삭제 — 데이터 손실!)

Stop 시 EC2 자체 과금은 멈추나, **storage (EBS) 는 계속 과금** (~$1/월).
Terminate 시 모든 과금 멈추나 데이터 손실. **신중 결정**.

---

## 완료 후

본인이 위 ✅ 다 했으면:
> "Step 3 완료. Step 4 진행."

또는 막힌 부분 있으면:
> "Step 3 의 X.X 에서 막힘. 에러: [에러 메시지]"

다음 Step 4 (Python 환경·패키지 설치) 안내 드립니다. Step 3 가 가장 어려웠고, Step 4 부터는 본인이 익숙한 Python 영역.
