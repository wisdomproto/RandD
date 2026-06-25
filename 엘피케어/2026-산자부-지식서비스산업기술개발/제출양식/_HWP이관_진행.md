# HWP 제출본 이관 진행 메모

`사업계획서_작성.html`(HTML 작업본) → KEIT 제출 양식 HWP로 옮기는 작업.

## 현황 (2026-06-25 기준)
- ✅ **1장**(필요성): 텍스트 완료
- ✅ **2장**(목표·내용): 텍스트 + 표/그림 이미지 17개 삽입 완료
- ⬜ **3~5장**: 미완 (조립 중 COM 에러로 중단)
- 작업본: `_작업본.hwp` (1·2장 반영본 — 원본 빈 양식 `연구개발계획서_260617.hwp` 복사본)

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

## ⚠️ 미해결 이슈
- 3~5장 조립 시 `api.Open()`에서 `pywintypes.com_error (-2147023170, '원격 프로시저를 호출하지 못했습니다')` 발생.
- 원인 추정: 직전 한글(Hwp.exe) 인스턴스가 안 닫혀 COM 충돌 / 좀비 프로세스.
- **해결 방향**: 실행 전 `taskkill /F /IM Hwp.exe` 로 한글 완전 종료 확인 → 단일 인스턴스로 한 섹션씩.
  build_hwp.py가 매번 `Hwp()`+`Open` 하는데, gen_py 캐시(`%TEMP%\gen_py`) 손상 시도 의심 → 캐시 삭제 후 재시도도 방법.
- 2장은 같은 코드로 성공했으므로 코드 로직 자체는 동작함(환경/타이밍 문제).

## 파일 목록
- `build_hwp.py` — 조립 스크립트 (pyhwpx + COM)
- `seq.json` — 2~5장 텍스트/이미지 시퀀스
- `서버.py` — `/upload_img`(이미지 base64 저장), `/save_json`(시퀀스 저장) 추가
- `_작업본.hwp` — 1·2장 반영 작업본 (이어서 작업할 파일)
- `연구개발계획서_260617.hwp` — 원본 빈 양식
- `../images/*.png` — 캡처된 표·그림 (fig5~10=AI/캡처, s*_t*=표, svgfig*=SVG그림)

## 참고: 본문 텍스트는 양식 서식 유지하며 직접 입력, 표·그림은 모두 이미지로 삽입(사용자 결정).
