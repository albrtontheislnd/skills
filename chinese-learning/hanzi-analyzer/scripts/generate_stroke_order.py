#!/usr/bin/env python3
"""
generate_stroke_order.py

Sinh ra MOT file HTML doc-lap (self-contained), su dung thu vien JS
`hanzi-writer` (tai qua CDN jsdelivr) de hien thi hoat hoa thu tu net
viet (stroke order) cho mot hoac nhieu chu Han.

Khong can cai dat npm / pip package nao them (chi dung Python stdlib).
File HTML sinh ra can duoc mo bang trinh duyet co ket noi Internet, vi
du lieu net chu (`hanzi-writer-data`) duoc hanzi-writer tai dong ve tu
CDN ngay trong trinh duyet.

Vi du:
    python3 generate_stroke_order.py 想 爱 --output stroke_order.html
    python3 generate_stroke_order.py 你好吗 --mode quiz --output quiz.html
    python3 generate_stroke_order.py 龍 --charset traditional --loop
"""

import argparse
import json
import sys
from pathlib import Path

HANZI_WRITER_CDN = "https://cdn.jsdelivr.net/npm/hanzi-writer@3/dist/hanzi-writer.min.js"

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<title>Stroke Order - {title}</title>
<script src="{cdn_url}"></script>
<style>
  body {{
    font-family: -apple-system, "Segoe UI", "Noto Sans", "Noto Sans SC", sans-serif;
    background: #111418;
    color: #eee;
    margin: 0;
    padding: 24px;
  }}
  h1 {{ font-size: 18px; font-weight: 500; color: #9aa4b2; margin-bottom: 20px; }}
  .grid {{
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
  }}
  .card {{
    background: #1a1e24;
    border-radius: 12px;
    padding: 16px;
    text-align: center;
    width: {size}px;
  }}
  .target {{
    width: {size}px;
    height: {size}px;
    background: #fff;
    border-radius: 8px;
    background-image:
      linear-gradient(#e5e5e5 1px, transparent 1px),
      linear-gradient(90deg, #e5e5e5 1px, transparent 1px);
    background-size: 50% 50%;
    background-position: -1px -1px;
  }}
  .char-label {{ margin-top: 10px; font-size: 22px; }}
  .status {{ margin-top: 4px; font-size: 12px; color: #7c8798; min-height: 16px; }}
  .buttons {{ margin-top: 10px; display: flex; gap: 8px; justify-content: center; flex-wrap: wrap; }}
  button {{
    background: #2b3038;
    color: #eee;
    border: none;
    border-radius: 6px;
    padding: 6px 10px;
    font-size: 12px;
    cursor: pointer;
  }}
  button:hover {{ background: #3a4048; }}
  .error {{ color: #e06060; font-size: 12px; margin-top: 8px; }}
</style>
</head>
<body>
<h1>Stroke order ({count} chu) &mdash; che do: {mode}</h1>
<div class="grid" id="grid"></div>

<script>
const CHARACTERS = {characters_json};
const MODE = "{mode}";
const LOOP = {loop_json};
const STROKE_DELAY = {delay};
const CHARSET = "{charset}";
const SIZE = {size};

// hanzi-writer-data mac dinh tren CDN chua ca chu gian the (simplified)
// va nhieu chu phon the pho bien (theo bo du lieu make-me-a-hanzi /
// cjk-vi). Neu mot ky tu khong co du lieu net (vi du chu qua hiem),
// hanzi-writer se bao loi qua callback onLoadCharDataError o duoi.
const charDataUrl = (char) =>
  `https://cdn.jsdelivr.net/npm/hanzi-writer-data@latest/${{encodeURIComponent(char)}}.json`;

const grid = document.getElementById("grid");

CHARACTERS.forEach((char, idx) => {{
  const card = document.createElement("div");
  card.className = "card";

  const target = document.createElement("div");
  target.className = "target";
  target.id = `target-${{idx}}`;
  target.style.width = SIZE + "px";
  target.style.height = SIZE + "px";

  const label = document.createElement("div");
  label.className = "char-label";
  label.textContent = char;

  const status = document.createElement("div");
  status.className = "status";
  status.id = `status-${{idx}}`;
  status.textContent = "Dang tai du lieu net...";

  const buttons = document.createElement("div");
  buttons.className = "buttons";

  const btnAnimate = document.createElement("button");
  btnAnimate.textContent = "Xem lai (Animate)";
  const btnQuiz = document.createElement("button");
  btnQuiz.textContent = "Do vui (Quiz)";
  const btnOutline = document.createElement("button");
  btnOutline.textContent = "Hien/An khung net";

  buttons.append(btnAnimate, btnQuiz, btnOutline);
  card.append(target, label, status, buttons);
  grid.appendChild(card);

  const writer = HanziWriter.create(target.id, char, {{
    width: SIZE,
    height: SIZE,
    padding: 12,
    strokeAnimationSpeed: 1,
    delayBetweenStrokes: STROKE_DELAY,
    showOutline: true,
    charDataLoader: (c, onComplete) => {{
      fetch(charDataUrl(c))
        .then((res) => {{
          if (!res.ok) throw new Error("HTTP " + res.status);
          return res.json();
        }})
        .then(onComplete)
        .catch((err) => {{
          status.textContent = `Khong tim thay du lieu net cho "${{c}}"`;
          status.classList.add("error");
        }});
    }},
    onLoadCharDataSuccess: (data) => {{
      status.textContent = `${{data.strokes.length}} net`;
    }},
    onLoadCharDataError: () => {{
      status.textContent = `Loi tai du lieu net cho "${{char}}"`;
      status.classList.add("error");
    }},
  }});

  const runAnimation = () => {{
    writer.hideCharacter();
    if (LOOP) {{
      writer.loopCharacterAnimation();
    }} else {{
      writer.animateCharacter();
    }}
  }};

  const runQuiz = () => {{
    writer.quiz({{
      onComplete: (summary) => {{
        status.textContent = `Hoan thanh! So lan sai: ${{summary.totalMistakes}}`;
      }},
      onCorrectStroke: (strokeData) => {{
        status.textContent = `Net ${{strokeData.strokeNum + 1}}/${{strokeData.strokesRemaining + strokeData.strokeNum + 1}} dung`;
      }},
      onMistake: () => {{
        status.textContent = "Sai net, thu lai...";
      }},
    }});
  }};

  btnAnimate.addEventListener("click", runAnimation);
  btnQuiz.addEventListener("click", runQuiz);
  btnOutline.addEventListener("click", () => {{
    target.classList.toggle("no-outline");
    writer.updateColor("outline", target.classList.contains("no-outline") ? "#ffffff" : "#dddddd");
  }});

  // Hanh dong mac dinh khi trang vua tai xong
  if (MODE === "animate") {{
    writer.showOutline();
    setTimeout(runAnimation, 300 + idx * 200);
  }} else if (MODE === "quiz") {{
    writer.hideCharacter();
    setTimeout(runQuiz, 300 + idx * 200);
  }} else {{
    // "both": hien khung net, cho nguoi dung tu bam nut
    writer.showOutline();
  }}
}});
</script>
</body>
</html>
"""


def parse_characters(raw_args):
    """
    Nhan danh sach argument tu dong lenh (moi phan tu co the la 1 chu
    hoac ca mot chuoi nhieu chu) va tach thanh danh sach tung chu Han
    rieng le, loai bo khoang trang / dau cau khong phai chu Han co ban.
    """
    chars = []
    for chunk in raw_args:
        for ch in chunk:
            if ch.strip() == "":
                continue
            if ch not in chars:
                chars.append(ch)
    return chars


def main():
    parser = argparse.ArgumentParser(
        description="Sinh HTML animate/quiz thu tu net viet chu Han bang hanzi-writer."
    )
    parser.add_argument(
        "characters",
        nargs="+",
        help="Mot hoac nhieu chu Han, hoac mot chuoi nhieu chu (vi du: 想 hoac 你好吗)",
    )
    parser.add_argument(
        "--output", "-o", default="stroke_order.html", help="Duong dan file HTML output"
    )
    parser.add_argument(
        "--mode",
        choices=["animate", "quiz", "both"],
        default="both",
        help="animate: tu dong phat hoat hoa | quiz: che do do vui viet chu | both: hien khung net, nguoi dung tu chon nut (mac dinh)",
    )
    parser.add_argument(
        "--loop", action="store_true", help="Lap lai hoat hoa lien tuc (chi ap dung mode=animate)"
    )
    parser.add_argument(
        "--delay", type=int, default=800, help="Do tre giua cac net (ms), mac dinh 800"
    )
    parser.add_argument(
        "--size", type=int, default=200, help="Kich thuoc moi o chu (px), mac dinh 200"
    )
    parser.add_argument(
        "--charset",
        choices=["auto", "simplified", "traditional"],
        default="auto",
        help="Chi de ghi chu trong tieu de HTML; du lieu net van lay theo dung ky tu Unicode duoc truyen vao",
    )

    args = parser.parse_args()
    characters = parse_characters(args.characters)

    if not characters:
        print("Khong tim thay chu Han hop le trong tham so dau vao.", file=sys.stderr)
        sys.exit(1)

    html = HTML_TEMPLATE.format(
        title=" ".join(characters),
        cdn_url=HANZI_WRITER_CDN,
        size=args.size,
        count=len(characters),
        mode=args.mode,
        characters_json=json.dumps(characters, ensure_ascii=False),
        loop_json=json.dumps(bool(args.loop)),
        delay=args.delay,
        charset=args.charset,
    )

    out_path = Path(args.output)
    out_path.write_text(html, encoding="utf-8")
    print(f"Da tao file: {out_path.resolve()}")
    print(f"So chu: {len(characters)} -> {' '.join(characters)}")
    print("Mo file nay bang trinh duyet (co ket noi Internet) de xem hoat hoa net viet.")


if __name__ == "__main__":
    main()
