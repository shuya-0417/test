<?php
/**
 * Template Name: Cine Lish プレミアム LP
 *
 * 使い方：子テーマ直下にこのファイルを置き、画像を「子テーマ/cinelish/hero.webp」に置く。
 * 固定ページの「テンプレート」でこのLPを選ぶ。
 */
?><!doctype html>
<html <?php language_attributes(); ?>>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="『能動的に読む』時間で自分を取り戻す。走り続けるあなたが、折れないための場所。映画編集者Shuyaのエッセイを毎週お届けします。月額500円・いつでも解約OK。">
<meta property="og:title" content="Cine Lish プレミアム">
<meta property="og:description" content="『能動的に読む』時間で自分を取り戻す。走り続けるあなたが、折れないための場所。">
<meta property="og:image" content="<?php echo esc_url( get_stylesheet_directory_uri() . '/cinelish/hero.webp' ); ?>">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;1,500&family=Shippori+Mincho:wght@400;500;700&display=swap" rel="stylesheet">
<?php wp_head(); ?>
<style>
  :root {
    --bg: #f4f2ee;
    --bg-alt: #ebe8e2;
    --ink: #2b2724;
    --ink-soft: #5e5852;
    --ink-faint: #8d867e;
    --line: #d6d1c9;
    --brown: #4a2c22;
    --gold-1: #a8873a;
    --gold-2: #d9bf72;
    --gold-3: #f1e2b0;
    --dark: #1d1b19;
    --dark-ink: #e9e5de;
    --serif-en: "Cormorant Garamond", "Times New Roman", serif;
    --serif-ja: "Shippori Mincho", "Hiragino Mincho ProN", "Yu Mincho", serif;
  }

  * { box-sizing: border-box; margin: 0; padding: 0; }
  html { scroll-behavior: smooth; }
  body {
    background: var(--bg);
    color: var(--ink);
    font-family: var(--serif-ja);
    font-size: 16px;
    line-height: 2.1;
    letter-spacing: .06em;
    -webkit-font-smoothing: antialiased;
    overflow-x: hidden;
  }
  img { display: block; max-width: 100%; height: auto; }
  a { color: inherit; }

  .wrap { width: min(680px, 100% - 40px); margin-inline: auto; }

  .gold {
    background: linear-gradient(100deg, var(--gold-1) 0%, var(--gold-2) 45%, var(--gold-3) 70%, var(--gold-2) 100%);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
  }

  /* ---------- Hero ---------- */
  .hero { position: relative; background: #e9e8e5; }
  .hero img { width: 100%; max-width: 1440px; margin-inline: auto; }
  .hero::after {
    content: "";
    position: absolute; inset: auto 0 0 0; height: 18%;
    background: linear-gradient(to bottom, transparent, var(--bg));
    pointer-events: none;
  }
  .hero-copy { display: none; }

  /* ---------- Sections ---------- */
  section { padding: 120px 0; }
  .eyebrow {
    font-family: var(--serif-en);
    font-style: italic;
    font-size: 15px;
    letter-spacing: .25em;
    color: var(--ink-faint);
    text-align: center;
    margin-bottom: 18px;
  }
  .rule {
    width: 1px; height: 64px; margin: 0 auto 56px;
    background: linear-gradient(var(--line), transparent);
  }
  h2 {
    font-weight: 500;
    font-size: clamp(22px, 4.2vw, 30px);
    line-height: 1.8;
    letter-spacing: .12em;
    text-align: center;
    margin-bottom: 48px;
  }
  p + p { margin-top: 1.6em; }
  .center { text-align: center; }
  .soft { color: var(--ink-soft); }

  /* Intro questions */
  .questions p {
    font-size: clamp(18px, 3.4vw, 22px);
    text-align: center;
    line-height: 2;
  }

  .tag {
    display: block;
    width: fit-content;
    margin: 72px auto 0;
    padding: 10px 28px;
    border-top: 1px solid var(--line);
    border-bottom: 1px solid var(--line);
    font-size: 14px;
    letter-spacing: .3em;
    color: var(--ink-soft);
  }

  /* Contrast */
  .contrast { background: var(--bg-alt); }
  .pair {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1px;
    background: var(--line);
    border: 1px solid var(--line);
    margin: 56px 0;
  }
  .pair > div { background: var(--bg-alt); padding: 36px 28px; }
  .pair h3 {
    font-family: var(--serif-en);
    font-weight: 500;
    font-size: 26px;
    letter-spacing: .08em;
    margin-bottom: 4px;
  }
  .pair small { display: block; font-size: 13px; color: var(--ink-faint); margin-bottom: 18px; letter-spacing: .2em; }
  .pair p { font-size: 15px; line-height: 2; }
  .pair .passive { color: var(--ink-faint); }
  .pair .active h3 { color: var(--brown); }

  /* Statement */
  .statement {
    background: var(--dark);
    color: var(--dark-ink);
    text-align: center;
  }
  .statement .eyebrow { color: #8a837a; }
  .statement .big {
    font-size: clamp(22px, 4.6vw, 34px);
    line-height: 1.9;
    letter-spacing: .14em;
    margin-bottom: 48px;
  }
  .statement p { color: #bdb6ac; }

  /* Benefits */
  .benefits ol { list-style: none; border-top: 1px solid var(--line); }
  .benefits li {
    display: grid;
    grid-template-columns: 72px 1fr;
    gap: 8px 20px;
    padding: 40px 0;
    border-bottom: 1px solid var(--line);
  }
  .benefits .num {
    font-family: var(--serif-en);
    font-size: 44px;
    line-height: 1;
    color: var(--gold-1);
    font-style: italic;
  }
  .benefits h3 { font-weight: 500; font-size: 18px; line-height: 1.8; letter-spacing: .08em; }
  .benefits li p { grid-column: 2; font-size: 14px; color: var(--ink-soft); line-height: 1.9; }

  /* Price */
  .price-card {
    margin: 0 auto;
    max-width: 460px;
    padding: 56px 32px;
    text-align: center;
    border: 1px solid var(--line);
    background: #fbfaf8;
    position: relative;
  }
  .price-card::before {
    content: "";
    position: absolute; inset: 8px;
    border: 1px solid #ece8e1;
    pointer-events: none;
  }
  .price-card .name {
    font-family: var(--serif-en);
    font-size: 30px;
    color: var(--brown);
    letter-spacing: .06em;
    line-height: 1.4;
  }
  .price-card .name span { font-family: var(--serif-ja); font-size: 22px; margin-left: .3em; }
  .price {
    margin: 28px 0 8px;
    font-family: var(--serif-en);
    font-size: 64px;
    line-height: 1;
    letter-spacing: .02em;
  }
  .price small { font-family: var(--serif-ja); font-size: 16px; color: var(--ink-soft); margin-left: 4px; }
  .price-card ul { list-style: none; margin: 24px 0 36px; font-size: 14px; color: var(--ink-soft); line-height: 2.2; }

  /* CTA */
  .cta {
    position: relative;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 14px;
    min-width: min(100%, 340px);
    padding: 20px 40px;
    background: var(--dark);
    color: #f5efe2;
    text-decoration: none;
    font-size: 16px;
    letter-spacing: .16em;
    border: 1px solid var(--dark);
    transition: background .4s ease, color .4s ease;
    overflow: hidden;
  }
  .cta::after { content: "→"; font-family: var(--serif-en); transition: transform .4s ease; }
  .cta:hover { background: transparent; color: var(--dark); }
  .cta:hover::after { transform: translateX(4px); }
  .cta:focus-visible { outline: 2px solid var(--gold-1); outline-offset: 4px; }
  .cta-block { text-align: center; margin-top: 56px; }
  .cta-note { margin-top: 14px; font-size: 12px; color: var(--ink-faint); letter-spacing: .14em; }

  /* Closing */
  .closing {
    background: linear-gradient(var(--bg), var(--bg-alt));
    text-align: center;
  }
  .closing .lead {
    font-size: clamp(20px, 4vw, 28px);
    line-height: 2;
    letter-spacing: .14em;
    margin: 40px 0;
  }
  .closing .wait { font-size: 18px; letter-spacing: .3em; margin-top: 48px; }

  footer {
    padding: 48px 0 120px;
    text-align: center;
    font-family: var(--serif-en);
    font-size: 13px;
    letter-spacing: .2em;
    color: var(--ink-faint);
  }

  /* Sticky CTA (mobile) */
  .sticky {
    position: fixed; left: 0; right: 0; bottom: 0;
    padding: 12px 16px calc(12px + env(safe-area-inset-bottom));
    background: rgba(244,242,238,.92);
    backdrop-filter: blur(8px);
    border-top: 1px solid var(--line);
    transform: translateY(100%);
    transition: transform .5s ease;
    z-index: 10;
    display: none;
  }
  .sticky.show { transform: translateY(0); }
  .sticky .cta { width: 100%; padding: 16px 20px; font-size: 15px; }

  /* Reveal */
  .reveal { opacity: 0; transform: translateY(16px); transition: opacity 1.2s ease, transform 1.2s ease; }
  .reveal.in { opacity: 1; transform: none; }
  @media (prefers-reduced-motion: reduce) {
    .reveal { opacity: 1; transform: none; transition: none; }
    html { scroll-behavior: auto; }
  }

  @media (max-width: 640px) {
    body { font-size: 15px; line-height: 2; }
    section { padding: 88px 0; }
    .wrap { width: calc(100% - 32px); }
    .pair { grid-template-columns: 1fr; }
    .benefits li { grid-template-columns: 52px 1fr; padding: 32px 0; }
    .benefits .num { font-size: 36px; }
    .sticky { display: block; }
    .br-pc { display: none; }
  }
  @media (min-width: 641px) { .br-sp { display: none; } }
</style>
</head>
<body <?php body_class(); ?>>
<?php wp_body_open(); ?>

<header class="hero">
  <img src="<?php echo esc_url( get_stylesheet_directory_uri() . '/cinelish/hero.webp' ); ?>" width="1430" height="1046"
       alt="Cine Lish プレミアム ―『能動的に読む』時間で自分を取り戻す。走り続けるあなたが、折れないための場所。">
</header>

<main>

  <!-- 問いかけ -->
  <section class="questions">
    <div class="wrap">
      <p class="reveal">忙しい毎日の中で、<br class="br-sp">自分自身を見失っていませんか。</p>
      <p class="reveal">日々、自分の一日の行動に<br class="br-sp">納得できていますか？</p>
      <span class="tag reveal">CineLish プレミアム会員</span>
    </div>
  </section>

  <!-- 受け身 vs 能動 -->
  <section class="contrast">
    <div class="wrap">
      <p class="eyebrow reveal">Passive / Active</p>
      <h2 class="reveal">時間が、<br class="br-sp">溶けていませんか。</h2>
      <p class="reveal">夢を追っているはずなのに、気づけば動画やSNSのリールを流し見して、時間が溶けていた…。</p>

      <div class="pair reveal">
        <div class="passive">
          <h3>Passive</h3>
          <small>受け身で眺める</small>
          <p>流れてくるものを、ただ眺めるだけの時間。あとに何も残らないことが多い。</p>
        </div>
        <div class="active">
          <h3>Active</h3>
          <small>能動的に読む</small>
          <p>自分の意思で読み、考える時間。人が本来の力を発揮するのは、この瞬間です。</p>
        </div>
      </div>

      <p class="reveal center soft">人が本来力を発揮するのは、<br class="br-sp">自分の意思で、<br class="br-pc">能動的に行動しているときです。</p>
    </div>
  </section>

  <!-- ステートメント -->
  <section class="statement">
    <div class="wrap">
      <p class="eyebrow reveal">Concept</p>
      <p class="big reveal">あえて、<br>「文章を能動的に読む」<br>体験を。</p>
      <p class="reveal">映画や日々の話をきっかけに、<br>自分のペースで読み、考え、自分に立ち返る。</p>
      <p class="reveal">その時間が、流し見では得られないものを残し、<br class="br-pc">夢を追うあなたが前を向くきっかけになります。</p>
      <p class="reveal">夢の途中で立ち止まりたくなったときにこそ、<br class="br-pc">ぴったりの場所です。</p>
    </div>
  </section>

  <!-- 受け取れるもの -->
  <section class="benefits">
    <div class="wrap">
      <p class="eyebrow reveal">What you receive</p>
      <h2 class="reveal">CineLish プレミアムで<br>受け取れるもの</h2>
      <ol>
        <li class="reveal">
          <span class="num">01</span>
          <h3>月3〜4本、映画編集者Shuyaの<br class="br-pc">気づきと発見を深めるエッセイ</h3>
          <p>映画や日常から生まれた、余韻に浸る言葉と想い。</p>
        </li>
        <li class="reveal">
          <span class="num">02</span>
          <h3>「能動的に読む」体験と、<br class="br-sp">自分に還る時間</h3>
          <p>動画の流し見ではなく、自分のペースで読み、考える時間を。</p>
        </li>
        <li class="reveal">
          <span class="num">03</span>
          <h3>夢の途中で立ち止まりたくなったときに、<br class="br-pc">戻ってこられる場所</h3>
          <p>走り続けて自分を見失いそうなとき、ここに戻れば、また自分を取り戻せる。</p>
        </li>
        <li class="reveal">
          <span class="num">04</span>
          <h3>会員向けのキャンペーン・イベント・<br class="br-pc">コミュニティ企画</h3>
          <p>今後、会員の皆さまに向けた企画も予定しています。</p>
        </li>
      </ol>
    </div>
  </section>

  <!-- 料金 -->
  <section id="join" style="padding-top:0">
    <div class="wrap">
      <div class="price-card reveal">
        <p class="name">Cine Lish<span class="gold">プレミアム</span></p>
        <p class="price">¥500<small>／月</small></p>
        <ul>
          <li>毎週1本程度お届け</li>
          <li>いつでも解約OK</li>
        </ul>
        <a class="cta js-signup" href="#">プレミアム会員に登録する</a>
      </div>
    </div>
  </section>

  <!-- クロージング -->
  <section class="closing">
    <div class="wrap">
      <div class="rule reveal"></div>
      <p class="reveal soft">走り続けて自分を見失いそうなとき、<br>ここに戻ってくれば、また自分を取り戻せる。<br>そんな余白のような場所でありたいと思っています。</p>
      <p class="lead reveal">余韻に還り、夢を思い出す。<br>走り続けるあなたが、<br class="br-sp">折れないための場所。</p>
      <p class="wait reveal">あなたを待っています。</p>
      <div class="cta-block reveal">
        <a class="cta js-signup" href="#">Cine Lish プレミアムに登録する</a>
        <p class="cta-note">月額500円・いつでも解約OK</p>
      </div>
    </div>
  </section>

</main>

<footer>&copy; Cine Lish</footer>

<div class="sticky" aria-hidden="true">
  <a class="cta js-signup" href="#" tabindex="-1">プレミアム会員に登録する</a>
</div>

<script>
  // ▼ 登録ページのURLをここに入れてください（全ボタンに反映されます）
  const SIGNUP_URL = "#"; // 例: "https://note.com/xxxx/membership"

  document.querySelectorAll(".js-signup").forEach(a => {
    a.href = SIGNUP_URL;
    if (/^https?:/.test(SIGNUP_URL)) { a.target = "_blank"; a.rel = "noopener"; }
  });

  // スクロールでふわっと表示
  const io = new IntersectionObserver(entries => {
    entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); } });
  }, { threshold: 0.15, rootMargin: "0px 0px -40px 0px" });
  document.querySelectorAll(".reveal").forEach(el => io.observe(el));

  // スマホ下部の固定ボタン：ヒーローを過ぎたら表示、料金カードが見えている間は隠す
  const sticky = document.querySelector(".sticky");
  const hero = document.querySelector(".hero");
  const join = document.querySelector("#join");
  let pastHero = false, joinVisible = false;
  const update = () => sticky.classList.toggle("show", pastHero && !joinVisible);
  new IntersectionObserver(([e]) => { pastHero = !e.isIntersecting; update(); }).observe(hero);
  new IntersectionObserver(([e]) => { joinVisible = e.isIntersecting; update(); }).observe(join);
</script>
<?php wp_footer(); ?>
</body>
</html>
