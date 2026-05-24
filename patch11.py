#!/usr/bin/env python3
"""patch11.py — redesign share card canvas rendering"""

PATH = '/sessions/cool-nifty-clarke/mnt/outputs/index.html'

with open(PATH, 'r', encoding='utf-8') as f:
    src = f.read()

# Slice out the old generateShareCard function and replace it
START_MARKER = '\nasync function generateShareCard(entry, sp) {'
END_MARKER   = '\nfunction CatchCard('

si = src.index(START_MARKER)
ei = src.index(END_MARKER, si)
old_fn = src[si:ei]

NEW_FN = r"""
async function generateShareCard(entry, sp) {
  const W = 1080, H = 580;
  const c = document.createElement('canvas');
  c.width = W; c.height = H;
  const ctx = c.getContext('2d');
  await document.fonts.ready;

  // ── Rounded rect helper ──
  function rrect(x, y, w, h, r) {
    ctx.beginPath();
    ctx.moveTo(x+r, y);
    ctx.lineTo(x+w-r, y); ctx.quadraticCurveTo(x+w, y,   x+w, y+r);
    ctx.lineTo(x+w, y+h-r); ctx.quadraticCurveTo(x+w, y+h, x+w-r, y+h);
    ctx.lineTo(x+r, y+h); ctx.quadraticCurveTo(x,   y+h, x,   y+h-r);
    ctx.lineTo(x, y+r); ctx.quadraticCurveTo(x,   y,   x+r, y);
    ctx.closePath();
  }

  // ── Pill badge helper — returns badge width ──
  function badge(text, x, y, color) {
    ctx.font = 'bold 30px Inter,system-ui';
    const tw = ctx.measureText(text).width;
    const bh = 50, px = 22, r = 25;
    const bw = tw + px * 2;
    rrect(x, y, bw, bh, r);
    ctx.fillStyle = color + '28'; ctx.fill();
    ctx.strokeStyle = color + '80'; ctx.lineWidth = 1.5; ctx.stroke();
    ctx.fillStyle = color;
    ctx.textBaseline = 'middle';
    ctx.fillText(text, x + px, y + bh / 2);
    return bw;
  }

  // ══════════════════════════════════════════
  // BACKGROUND
  // ══════════════════════════════════════════
  if (entry.photo) {
    // Full-bleed photo
    await new Promise(resolve => {
      const img = new Image();
      img.onload = () => {
        const scale = Math.max(W / img.width, H / img.height);
        const dw = img.width * scale, dh = img.height * scale;
        ctx.drawImage(img, (W - dw) / 2, (H - dh) / 2, dw, dh);
        resolve();
      };
      img.src = entry.photo;
    });
    // Cinematic scrim — light at top, heavy at bottom
    const scrim = ctx.createLinearGradient(0, 0, 0, H);
    scrim.addColorStop(0,    'rgba(5,10,22,0.18)');
    scrim.addColorStop(0.38, 'rgba(5,10,22,0.08)');
    scrim.addColorStop(0.62, 'rgba(5,10,22,0.55)');
    scrim.addColorStop(1,    'rgba(5,10,22,0.97)');
    ctx.fillStyle = scrim; ctx.fillRect(0, 0, W, H);
    // Edge vignettes
    const lv = ctx.createLinearGradient(0, 0, 180, 0);
    lv.addColorStop(0, 'rgba(5,10,22,0.65)'); lv.addColorStop(1, 'rgba(5,10,22,0)');
    ctx.fillStyle = lv; ctx.fillRect(0, 0, 180, H);
    const rv = ctx.createLinearGradient(W - 130, 0, W, 0);
    rv.addColorStop(0, 'rgba(5,10,22,0)'); rv.addColorStop(1, 'rgba(5,10,22,0.7)');
    ctx.fillStyle = rv; ctx.fillRect(W - 130, 0, 130, H);
  } else {
    // No photo: rich dark gradient
    const bg = ctx.createLinearGradient(0, 0, W, H);
    bg.addColorStop(0, '#060B19'); bg.addColorStop(1, '#10182C');
    ctx.fillStyle = bg; ctx.fillRect(0, 0, W, H);
    // Fine grid
    ctx.strokeStyle = 'rgba(0,201,167,0.055)'; ctx.lineWidth = 0.5;
    for (let x = 0; x < W; x += 44) { ctx.beginPath(); ctx.moveTo(x,0); ctx.lineTo(x,H); ctx.stroke(); }
    for (let y = 0; y < H; y += 44) { ctx.beginPath(); ctx.moveTo(0,y); ctx.lineTo(W,y); ctx.stroke(); }
    // Species colour radial bloom left-of-centre
    const bloom = ctx.createRadialGradient(300, H * 0.5, 0, 300, H * 0.5, 420);
    bloom.addColorStop(0,   sp.color + '60');
    bloom.addColorStop(0.5, sp.color + '22');
    bloom.addColorStop(1,   'rgba(0,0,0,0)');
    ctx.fillStyle = bloom; ctx.fillRect(0, 0, W, H);
    // Large watermark letter
    ctx.font = 'bold 440px Inter,system-ui';
    ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
    ctx.fillStyle = sp.color + '16';
    ctx.fillText(sp.name[0], 280, H / 2 + 28);
  }

  // ══════════════════════════════════════════
  // OVERLAY DECORATION
  // ══════════════════════════════════════════

  // Teal radial glow along the bottom
  const tg = ctx.createRadialGradient(W * 0.42, H + 60, 0, W * 0.42, H + 60, 340);
  tg.addColorStop(0, 'rgba(0,201,167,0.28)'); tg.addColorStop(1, 'rgba(0,0,0,0)');
  ctx.fillStyle = tg; ctx.fillRect(0, H - 220, W, 220);

  // Left accent bar — gradient fade top/bottom
  const bar = ctx.createLinearGradient(0, 0, 0, H);
  bar.addColorStop(0,   'rgba(0,201,167,0.3)');
  bar.addColorStop(0.4, 'rgba(0,201,167,1)');
  bar.addColorStop(0.7, 'rgba(0,201,167,1)');
  bar.addColorStop(1,   'rgba(0,201,167,0.3)');
  ctx.fillStyle = bar; ctx.fillRect(0, 0, 6, H);

  // Top-right: "TIGHT LINES" label
  ctx.textAlign = 'right'; ctx.textBaseline = 'alphabetic';
  ctx.font = '600 15px Inter,system-ui';
  ctx.letterSpacing = '2px';
  ctx.fillStyle = 'rgba(255,255,255,0.3)';
  ctx.fillText('TIGHT LINES', W - 42, 50);
  ctx.letterSpacing = '0px';

  // Small fish icon top-right (SVG-style path, scaled)
  ctx.save();
  ctx.translate(W - 104, 30);
  ctx.scale(0.85, 0.85);
  ctx.strokeStyle = 'rgba(255,255,255,0.22)'; ctx.lineWidth = 1.6; ctx.lineJoin = 'round';
  ctx.beginPath();
  ctx.moveTo(4, 12); ctx.bezierCurveTo(14,4, 28,8, 34,12);
  ctx.bezierCurveTo(28,16, 14,20, 4,12);
  ctx.moveTo(4,12); ctx.lineTo(-4,6); ctx.moveTo(4,12); ctx.lineTo(-4,18);
  ctx.stroke();
  ctx.restore();

  // ══════════════════════════════════════════
  // TEXT CONTENT — bottom-left
  // ══════════════════════════════════════════
  ctx.textAlign = 'left';
  const tx = 48;
  let ty = H - 210;

  // Species name with text shadow
  ctx.shadowColor = 'rgba(0,0,0,0.9)'; ctx.shadowBlur = 24; ctx.shadowOffsetY = 2;
  ctx.font = 'bold 84px Inter,system-ui';
  ctx.fillStyle = '#FFFFFF';
  ctx.textBaseline = 'alphabetic';
  ctx.fillText(sp.name, tx, ty);
  ctx.shadowBlur = 0; ctx.shadowOffsetY = 0;
  ty += 16;

  // Māori name
  if (sp.maori) {
    ctx.font = 'italic 27px Inter,system-ui';
    ctx.fillStyle = 'rgba(255,255,255,0.42)';
    ctx.fillText(sp.maori, tx + 2, ty + 28);
    ty += 54;
  } else { ty += 34; }

  ty += 20;

  // Stat badges
  ctx.textBaseline = 'middle';
  let bx = tx;
  if (entry.length) { bx += badge(entry.length + ' cm', bx, ty, 'rgba(0,201,167,1)') + 12; }
  if (entry.weight) { badge(entry.weight + ' kg', bx, ty, 'rgba(245,166,35,1)'); }
  ty += 68;

  // Location · Date line
  ctx.textBaseline = 'alphabetic';
  ctx.font = '400 20px Inter,system-ui';
  ctx.fillStyle = 'rgba(255,255,255,0.48)';
  const parts = [];
  if (entry.location) parts.push('\u{1F4CD} ' + entry.location);
  if (entry.date) parts.push(new Date(entry.date).toLocaleDateString('en-NZ', { day:'numeric', month:'long', year:'numeric' }));
  if (parts.length) {
    ctx.shadowColor = 'rgba(0,0,0,0.7)'; ctx.shadowBlur = 12;
    ctx.fillText(parts.join('  ·  '), tx, ty);
    ctx.shadowBlur = 0;
  }

  // Bottom gradient rule
  const rule = ctx.createLinearGradient(0, 0, W, 0);
  rule.addColorStop(0,   'rgba(0,201,167,0)');
  rule.addColorStop(0.25,'rgba(0,201,167,0.9)');
  rule.addColorStop(0.75,'rgba(0,201,167,0.9)');
  rule.addColorStop(1,   'rgba(0,201,167,0)');
  ctx.fillStyle = rule; ctx.fillRect(0, H - 3, W, 3);

  return c.toDataURL('image/png');
}
"""

src = src[:si] + NEW_FN + src[ei:]

with open(PATH, 'w', encoding='utf-8') as f:
    f.write(src)

delta = len(src) - (len(src) - len(NEW_FN) + len(old_fn))
print(f"=== patch11: share card redesign, {len(NEW_FN)-len(old_fn):+d} bytes ===")
print(f"  ✓ generateShareCard replaced ({len(old_fn)} → {len(NEW_FN)} chars)")
