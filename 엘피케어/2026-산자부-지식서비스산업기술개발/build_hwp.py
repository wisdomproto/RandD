# -*- coding: utf-8 -*-
import json, os, sys
from pyhwpx import Hwp

BASE = os.path.dirname(os.path.abspath(__file__))
seq = json.load(open(os.path.join(BASE, "seq.json"), encoding="utf-8"))

BOUNDS = {
    's2': ("2. 연구개발과제의 목표 및 내용", "3. 연구개발과제의 추진전략·방법 및 추진체계"),
    's3': ("3. 연구개발과제의 추진전략·방법 및 추진체계", "4. 연구개발성과의 활용방안 및 기대효과"),
    's4': ("4. 연구개발성과의 활용방안 및 기대효과", "5. 연구개발성과의 사업화 전략 및 계획"),
    's5': ("5. 연구개발성과의 사업화 전략 및 계획", "6. 연구개발 안전 및 보안조치 이행계획"),
}

h = Hwp(visible=True)
api = h.hwp
try:
    api.SetMessageBoxMode(0x00020000)  # 모든 메시지박스 자동 응답(기본값 선택)
except Exception as e:
    print("SetMessageBoxMode skip:", e, flush=True)
api.Open(os.path.join(BASE, "제출양식", "_작업본.hwp"), "HWP", "")

def find(t):
    f = api.HParameterSet.HFindReplace
    api.HAction.GetDefault("RepeatFind", f.HSet)
    f.FindString = t; f.Direction = 0; f.IgnoreMessage = 1
    return api.HAction.Execute("RepeatFind", f.HSet)

def run(a): api.HAction.Run(a)
def para(): return api.GetPosBySet().Item("Para")

def ins_text(txt):
    s = api.HParameterSet.HInsertText
    api.HAction.GetDefault("InsertText", s.HSet)
    s.Text = txt
    api.HAction.Execute("InsertText", s.HSet)

def ins_pic(path):
    try:
        h.insert_picture(path)
        return True
    except Exception:
        return False

def do_section(sec):
    st, en = BOUNDS[sec]
    print("[%s] find bounds" % sec, flush=True)
    run("MoveDocBegin")
    find(st); find(st)            # 목차 건너 본문
    run("MoveLineBegin"); sp = para()
    r2 = find(en)                  # 본문 시작 이후 = 다음 장 본문
    run("MoveLineBegin"); ep = para()
    print("[%s] sp=%s ep=%s foundEnd=%s" % (sec, sp, ep, r2), flush=True)
    if ep <= sp or (ep - sp) > 2000:
        print("[%s] ABORT bad range" % sec, flush=True)
        return -1
    api.SelectText(sp, 0, ep, 0)
    run("Delete")
    print("[%s] deleted; insert %d items" % (sec, len(seq[sec])), flush=True)
    first = True
    nimg = 0
    for i, it in enumerate(seq[sec]):
        if not first: run("BreakPara")
        first = False
        t = it['t']; x = it.get('x', '')
        if t == 'i':
            p = os.path.join(BASE, "images", x + ".png")
            print("[%s] item%d IMG %s exists=%s" % (sec, i, x, os.path.exists(p)), flush=True)
            if os.path.exists(p) and ins_pic(p):
                nimg += 1
            else:
                ins_text("[그림: %s]" % x)
        elif t == 'l':
            ins_text("  - " + x)
        else:
            ins_text(x)
    print("[%s] done nimg=%d" % (sec, nimg), flush=True)
    run("BreakPara")
    return nimg

targets = sys.argv[1:] or ['s2']
res = {}
for sec in targets:
    res[sec] = do_section(sec)

api.SaveAs(os.path.join(BASE, "제출양식", "_작업본.hwp"), "HWP", "")
h.quit()
print("done", targets, "imgs:", res)
