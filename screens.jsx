// Tight Lines — screens (Dashboard, Conditions, Catch, Settings)
// Depends on components.jsx + data.js loaded globally

const { useState: useStateS, useEffect: useEffectS, useRef: useRefS, useMemo: useMemoS } = React;
const D = window.TL_DATA;

// helper: stagger entrance — each child fades & rises with delay
function StaggerList({ children, gap = 12, delay = 0 }) {
  const arr = React.Children.toArray(children);
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap }}>
      {arr.map((c, i) => (
        <div key={i} style={{
          animation: `tl-stagger .55s cubic-bezier(.21,.61,.35,1) ${delay + i * 0.06}s both`,
        }}>{c}</div>
      ))}
    </div>
  );
}

function MotionTag({ children, top, left, right, bottom, anchor = 'tl', shown }) {
  if (!shown) return null;
  return (
    <div style={{
      position: 'absolute', top, left, right, bottom,
      zIndex: 90, pointerEvents: 'none',
      fontFamily: 'JetBrains Mono, ui-monospace, monospace',
      fontSize: 9, lineHeight: 1.35,
      color: 'var(--amber)',
      background: 'rgba(10,15,30,0.85)',
      border: '1px dashed var(--amber)',
      padding: '4px 7px',
      borderRadius: 4,
      maxWidth: 160,
      backdropFilter: 'blur(8px)',
      WebkitBackdropFilter: 'blur(8px)',
      letterSpacing: 0.2,
    }}>
      <div style={{ fontWeight: 700, marginBottom: 1, fontSize: 8, opacity: 0.7 }}>
        ◆ MOTION
      </div>
      {children}
    </div>
  );
}

