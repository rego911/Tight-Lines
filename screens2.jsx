// Tight Lines — Catch Forecast + Settings screens

// ═════════════════════════════════════════════════════════════
// CATCH FORECAST (priority screen)
// ═════════════════════════════════════════════════════════════
function Catch({ tweaks }) {
  const intensity = tweaks.glass;
  const showMotion = tweaks.motionLabels;
  const [activeId, setActiveId] = React.useState('snapper');
  const species = window.TL_DATA.species;
  const active = species.find(s => s.id === activeId) || species[0];

  return (
    <div style={{ height: '100%', overflowY: 'auto', paddingTop: 56, paddingBottom: 100, color: 'var(--ink)' }}>
      <div style={{ padding: '8px 18px 0' }}>
        <ScreenTitle eyebrow="Catch Forecast" title="Bite windows · 24h" />

        {/* Species selector chip row */}
        <div style={{ position: 'relative', margin: '0 -18px' }}>
          <div className="tl-hide-scrollbar" style={{ overflowX: 'auto', padding: '4px 18px 12px' }}>
            <div style={{ display: 'flex', gap: 8 }}>
              {species.map(s => (
                <SpeciesChip key={s.id} sp={s} active={s.id === activeId} onClick={() => setActiveId(s.id)} />
              ))}
            </div>
          </div>
          <MotionTag shown={showMotion} top={-2} right={6}>
            Chip active: fish icon<br/>
            morphs · ring fades in<br/>
            220ms · ease-out
          </MotionTag>
        </div>

        {/* Active species card */}
        <TLGlass intensity={intensity} padding={18} style={{ position: 'relative', marginTop: 4 }}>
          <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', gap: 12 }}>
            <div style={{ flex: 1 }}>
              <div style={{ fontSize: 11, color: 'var(--muted)', letterSpacing: 0.5, fontStyle: 'italic' }}>
                {active.maori}
              </div>
              <h2 style={{ margin: '2px 0 0', fontSize: 24, letterSpacing: -0.6, fontWeight: 700 }}>
                {active.name}
              </h2>
              <div style={{ display: 'flex', gap: 6, marginTop: 8, flexWrap: 'wrap' }}>
                <StatPill>{active.depthRange}</StatPill>
                <StatPill tone={active.conf === 'High' ? 'teal' : 'amber'}>
                  {active.conf} conf.
                </StatPill>
              </div>
            </div>
            {/* Big species score */}
            <ScoreBubble score={active.score} />
          </div>

          {/* Bite timeline */}
          <div style={{ marginTop: 22, position: 'relative' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline', marginBottom: 6 }}>
              <span style={{ fontSize: 11, letterSpacing: 1, textTransform: 'uppercase', color: 'var(--muted)' }}>
                Bite timeline
              </span>
              <span style={{ fontSize: 10, color: 'var(--muted)' }}>00 · 06 · 12 · 18 · 24</span>
            </div>
            <BiteTimeline windows={active.windows} nowHour={9.25} />
            <MotionTag shown={showMotion} top={20} right={-4}>
              Bands fade up<br/>
              left→right wipe<br/>
              900ms cubic-bezier
            </MotionTag>
          </div>

          {/* Forecast note */}
          <div style={{
            marginTop: 16, padding: '10px 12px',
            background: 'rgba(0,201,167,0.06)',
            border: '1px solid rgba(0,201,167,0.18)',
            borderRadius: 12,
            fontSize: 12, lineHeight: 1.45, color: 'rgba(255,255,255,0.85)',
          }}>
            <span style={{ color: 'var(--teal)', fontWeight: 700, marginRight: 6 }}>◆</span>
            {active.note}
          </div>

          {/* Window cards */}
          <div style={{ marginTop: 14 }}>
            <div style={{ fontSize: 11, letterSpacing: 1, textTransform: 'uppercase', color: 'var(--muted)', marginBottom: 6 }}>
              Today's peak windows
            </div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
              {active.windows.filter(w => w.level === 'hot').map((w, i) => (
                <PeakWindow key={i} window={w} />
              ))}
              {active.windows.filter(w => w.level === 'hot').length === 0 && (
                <div style={{ fontSize: 12, color: 'var(--muted)', fontStyle: 'italic', padding: '6px 0' }}>
                  No peak windows today — consider rescheduling or fishing deeper structure.
                </div>
              )}
            </div>
          </div>
        </TLGlass>

        {/* All species mini-rankings */}
        <div style={{ marginTop: 24 }}>
          <SectionHeader title="Other species" hint="Tap to switch" inset />
          <div style={{ display: 'flex', flexDirection: 'column', gap: 6, marginTop: 10 }}>
            {species.filter(s => s.id !== activeId).map(s => (
              <SpeciesRow key={s.id} sp={s} onClick={() => setActiveId(s.id)} intensity={intensity} />
            ))}
          </div>
        </div>

        {/* Methodology note */}
        <div style={{ marginTop: 22, fontSize: 10, color: 'rgba(255,255,255,0.3)', lineHeight: 1.6, padding: '0 4px' }}>
          Bite scores combine solunar tables, barometric movement, tidal flow,
          water temp vs species range, and 5y historical catch data. ±15% variance.
        </div>
      </div>
    </div>
  );
}

function SpeciesChip({ sp, active, onClick }) {
  const ring = active ? 'var(--teal)' : 'rgba(255,255,255,0.08)';
  const bg = active ? 'rgba(0,201,167,0.13)' : 'rgba(255,255,255,0.03)';
  return (
    <button onClick={onClick} style={{
      flexShrink: 0, display: 'flex', alignItems: 'center', gap: 8,
      padding: '8px 12px 8px 10px',
      background: bg, border: `1px solid ${ring}`,
      borderRadius: 999, cursor: 'pointer', color: 'inherit',
      transition: 'all .22s ease',
      transform: active ? 'translateY(-1px)' : 'none',
      boxShadow: active ? '0 4px 12px -4px rgba(0,201,167,0.5)' : 'none',
      fontFamily: 'Inter, system-ui',
    }}>
      <FishIcon id={sp.id} width={28} color={active ? 'var(--teal)' : 'rgba(255,255,255,0.55)'} active={active}/>
      <span style={{ fontSize: 12, fontWeight: 600, color: active ? 'var(--ink)' : 'var(--muted)' }}>
        {sp.name}
      </span>
      <span style={{
        fontSize: 10, fontWeight: 700,
        color: active ? 'var(--teal)' : 'rgba(255,255,255,0.4)',
        fontVariantNumeric: 'tabular-nums',
      }}>{sp.score}</span>
    </button>
  );
}

function ScoreBubble({ score }) {
  const tone = score >= 80 ? 'var(--teal)' : score >= 60 ? '#7BD4F0' : 'var(--amber)';
  return (
    <div style={{
      width: 70, height: 70, borderRadius: 999, position: 'relative',
      display: 'flex', alignItems: 'center', justifyContent: 'center',
      background: 'radial-gradient(circle at 30% 30%, rgba(255,255,255,0.06), transparent 60%)',
      border: `1.5px solid ${tone}`,
      boxShadow: `0 0 18px ${tone}55, inset 0 0 14px rgba(255,255,255,0.04)`,
      flexShrink: 0,
    }}>
      <div style={{ textAlign: 'center' }}>
        <div style={{ fontFamily: '"Inter Tight",Inter', fontSize: 26, fontWeight: 700, color: tone,
                      letterSpacing: -1, fontVariantNumeric: 'tabular-nums', lineHeight: 1 }}>
          {score}
        </div>
        <div style={{ fontSize: 8, color: 'var(--muted)', letterSpacing: 1, marginTop: 2 }}>SCORE</div>
      </div>
    </div>
  );
}

function BiteTimeline({ windows, nowHour = 9.25 }) {
  const colors = {
    hot:  { bg: 'linear-gradient(180deg, rgba(0,201,167,0.85), rgba(0,201,167,0.45))', glow: 'rgba(0,201,167,0.55)', label: 'HOT' },
    warm: { bg: 'linear-gradient(180deg, rgba(123,212,240,0.7), rgba(123,212,240,0.35))', glow: 'rgba(123,212,240,0.4)', label: 'WARM' },
    slow: { bg: 'linear-gradient(180deg, rgba(255,255,255,0.06), rgba(255,255,255,0.02))', glow: 'transparent', label: 'SLOW' },
  };
  return (
    <div style={{ position: 'relative' }}>
      {/* timeline track */}
      <div style={{
        position: 'relative', height: 56,
        background: 'rgba(255,255,255,0.03)', borderRadius: 10,
        overflow: 'hidden', border: '1px solid rgba(255,255,255,0.05)',
      }}>
        {/* hour ticks */}
        {[0,6,12,18,24].map(h => (
          <div key={h} style={{ position: 'absolute', top: 0, bottom: 0, left: `${(h/24)*100}%`,
                                 width: 1, background: 'rgba(255,255,255,0.06)' }} />
        ))}
        {/* bands */}
        {windows.map((w, i) => {
          const c = colors[w.level] || colors.slow;
          const left = (w.start / 24) * 100;
          const width = ((w.end - w.start) / 24) * 100;
          return (
            <div key={i} style={{
              position: 'absolute', left: `${left}%`, width: `${width}%`,
              top: 8, bottom: 8, borderRadius: 4,
              background: c.bg,
              boxShadow: `0 0 12px ${c.glow}`,
              animation: `tl-band-in .9s cubic-bezier(.21,.61,.35,1) ${i * 0.06}s both`,
              transformOrigin: 'left center',
            }} />
          );
        })}
        {/* NOW indicator */}
        <div style={{
          position: 'absolute', top: -4, bottom: -4, left: `${(nowHour/24)*100}%`,
          width: 2, background: 'var(--amber)',
          boxShadow: '0 0 12px var(--amber)',
        }}>
          <div style={{
            position: 'absolute', top: -10, left: '50%', transform: 'translateX(-50%)',
            background: 'var(--amber)', color: 'var(--bg)',
            fontSize: 8, fontWeight: 800, padding: '2px 5px', borderRadius: 3,
            letterSpacing: 0.5,
          }}>NOW</div>
        </div>
      </div>
      {/* axis */}
      <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: 4,
                    fontSize: 9, color: 'var(--muted)', letterSpacing: 0.5,
                    fontFamily: 'JetBrains Mono, monospace' }}>
        <span>00</span><span>06</span><span>12</span><span>18</span><span>24</span>
      </div>
      {/* legend */}
      <div style={{ display: 'flex', gap: 14, marginTop: 8, justifyContent: 'center' }}>
        {['hot','warm','slow'].map(k => {
          const c = colors[k];
          return (
            <div key={k} style={{ display: 'flex', alignItems: 'center', gap: 5 }}>
              <span style={{ width: 8, height: 8, borderRadius: 2, background: c.bg,
                             boxShadow: `0 0 4px ${c.glow}` }} />
              <span style={{ fontSize: 9, color: 'var(--muted)', letterSpacing: 1 }}>{c.label}</span>
            </div>
          );
        })}
      </div>
    </div>
  );
}

