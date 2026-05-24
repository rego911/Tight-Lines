// Tight Lines — shared components
// Globals: React, ReactDOM (UMD)
// Tokens are read from CSS vars on :root: --bg, --bg-2, --teal, --amber, --ink, --muted, --hairline, --glass-bg, --glass-blur

const { useState, useEffect, useRef, useMemo } = React;

// ─────────────────────────────────────────────────────────────
// Glass surface — frosted card (variable intensity)
// ─────────────────────────────────────────────────────────────
function TLGlass({ children, style = {}, radius = 20, glow = true, padding = 16, intensity = 'frosted', className = '' }) {
  const isFlat = intensity === 'flat';
  return (
    <div
      className={className}
      style={{
        position: 'relative',
        borderRadius: radius,
        padding,
        background: isFlat
          ? 'linear-gradient(180deg, rgba(255,255,255,0.04), rgba(255,255,255,0.015))'
          : 'linear-gradient(180deg, rgba(255,255,255,0.06), rgba(255,255,255,0.02))',
        backdropFilter: isFlat ? 'none' : 'blur(18px) saturate(140%)',
        WebkitBackdropFilter: isFlat ? 'none' : 'blur(18px) saturate(140%)',
        border: '1px solid var(--hairline)',
        boxShadow: glow && !isFlat
          ? 'inset 0 1px 0 rgba(255,255,255,0.06), inset 0 -40px 60px -30px rgba(0,201,167,0.05), 0 12px 32px -20px rgba(0,0,0,0.6)'
          : 'inset 0 1px 0 rgba(255,255,255,0.04), 0 6px 18px -12px rgba(0,0,0,0.6)',
        overflow: 'hidden',
        ...style,
      }}
    >
      {children}
    </div>
  );
}

// ─────────────────────────────────────────────────────────────
// Stat pill — small label badge
// ─────────────────────────────────────────────────────────────
function StatPill({ children, tone = 'default', style = {} }) {
  const tones = {
    default: { bg: 'rgba(255,255,255,0.06)', fg: 'var(--muted)', border: 'rgba(255,255,255,0.08)' },
    teal:    { bg: 'rgba(0,201,167,0.13)',  fg: 'var(--teal)',   border: 'rgba(0,201,167,0.32)' },
    amber:   { bg: 'rgba(245,166,35,0.13)', fg: 'var(--amber)',  border: 'rgba(245,166,35,0.32)' },
    red:     { bg: 'rgba(255,90,90,0.13)',  fg: '#FF8A8A',       border: 'rgba(255,90,90,0.32)' },
  };
  const t = tones[tone] || tones.default;
  return (
    <span style={{
      display: 'inline-flex', alignItems: 'center', gap: 6,
      padding: '4px 9px', fontSize: 11, fontWeight: 600,
      letterSpacing: 0.4, textTransform: 'uppercase',
      color: t.fg, background: t.bg,
      border: `1px solid ${t.border}`,
      borderRadius: 999,
      fontFamily: 'Inter, system-ui',
      ...style,
    }}>{children}</span>
  );
}

