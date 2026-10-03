"""index.html から WordPress 用ファイルを生成する: python3 wordpress/build.py"""
import re
from pathlib import Path

root = Path(__file__).resolve().parent.parent
src = (root / "index.html").read_text()
url_example = 'const SIGNUP_URL = "#"; // 例: "https://note.com/xxxx/membership"'

# 1) ページテンプレート（子テーマに置く）
img = "<?php echo esc_url( get_stylesheet_directory_uri() . '/cinelish/hero.webp' ); ?>"
t = src.replace('src="hero.webp"', f'src="{img}"').replace('content="hero.webp"', f'content="{img}"')
t = re.sub(r'src="img/([\w-]+\.jpg)"', lambda m: 'src="<?php echo esc_url( get_stylesheet_directory_uri() . \'/cinelish/img/' + m.group(1) + '\' ); ?>"', t)
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
body = body.replace('src="hero.webp"', 'src="【画像URL：hero.webp】"').replace('const SIGNUP_URL = "#";', url_example)
body = re.sub(r'src="img/([\w-]+\.jpg)"', r'src="【画像URL：\1】"', body)

# WordPressのメディアにアップ済みの画像URL（TCD用HTMLにそのまま入れる）
IMAGE_URLS = {
    "hero.webp": "https://www.cinelish-japan.tech/wp-content/uploads/2026/09/Premium-Subscription-Thumbnail.jpg",
    "prologue.jpg": "https://www.cinelish-japan.tech/wp-content/uploads/2026/10/18606FC4-C246-4C80-AB93-40FA6263E31B.jpg",
    "passive.jpg": "https://www.cinelish-japan.tech/wp-content/uploads/2026/10/laura-brain-YWQcSnBvmk0-unsplash-scaled.jpg",
    "active.jpg": "https://www.cinelish-japan.tech/wp-content/uploads/2026/10/jaeyoung-geoffrey-kang-V8TJgSmkJ0-unsplash-scaled.jpg",
    "note.jpg": "https://www.cinelish-japan.tech/wp-content/uploads/2026/10/aaron-burden-CKlHKtCJZKk-unsplash-scaled.jpg",
    "epilogue.jpg": "https://www.cinelish-japan.tech/wp-content/uploads/2026/10/valeriia-fokina-m0TID6J9Ahg-unsplash-scaled.jpg",
}
tcd_body = body
for name, url in IMAGE_URLS.items():
    tcd_body = tcd_body.replace("【画像URL：" + name + "】", url)
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
    "     ・画像URLは入力済み\n"
    '     ・codocの登録ボタン入り（チケットの中）。ほかの登録ボタンはチケットまで移動します\n'
    "     ※ エディタの自動整形で崩れないよう、あえて1行にしています（Ctrl+F で検索して書き換えてください） -->\n"
    + one_line(fonts + tcd_body) + "\n"
)

# 4) TCDテーマ用：CSS込みのHTML1枚（追加CSSが効かない環境向け）
mini = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
mini = re.sub(r"\s*\n\s*", " ", mini)
mini = re.sub(r"\s*([{};,>])\s*", r"\1", mini).strip()
(tcd / "cinelish-lp-all-in-one.html").write_text(
    "<!-- Cine Lish プレミアム LP（TCDテーマ・CSS込み版）\n"
    "     これ1つを固定ページ本文の「カスタムHTML」ブロック（クラシックエディタなら「テキスト」タブ）に貼るだけ。追加CSSは不要。\n"
    "     ・画像URLは入力済み\n"
    '     ・SIGNUP_URL = "#" の # → 登録ページのURL -->\n'
    + one_line(fonts + "<style>" + mini + "</style>" + tcd_body) + "\n"
)

# 5) TCDテーマ用：1行に圧縮したCSS（コピー漏れを防ぐため）
(tcd / "cinelish-lp.min.css").write_text(mini + "\n")