// ═════════════════════════════════════════════════════════════
// DASHBOARD
// ═════════════════════════════════════════════════════════════
function Dashboard({ tweaks }) {
  const intensity = tweaks.glass;
  const showMotion = tweaks.motionLabels;
  const gaugeVariant = tweaks.gauge;
  const n = D.now;
  const scrollRef = useRefS(null);
  const [pull, setPull] = useStateS(0); // 0..1 pull-to-refresh state
  const [refreshing, setRefreshing] = useStateS(false);
  const startY = useRefS(null);

  // pull to refresh handlers
  const onTouchStart = (e) => {
    if (scrollRef.current && scrollRef.current.scrollTop <= 0) {
      startY.current = e.touches ? e.touches[0].clientY : e.clientY;
    }
  };
  const onTouchMove = (e) => {
    if (startY.current == null) return;
    const y = e.touches ? e.touches[0].clientY : e.clientY;
    const dy = y - startY.current;
    if (dy > 0) {
      e.preventDefault?.();
      setPull(Math.min(1, dy / 120));
    }
  };
  const onTouchEnd = () => {
    if (pull > 0.7) {
      setRefreshing(true);
      setTimeout(() => { setRefreshing(false); setPull(0); }, 1600);
    } else {
      setPull(0);
    }
    startY.current = null;
  };
  useEffectS(() => {
    if (refreshing) {
      const id = setTimeout(() => setRefreshing(false), 1800);
      return () => clearTimeout(id);
    }
  }, [refreshing]);

  // hourly horizontal scroll parallax
  const hourlyRef = useRefS(null);
  const [hourlyScroll, setHourlyScroll] = useStateS(0);
  const onHourlyScroll = () => {
    if (hourlyRef.current) setHourlyScroll(hourlyRef.current.scrollLeft);
  };

  return (
    <div
      ref={scrollRef}
      onTouchStart={onTouchStart} onTouchMove={onTouchMove} onTouchEnd={onTouchEnd}
      onMouseDown={onTouchStart} onMouseMove={(e) => e.buttons === 1 && onTouchMove(e)} onMouseUp={onTouchEnd}
      style={{ height: '100%', overflowY: 'auto', overflowX: 'hidden', position: 'relative',
               paddingTop: 56, paddingBottom: 100, color: 'var(--ink)' }}
    >
      {/* pull-to-refresh visual */}
      <PullRefresh active={pull > 0 || refreshing} progress={pull} refreshing={refreshing} />

      {/* top hero gradient */}
      <div style={{ position: 'absolute', inset: '0 0 auto 0', height: 360,
                    background: 'radial-gradient(ellipse 80% 60% at 50% 0%, rgba(0,201,167,0.15), transparent 70%)',
                    pointerEvents: 'none', zIndex: 0 }} />

      <div style={{ position: 'relative', zIndex: 1, padding: '8px 18px 0', transform: `translateY(${pull * 30}px)` }}>
        {/* location + date */}
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 18 }}>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: 6, color: 'var(--muted)', fontSize: 12, letterSpacing: 0.5 }}>
              <svg width="11" height="11" viewBox="0 0 12 12"><circle cx="6" cy="6" r="2.5" fill="var(--teal)"/><circle cx="6" cy="6" r="5" fill="none" stroke="var(--teal)" strokeOpacity="0.35"/></svg>
              {D.location.region}
            </div>
            <div style={{ fontSize: 22, fontWeight: 700, marginTop: 2, letterSpacing: -0.5 }}>{D.location.name}</div>
          </div>
          <div style={{ textAlign: 'right', fontSize: 11, color: 'var(--muted)', letterSpacing: 0.5, lineHeight: 1.4 }}>
            MON 18 MAY<br/>
            <span style={{ color: 'var(--ink)' }}>09:14 NZST</span>
          </div>
        </div>

        {/* Fishing Score hero */}
        <div style={{ position: 'relative', marginBottom: 8 }}>
          <FishingScore score={n.score} variant={gaugeVariant} size={232} sub="Excellent — fish on" />
          <MotionTag shown={showMotion} top={4} right={-4}>
            Gauge arc 0→{n.score}<br/>
            1400ms · ease-out-cubic<br/>
            Liquid fill loops 5–6s
          </MotionTag>
        </div>

        {/* Quick stat row pills */}
        <div style={{ display: 'flex', gap: 8, justifyContent: 'center', marginBottom: 18, flexWrap: 'wrap' }}>
          <StatPill tone="teal">↑ {n.tideState}</StatPill>
          <StatPill tone="amber">{n.uvLabel} UV {n.uv}</StatPill>
          <StatPill>Moon 78%</StatPill>
        </div>

        {/* stat tiles */}
        <StaggerList delay={0.2}>
          <StatTilesGrid n={n} intensity={intensity} showMotion={showMotion} />
        </StaggerList>
      </div>

      {/* Hourly forecast horizontal scroll */}
      <div style={{ marginTop: 26, position: 'relative' }}>
        <SectionHeader title="Hourly outlook" hint="Bite score / hour" />
        <div ref={hourlyRef} onScroll={onHourlyScroll}
             style={{ overflowX: 'auto', overflowY: 'hidden', padding: '0 18px 8px',
                      scrollSnapType: 'x mandatory', WebkitOverflowScrolling: 'touch' }}
             className="tl-hide-scrollbar">
          <div style={{ display: 'flex', gap: 10 }}>
            {D.hourly.map((h, i) => (
              <HourCard key={i} h={h} idx={i} scroll={hourlyScroll} intensity={intensity} />
            ))}
          </div>
        </div>
        <MotionTag shown={showMotion} top={10} right={14}>
          Parallax depth<br/>
          translateZ on scroll<br/>
          ±12px @ 0.4× rate
        </MotionTag>
      </div>

      {/* 7-day */}
      <div style={{ marginTop: 26, padding: '0 18px' }}>
        <SectionHeader title="7-day outlook" hint="Peak bite windows" inset />
        <TLGlass intensity={intensity} padding={0} style={{ marginTop: 8 }}>
          {D.daily.map((d, i) => (
            <DailyRow key={i} d={d} highlight={i === 0} last={i === D.daily.length - 1} />
          ))}
        </TLGlass>
      </div>

      <div style={{ padding: '20px 18px', textAlign: 'center', fontSize: 10, color: 'rgba(255,255,255,0.25)', letterSpacing: 1.5 }}>
        TIDE & METOCEAN · LINZ · NIWA
      </div>
    </div>
  );
}