// ─────────────────────────────────────────────────────────────
// Weather icon — morphing SVG (sun → partly → cloud → rain)
// All states share the same SVG groups; uses opacity & transform animations.
// ─────────────────────────────────────────────────────────────
function WeatherIcon({ cond = 'clear', size = 28, animate = true }) {
  const showSun   = cond === 'clear' || cond === 'partly';
  const showCloud = cond === 'partly' || cond === 'cloud' || cond === 'rain';
  const showRain  = cond === 'rain';
  return (
    <svg width={size} height={size} viewBox="0 0 32 32" style={{ overflow: 'visible' }}>
      {/* Sun */}
      <g style={{
        opacity: showSun ? 1 : 0,
        transform: showSun ? (cond === 'partly' ? 'translate(-3px,-3px) scale(0.78)' : 'scale(1)') : 'scale(0.5)',
        transformOrigin: '50% 50%',
        transition: animate ? 'opacity .45s ease, transform .55s cubic-bezier(.4,.0,.2,1)' : 'none',
      }}>
        <circle cx="16" cy="16" r="5.5" fill="url(#tl-sun-grad)" />
        {[0,45,90,135,180,225,270,315].map(a => (
          <rect key={a} x="15.2" y="3" width="1.6" height="3.6" rx="0.8" fill="var(--amber)"
                transform={`rotate(${a} 16 16)`} opacity="0.85"/>
        ))}
      </g>
      {/* Cloud */}
      <g style={{
        opacity: showCloud ? 1 : 0,
        transform: showCloud ? (cond === 'partly' ? 'translate(4px,3px) scale(0.9)' : 'scale(1.05)') : 'translate(0,8px) scale(0.7)',
        transformOrigin: '50% 50%',
        transition: animate ? 'opacity .45s ease .05s, transform .55s cubic-bezier(.4,.0,.2,1)' : 'none',
      }}>
        <path d="M9 20.5h14.5a4.2 4.2 0 0 0 .4-8.37 6.2 6.2 0 0 0-12.04-1.1A4.4 4.4 0 0 0 9 20.5z"
              fill="url(#tl-cloud-grad)" stroke="rgba(255,255,255,0.18)" strokeWidth="0.6" />
      </g>
      {/* Rain */}
      <g style={{
        opacity: showRain ? 1 : 0,
        transition: animate ? 'opacity .35s ease .1s' : 'none',
      }}>
        {[10, 15, 20, 25].map((x, i) => (
          <line key={x} x1={x} y1="22" x2={x - 1.5} y2="27"
                stroke="var(--teal)" strokeWidth="1.4" strokeLinecap="round"
                style={animate ? { animation: `tl-rain 1.1s ${i*0.12}s infinite ease-in` } : {}} />
        ))}
      </g>
      <defs>
        <radialGradient id="tl-sun-grad" cx="50%" cy="45%" r="60%">
          <stop offset="0%" stopColor="#FFD79A" />
          <stop offset="60%" stopColor="var(--amber)" />
          <stop offset="100%" stopColor="#C77A0E" />
        </radialGradient>
        <linearGradient id="tl-cloud-grad" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor="rgba(255,255,255,0.85)" />
          <stop offset="100%" stopColor="rgba(170,200,225,0.55)" />
        </linearGradient>
      </defs>
    </svg>
  );
}

// ─────────────────────────────────────────────────────────────
// Pressure trend arrow — animated direction + glow severity
// ─────────────────────────────────────────────────────────────
function PressureArrow({ trend = 'rising', delta = 2.1, size = 18 }) {
  const isRising = trend === 'rising';
  const isFalling = trend === 'falling';
  const color = isRising ? 'var(--teal)' : isFalling ? 'var(--amber)' : 'var(--muted)';
  const glow = Math.min(20, Math.abs(delta) * 6);
  return (
    <span style={{
      display: 'inline-flex', alignItems: 'center', gap: 4,
      color, fontWeight: 600, fontSize: 12,
      filter: `drop-shadow(0 0 ${glow}px ${color}88)`,
      transition: 'filter .6s ease',
    }}>
      <svg width={size} height={size} viewBox="0 0 16 16" style={{
        transform: isRising ? 'rotate(-45deg)' : isFalling ? 'rotate(135deg)' : 'rotate(90deg)',
        transition: 'transform .9s cubic-bezier(.34,1.56,.64,1)',
      }}>
        <path d="M3 8h10M9 4l4 4-4 4" fill="none" stroke={color} strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" />
      </svg>
      {delta > 0 ? '+' : ''}{delta} hPa
    </span>
  );
}