# 6) プレビュー用ページ（Artifact で公開して、スマホ・PCで確認しながら調整する用）
#    実サイト（TCD CODE.）の本文幅 690px を再現。プレビューではフェードインを切って最初から全部見せる。
pv_head = src[src.index("<title>"):src.index("</head>")]
pv_head = pv_head.replace('<meta property="og:image" content="hero.webp">\n', "")
CODOC_MOCK = '<div style="display:inline-block;padding:16px 36px;border-radius:6px;background:#1b1917;color:#f4eee3;font:700 14px/1.4 serif;letter-spacing:.12em">購読する（codocのボタン見本）</div>'
pv_body = src[src.index('<div id="cinelish-lp">'):src.index("</body>")]
pv_body = re.sub(r'<script src="https://codoc.jp[^<]*</script>', "", pv_body)
pv_body = re.sub(r'<div id="codoc-subscription-tuq1lf60NQ" class="codoc-subscriptions" ?></div>', lambda m: CODOC_MOCK, pv_body)
_unused = (
    '<div style="display:inline-block;padding:16px 36px;border-radius:6px;background:#1b1917;color:#f4eee3;font:700 14px/1.4 serif;letter-spacing:.12em">購読する（codocのボタン見本）</div>')
frame = """<style>
  /* プレビュー枠：実サイトの本文幅（690px）を再現 */
  html, body { background: #ffffff; color: #262220; }
  body { padding-block: 0; padding-inline: 20px; }
  .pv-frame { max-width: 690px; margin: 0 auto; }
  #cinelish-lp.cl-js .cl-reveal { opacity: 1; transform: none; }
  .pv-note { max-width: 690px; margin: 0 auto; padding: 14px 0; font: 12px/1.6 system-ui, sans-serif; color: #7a736b; letter-spacing: .04em; }
</style>
"""
pv = (pv_head + frame + '<p class="pv-note">プレビュー（実サイトの本文幅 690px で表示）</p>\n<div class="pv-frame">\n'
      + pv_body + "</div>\n")
(root / "preview").mkdir(exist_ok=True)
(root / "preview" / "index.html").write_text(pv)

# 7) 登録ページ（codocの登録ボタン入り）
reg = (root / "register" / "index.html").read_text()
reg_css = reg[reg.index("<style>") + len("<style>"):reg.index("</style>")]
reg_css = reg_css.replace("#cinelish-reg", "#cinelish-reg#cinelish-reg")
reg_mini = re.sub(r"/\*.*?\*/", "", reg_css, flags=re.S)
reg_mini = re.sub(r"\s*\n\s*", " ", reg_mini)
reg_mini = re.sub(r"\s*([{};,>])\s*", r"\1", reg_mini).strip()
(tcd / "register.min.css").write_text(reg_mini + "\n")
reg_fonts = reg[reg.index('<link rel="preconnect"'):reg.index("<style>")].strip()
reg_body = reg[reg.index('<div id="cinelish-reg">'):reg.index("</body>")].strip()
(tcd / "register.html").write_text(
    "<!-- Cine Lish プレミアム 登録ページ用HTML（TCDテーマ）\n"
    "     貼り付け先：登録ページ（/register/）本文の「テキスト」タブ（またはカスタムHTMLブロック）\n"
    "     CSSは register.min.css を、このページのカスタムCSS欄へ\n"
    "     ※ 1行にしています。codocの登録ボタンのコードも入っています -->\n"
    + one_line(reg_fonts + reg_body) + "\n"
)
# 登録ページのプレビュー（codocのボタンは表示できないので見本の枠を置く）
mock = ('<div style="display:inline-block;padding:16px 36px;border-radius:6px;'
        'background:linear-gradient(90deg,#ff6b6b,#f7b733,#4ecdc4,#5567ff);color:#fff;'
        'font:700 15px/1.4 system-ui,sans-serif;letter-spacing:.04em">月額500円で購読する（codocのボタン見本）</div>')
reg_pv = reg[reg.index("<title>"):reg.index("</head>")] + """<style>
  html, body { background: #ffffff; color: #262220; }
  body { padding-block: 0; padding-inline: 20px; }
  .pv-frame { max-width: 690px; margin: 0 auto; }
  .pv-note { max-width: 690px; margin: 0 auto; padding: 14px 0; font: 12px/1.6 system-ui, sans-serif; color: #7a736b; }
</style>
<p class="pv-note">プレビュー（登録ページ／codocのボタンは見本を表示）</p>
<div class="pv-frame">
""" + reg_body.replace('<div id="codoc-subscription-tuq1lf60NQ" class="codoc-subscriptions"></div>', mock) + "</div>\n"
reg_pv = re.sub(r'<script src="https://codoc.jp[^<]*</script>', "", reg_pv)
(root / "register" / "preview.html").write_text(reg_pv)
