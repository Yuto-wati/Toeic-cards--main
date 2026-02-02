from __future__ import annotations

import csv
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple


# ======= 設定 =======
PROJECT_DIR = Path(__file__).resolve().parent
CSV_PATH = PROJECT_DIR / "cards.csv"
TEMPLATE_PATH = PROJECT_DIR / "template_slide.html"
OUT_DIR = PROJECT_DIR / "out"

# ルール（必要なら調整）
MAX_LINES_MAIN = 3
MAX_CHARS_PER_LINE = 18  # 全角目安（厳密ではなく“検知用”）
MAX_EMOJI_PER_SLIDE = 1

SLIDE_SPECS = [
    ("01_hook", "Slide 1｜Hook"),
    ("02_core", "Slide 2｜コアイメージ"),
    ("03_meaning", "Slide 3｜基本の意味"),
    ("04_usage", "Slide 4｜実用イメージ"),
    ("05_example", "Slide 5｜例文"),
    ("06_summary", "Slide 6｜まとめ"),
]


# ======= ユーティリティ =======
EMOJI_REGEX = re.compile(
    "[\U0001F300-\U0001FAFF\U00002700-\U000027BF\U00002600-\U000026FF]"
)

def count_emojis(s: str) -> int:
    return len(EMOJI_REGEX.findall(s or ""))

def visual_len(s: str) -> int:
    """
    全角/半角の厳密計算は環境依存になりがちなので、
    まずは“ざっくり長さ”で検知する用。
    """
    return len(s or "")

def apply_emphasis(text: str) -> str:
    """
    【強調】を <span class="em">強調</span> に変換
    """
    if not text:
        return ""
    # 入れ子は想定しない（シンプル運用）
    return re.sub(r"【(.+?)】", r'<span class="em">\1</span>', text)

def split_usage_points(raw: str) -> List[str]:
    if not raw:
        return []
    parts = [p.strip() for p in raw.split("｜")]
    return [p for p in parts if p]


# ======= データモデル =======
@dataclass
class CardRow:
    id: str
    phrase: str
    meaning: str
    core_image: str
    usage_points: str
    example_en: str
    example_jp: str
    cta: str

    @staticmethod
    def from_dict(d: Dict[str, str]) -> "CardRow":
        required = ["id", "phrase", "meaning", "core_image", "usage_points", "example_en", "example_jp", "cta"]
        missing = [k for k in required if k not in d]
        if missing:
            raise ValueError(f"CSV columns missing: {missing}")
        return CardRow(**{k: (d.get(k) or "").strip() for k in required})


# ======= スライド文生成（音声なしで完結する想定） =======
def build_slide_texts(row: CardRow) -> Dict[str, Dict[str, str]]:
    """
    6枚分の表示テキスト（MAIN/SUB/NOTE）を作る。
    句動詞用に最適化。
    """
    # Hook：短く刺す
    # 句動詞と意味を短く表示
    hook_main = f'{row.phrase}\n=\n{row.meaning}'
    hook_sub = "だけだと思ってない？"
    hook_note = "使い方で意味が変わる"

    # Core: コアイメージをそのまま表示
    core_main = row.core_image
    core_sub = "コアイメージ"
    core_note = "軸が分かると暗記が減る"

    # Meaning: 基本の意味
    # 句動詞を大きく、意味を下に
    meaning_main = row.phrase
    meaning_sub = row.meaning
    meaning_note = ""

    # Usage: 実用イメージ
    # usage_pointsをそのまま使用
    usage_main = row.usage_points if row.usage_points else "実用場面"
    usage_sub = ""
    usage_note = "場面が見えると覚えやすい"

    # Example: 例文
    example_main = row.example_en
    example_sub = row.example_jp
    example_note = ""

    # Summary: まとめ
    # 句動詞と意味を再確認
    summary_main = f'{row.phrase}\n=\n{row.meaning}'
    summary_sub = ""
    summary_note = row.cta or "保存して復習"

    return {
        "01_hook": {"BADGE": "HOOK", "MAIN": hook_main, "SUB": hook_sub, "NOTE": hook_note},
        "02_core": {"BADGE": "CORE", "MAIN": core_main, "SUB": core_sub, "NOTE": core_note},
        "03_meaning": {"BADGE": "MEANING", "MAIN": meaning_main, "SUB": meaning_sub, "NOTE": meaning_note},
        "04_usage": {"BADGE": "USAGE", "MAIN": usage_main, "SUB": usage_sub, "NOTE": usage_note},
        "05_example": {"BADGE": "EXAMPLE", "MAIN": example_main, "SUB": example_sub, "NOTE": example_note},
        "06_summary": {"BADGE": "SUMMARY", "MAIN": summary_main, "SUB": summary_sub, "NOTE": summary_note},
    }



