// Tight Lines — main App: routing, bottom nav, tweaks panel

const TWEAK_DEFAULTS = /*EDITMODE-BEGIN*/{
  "glass": "frosted",
  "mode": "night",
  "gauge": "arc",
  "motionLabels": false
}/*EDITMODE-END*/;

function App() {
  const [screen, setScreen] = React.useState('dashboard');
  const [tweaks, setTweak] = window.useTweaks(TWEAK_DEFAULTS);

  // apply day/night CSS variables
  React.useEffect(() => {
    const root = document.documentElement;
    if (tweaks.mode === 'predawn') {
      root.style.setProperty('--bg',  '#1A1320');
      root.style.setProperty('--bg-2','#2A1B2C');
      root.style.setProperty('--bg-grad', 'radial-gradient(ellipse 100% 50% at 50% 0%, #3A2235, #1A1320 70%)');
    } else {
      root.style.setProperty('--bg',  '#0A0F1E');
      root.style.setProperty('--bg-2','#101830');
      root.style.setProperty('--bg-grad', 'radial-gradient(ellipse 100% 60% at 50% -10%, #102540, #0A0F1E 70%)');
    }
  }, [tweaks.mode]);

  const screens = {
    dashboard: <Dashboard tweaks={tweaks} />,
    conditions: <Conditions tweaks={tweaks} />,
    catch: <Catch tweaks={tweaks} />,
    settings: <Settings tweaks={tweaks} />,
  };

  return (
    <div style={{
      width: '100%', height: '100%', position: 'relative',
      background: 'var(--bg-grad), var(--bg)',
      backgroundBlendMode: 'normal',
      fontFamily: 'Inter, system-ui, sans-serif',
      color: 'var(--ink)',
      overflow: 'hidden',
    }}>
      <div key={screen} style={{
        position: 'absolute', inset: 0,
        animation: 'tl-screen-in .4s cubic-bezier(.21,.61,.35,1)',
      }}>
        {screens[screen]}
      </div>
      <BottomNav active={screen} onChange={setScreen} />

      <window.TweaksPanel title="Tweaks" defaultPosition={{ right: 20, bottom: 100 }}>
        <window.TweakSection label="Surface">
          <window.TweakRadio
            label="Glass"
            value={tweaks.glass}
            onChange={v => setTweak('glass', v)}
            options={[{ value: 'frosted', label: 'Frosted' }, { value: 'flat', label: 'Flat' }]}
          />
        </window.TweakSection>
        <window.TweakSection label="Mode">
          <window.TweakRadio
            label="Theme"
            value={tweaks.mode}
            onChange={v => setTweak('mode', v)}
            options={[{ value: 'night', label: 'Deep navy' }, { value: 'predawn', label: 'Predawn' }]}
          />
        </window.TweakSection>
        <window.TweakSection label="Gauge">
          <window.TweakRadio
            label="Style"
            value={tweaks.gauge}
            onChange={v => setTweak('gauge', v)}
            options={[
              { value: 'arc', label: 'Arc' },
              { value: 'liquid', label: 'Liquid' },
              { value: 'segmented', label: 'Segments' },
            ]}
          />
        </window.TweakSection>
        <window.TweakSection label="Annotations">
          <window.TweakToggle
            label="Motion specs overlay"
            value={tweaks.motionLabels}
            onChange={v => setTweak('motionLabels', v)}
          />
        </window.TweakSection>
        <div style={{ marginTop: 10, fontSize: 10, color: 'rgba(255,255,255,0.4)', lineHeight: 1.5 }}>
          Style guide:&nbsp;
          <a href="style-guide.html" target="_blank" style={{ color: 'var(--teal)' }}>open ↗</a>
        </div>
      </window.TweaksPanel>
    </div>
  );
}

function ScreenTransition({ children, screenKey }) {
  return (
    <div key={screenKey} style={{
      position: 'absolute', inset: 0,
      animation: 'tl-screen-in .4s cubic-bezier(.21,.61,.35,1)',
    }}>
      {children}
    </div>
  );
}

