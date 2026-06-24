# -*- coding: utf-8 -*-
"""사업계획서 이미지 업로드 지원 로컬 서버.

- GET            : 정적 파일 서빙 (사업계획서_작성.html, 이미지_프롬프트.html, images/ 등)
- POST /upload?fig=N : 본문(raw 이미지 바이트)을 images/figN.png 로 저장
- POST /delete?fig=N : images/figN.png 삭제

실행:  python 서버.py [포트]   (기본 8000)
"""
import os
import sys
import json
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

ROOT = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(ROOT, "images")
os.makedirs(IMG_DIR, exist_ok=True)

MAX_BYTES = 25 * 1024 * 1024  # 25MB 상한


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=ROOT, **k)

    # --- 공통 JSON 응답 ---
    def _json(self, code, obj):
        body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def _fig_param(self):
        q = parse_qs(urlparse(self.path).query)
        fig = q.get("fig", [None])[0]
        return fig if (fig and fig.isdigit()) else None

    def do_POST(self):
        path = urlparse(self.path).path
        if path == "/upload":
            fig = self._fig_param()
            if not fig:
                return self._json(400, {"ok": False, "err": "fig 파라미터 필요"})
            length = int(self.headers.get("Content-Length", 0))
            if length <= 0 or length > MAX_BYTES:
                return self._json(400, {"ok": False, "err": "크기 오류"})
            data = self.rfile.read(length)
            out = os.path.join(IMG_DIR, "fig%s.png" % fig)
            with open(out, "wb") as f:
                f.write(data)
            return self._json(200, {"ok": True, "path": "images/fig%s.png" % fig})

        if path == "/delete":
            fig = self._fig_param()
            if not fig:
                return self._json(400, {"ok": False, "err": "fig 파라미터 필요"})
            out = os.path.join(IMG_DIR, "fig%s.png" % fig)
            existed = os.path.exists(out)
            if existed:
                os.remove(out)
            return self._json(200, {"ok": True, "removed": existed})

        self._json(404, {"ok": False, "err": "알 수 없는 경로"})

    # 이미지 즉시 갱신 위해 캐시 비활성
    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def log_message(self, *a):
        pass  # 콘솔 조용히


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    srv = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    print("Serving %s" % ROOT)
    print("  http://localhost:%d/사업계획서_작성.html" % port)
    print("  http://localhost:%d/이미지_프롬프트.html" % port)
    print("  (POST /upload?fig=N, /delete?fig=N 지원)")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        srv.shutdown()