# ======= 検証 =======
def validate_slide(slide_key: str, block: Dict[str, str]) -> List[str]:
    errs: List[str] = []

    main = block.get("MAIN", "")
    # MAINの行数チェック
    main_lines = [ln for ln in (main or "").split("\n") if ln.strip() != ""]
    if len(main_lines) > MAX_LINES_MAIN:
        errs.append(f"{slide_key}: MAIN lines > {MAX_LINES_MAIN} ({len(main_lines)})")

    # 1行の長さチェック（目安）
    too_long = [ln for ln in main_lines if visual_len(ln) > MAX_CHARS_PER_LINE]
    if too_long:
        errs.append(f"{slide_key}: MAIN line too long (>{MAX_CHARS_PER_LINE}): {too_long[0]}")

    # 絵文字数（MAIN+SUB+NOTE合算）
    emoji_total = count_emojis(main) + count_emojis(block.get("SUB", "")) + count_emojis(block.get("NOTE", ""))
    if emoji_total > MAX_EMOJI_PER_SLIDE:
        errs.append(f"{slide_key}: emoji > {MAX_EMOJI_PER_SLIDE} ({emoji_total})")

    return errs


# ======= HTML生成 =======
def render_template(template: str, title: str, values: Dict[str, str]) -> str:
    html = template
    html = html.replace("{{TITLE}}", title)

    # 強調のHTML変換
    values2 = {k: apply_emphasis(v) for k, v in values.items()}

    for key in ["BADGE", "MAIN", "SUB", "NOTE"]:
        html = html.replace(f"{{{{{key}}}}}", values2.get(key, ""))

    return html


def ensure_out_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def main() -> None:
    if not CSV_PATH.exists():
        raise FileNotFoundError(f"cards.csv not found: {CSV_PATH}")
    if not TEMPLATE_PATH.exists():
        raise FileNotFoundError(f"template_slide.html not found: {TEMPLATE_PATH}")

    template = TEMPLATE_PATH.read_text(encoding="utf-8")

    ensure_out_dir(OUT_DIR)

    with CSV_PATH.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        rows = [CardRow.from_dict(d) for d in reader]

    all_errors: List[Tuple[str, str]] = []

    for row in rows:
        pack = build_slide_texts(row)
        item_dir = OUT_DIR / row.id
        ensure_out_dir(item_dir)

        for slide_key, slide_title in SLIDE_SPECS:
            if slide_key not in pack:
                all_errors.append((row.id, f"Missing slide content: {slide_key}"))
                continue

            block = pack[slide_key]
            errs = validate_slide(slide_key, block)
            for e in errs:
                all_errors.append((row.id, e))

            out_html = render_template(
                template=template,
                title=f"{row.id} {slide_title}",
                values=block,
            )

            out_path = item_dir / f"{slide_key}.html"
            out_path.write_text(out_html, encoding="utf-8")

    # レポート
    if all_errors:
        print("=== VALIDATION WARNINGS ===")
        for cid, msg in all_errors:
            print(f"[{cid}] {msg}")
        print("=== END ===")
    else:
        print("OK: generated without warnings.")

    print(f"Output dir: {OUT_DIR}")


if __name__ == "__main__":
    main()