function PullRefresh({ active, progress, refreshing }) {
  return (
    <div style={{
      position: 'absolute', top: 8, left: 0, right: 0, height: 80,
      display: 'flex', alignItems: 'flex-end', justifyContent: 'center',
      opacity: active || refreshing ? 1 : 0,
      transition: 'opacity .3s',
      pointerEvents: 'none', zIndex: 5,
    }}>
      <svg width="60" height="80" viewBox="0 0 60 80">
        {/* line */}
        <line x1="30" y1="0" x2="30" y2={refreshing ? 50 : 12 + progress * 38}
              stroke="rgba(0,201,167,0.5)" strokeWidth="1" strokeDasharray="2 3" />
        {/* lure */}
        <g style={{
          transform: `translateY(${refreshing ? 50 : 12 + progress * 38}px)`,
          animation: refreshing ? 'tl-lure-bob 1.4s ease-in-out infinite' : 'none',
          transformOrigin: '30px 50px',
        }}>
          <circle cx="30" cy="0" r="5" fill="var(--amber)" style={{ filter: 'drop-shadow(0 0 6px rgba(245,166,35,0.6))' }}/>
          <path d="M30 5 L 27 11 L 33 11 Z" fill="var(--amber)" />
          <path d="M28 12 L 30 18 M 32 12 L 30 18" stroke="var(--amber)" strokeWidth="1" strokeLinecap="round" />
        </g>
        {refreshing && (
          <text x="30" y="74" fontSize="8" fill="var(--teal)" textAnchor="middle"
                fontFamily="JetBrains Mono, monospace" letterSpacing="0.5">FETCHING…</text>
        )}
      </svg>
    </div>
  );
}

function SectionHeader({ title, hint, inset = false }) {
  return (
    <div style={{
      display: 'flex', alignItems: 'baseline', justifyContent: 'space-between',
      padding: inset ? 0 : '0 18px', marginBottom: 8,
    }}>
      <h3 style={{ margin: 0, fontSize: 13, letterSpacing: 1.2, textTransform: 'uppercase',
                   color: 'var(--ink)', fontWeight: 600 }}>{title}</h3>
      <span style={{ fontSize: 10, color: 'var(--muted)', letterSpacing: 1 }}>{hint}</span>
    </div>
  );
}

function StatTilesGrid({ n, intensity, showMotion }) {
  const tiles = [
    { icon: 'wind',    label: 'Wind',      value: `${n.windSpeed}`, unit: 'kt', sub: `${n.windDirLabel} · gust ${n.windGust}`, tone: 'default' },
    { icon: 'wave',    label: 'Swell',     value: `${n.waveHeight}`, unit: 'm', sub: `${n.swellPeriod}s ${n.swellDir}`, tone: 'default' },
    { icon: 'water',   label: 'Water',     value: `${n.waterTemp}`,  unit: '°C', sub: `Air ${n.airTemp}°`, tone: 'default' },
    { icon: 'tide',    label: 'Tide',      value: `${n.tideHeight}`, unit: 'm', sub: `${n.nextTide}`, tone: 'teal' },
    { icon: 'baro',    label: 'Pressure',  value: `${n.barometric}`, unit: 'hPa', sub: null, tone: 'default', pressure: true },
    { icon: 'uv',      label: 'UV',        value: `${n.uv}`,         unit: n.uvLabel, sub: 'Peak 13:20', tone: 'amber' },
  ];
  return (
    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: 8, position: 'relative' }}>
      {tiles.map((t, i) => <StatTile key={i} {...t} intensity={intensity} idx={i} />)}
      <MotionTag shown={showMotion} top={-2} left={-130} bottom={undefined}>
        Cards stagger up<br/>
        translateY 14→0<br/>
        60ms apart · 550ms
      </MotionTag>
    </div>
  );
}

function StatTile({ icon, label, value, unit, sub, tone = 'default', intensity, idx, pressure }) {
  const toneColor = tone === 'teal' ? 'var(--teal)' : tone === 'amber' ? 'var(--amber)' : 'var(--ink)';
  return (
    <TLGlass intensity={intensity} padding={10} style={{ minHeight: 88 }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 6 }}>
        <span style={{ fontSize: 9, letterSpacing: 1, textTransform: 'uppercase', color: 'var(--muted)', fontWeight: 600 }}>
          {label}
        </span>
        <TileIcon kind={icon} color={toneColor} />
      </div>
      <div style={{ display: 'flex', alignItems: 'baseline', gap: 3 }}>
        <span style={{ fontFamily: '"Inter Tight", Inter, system-ui',
                       fontSize: 24, fontWeight: 700, letterSpacing: -1, color: toneColor,
                       fontVariantNumeric: 'tabular-nums' }}>{value}</span>
        <span style={{ fontSize: 10, color: 'var(--muted)', fontWeight: 600 }}>{unit}</span>
      </div>
      {pressure ? (
        <div style={{ marginTop: 4 }}>
          <PressureArrow trend={D.now.barometricTrend} delta={D.now.barometricDelta} />
        </div>
      ) : sub ? (
        <div style={{ marginTop: 4, fontSize: 10, color: 'var(--muted)' }}>{sub}</div>
      ) : null}
    </TLGlass>
  );
}