// ─────────────────────────────────────────────────────────────
// Fishing Score gauge — 3 variants
//   variant: 'arc' | 'liquid' | 'segmented'
// ─────────────────────────────────────────────────────────────
function FishingScore({ score = 84, variant = 'arc', size = 220, label = 'Fishing Score', sub = 'Excellent' }) {
  const [animScore, setAnimScore] = useState(0);
  useEffect(() => {
    let frame;
    const start = performance.now();
    const dur = 1400;
    const ease = t => 1 - Math.pow(1 - t, 3);
    const tick = (now) => {
      const t = Math.min(1, (now - start) / dur);
      setAnimScore(score * ease(t));
      if (t < 1) frame = requestAnimationFrame(tick);
    };
    frame = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(frame);
  }, [score, variant]);

  const cx = size / 2, cy = size / 2;
  const stroke = 14;
  const r = (size - stroke) / 2 - 6;
  const sweep = 270; // degrees
  const startAngle = 135; // top-left start
  const circ = 2 * Math.PI * r;
  const arcLen = circ * (sweep / 360);
  const filled = arcLen * (animScore / 100);

  const tone = score >= 80 ? 'var(--teal)' : score >= 60 ? '#7BD4F0' : 'var(--amber)';
  const toneSoft = score >= 80 ? 'rgba(0,201,167,0.18)' : score >= 60 ? 'rgba(123,212,240,0.18)' : 'rgba(245,166,35,0.18)';

  // common centre text
  const centre = (
    <div style={{
      position: 'absolute', inset: 0,
      display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center',
      pointerEvents: 'none',
    }}>
      <span style={{
        fontFamily: '"Inter Tight", Inter, system-ui',
        fontWeight: 700, fontSize: size * 0.32, letterSpacing: -2,
        color: 'var(--ink)', lineHeight: 1,
        fontVariantNumeric: 'tabular-nums',
      }}>{Math.round(animScore)}</span>
      <span style={{
        fontSize: 11, letterSpacing: 1.4, textTransform: 'uppercase',
        color: 'var(--muted)', marginTop: 6,
      }}>{label}</span>
      <span style={{
        fontSize: 12, color: tone, marginTop: 2, fontWeight: 600,
      }}>{sub}</span>
    </div>
  );

  if (variant === 'liquid') {
    // full ring + animated wave fill in centre
    const fillPct = animScore / 100;
    return (
      <div style={{ position: 'relative', width: size, height: size, margin: '0 auto' }}>
        <svg width={size} height={size}>
          <defs>
            <linearGradient id="tl-liquid-grad" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor={tone} stopOpacity="0.85" />
              <stop offset="100%" stopColor={tone} stopOpacity="0.35" />
            </linearGradient>
            <clipPath id="tl-liquid-clip"><circle cx={cx} cy={cy} r={r - 4} /></clipPath>
          </defs>
          {/* outer ring */}
          <circle cx={cx} cy={cy} r={r} fill="none" stroke={toneSoft} strokeWidth={stroke * 0.5} />
          <circle cx={cx} cy={cy} r={r} fill="none" stroke={tone} strokeWidth={stroke * 0.5}
                  strokeDasharray={`${circ * fillPct} ${circ}`} strokeLinecap="round"
                  transform={`rotate(-90 ${cx} ${cy})`} style={{ filter: `drop-shadow(0 0 8px ${tone}66)` }}/>
          {/* liquid wave */}
          <g clipPath="url(#tl-liquid-clip)">
            <rect x="0" y={size - (size * fillPct) - 8} width={size * 3} height={size}
                  fill="url(#tl-liquid-grad)">
              <animateTransform attributeName="transform" type="translate" from="0,0" to={`-${size},0`}
                                dur="6s" repeatCount="indefinite" />
            </rect>
            <path d={waveD(size, 8, 0)} fill={tone} opacity="0.5" transform={`translate(0,${size - (size * fillPct) - 8})`}>
              <animateTransform attributeName="transform" type="translate"
                                values={`-${size},${size - (size*fillPct) - 8}; 0,${size - (size*fillPct) - 8}`}
                                dur="5s" repeatCount="indefinite" additive="sum" />
            </path>
          </g>
        </svg>
        {centre}
      </div>
    );
  }

  if (variant === 'segmented') {
    const segments = 36;
    const litCount = Math.round(segments * (animScore / 100));
    return (
      <div style={{ position: 'relative', width: size, height: size, margin: '0 auto' }}>
        <svg width={size} height={size}>
          {Array.from({ length: segments }).map((_, i) => {
            const a = startAngle + (i / (segments - 1)) * sweep;
            const x1 = cx + (r - 18) * Math.cos(a * Math.PI / 180);
            const y1 = cy + (r - 18) * Math.sin(a * Math.PI / 180);
            const x2 = cx + r * Math.cos(a * Math.PI / 180);
            const y2 = cy + r * Math.sin(a * Math.PI / 180);
            const lit = i < litCount;
            return (
              <line key={i} x1={x1} y1={y1} x2={x2} y2={y2}
                    stroke={lit ? tone : 'rgba(255,255,255,0.08)'} strokeWidth="3" strokeLinecap="round"
                    style={lit ? { filter: `drop-shadow(0 0 4px ${tone}88)` } : {}} />
            );
          })}
        </svg>
        {centre}
      </div>
    );
  }

  // default: arc
  // build arc path
  const a0 = startAngle * Math.PI / 180;
  const a1 = (startAngle + sweep) * Math.PI / 180;
  const x0 = cx + r * Math.cos(a0), y0 = cy + r * Math.sin(a0);
  const x1 = cx + r * Math.cos(a1), y1 = cy + r * Math.sin(a1);
  const largeArc = sweep > 180 ? 1 : 0;
  const d = `M ${x0} ${y0} A ${r} ${r} 0 ${largeArc} 1 ${x1} ${y1}`;
  return (
    <div style={{ position: 'relative', width: size, height: size, margin: '0 auto' }}>
      <svg width={size} height={size}>
        <defs>
          <linearGradient id="tl-arc-grad" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0%" stopColor={tone} stopOpacity="1" />
            <stop offset="100%" stopColor={tone} stopOpacity="0.65" />
          </linearGradient>
          <clipPath id="tl-arc-fill-clip"><path d={d} stroke="black" strokeWidth={stroke} fill="none" /></clipPath>
        </defs>
        <path d={d} fill="none" stroke="rgba(255,255,255,0.07)" strokeWidth={stroke} strokeLinecap="round" />
        <path d={d} fill="none" stroke="url(#tl-arc-grad)" strokeWidth={stroke} strokeLinecap="round"
              strokeDasharray={`${filled} ${arcLen - filled + 0.001}`}
              style={{ filter: `drop-shadow(0 0 10px ${tone}55)`, transition: 'stroke-dasharray .1s linear' }}/>
        {/* tick marks at 0, 50, 100 */}
        {[0, 0.25, 0.5, 0.75, 1].map((t, i) => {
          const a = (startAngle + sweep * t) * Math.PI / 180;
          const inner = r - 18, outer = r - 24;
          return (
            <line key={i}
              x1={cx + inner * Math.cos(a)} y1={cy + inner * Math.sin(a)}
              x2={cx + outer * Math.cos(a)} y2={cy + outer * Math.sin(a)}
              stroke="rgba(255,255,255,0.18)" strokeWidth="1" />
          );
        })}
      </svg>
      {centre}
    </div>
  );
}

