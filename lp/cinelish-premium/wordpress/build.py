"""index.html から WordPress 用ファイルを生成する: python3 wordpress/build.py"""
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