function TileIcon({ kind, color = 'currentColor', size = 14 }) {
  const stroke = { fill: 'none', stroke: color, strokeWidth: 1.5, strokeLinecap: 'round', strokeLinejoin: 'round' };
  switch (kind) {
    case 'wind':  return <svg width={size} height={size} viewBox="0 0 16 16"><path d="M2 6h7a2 2 0 1 0-2-2M2 10h11a2 2 0 1 1-2 2M2 8h5" {...stroke}/></svg>;
    case 'wave':  return <svg width={size} height={size} viewBox="0 0 16 16"><path d="M1 8c2 -2 4 -2 6 0s4 2 6 0s2 0 2 0M1 12c2 -2 4 -2 6 0s4 2 6 0s2 0 2 0" {...stroke}/></svg>;
    case 'water': return <svg width={size} height={size} viewBox="0 0 16 16"><path d="M8 2c -3 4 -5 7 -5 9a5 5 0 0 0 10 0c0 -2 -2 -5 -5 -9z" {...stroke}/></svg>;
    case 'tide':  return <svg width={size} height={size} viewBox="0 0 16 16"><path d="M1 11h14M3 11l3 -5l4 5l3 -3" {...stroke}/></svg>;
    case 'baro':  return <svg width={size} height={size} viewBox="0 0 16 16"><circle cx="8" cy="8" r="5.5" {...stroke}/><path d="M8 8l3 -3" {...stroke}/></svg>;
    case 'uv':    return <svg width={size} height={size} viewBox="0 0 16 16"><circle cx="8" cy="8" r="3" {...stroke}/><path d="M8 1v2M8 13v2M1 8h2M13 8h2M3 3l1.5 1.5M11.5 11.5L13 13M3 13l1.5 -1.5M11.5 4.5L13 3" {...stroke}/></svg>;
    case 'moon':  return <svg width={size} height={size} viewBox="0 0 16 16"><path d="M11 2a6 6 0 1 0 3 11A5 5 0 0 1 11 2z" {...stroke}/></svg>;
    default: return null;
  }
}

function HourCard({ h, idx, scroll, intensity }) {
  // parallax depth: each card translates based on offset from current scroll
  const cardW = 72, gap = 10;
  const cardCenter = idx * (cardW + gap) + cardW / 2;
  const viewCenter = scroll + 170; // ~half view width
  const offset = (cardCenter - viewCenter);
  const parallax = -offset * 0.05;
  const depth = Math.max(0.7, 1 - Math.abs(offset) / 600);
  const tone = h.score >= 75 ? 'var(--teal)' : h.score >= 55 ? '#7BD4F0' : 'var(--muted)';
  return (
    <div style={{
      scrollSnapAlign: 'start',
      transform: `translateX(${parallax}px) translateZ(0) scale(${depth})`,
      transition: 'transform 80ms linear',
      opacity: depth,
    }}>
      <TLGlass intensity={intensity} padding={10} style={{
        width: cardW, textAlign: 'center', position: 'relative',
        ...(idx === 0 ? { border: '1px solid rgba(245,166,35,0.4)' } : {}),
      }}>
        {idx === 0 && <NowDot />}
        <div style={{ fontSize: 10, color: 'var(--muted)', letterSpacing: 0.5, fontWeight: 600 }}>
          {h.label.toUpperCase()}
        </div>
        <div style={{ margin: '8px 0 4px', display: 'flex', justifyContent: 'center' }}>
          <WeatherIcon cond={h.cond} size={28} />
        </div>
        <div style={{ fontFamily: '"Inter Tight", Inter', fontSize: 18, fontWeight: 700, color: 'var(--ink)' }}>
          {h.temp}°
        </div>
        <div style={{ marginTop: 6, height: 3, background: 'rgba(255,255,255,0.06)', borderRadius: 2, overflow: 'hidden' }}>
          <div style={{ width: `${h.score}%`, height: '100%', background: tone,
                        boxShadow: `0 0 4px ${tone}` }}/>
        </div>
        <div style={{ marginTop: 4, fontSize: 9, color: tone, fontWeight: 600 }}>{h.score}</div>
      </TLGlass>
    </div>
  );
}