function waveD(w, amp, phase) {
  // sine wave path along top
  const pts = [];
  for (let x = 0; x <= w; x += 8) {
    pts.push([x, amp + amp * Math.sin((x / w) * Math.PI * 4 + phase)]);
  }
  return 'M0,' + (amp*2+4) + ' ' + pts.map(p => `L${p[0]},${p[1]}`).join(' ') + ` L${w},${amp*2+4} Z`;
}

// ─────────────────────────────────────────────────────────────
// Tide chart — smooth animated wave curve
// ─────────────────────────────────────────────────────────────
function TideChart({ data, events, height = 130, nowIdx = 16, showLabels = true }) {
  const ref = useRef(null);
  const [w, setW] = useState(340);
  useEffect(() => {
    if (!ref.current) return;
    const ro = new ResizeObserver(entries => {
      setW(entries[0].contentRect.width);
    });
    ro.observe(ref.current);
    return () => ro.disconnect();
  }, []);
  const maxH = Math.max(...data.map(d => d.height));
  const minH = Math.min(...data.map(d => d.height));
  const pad = 14;
  const innerH = height - pad * 2 - 12;
  const xFor = (i) => (i / (data.length - 1)) * (w - pad * 2) + pad;
  const yFor = (h) => pad + innerH * (1 - (h - minH) / (maxH - minH || 1));

  // smooth path via cardinal-ish curve
  const pts = data.map((d, i) => [xFor(i), yFor(d.height)]);
  const pathD = useMemo(() => {
    if (pts.length === 0) return '';
    let s = `M ${pts[0][0]} ${pts[0][1]}`;
    for (let i = 1; i < pts.length; i++) {
      const p0 = pts[i - 1], p1 = pts[i];
      const cx = (p0[0] + p1[0]) / 2;
      s += ` C ${cx} ${p0[1]}, ${cx} ${p1[1]}, ${p1[0]} ${p1[1]}`;
    }
    return s;
  }, [pts.map(p => p[0] + ',' + p[1]).join(' ')]);

  const fillD = pathD + ` L ${pts[pts.length-1][0]} ${height} L ${pts[0][0]} ${height} Z`;
  const nowX = xFor(nowIdx);
  const nowY = yFor(data[nowIdx].height);

  return (
    <div ref={ref} style={{ width: '100%', position: 'relative', height }}>
      <svg width={w} height={height} style={{ display: 'block', overflow: 'visible' }}>
        <defs>
          <linearGradient id="tl-tide-fill" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%"  stopColor="var(--teal)" stopOpacity="0.4" />
            <stop offset="100%" stopColor="var(--teal)" stopOpacity="0" />
          </linearGradient>
        </defs>
        {/* faint grid */}
        {[0.25, 0.5, 0.75].map(t => (
          <line key={t} x1={pad} y1={pad + innerH * t} x2={w - pad} y2={pad + innerH * t}
                stroke="rgba(255,255,255,0.05)" strokeDasharray="2 4" />
        ))}
        {/* fill — gentle undulation via translate animation on a clone path */}
        <g className="tl-tide-undulate">
          <path d={fillD} fill="url(#tl-tide-fill)" />
          <path d={pathD} fill="none" stroke="var(--teal)" strokeWidth="2"
                style={{ filter: 'drop-shadow(0 0 6px rgba(0,201,167,0.35))' }} />
        </g>
        {/* events */}
        {events && events.map((e, i) => {
          const hour = parseInt(e.time.slice(0,2),10) + parseInt(e.time.slice(3),10)/60;
          const idx = Math.round((hour / 24) * (data.length - 1));
          const ex = xFor(idx), ey = yFor(e.height);
          return (
            <g key={i}>
              <circle cx={ex} cy={ey} r="3" fill="var(--bg)" stroke="var(--teal)" strokeWidth="1.5" />
              {showLabels && <text x={ex} y={ey - 10} fontSize="9" fill="var(--muted)" textAnchor="middle"
                    fontFamily="Inter, system-ui" letterSpacing="0.4">{e.label.toUpperCase()} {e.time}</text>}
            </g>
          );
        })}
        {/* NOW indicator */}
        <line x1={nowX} y1={pad - 4} x2={nowX} y2={height - 14}
              stroke="var(--amber)" strokeWidth="1" strokeDasharray="2 3" opacity="0.55" />
        <circle cx={nowX} cy={nowY} r="5" fill="var(--amber)"
                style={{ filter: 'drop-shadow(0 0 8px var(--amber))' }}>
          <animate attributeName="r" values="5;7;5" dur="2.2s" repeatCount="indefinite" />
        </circle>
        <circle cx={nowX} cy={nowY} r="2" fill="#0A0F1E" />
      </svg>
    </div>
  );
}

