# HWP 제출본 이관 진행 메모

`사업계획서_작성.html`(HTML 작업본) → KEIT 제출 양식 HWP로 옮기는 작업.

## 현황 (2026-06-25 기준)
- ✅ **1장**(필요성): 텍스트 완료
- ✅ **2장**(목표·내용): 텍스트 + 표/그림 이미지 17개 삽입 완료
- ✅ **3장**(추진전략·체계): 35항목 + 그림 2개(`s3_t0` 추진체계, `s3_t1` 일자리표)
- ✅ **4장**(활용·기대효과): 24항목 + 그림 2개(`svgfig2`, `s4_t0`)
- ✅ **5장**(사업화 전략): 25항목 + 그림 7개(`svgfig3`, `s5_t0~5`)
- ✅ **요약문**(표#2): 연구개발 목표 및 내용 6셀(H15 최종목표·H16 전체내용·H17/H18 1단계·H19/H20 2단계 1·2·3차년도) + 활용·기대효과(C22, 기술기여도 표는 보존). ⏳ 미작성: 과제명·전체기간·총연구개발비·기술분류(디자인과제 잔재)·과제특성(서비스형)·국문/영문 핵심어
- 작업본: `_작업본.hwp` (1~5장+요약문, 9.2MB). 백업 = `_작업본_백업_1·2장.hwp`·`_작업본_백업_요약전.hwp`·`_요약전2.hwp`·`_활용전.hwp`
- ⚠️ **HWP ↔ HTML 재동기화 필요**: 2026-06-26 평가위원 4축 검토(도전성·창의성/연구역량·사업성/논리흐름/양식·톤) 반영해 `사업계획서_작성.html` 본문을 대폭 수정(톤다운·논리연결·난제 해결접근·정답셋 정의·반복정리). **HWP 요약문은 구 HTML 기준으로 채운 상태**라 본문과 어긋남 → HTML 확정 후 1~5장+요약문 재이관 권장. 미해결 핵심 = 실데이터 빈칸(AI책임자 실적·재무·단위경제·SAM/SOM·인건비계상률·인터뷰/LOI)

## 전제 (다른 컴퓨터)
- 한컴오피스(한글) 설치 필수
- `pip install pyhwpx olefile python-hwpx beautifulsoup4 lxml`

## 작업 순서
1. **보안모듈 등록** (한글 COM 접근 팝업 제거):
   `python -c "from pyhwpx import Hwp; h=Hwp(visible=False); h.quit()"`
   → `FilePathCheckerModule.dll` 레지스트리 등록됨 (이후 COM Open 시 팝업 없음)
2. **표/그림 캡처** — 이미 완료되어 `images/`에 저장됨. (다시 할 경우)
   - `python 서버.py 8000` 실행 → 브라우저 `localhost:8000/사업계획서_작성.html`
   - 콘솔(개발자도구)에서 html2canvas(CDN)로 표·그림 캡처 → `POST /upload_img?name=X` (서버가 `images/X.png` 저장)
   - 결과: `s2_t0~9, s3_t0~1, s4_t0, s5_t0~5`(표 19) + `svgfig0~3`(SVG 그림 4: s1·s2·s4·s5)
3. **시퀀스**: `seq.json` = 2~5장 DOM 순서 (t=h소제목/p문단/l리스트/i이미지, x=텍스트 또는 이미지이름)
4. **조립**: `python build_hwp.py s3 s4 s5` (또는 s2부터 재실행 가능)
   - 양식의 장 영역(예 "2. …목표 및 내용" 본문 ~ "3. …추진전략" 본문)을 SelectText로 선택·삭제
   - seq 순서대로 텍스트(소제목/○문단/- 리스트)·이미지(`images/*.png`) 삽입

## ✅ 해결된 이슈 — 보안 다이얼로그 (2026-06-25 갱신: 헤드리스 가능해짐)
- 증상은 `api.Open()` 무한 대기였으나, 진짜 원인은 한글 **파일접근 보안 승인 다이얼로그**.
- **최종 해결: `Hwp.register_regedit()` 1회 호출로 보안모듈 레지스트리 등록됨** → 이후 `Hwp(visible=False)` 헤드리스로 다이얼로그·수동클릭 없이 Open/편집/저장 가능. (`RegisterModule(...)`은 이 PC서 False지만 register_regedit가 됐으면 무관.)
  - 과거엔 `visible=True` + "모두 허용(N)" 수동클릭으로 우회했음 — 등록 후엔 불필요.
- **셀 채우기 노하우(요약문 작업서 확정):** `TableCellBlock`+`Delete`로는 셀 비우기 안 됨(새 텍스트가 기존 placeholder 앞에 붙음). → 셀 진입 후 `Cancel`→`MoveListBegin`→`MoveSelListEnd`→`Delete`로 비우고, 줄마다 `BreakPara`+`InsertText`. 병합셀 많은 표는 `get_cell_addr` dup-skip 순회. `SaveAs` 먼저 저장(이후 `quit()` com_error는 무해).
- **이식성**: `BASE`를 스크립트 위치 기준(`os.path.dirname(__file__)`)으로 변경.
- 실행 전 `taskkill /F /IM Hwp.exe`로 좀비 인스턴스 정리(특히 직전 실행이 안 닫혔으면 다음 Open이 파일잠금으로 멈춤 — kill 후 재시도).

## 파일 목록
- `build_hwp.py` — 조립 스크립트 (pyhwpx + COM)
- `seq.json` — 2~5장 텍스트/이미지 시퀀스
- `서버.py` — `/upload_img`(이미지 base64 저장), `/save_json`(시퀀스 저장) 추가
- `_작업본.hwp` — 1·2장 반영 작업본 (이어서 작업할 파일)
- `연구개발계획서_260617.hwp` — 원본 빈 양식
- `../images/*.png` — 캡처된 표·그림 (fig5~10=AI/캡처, s*_t*=표, svgfig*=SVG그림)

## 참고: 본문 텍스트는 양식 서식 유지하며 직접 입력, 표·그림은 모두 이미지로 삽입(사용자 결정).