function NowDot() {
  return (
    <span style={{
      position: 'absolute', top: -4, right: -4,
      display: 'flex', alignItems: 'center', gap: 3,
      padding: '2px 6px', background: 'var(--amber)',
      color: 'var(--bg)', fontSize: 8, fontWeight: 800, letterSpacing: 0.5,
      borderRadius: 999,
      boxShadow: '0 0 10px rgba(245,166,35,0.7)',
    }}>
      <span style={{ width: 4, height: 4, borderRadius: 999, background: 'var(--bg)',
                     animation: 'tl-pulse 1.4s infinite ease-in-out' }}/>
      NOW
    </span>
  );
}

function DailyRow({ d, highlight, last }) {
  const tone = d.score >= 75 ? 'var(--teal)' : d.score >= 55 ? '#7BD4F0' : 'var(--amber)';
  return (
    <div style={{
      display: 'grid', gridTemplateColumns: '60px 28px 1fr 70px 50px', alignItems: 'center', gap: 10,
      padding: '12px 14px', borderBottom: last ? 'none' : '1px solid rgba(255,255,255,0.04)',
      ...(highlight ? { background: 'linear-gradient(90deg, rgba(0,201,167,0.04), transparent)' } : {}),
    }}>
      <div>
        <div style={{ fontWeight: 600, fontSize: 13, color: 'var(--ink)' }}>{d.day}</div>
        <div style={{ fontSize: 10, color: 'var(--muted)' }}>{d.date}</div>
      </div>
      <WeatherIcon cond={d.cond} size={22} />
      <div style={{ fontSize: 10, color: 'var(--muted)', display: 'flex', alignItems: 'center', gap: 4 }}>
        {d.peakWindow !== '—' && <span style={{ width: 5, height: 5, borderRadius: 999, background: 'var(--amber)', boxShadow: '0 0 6px var(--amber)' }} />}
        {d.peakWindow}
      </div>
      <div style={{ fontSize: 11, color: 'var(--muted)', textAlign: 'right' }}>
        <span style={{ color: 'var(--ink)' }}>{d.hi}°</span> <span>{d.lo}°</span>
      </div>
      <div style={{ textAlign: 'right' }}>
        <span style={{
          display: 'inline-block', padding: '3px 7px', background: `${tone === 'var(--teal)' ? 'rgba(0,201,167,0.15)' : tone === '#7BD4F0' ? 'rgba(123,212,240,0.15)' : 'rgba(245,166,35,0.15)'}`,
          color: tone, borderRadius: 6, fontSize: 11, fontWeight: 700,
          fontVariantNumeric: 'tabular-nums', minWidth: 30, textAlign: 'center',
        }}>{d.score}</span>
      </div>
    </div>
  );
}