function PeakWindow({ window: w }) {
  const fmt = (h) => {
    const hr = Math.floor(h);
    const mn = Math.round((h - hr) * 60);
    return `${String(hr).padStart(2,'0')}:${String(mn).padStart(2,'0')}`;
  };
  const dur = w.end - w.start;
  return (
    <div style={{
      display: 'flex', alignItems: 'center', gap: 10,
      padding: '8px 12px', borderRadius: 10,
      background: 'rgba(0,201,167,0.06)',
      border: '1px solid rgba(0,201,167,0.18)',
    }}>
      <span style={{ width: 6, height: 32, background: 'var(--teal)', borderRadius: 3,
                     boxShadow: '0 0 6px var(--teal)' }}/>
      <div style={{ flex: 1 }}>
        <div style={{ fontFamily: '"Inter Tight",Inter', fontWeight: 700, fontSize: 16, letterSpacing: -0.3 }}>
          {fmt(w.start)} – {fmt(w.end)}
        </div>
        <div style={{ fontSize: 10, color: 'var(--muted)' }}>
          {Math.round(dur * 60)} min · solunar major
        </div>
      </div>
      <button style={{
        background: 'rgba(0,201,167,0.15)', border: '1px solid rgba(0,201,167,0.4)',
        color: 'var(--teal)', fontSize: 10, fontWeight: 700,
        padding: '5px 10px', borderRadius: 999, letterSpacing: 0.8,
        cursor: 'pointer', textTransform: 'uppercase',
      }}>Remind</button>
    </div>
  );
}