// ─────────────────────────────────────────────────────────────
// Bottom Nav — icon morphs + label fade on active state
// ─────────────────────────────────────────────────────────────
function BottomNav({ active, onChange }) {
  const items = [
    { id: 'dashboard',  label: 'Today',      icon: NavHomeIcon },
    { id: 'conditions', label: 'Conditions', icon: NavConditionsIcon },
    { id: 'catch',      label: 'Catch',      icon: NavCatchIcon },
    { id: 'settings',   label: 'Spots',      icon: NavSpotsIcon },
  ];
  return (
    <div style={{
      position: 'absolute', left: 12, right: 12, bottom: 18, zIndex: 50,
      borderRadius: 24,
      background: 'rgba(10,15,30,0.65)',
      backdropFilter: 'blur(22px) saturate(160%)',
      WebkitBackdropFilter: 'blur(22px) saturate(160%)',
      border: '1px solid rgba(255,255,255,0.08)',
      boxShadow: '0 16px 40px -16px rgba(0,0,0,0.7), inset 0 1px 0 rgba(255,255,255,0.06)',
      padding: '8px 8px',
      display: 'flex', gap: 2,
    }}>
      {items.map(it => {
        const on = active === it.id;
        const Icon = it.icon;
        return (
          <button key={it.id} onClick={() => onChange(it.id)} style={{
            flex: 1, background: 'transparent', border: 'none', cursor: 'pointer',
            padding: '8px 4px',
            display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 4,
            color: on ? 'var(--teal)' : 'rgba(255,255,255,0.55)',
            position: 'relative',
            fontFamily: 'Inter, system-ui',
          }}>
            {on && (
              <span style={{
                position: 'absolute', top: 3, left: '50%', transform: 'translateX(-50%)',
                width: 24, height: 3, borderRadius: 2,
                background: 'var(--teal)',
                boxShadow: '0 0 8px var(--teal)',
                animation: 'tl-pop .35s cubic-bezier(.34,1.56,.64,1)',
              }}/>
            )}
            <Icon active={on} />
            <span style={{
              fontSize: 9.5, letterSpacing: 0.5, fontWeight: on ? 700 : 500,
              opacity: on ? 1 : 0.75,
              transform: on ? 'translateY(0)' : 'translateY(1px)',
              transition: 'all .25s ease',
            }}>{it.label}</span>
          </button>
        );
      })}
    </div>
  );
}

// Bottom nav icons — morph slightly when active (stroke→fill)
function NavHomeIcon({ active }) {
  return (
    <svg width="22" height="22" viewBox="0 0 22 22" fill="none">
      <path d="M3 11l8-6 8 6v8a1 1 0 0 1-1 1h-4v-5h-6v5H4a1 1 0 0 1-1-1v-8z"
            stroke="currentColor" strokeWidth="1.6" strokeLinejoin="round"
            fill={active ? 'currentColor' : 'transparent'}
            fillOpacity={active ? 0.18 : 0}
            style={{ transition: 'fill-opacity .25s ease' }}/>
    </svg>
  );
}
function NavConditionsIcon({ active }) {
  return (
    <svg width="22" height="22" viewBox="0 0 22 22" fill="none">
      <circle cx="11" cy="9" r="3" stroke="currentColor" strokeWidth="1.6"
              fill={active ? 'currentColor' : 'transparent'} fillOpacity={active ? 0.2 : 0}/>
      <path d="M3 16c2 -2 4 -2 6 0s4 2 6 0s2 0 2 0M3 19c2 -2 4 -2 6 0s4 2 6 0s2 0 2 0" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" fill="none"/>
    </svg>
  );
}
function NavCatchIcon({ active }) {
  return (
    <svg width="26" height="22" viewBox="0 0 26 22" fill={active ? 'currentColor' : 'none'}>
      <path d="M2 11 Q 7 5, 18 6 Q 22 7, 24 11 Q 22 15, 18 16 Q 7 17, 2 11 L 0 7 L 3 11 L 0 15 Z"
            stroke="currentColor" strokeWidth="1.6" strokeLinejoin="round"
            fillOpacity={active ? 0.18 : 0}/>
      <circle cx="19" cy="10" r="0.9" fill={active ? 'var(--bg)' : 'currentColor'}/>
    </svg>
  );
}
function NavSpotsIcon({ active }) {
  return (
    <svg width="22" height="22" viewBox="0 0 22 22" fill="none">
      <path d="M11 2C7.7 2 5 4.7 5 8c0 4.5 6 11 6 11s6-6.5 6-11c0-3.3-2.7-6-6-6z"
            stroke="currentColor" strokeWidth="1.6" strokeLinejoin="round"
            fill={active ? 'currentColor' : 'transparent'} fillOpacity={active ? 0.18 : 0}/>
      <circle cx="11" cy="8" r="2.4" stroke="currentColor" strokeWidth="1.6" fill={active ? 'var(--bg)' : 'transparent'}/>
    </svg>
  );
}

window.App = App;