// ═════════════════════════════════════════════════════════════
// CONDITIONS DETAIL
// ═════════════════════════════════════════════════════════════
function Conditions({ tweaks }) {
  const intensity = tweaks.glass;
  const showMotion = tweaks.motionLabels;
  const n = D.now;
  return (
    <div style={{ height: '100%', overflowY: 'auto', paddingTop: 56, paddingBottom: 100, color: 'var(--ink)' }}>
      <div style={{ padding: '8px 18px 0' }}>
        <ScreenTitle eyebrow="Detailed conditions" title="Now off Cape Brett" />

        {/* Wind */}
        <StaggerList>
          <TLGlass intensity={intensity} padding={16} style={{ position: 'relative' }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 8 }}>
              <SubTitle icon="wind">Wind</SubTitle>
              <StatPill tone="teal">Light–moderate</StatPill>
            </div>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 14, alignItems: 'center' }}>
              <WindCompass bearing={n.windDir} speed={n.windSpeed} gust={n.windGust} size={150} />
              <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
                <BigMetric value={n.windSpeed} unit="kt" label={`${n.windDirLabel} · ${n.windDir}°`} />
                <SmallStat label="Gust" value={`${n.windGust} kt`} />
                <SmallStat label="6h trend" value="Easing" tone="teal" />
                <SmallStat label="Forecast peak" value="14 kt · 13:00" />
              </div>
            </div>
            <MotionTag shown={showMotion} top={70} right={4}>
              Compass needle<br/>
              Spring k=0.06 d=0.18<br/>
              Overshoots → settles
            </MotionTag>
          </TLGlass>

          {/* Tide */}
          <TLGlass intensity={intensity} padding={16} style={{ position: 'relative' }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 12 }}>
              <SubTitle icon="tide">Tides</SubTitle>
              <span style={{ fontSize: 11, color: 'var(--muted)' }}>Mon 18 May · LINZ</span>
            </div>
            <TideChart data={D.tide} events={D.tideEvents} nowIdx={18} />
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4,1fr)', gap: 4, marginTop: 12 }}>
              {D.tideEvents.map(e => (
                <div key={e.time} style={{ textAlign: 'center', padding: 6, background: 'rgba(255,255,255,0.03)', borderRadius: 8 }}>
                  <div style={{ fontSize: 9, color: 'var(--muted)', letterSpacing: 1 }}>{e.label.toUpperCase()}</div>
                  <div style={{ fontWeight: 700, fontSize: 13, marginTop: 2, fontFamily: '"Inter Tight",Inter' }}>{e.time}</div>
                  <div style={{ fontSize: 9, color: 'var(--teal)' }}>{e.height}m</div>
                </div>
              ))}
            </div>
            <MotionTag shown={showMotion} top={36} left={-100}>
              Tide curve<br/>
              Perpetual SVG path<br/>
              undulation ±3px · 4s loop
            </MotionTag>
          </TLGlass>

          {/* Swell + moon split */}
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 10 }}>
            <TLGlass intensity={intensity} padding={14}>
              <SubTitle icon="wave">Swell</SubTitle>
              <BigMetric value={n.waveHeight} unit="m" label={`${n.swellPeriod}s · ${n.swellDir}`} style={{ marginTop: 6 }} />
              <div style={{ marginTop: 14 }}>
                {/* swell amp meter */}
                <svg width="100%" height="42" viewBox="0 0 100 42" preserveAspectRatio="none">
                  <path d="M0 28 Q 12 18, 25 28 T 50 28 T 75 28 T 100 28 L 100 42 L 0 42 Z" fill="rgba(0,201,167,0.18)"/>
                  <path d="M0 28 Q 12 18, 25 28 T 50 28 T 75 28 T 100 28" fill="none" stroke="var(--teal)" strokeWidth="1.5"
                        style={{ filter: 'drop-shadow(0 0 4px var(--teal))' }}/>
                </svg>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: 4, fontSize: 9, color: 'var(--muted)' }}>
                  <span>Wind wave 0.4m</span><span>Primary 1.2m</span>
                </div>
              </div>
            </TLGlass>
            <TLGlass intensity={intensity} padding={14}>
              <SubTitle icon="moon">Moon</SubTitle>
              <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginTop: 4 }}>
                <MoonPhase illum={n.moonIllum} size={56} />
                <div>
                  <div style={{ fontSize: 13, fontWeight: 600 }}>{n.moonPhase}</div>
                  <div style={{ fontSize: 10, color: 'var(--muted)', marginTop: 2 }}>78% illum.</div>
                </div>
              </div>
              <div style={{ marginTop: 14, fontSize: 10, color: 'var(--muted)' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                  <span>Rise</span><span style={{ color: 'var(--ink)', fontWeight: 600 }}>15:42</span>
                </div>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: 4 }}>
                  <span>Set</span><span style={{ color: 'var(--ink)', fontWeight: 600 }}>04:18</span>
                </div>
              </div>
            </TLGlass>
          </div>

          {/* Pressure */}
          <TLGlass intensity={intensity} padding={16} style={{ position: 'relative' }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
              <SubTitle icon="baro">Barometric pressure</SubTitle>
              <PressureArrow trend={n.barometricTrend} delta={n.barometricDelta} size={20} />
            </div>
            <div style={{ display: 'flex', alignItems: 'baseline', gap: 8, marginTop: 8 }}>
              <span style={{ fontFamily: '"Inter Tight",Inter', fontSize: 38, fontWeight: 700, letterSpacing: -1.5,
                             fontVariantNumeric: 'tabular-nums' }}>{n.barometric}</span>
              <span style={{ color: 'var(--muted)', fontSize: 13 }}>hPa</span>
            </div>
            {/* 24h sparkline */}
            <svg width="100%" height="38" viewBox="0 0 200 38" preserveAspectRatio="none" style={{ marginTop: 8 }}>
              <path d="M0 22 L 20 24 L 40 26 L 60 22 L 80 18 L 100 14 L 120 12 L 140 10 L 160 9 L 180 7 L 200 6"
                    fill="none" stroke="var(--teal)" strokeWidth="1.5"
                    style={{ filter: 'drop-shadow(0 0 4px rgba(0,201,167,0.4))' }}/>
              <circle cx="200" cy="6" r="3" fill="var(--teal)"/>
            </svg>
            <div style={{ marginTop: 4, fontSize: 11, color: 'var(--muted)' }}>
              Rising steadily — classic post-front pattern. Fish typically <span style={{ color: 'var(--teal)' }}>respond well</span> 6–18h after.
            </div>
            <MotionTag shown={showMotion} top={14} right={120}>
              Pressure arrow<br/>
              Rotates -45° (rising)<br/>
              Glow scales w/ |Δ|
            </MotionTag>
          </TLGlass>

          {/* Sun */}
          <TLGlass intensity={intensity} padding={14}>
            <SubTitle icon="uv">Sun & light</SubTitle>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4,1fr)', gap: 6, marginTop: 10 }}>
              {[
                ['Dawn', n.dawn],
                ['Sunrise', n.sunrise],
                ['Sunset', n.sunset],
                ['Dusk', n.dusk],
              ].map(([k, v]) => (
                <div key={k} style={{ textAlign: 'center' }}>
                  <div style={{ fontSize: 9, color: 'var(--muted)', letterSpacing: 1 }}>{k.toUpperCase()}</div>
                  <div style={{ fontWeight: 700, fontSize: 13, marginTop: 2, fontFamily: '"Inter Tight",Inter' }}>{v}</div>
                </div>
              ))}
            </div>
          </TLGlass>
        </StaggerList>
      </div>
    </div>
  );
}