function SpeciesRow({ sp, onClick, intensity }) {
  const tone = sp.score >= 75 ? 'var(--teal)' : sp.score >= 60 ? '#7BD4F0' : 'var(--amber)';
  return (
    <button onClick={onClick} style={{
      display: 'grid', gridTemplateColumns: '40px 1fr auto auto', gap: 10, alignItems: 'center',
      width: '100%', padding: '10px 12px',
      background: 'rgba(255,255,255,0.025)',
      border: '1px solid rgba(255,255,255,0.05)',
      borderRadius: 12, cursor: 'pointer', color: 'inherit',
      textAlign: 'left', fontFamily: 'Inter, system-ui',
    }}>
      <FishIcon id={sp.id} width={36} color="rgba(255,255,255,0.55)" />
      <div>
        <div style={{ fontSize: 13, fontWeight: 600 }}>{sp.name}</div>
        <div style={{ fontSize: 10, color: 'var(--muted)' }}>{sp.maori}</div>
      </div>
      <div style={{ display: 'flex', gap: 1.5, alignItems: 'flex-end' }}>
        {sp.windows.slice(0, 10).map((w, i) => {
          const c = w.level === 'hot' ? 'var(--teal)' : w.level === 'warm' ? '#7BD4F0' : 'rgba(255,255,255,0.15)';
          return <span key={i} style={{ width: 3, height: w.level === 'hot' ? 18 : w.level === 'warm' ? 12 : 6, background: c, borderRadius: 1, boxShadow: w.level !== 'slow' ? `0 0 3px ${c}` : 'none' }}/>;
        })}
      </div>
      <span style={{
        minWidth: 30, textAlign: 'center', padding: '4px 8px', borderRadius: 6,
        background: tone === 'var(--teal)' ? 'rgba(0,201,167,0.13)' : tone === '#7BD4F0' ? 'rgba(123,212,240,0.13)' : 'rgba(245,166,35,0.13)',
        color: tone, fontWeight: 700, fontSize: 12, fontVariantNumeric: 'tabular-nums',
      }}>{sp.score}</span>
    </button>
  );
}

