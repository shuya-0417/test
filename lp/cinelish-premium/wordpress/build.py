"""index.html から WordPress 用ファイルを生成する: python3 wordpress/build.py"""
import re
from pathlib import Path

root = Path(__file__).resolve().parent.parent
src = (root / "index.html").read_text()
url_example = 'const SIGNUP_URL = "#"; // 例: "https://note.com/xxxx/membership"'

# 1) ページテンプレート（子テーマに置く）
img = "<?php echo esc_url( get_stylesheet_directory_uri() . '/cinelish/hero.webp' ); ?>"
t = src.replace('src="hero.webp"', f'src="{img}"').replace('content="hero.webp"', f'content="{img}"')
t = t.replace('<!doctype html>\n<html lang="ja">', '''<?php
/**
 * Template Name: Cine Lish プレミアム LP
 *
 * 使い方：子テーマ直下にこのファイルを置き、画像を「子テーマ/cinelish/hero.webp」に置く。
 * 固定ページの「テンプレート」でこのLPを選ぶ。
 * CSSはすべて #cinelish-lp の内側だけに効くので、サイトの他のページや設定には影響しません。
 */
?><!doctype html>
<html <?php language_attributes(); ?>>''')
t = t.replace("<title>Cine Lish プレミアム</title>\n", "")
t = t.replace("<style>", "<?php wp_head(); ?>\n<style>", 1)
t = t.replace("<body>", "<body <?php body_class(); ?>>\n<?php wp_body_open(); ?>", 1)
t = t.replace("</body>", "<?php wp_footer(); ?>\n</body>")
t = t.replace('const SIGNUP_URL = "#";', url_example)
(root / "wordpress" / "page-cinelish-premium.php").write_text(t)

# 2) カスタムHTMLブロック用（固定ページ本文に貼る）
head = src[src.index('<link rel="preconnect"'):src.index("</head>")].strip()
body = src[src.index('<div id="cinelish-lp">'):src.index("</body>")].strip()
body = body.replace('src="hero.webp"', 'src="【ここに画像URL】"').replace('const SIGNUP_URL = "#";', url_example)
(root / "wordpress" / "custom-html-block.html").write_text(
    "<!-- Cine Lish プレミアム LP：WordPressの「カスタムHTML」ブロックにこのファイルの中身を丸ごと貼り付け -->\n"
    "<!-- 【ここに画像URL】を、メディアにアップした hero.webp のURLに置き換える -->\n"
    + head + "\n\n" + body + "\n"
)

def one_line(html):
    """クラシックエディタの自動整形（改行→<br>/<p>）で崩れないよう、1行にまとめる"""
    import re
    html = re.sub(r"<!--.*?-->", "", html, flags=re.S)
    # <script> 内のJS行コメントを /* */ に（1行にしても後ろのコードが消えないように）
    html = re.sub(r"<script>.*?</script>",
                  lambda m: re.sub(r"(?<![:\"])//\s*(.*?)$", r"/* \1 */", m.group(0), flags=re.M),
                  html, flags=re.S)
    html = re.sub(r"\s*\n\s*", " ", html)
    return re.sub(r">\s+<", "><", html).strip()


# 3) TCDテーマ用：CSS と HTML を分けて出力
#    TCDの本文用スタイル（#article .post_content p など）より確実に優先させるため、
#    セレクタを #cinelish-lp#cinelish-lp（IDを2回）にして詳細度を上げている。
tcd = root / "wordpress" / "tcd"
tcd.mkdir(exist_ok=True)
css = src[src.index("<style>") + len("<style>"):src.index("</style>")].strip("\n")
css = css.replace("#cinelish-lp", "#cinelish-lp#cinelish-lp")
css = "\n".join(line[2:] if line.startswith("  ") else line for line in css.split("\n"))
(tcd / "cinelish-lp.css").write_text(
    "/* Cine Lish プレミアム LP 用CSS（TCDテーマ）\n"
    " * 貼り付け先：外観 → カスタマイズ → 追加CSS（またはTCDの「カスタムCSS」欄）\n"
    " * すべて #cinelish-lp の内側だけに効くので、サイトの他の部分には影響しません。 */\n\n"
    + css + "\n"
)
fonts = src[src.index('<link rel="preconnect"'):src.index("<style>")].strip()
(tcd / "cinelish-lp.html").write_text(
    "<!-- Cine Lish プレミアム LP 用HTML（TCDテーマ）\n"
    "     貼り付け先：固定ページ本文の「カスタムHTML」ブロック（クラシックエディタなら「テキスト」タブ）\n"
    "     ・【ここに画像URL】→ メディアにアップした hero.webp のURL\n"
    '     ・SIGNUP_URL = "#" の # → 登録ページのURL\n'
    "     ※ エディタの自動整形で崩れないよう、あえて1行にしています（Ctrl+F で検索して書き換えてください） -->\n"
    + one_line(fonts + body) + "\n"
)

# 4) TCDテーマ用：CSS込みのHTML1枚（追加CSSが効かない環境向け）
mini = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
mini = re.sub(r"\s*\n\s*", " ", mini)
mini = re.sub(r"\s*([{};,>])\s*", r"\1", mini).strip()
(tcd / "cinelish-lp-all-in-one.html").write_text(
    "<!-- Cine Lish プレミアム LP（TCDテーマ・CSS込み版）\n"
    "     これ1つを固定ページ本文の「カスタムHTML」ブロック（クラシックエディタなら「テキスト」タブ）に貼るだけ。追加CSSは不要。\n"
    "     ・【ここに画像URL】→ メディアにアップした hero.webp のURL\n"
    '     ・SIGNUP_URL = "#" の # → 登録ページのURL -->\n'
    + one_line(fonts + "<style>" + mini + "</style>" + body) + "\n"
)

# 5) TCDテーマ用：1行に圧縮したCSS（コピー漏れを防ぐため）
(tcd / "cinelish-lp.min.css").write_text(mini + "\n")