function ScreenTitle({ eyebrow, title }) {
  return (
    <div style={{ marginBottom: 16 }}>
      <div style={{ fontSize: 10, letterSpacing: 1.5, textTransform: 'uppercase', color: 'var(--teal)' }}>{eyebrow}</div>
      <h1 style={{ margin: '4px 0 0', fontSize: 26, fontWeight: 700, letterSpacing: -0.7 }}>{title}</h1>
    </div>
  );
}

function SubTitle({ icon, children }) {
  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
      {icon && <TileIcon kind={icon} size={16} color="var(--teal)" />}
      <h3 style={{ margin: 0, fontSize: 13, letterSpacing: 1.2, textTransform: 'uppercase', fontWeight: 600 }}>{children}</h3>
    </div>
  );
}

function BigMetric({ value, unit, label, style = {} }) {
  return (
    <div style={style}>
      <div style={{ display: 'flex', alignItems: 'baseline', gap: 4 }}>
        <span style={{ fontFamily: '"Inter Tight",Inter', fontSize: 36, fontWeight: 700, letterSpacing: -1.5,
                       fontVariantNumeric: 'tabular-nums' }}>{value}</span>
        <span style={{ color: 'var(--muted)', fontSize: 12 }}>{unit}</span>
      </div>
      {label && <div style={{ fontSize: 11, color: 'var(--muted)', marginTop: -2 }}>{label}</div>}
    </div>
  );
}

function SmallStat({ label, value, tone }) {
  return (
    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center',
                  fontSize: 11, padding: '6px 0', borderTop: '1px solid rgba(255,255,255,0.04)' }}>
      <span style={{ color: 'var(--muted)' }}>{label}</span>
      <span style={{ color: tone === 'teal' ? 'var(--teal)' : 'var(--ink)', fontWeight: 600 }}>{value}</span>
    </div>
  );
}

Object.assign(window, { Dashboard, Conditions, MotionTag, StaggerList, SectionHeader, SubTitle, ScreenTitle, TileIcon });
