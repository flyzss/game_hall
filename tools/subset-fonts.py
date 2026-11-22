"""字体子集化：只保留页面里实际用到的字，生成 fonts/ZCOOLXiaoWei-subset.woff。

用法（在项目根目录）：
    python tools/subset-fonts.py

修改 index.html 的文字后需要重新运行，否则新字会回退成系统字体。
依赖：pip install fonttools
"""
import pathlib
import re
import shutil

from fontTools import subset

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "tools" / "fontsrc"
OUT = ROOT / "fonts"


def used_chars() -> str:
    text = (ROOT / "index.html").read_text(encoding="utf-8")
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    ascii_ = "".join(chr(c) for c in range(0x20, 0x7F))
    return "".join(sorted(set(re.findall(r"[^\x00-\x7f]", text)) | set(ascii_)))


def main() -> None:
    OUT.mkdir(exist_ok=True)
    opts = subset.Options()
    opts.flavor = "woff"
    opts.layout_features = ["*"]
    font = subset.load_font(str(SRC / "ZCOOLXiaoWei-Regular.ttf"), opts)
    sub = subset.Subsetter(opts)
    sub.populate(text=used_chars())
    sub.subset(font)
    target = OUT / "ZCOOLXiaoWei-subset.woff"
    subset.save_font(font, str(target), opts)
    shutil.copy(SRC / "OFL-zcoolxiaowei.txt", OUT / "OFL-zcoolxiaowei.txt")
    print(f"{target.name}: {target.stat().st_size / 1024:.1f} KB")


if __name__ == "__main__":
    main()