// ═════════════════════════════════════════════════════════════
// SETTINGS / LOCATION
// ═════════════════════════════════════════════════════════════
function Settings({ tweaks }) {
  const intensity = tweaks.glass;
  const [q, setQ] = React.useState('');
  const D = window.TL_DATA;
  return (
    <div style={{ height: '100%', overflowY: 'auto', paddingTop: 56, paddingBottom: 100, color: 'var(--ink)' }}>
      <div style={{ padding: '8px 18px 0' }}>
        <ScreenTitle eyebrow="Settings" title="Spots & preferences" />

        {/* Search */}
        <div style={{
          position: 'relative', marginBottom: 14,
          background: 'rgba(255,255,255,0.04)',
          border: '1px solid rgba(255,255,255,0.08)',
          borderRadius: 14, padding: '10px 14px',
          display: 'flex', alignItems: 'center', gap: 10,
        }}>
          <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
            <circle cx="7" cy="7" r="5" stroke="var(--muted)" strokeWidth="1.5"/>
            <path d="M11 11l3 3" stroke="var(--muted)" strokeWidth="1.5" strokeLinecap="round"/>
          </svg>
          <input value={q} onChange={e => setQ(e.target.value)} placeholder="Search a spot or coordinates"
                 style={{ flex: 1, background: 'transparent', border: 'none', outline: 'none',
                          color: 'var(--ink)', fontSize: 14, fontFamily: 'inherit' }}/>
          <span style={{ fontSize: 9, padding: '2px 6px', background: 'rgba(255,255,255,0.06)',
                         color: 'var(--muted)', borderRadius: 4, fontFamily: 'JetBrains Mono, monospace' }}>⌘K</span>
        </div>

        {/* Map fragment */}
        <TLGlass intensity={intensity} padding={0} style={{ overflow: 'hidden', marginBottom: 16 }}>
          <DarkMap />
          <div style={{ padding: '12px 14px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <div>
              <div style={{ fontSize: 12, fontWeight: 600, letterSpacing: -0.2 }}>{D.location.name}</div>
              <div style={{ fontSize: 10, color: 'var(--muted)', fontFamily: 'JetBrains Mono, monospace', marginTop: 2 }}>
                35.18°S · 174.33°E
              </div>
            </div>
            <StatPill tone="teal">Active</StatPill>
          </div>
        </TLGlass>

        {/* Recent locations */}
        <SectionHeader title="Recent spots" hint="Tap to switch" inset />
        <div style={{ marginTop: 8, display: 'flex', flexDirection: 'column', gap: 6 }}>
          {D.recentLocations.map((loc, i) => (
            <LocationRow key={i} loc={loc} active={i === 0} />
          ))}
        </div>

        {/* Preferences */}
        <div style={{ marginTop: 22 }}>
          <SectionHeader title="Preferences" hint="" inset />
          <TLGlass intensity={intensity} padding={0} style={{ marginTop: 8 }}>
            <PrefRow label="Units" value="Metric · kt · °C" />
            <PrefRow label="Time format" value="24-hour" />
            <PrefRow label="Tide datum" value="LAT (Lowest Astron.)" />
            <PrefRow label="Notifications" value="2 active" tone="teal" />
            <PrefRow label="Watch face" value="Score + tide" last />
          </TLGlass>
        </div>

        {/* Footer */}
        <div style={{ padding: '24px 0 8px', textAlign: 'center', fontSize: 10, color: 'rgba(255,255,255,0.25)', letterSpacing: 1.5 }}>
          TIGHT LINES · v2.4 · MADE IN AOTEAROA
        </div>
      </div>
    </div>
  );
}

function DarkMap() {
  // Stylised dark map fragment — land mass (Bay of Islands)
  return (
    <div style={{ position: 'relative', height: 180, background: '#070C19', overflow: 'hidden' }}>
      <svg width="100%" height="100%" viewBox="0 0 400 180" preserveAspectRatio="xMidYMid slice">
        <defs>
          <pattern id="tl-map-grid" width="36" height="36" patternUnits="userSpaceOnUse">
            <path d="M36 0H0V36" fill="none" stroke="rgba(0,201,167,0.06)" strokeWidth="0.5"/>
          </pattern>
          <radialGradient id="tl-map-vignette" cx="50%" cy="50%" r="60%">
            <stop offset="0%" stopColor="rgba(0,201,167,0.1)"/>
            <stop offset="100%" stopColor="rgba(0,0,0,0)"/>
          </radialGradient>
        </defs>
        <rect width="400" height="180" fill="url(#tl-map-grid)"/>
        <rect width="400" height="180" fill="url(#tl-map-vignette)"/>
        {/* land */}
        <path d="M-10 100 Q 50 80, 110 90 Q 160 100, 200 70 Q 260 50, 310 80 Q 350 100, 410 70 L 410 -10 L -10 -10 Z"
              fill="rgba(255,255,255,0.04)" stroke="rgba(0,201,167,0.25)" strokeWidth="0.8"/>
        <path d="M30 130 Q 50 110, 70 130 Q 90 145, 80 160 Q 60 175, 40 165 Q 20 155, 30 130 Z"
              fill="rgba(255,255,255,0.05)" stroke="rgba(0,201,167,0.18)" strokeWidth="0.6"/>
        <path d="M150 140 Q 165 135, 175 145 Q 175 158, 160 162 Q 145 155, 150 140 Z"
              fill="rgba(255,255,255,0.05)" stroke="rgba(0,201,167,0.18)" strokeWidth="0.6"/>
        {/* depth contours */}
        <path d="M0 130 Q 80 140, 160 130 T 320 135 T 400 130" fill="none" stroke="rgba(0,201,167,0.15)" strokeWidth="0.5" strokeDasharray="3 4"/>
        <path d="M0 155 Q 80 165, 160 155 T 320 160 T 400 155" fill="none" stroke="rgba(0,201,167,0.1)" strokeWidth="0.5" strokeDasharray="3 4"/>
        {/* compass */}
        <g transform="translate(360, 28)">
          <circle r="14" fill="none" stroke="rgba(255,255,255,0.2)" strokeWidth="0.8"/>
          <path d="M0 -10 L 3 0 L 0 10 L -3 0 Z" fill="var(--amber)"/>
          <text y="-16" textAnchor="middle" fontSize="7" fill="var(--amber)" fontFamily="Inter">N</text>
        </g>
        {/* marker */}
        <g transform="translate(220, 130)">
          <circle r="18" fill="rgba(245,166,35,0.18)">
            <animate attributeName="r" values="18;26;18" dur="2.4s" repeatCount="indefinite"/>
            <animate attributeName="opacity" values="0.6;0.1;0.6" dur="2.4s" repeatCount="indefinite"/>
          </circle>
          <circle r="6" fill="var(--amber)" stroke="white" strokeWidth="1.5"
                  style={{ filter: 'drop-shadow(0 0 6px var(--amber))' }}/>
        </g>
        {/* scale bar */}
        <g transform="translate(16, 158)">
          <rect width="40" height="2" fill="rgba(255,255,255,0.4)"/>
          <text y="-4" fontSize="7" fill="rgba(255,255,255,0.5)" fontFamily="JetBrains Mono, monospace">2 NM</text>
        </g>
      </svg>
    </div>
  );
}

function LocationRow({ loc, active }) {
  const tone = loc.score >= 75 ? 'var(--teal)' : loc.score >= 60 ? '#7BD4F0' : 'var(--amber)';
  return (
    <button style={{
      display: 'flex', alignItems: 'center', gap: 10, width: '100%',
      padding: '10px 12px',
      background: active ? 'rgba(0,201,167,0.06)' : 'rgba(255,255,255,0.025)',
      border: active ? '1px solid rgba(0,201,167,0.25)' : '1px solid rgba(255,255,255,0.05)',
      borderRadius: 12, color: 'inherit', textAlign: 'left', cursor: 'pointer',
      fontFamily: 'Inter, system-ui',
    }}>
      <div style={{
        width: 28, height: 28, borderRadius: 8,
        background: 'rgba(255,255,255,0.04)',
        display: 'flex', alignItems: 'center', justifyContent: 'center',
        border: '1px solid rgba(255,255,255,0.06)',
      }}>
        {loc.favourite ? (
          <svg width="14" height="14" viewBox="0 0 16 16" fill="var(--amber)">
            <path d="M8 1l2 4.5 5 .6-3.7 3.4 1 5L8 12l-4.3 2.5 1-5L1 6.1l5-.6L8 1z"/>
          </svg>
        ) : (
          <svg width="12" height="14" viewBox="0 0 12 14" fill="none">
            <path d="M6 1C3.8 1 2 2.8 2 5c0 3 4 8 4 8s4-5 4-8c0-2.2-1.8-4-4-4z" stroke="var(--muted)" strokeWidth="1"/>
            <circle cx="6" cy="5" r="1.5" fill="var(--muted)"/>
          </svg>
        )}
      </div>
      <div style={{ flex: 1 }}>
        <div style={{ fontSize: 13, fontWeight: 600 }}>{loc.name}</div>
        <div style={{ fontSize: 10, color: 'var(--muted)' }}>{loc.region}</div>
      </div>
      <span style={{
        padding: '3px 7px', borderRadius: 6, fontSize: 11, fontWeight: 700,
        color: tone, background: tone === 'var(--teal)' ? 'rgba(0,201,167,0.13)' : tone === '#7BD4F0' ? 'rgba(123,212,240,0.13)' : 'rgba(245,166,35,0.13)',
      }}>{loc.score}</span>
    </button>
  );
}

function PrefRow({ label, value, tone, last }) {
  return (
    <div style={{
      display: 'flex', justifyContent: 'space-between', alignItems: 'center',
      padding: '14px 16px', borderBottom: last ? 'none' : '1px solid rgba(255,255,255,0.04)',
    }}>
      <span style={{ fontSize: 13, color: 'var(--ink)' }}>{label}</span>
      <span style={{ display: 'inline-flex', alignItems: 'center', gap: 6, fontSize: 12,
                     color: tone === 'teal' ? 'var(--teal)' : 'var(--muted)' }}>
        {value}
        <svg width="6" height="10" viewBox="0 0 6 10"><path d="M1 1l4 4-4 4" stroke="var(--muted)" strokeWidth="1.4" fill="none" strokeLinecap="round"/></svg>
      </span>
    </div>
  );
}

Object.assign(window, { Catch, Settings });
