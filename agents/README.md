# Claude Code 에이전트

연구비(정부 R&D 과제 연구개발계획서) 작업용 Claude Code 서브에이전트 원본을 버전관리하는 폴더.

## 에이전트 목록
- `research-proposal-writer.md` — 정부 R&D 사업계획서 작성 전문가. 공고문·양식·기존 제출본을 전수 분석해 평가배점에 맞춰 계획서를 끝까지 써낸다. 과제를 하나 끝낼 때마다 부처별 양식 노하우를 누적한다.

## 다른 컴퓨터에서 사용하는 법

Claude Code는 에이전트를 두 위치에서 인식한다:
- `~/.claude/agents/` — **그 PC의 모든 프로젝트**에서 사용 (전역, 권장)
- `<프로젝트>/.claude/agents/` — 그 프로젝트에서만

이 repo를 clone/pull 한 뒤, 에이전트 파일을 홈의 전역 폴더로 복사하면 끝.

### Windows (PowerShell)
```powershell
git clone https://github.com/wisdomproto/RandD.git   # 처음 1회
# 이후 갱신은: git -C RandD pull

New-Item -ItemType Directory -Force "$env:USERPROFILE\.claude\agents" | Out-Null
Copy-Item ".\RandD\agents\research-proposal-writer.md" "$env:USERPROFILE\.claude\agents\" -Force
```

### macOS / Linux
```bash
git clone https://github.com/wisdomproto/RandD.git    # 처음 1회
mkdir -p ~/.claude/agents
cp RandD/agents/research-proposal-writer.md ~/.claude/agents/
```

복사 후 Claude Code를 새로 켜면 `research-proposal-writer` 에이전트가 모든 프로젝트에서 잡힌다.

## 에이전트를 수정했을 때 (노하우 누적)
작업하면서 에이전트를 개선했다면, **이 repo의 `agents/` 원본도 같이 갱신**해야 다른 PC에 반영된다.

```powershell
Copy-Item "$env:USERPROFILE\.claude\agents\research-proposal-writer.md" ".\RandD\agents\" -Force
git -C RandD add agents/ ; git -C RandD commit -m "chore: research-proposal-writer 노하우 갱신" ; git -C RandD push
```

> 주의: 에이전트 원본이 특정 프로젝트의 `.claude/agents/`(예: dflo)에 있고 그 repo의 `.gitignore`가 `.claude/`를 막고 있으면 git에 안 올라간다. 원본은 항상 이 repo(또는 `~/.claude/agents/`)를 기준으로 관리할 것.