// ─────────────────────────────────────────────────────────────
// Wind compass — animated needle with spring overshoot
// ─────────────────────────────────────────────────────────────
function WindCompass({ bearing = 218, speed = 11, gust = 17, size = 200 }) {
  const [angle, setAngle] = useState(bearing - 90); // start offset
  useEffect(() => {
    // spring towards bearing
    let target = bearing;
    let cur = bearing - 60;
    let v = 0;
    let raf;
    const tick = () => {
      const k = 0.06;
      const f = (target - cur) * k - v * 0.18;
      v += f;
      cur += v;
      setAngle(cur);
      if (Math.abs(target - cur) > 0.3 || Math.abs(v) > 0.05) {
        raf = requestAnimationFrame(tick);
      } else {
        setAngle(target);
      }
    };
    raf = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(raf);
  }, [bearing]);
  const cx = size / 2, cy = size / 2;
  const r = size / 2 - 8;
  return (
    <div style={{ position: 'relative', width: size, height: size, margin: '0 auto' }}>
      <svg width={size} height={size}>
        <defs>
          <radialGradient id="tl-comp-bg" cx="50%" cy="50%" r="55%">
            <stop offset="0%"  stopColor="rgba(0,201,167,0.08)" />
            <stop offset="100%" stopColor="rgba(0,0,0,0)" />
          </radialGradient>
        </defs>
        <circle cx={cx} cy={cy} r={r} fill="url(#tl-comp-bg)" stroke="rgba(255,255,255,0.08)" />
        <circle cx={cx} cy={cy} r={r - 14} fill="none" stroke="rgba(255,255,255,0.05)" strokeDasharray="1 5" />
        {/* tick marks every 15° */}
        {Array.from({ length: 24 }).map((_, i) => {
          const a = (i * 15) * Math.PI / 180;
          const major = i % 6 === 0;
          const inner = r - (major ? 14 : 9);
          const outer = r - 4;
          return (
            <line key={i}
              x1={cx + inner * Math.cos(a - Math.PI/2)} y1={cy + inner * Math.sin(a - Math.PI/2)}
              x2={cx + outer * Math.cos(a - Math.PI/2)} y2={cy + outer * Math.sin(a - Math.PI/2)}
              stroke={major ? 'rgba(255,255,255,0.4)' : 'rgba(255,255,255,0.15)'} strokeWidth={major ? 1.5 : 1} />
          );
        })}
        {/* cardinal letters */}
        {['N','E','S','W'].map((l, i) => {
          const a = (i * 90) * Math.PI / 180 - Math.PI / 2;
          const rr = r - 26;
          return (
            <text key={l} x={cx + rr * Math.cos(a)} y={cy + rr * Math.sin(a) + 4}
                  fontSize="11" fill={l === 'N' ? 'var(--amber)' : 'var(--muted)'} textAnchor="middle"
                  fontFamily="Inter, system-ui" fontWeight="600" letterSpacing="0.5">{l}</text>
          );
        })}
        {/* needle */}
        <g transform={`rotate(${angle} ${cx} ${cy})`} style={{ transition: 'transform 60ms linear' }}>
          <path d={`M ${cx} ${cy - r + 12} L ${cx - 8} ${cy + 8} L ${cx} ${cy} L ${cx + 8} ${cy + 8} Z`}
                fill="var(--teal)" style={{ filter: 'drop-shadow(0 0 6px rgba(0,201,167,0.6))' }}/>
          <path d={`M ${cx} ${cy + r - 12} L ${cx - 6} ${cy - 4} L ${cx} ${cy} L ${cx + 6} ${cy - 4} Z`}
                fill="rgba(255,255,255,0.25)" />
        </g>
        <circle cx={cx} cy={cy} r="4" fill="var(--ink)" />
      </svg>
      {/* centre stat */}
      <div style={{
        position: 'absolute', top: '52%', left: '50%', transform: 'translate(-50%, 8px)',
        textAlign: 'center', pointerEvents: 'none',
      }}>
        <div style={{ fontSize: 10, color: 'var(--muted)', letterSpacing: 1.2, textTransform: 'uppercase' }}>
          Gust {gust}kt
        </div>
      </div>
    </div>
  );
}

// ─────────────────────────────────────────────────────────────
// Moon phase
// ─────────────────────────────────────────────────────────────
function MoonPhase({ illum = 0.78, size = 64 }) {
  // simple crescent via two arcs
  const r = size / 2 - 2;
  const offset = (1 - illum * 2) * r; // -r to r
  return (
    <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`}>
      <defs>
        <radialGradient id="tl-moon" cx="40%" cy="40%" r="60%">
          <stop offset="0%" stopColor="#FFF7E0" />
          <stop offset="100%" stopColor="#9CA3B5" />
        </radialGradient>
      </defs>
      <circle cx={size/2} cy={size/2} r={r} fill="rgba(255,255,255,0.05)" stroke="rgba(255,255,255,0.1)" />
      <path d={`M ${size/2} ${size/2 - r} A ${r} ${r} 0 1 1 ${size/2} ${size/2 + r} A ${Math.abs(offset)} ${r} 0 1 ${offset > 0 ? 1 : 0} ${size/2} ${size/2 - r} Z`}
            fill="url(#tl-moon)" />
    </svg>
  );
}

// ─────────────────────────────────────────────────────────────
// Fish silhouette icons
// ─────────────────────────────────────────────────────────────
const FISH_SVGS = {
  snapper:  'M2 16 Q 8 6, 26 8 Q 38 10, 44 16 Q 38 22, 26 24 Q 8 26, 2 16 L 0 11 L 4 16 L 0 21 Z',
  kingfish: 'M2 16 Q 10 4, 32 6 Q 44 10, 46 16 Q 44 22, 32 26 Q 10 28, 2 16 L 0 12 L 5 16 L 0 20 Z',
  marlin:   'M0 17 L 14 14 Q 22 4, 38 8 Q 50 12, 52 16 Q 50 20, 38 24 Q 22 28, 14 18 L 0 17 Z',
  kahawai:  'M2 16 Q 8 8, 24 8 Q 36 10, 42 16 Q 36 22, 24 24 Q 8 24, 2 16 L 0 11 L 4 16 L 0 21 Z',
  trevally: 'M2 16 Q 10 6, 28 8 Q 38 10, 42 16 Q 38 22, 28 24 Q 10 26, 2 16 L 0 11 L 4 16 L 0 21 Z',
  hapuka:   'M3 16 Q 10 4, 30 6 Q 42 10, 46 16 Q 42 22, 30 26 Q 10 28, 3 16 L 0 11 L 5 16 L 0 21 Z',
  tarakihi: 'M2 16 Q 8 8, 22 8 Q 32 10, 38 16 Q 32 22, 22 24 Q 8 24, 2 16 L 0 11 L 4 16 L 0 21 Z',
};
function FishIcon({ id = 'snapper', width = 46, color = 'currentColor', active = false }) {
  const d = FISH_SVGS[id] || FISH_SVGS.snapper;
  const vbW = id === 'marlin' ? 52 : 46;
  return (
    <svg width={width} height={width * 32 / vbW} viewBox={`0 0 ${vbW} 32`} fill={color}>
      <path d={d} opacity={active ? 1 : 0.85}/>
      <circle cx={vbW - 14} cy="14" r="1.2" fill="var(--bg)" />
    </svg>
  );
}

// expose
Object.assign(window, {
  TLGlass, StatPill, WeatherIcon, PressureArrow,
  FishingScore, TideChart, WindCompass, MoonPhase, FishIcon,
});
