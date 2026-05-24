#!/usr/bin/env python3
"""patch6.py — wire prefs to app + fix nearby spots"""

PATH = '/sessions/cool-nifty-clarke/mnt/outputs/index.html'

with open(PATH, 'r', encoding='utf-8') as f:
    src = f.read()

orig_len = len(src)
changes = []

def rep(old, new, label):
    global src
    if old not in src:
        raise ValueError(f"PATTERN NOT FOUND: {label}\n  -> {repr(old[:120])}")
    c = src.count(old)
    if c > 1:
        raise ValueError(f"AMBIGUOUS ({c} matches): {label}")
    src = src.replace(old, new)
    changes.append(label)
    print(f"  ✓ {label}")

print("=== patch6: prefs wiring + nearby spots fix ===")

# ─────────────────────────────────────────────────────────────────────────────
# A1: Add prefs state to App
# ─────────────────────────────────────────────────────────────────────────────
rep(
    "  const [userGeoLoc, setUserGeoLoc] = React.useState(null);",
    (
        "  const [userGeoLoc, setUserGeoLoc] = React.useState(null);\n"
        "  const [prefs, setPrefs] = React.useState({\n"
        "    'Units': 'Metric · kt · °C', 'Time format': '24-hour',\n"
        "    'Tide datum': 'LAT (Lowest Astron.)', 'Notifications': '2 active', 'Watch face': 'Score + tide',\n"
        "  });\n"
        "  const handlePrefsChange = (label, value) => setPrefs(p => ({ ...p, [label]: value }));"
    ),
    "A1-prefs-state-in-App"
)

# ─────────────────────────────────────────────────────────────────────────────
# A2: Pass prefs to Dashboard
# ─────────────────────────────────────────────────────────────────────────────
rep(
    "    dashboard:  <Dashboard tweaks={tweaks} activeLocation={activeLocation} onLocationSelect={handleLocationSelect} setUserGeoLoc={setUserGeoLoc} />,",
    "    dashboard:  <Dashboard tweaks={tweaks} activeLocation={activeLocation} onLocationSelect={handleLocationSelect} setUserGeoLoc={setUserGeoLoc} prefs={prefs} />,",
    "A2-dashboard-gets-prefs"
)

# ─────────────────────────────────────────────────────────────────────────────
# A3a: Pass prefs to Conditions
# ─────────────────────────────────────────────────────────────────────────────
rep(
    "    conditions: <Conditions tweaks={tweaks} activeLocation={activeLocation} />,",
    "    conditions: <Conditions tweaks={tweaks} activeLocation={activeLocation} prefs={prefs} />,",
    "A3a-conditions-gets-prefs"
)

# ─────────────────────────────────────────────────────────────────────────────
# A3b: Pass prefs+onPrefsChange to Settings
# ─────────────────────────────────────────────────────────────────────────────
rep(
    "    settings:   <Settings tweaks={tweaks} onLocationSelect={handleLocationSelect} activeLocation={activeLocation} userGeoLoc={userGeoLoc} setUserGeoLoc={setUserGeoLoc} />,",
    "    settings:   <Settings tweaks={tweaks} onLocationSelect={handleLocationSelect} activeLocation={activeLocation} userGeoLoc={userGeoLoc} setUserGeoLoc={setUserGeoLoc} prefs={prefs} onPrefsChange={handlePrefsChange} />,",
    "A3b-settings-gets-prefs"
)

# ─────────────────────────────────────────────────────────────────────────────
# A4: Dashboard — accept prefs prop, derive gaugeVariant from Watch face
# ─────────────────────────────────────────────────────────────────────────────
rep(
    (
        "function Dashboard({ tweaks, activeLocation, onLocationSelect, setUserGeoLoc }) {\n"
        "  const D = React.useContext(LocationDataCtx);\n"
        "  const intensity = tweaks.glass;\n"
        "  const showMotion = tweaks.motionLabels;\n"
        "  const gaugeVariant = tweaks.gauge;"
    ),
    (
        "function Dashboard({ tweaks, activeLocation, onLocationSelect, setUserGeoLoc, prefs }) {\n"
        "  const D = React.useContext(LocationDataCtx);\n"
        "  const intensity = tweaks.glass;\n"
        "  const showMotion = tweaks.motionLabels;\n"
        "  const _watchFace = prefs ? prefs['Watch face'] : 'Score + tide';\n"
        "  const gaugeVariant = _watchFace === 'Wind + swell' ? 'wind' : _watchFace === 'Full dashboard' ? 'arc' : tweaks.gauge;"
    ),
    "A4-Dashboard-prefs-gaugeVariant"
)

# ─────────────────────────────────────────────────────────────────────────────
# A5: Dashboard — pass prefs to StatTilesGrid
# ─────────────────────────────────────────────────────────────────────────────
rep(
    "          <StatTilesGrid n={n} intensity={intensity} showMotion={showMotion} />",
    "          <StatTilesGrid n={n} intensity={intensity} showMotion={showMotion} prefs={prefs} />",
    "A5-StatTilesGrid-gets-prefs"
)

# ─────────────────────────────────────────────────────────────────────────────
# A6: StatTilesGrid — accept prefs, apply unit conversions
# ─────────────────────────────────────────────────────────────────────────────
rep(
    (
        "function StatTilesGrid({ n, intensity, showMotion }) {\n"
        "  const tiles = [\n"
        "    { icon: 'wind',    label: 'Wind',      value: `${n.windSpeed}`, unit: 'kt', sub: `${n.windDirLabel} · gust ${n.windGust}`, tone: 'default' },\n"
        "    { icon: 'wave',    label: 'Swell',     value: `${n.waveHeight}`, unit: 'm', sub: `${n.swellPeriod}s ${n.swellDir}`, tone: 'default' },\n"
        "    { icon: 'water',   label: 'Water',     value: `${n.waterTemp}`,  unit: '°C', sub: `Air ${n.airTemp}°`, tone: 'default' },\n"
        "    { icon: 'tide',    label: 'Tide',      value: `${n.tideHeight}`, unit: 'm', sub: `${n.nextTide}`, tone: 'teal' },\n"
        "    { icon: 'baro',    label: 'Pressure',  value: `${n.barometric}`, unit: 'hPa', sub: null, tone: 'default', pressure: true, trend: n.barometricTrend, delta: n.barometricDelta },\n"
        "    { icon: 'uv',      label: 'UV',        value: `${n.uv}`,         unit: n.uvLabel, sub: 'Peak 13:20', tone: 'amber' },\n"
        "  ];"
    ),
    (
        "function StatTilesGrid({ n, intensity, showMotion, prefs }) {\n"
        "  const imperial = prefs && prefs['Units'] === 'Imperial · mph · °F';\n"
        "  const ktToMph = v => Math.round(v * 1.15078);\n"
        "  const mToFt   = v => (v * 3.28084).toFixed(1);\n"
        "  const cToF    = v => Math.round(v * 9/5 + 32);\n"
        "  const tiles = [\n"
        "    { icon: 'wind',  label: 'Wind',     value: imperial ? `${ktToMph(n.windSpeed)}` : `${n.windSpeed}`, unit: imperial ? 'mph' : 'kt', sub: `${n.windDirLabel} · gust ${imperial ? ktToMph(n.windGust) : n.windGust}${imperial?' mph':' kt'}`, tone: 'default' },\n"
        "    { icon: 'wave',  label: 'Swell',    value: imperial ? `${mToFt(n.waveHeight)}` : `${n.waveHeight}`, unit: imperial ? 'ft' : 'm', sub: `${n.swellPeriod}s ${n.swellDir}`, tone: 'default' },\n"
        "    { icon: 'water', label: 'Water',    value: imperial ? `${cToF(n.waterTemp)}` : `${n.waterTemp}`, unit: imperial ? '°F' : '°C', sub: `Air ${imperial ? cToF(n.airTemp) : n.airTemp}°`, tone: 'default' },\n"
        "    { icon: 'tide',  label: 'Tide',     value: imperial ? `${mToFt(n.tideHeight)}` : `${n.tideHeight}`, unit: imperial ? 'ft' : 'm', sub: `${n.nextTide}`, tone: 'teal' },\n"
        "    { icon: 'baro',  label: 'Pressure', value: `${n.barometric}`, unit: 'hPa', sub: null, tone: 'default', pressure: true, trend: n.barometricTrend, delta: n.barometricDelta },\n"
        "    { icon: 'uv',    label: 'UV',       value: `${n.uv}`, unit: n.uvLabel, sub: 'Peak 13:20', tone: 'amber' },\n"
        "  ];"
    ),
    "A6-StatTilesGrid-unit-conversions"
)

# ─────────────────────────────────────────────────────────────────────────────
# A7: Conditions — accept prefs prop
# ─────────────────────────────────────────────────────────────────────────────
rep(
    "function Conditions({ tweaks, activeLocation }) {",
    "function Conditions({ tweaks, activeLocation, prefs }) {",
    "A7-Conditions-accepts-prefs"
)

# ─────────────────────────────────────────────────────────────────────────────
# A8: Conditions wind — apply unit conversion
# ─────────────────────────────────────────────────────────────────────────────
rep(
    (
        "              <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>\n"
        '                <BigMetric value={n.windSpeed} unit="kt" label={`${n.windDirLabel} · ${n.windDir}°`} />\n'
        '                <SmallStat label="Gust" value={`${n.windGust} kt`} />\n'
        '                <SmallStat label="6h trend" value="Easing" tone="teal" />\n'
        '                <SmallStat label="Forecast peak" value="14 kt · 13:00" />\n'
        "              </div>"
    ),
    (
        "              <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>\n"
        "                {(() => {\n"
        "                  const imp = prefs && prefs['Units'] === 'Imperial · mph · °F';\n"
        "                  const spd = imp ? Math.round(n.windSpeed * 1.15078) : n.windSpeed;\n"
        "                  const gst = imp ? Math.round(n.windGust * 1.15078) : n.windGust;\n"
        "                  const u = imp ? 'mph' : 'kt';\n"
        "                  return (<>\n"
        "                    <BigMetric value={spd} unit={u} label={`${n.windDirLabel} · ${n.windDir}°`} />\n"
        "                    <SmallStat label=\"Gust\" value={`${gst} ${u}`} />\n"
        "                    <SmallStat label=\"6h trend\" value=\"Easing\" tone=\"teal\" />\n"
        "                    <SmallStat label=\"Forecast peak\" value={`${imp?Math.round(14*1.15078):14} ${u} · 13:00`} />\n"
        "                  </>);\n"
        "                })()}\n"
        "              </div>"
    ),
    "A8-Conditions-wind-units"
)

# ─────────────────────────────────────────────────────────────────────────────
# A9: Conditions swell — apply unit conversion
# ─────────────────────────────────────────────────────────────────────────────
rep(
    (
        '              <SubTitle icon="wave">Swell</SubTitle>\n'
        "              <BigMetric value={n.waveHeight} unit=\"m\" label={`${n.swellPeriod}s · ${n.swellDir}`} style={{ marginTop: 6 }} />"
    ),
    (
        '              <SubTitle icon="wave">Swell</SubTitle>\n'
        "              {(() => {\n"
        "                const imp = prefs && prefs['Units'] === 'Imperial · mph · °F';\n"
        "                const h = imp ? (n.waveHeight * 3.28084).toFixed(1) : n.waveHeight;\n"
        "                return <BigMetric value={h} unit={imp?'ft':'m'} label={`${n.swellPeriod}s · ${n.swellDir}`} style={{ marginTop: 6 }} />;\n"
        "              })()}"
    ),
    "A9-Conditions-swell-units"
)

# ─────────────────────────────────────────────────────────────────────────────
# A10: Conditions sun times — apply 12h format
# ─────────────────────────────────────────────────────────────────────────────
rep(
    (
        "              {[\n"
        "                ['Dawn', n.dawn],\n"
        "                ['Sunrise', n.sunrise],\n"
        "                ['Sunset', n.sunset],\n"
        "                ['Dusk', n.dusk],\n"
        "              ].map(([k, v]) => (\n"
        "                <div key={k} style={{ textAlign: 'center' }}>\n"
        "                  <div style={{ fontSize: 9, color: 'var(--muted)', letterSpacing: 1 }}>{k.toUpperCase()}</div>\n"
        '                  <div style={{ fontWeight: 700, fontSize: 13, marginTop: 2, fontFamily: \'"Inter Tight",Inter\' }}>{v}</div>\n'
        "                </div>\n"
        "              ))}\n"
        "            </div>"
    ),
    (
        "              {(() => {\n"
        "                const is12 = prefs && prefs['Time format'] === '12-hour';\n"
        "                const fmt = t => { if (!t || !is12) return t; const [h,m] = t.split(':').map(Number); return `${h%12||12}:${String(m).padStart(2,'0')}${h>=12?'pm':'am'}`; };\n"
        "                return [\n"
        "                  ['Dawn', n.dawn], ['Sunrise', n.sunrise], ['Sunset', n.sunset], ['Dusk', n.dusk],\n"
        "                ].map(([k, v]) => (\n"
        "                  <div key={k} style={{ textAlign: 'center' }}>\n"
        "                    <div style={{ fontSize: 9, color: 'var(--muted)', letterSpacing: 1 }}>{k.toUpperCase()}</div>\n"
        '                    <div style={{ fontWeight: 700, fontSize: 13, marginTop: 2, fontFamily: \'"Inter Tight",Inter\' }}>{fmt(v)}</div>\n'
        "                  </div>\n"
        "                ));\n"
        "              })()}\n"
        "            </div>"
    ),
    "A10-Conditions-sun-12h-format"
)

# ─────────────────────────────────────────────────────────────────────────────
# A11: Settings — accept prefs/onPrefsChange props
# ─────────────────────────────────────────────────────────────────────────────
rep(
    "function Settings({ tweaks, onLocationSelect, activeLocation, userGeoLoc, setUserGeoLoc }) {",
    "function Settings({ tweaks, onLocationSelect, activeLocation, userGeoLoc, setUserGeoLoc, prefs: prefsProp, onPrefsChange }) {",
    "A11-Settings-accepts-prefs"
)

# ─────────────────────────────────────────────────────────────────────────────
# A12: Settings — replace local prefs state with prop-backed fallback
# ─────────────────────────────────────────────────────────────────────────────
rep(
    (
        "  const [prefs, setPrefs]       = React.useState({\n"
        "    'Units': 'Metric · kt · °C', 'Time format': '24-hour',\n"
        "    'Tide datum': 'LAT (Lowest Astron.)', 'Notifications': '2 active', 'Watch face': 'Score + tide',\n"
        "  });"
    ),
    (
        "  const prefs = prefsProp || {\n"
        "    'Units': 'Metric · kt · °C', 'Time format': '24-hour',\n"
        "    'Tide datum': 'LAT (Lowest Astron.)', 'Notifications': '2 active', 'Watch face': 'Score + tide',\n"
        "  };"
    ),
    "A12-Settings-remove-local-prefs"
)

# ─────────────────────────────────────────────────────────────────────────────
# A13: Settings cyclePref — call onPrefsChange instead of local setPrefs
# ─────────────────────────────────────────────────────────────────────────────
rep(
    (
        "  const cyclePref = label => {\n"
        "    const opts = PREF_OPTIONS[label];\n"
        "    setPrefs(p => ({ ...p, [label]: opts[(opts.indexOf(p[label]) + 1) % opts.length] }));\n"
        "  };"
    ),
    (
        "  const cyclePref = label => {\n"
        "    const opts = PREF_OPTIONS[label];\n"
        "    const next = opts[(opts.indexOf(prefs[label]) + 1) % opts.length];\n"
        "    if (onPrefsChange) onPrefsChange(label, next);\n"
        "  };"
    ),
    "A13-Settings-cyclePref-lifts-state"
)

# ─────────────────────────────────────────────────────────────────────────────
# B1: Nearby spots — always show, prompt if no geo
# ─────────────────────────────────────────────────────────────────────────────
rep(
    (
        "        {/* ── Nearby spots ── */}\n"
        "        {(nearbyLoading || nearbySpots.length > 0) && (\n"
        "          <div style={{ marginTop:28 }}>\n"
        "            <div style={{ display:'flex', alignItems:'center', justifyContent:'space-between', marginBottom:10 }}>\n"
        "              <SectionHeader title=\"Nearby hot spots\" hint=\"Tap to navigate\" inset />\n"
        "              {nearbyLoading && (\n"
        "                <span style={{ fontSize:10, color:'var(--teal)', letterSpacing:0.5 }}>Scanning…</span>\n"
        "              )}\n"
        "            </div>\n"
        "            {nearbyLoading && nearbySpots.length === 0\n"
        "              ? <div style={{ display:'flex', flexDirection:'column', gap:6 }}>\n"
        "                  {[0,1,2].map(i => (\n"
        "                    <div key={i} style={{ height:68, borderRadius:12, background:'rgba(255,255,255,0.03)', animation:'tl-stagger .8s ease infinite alternate' }}/>\n"
        "                  ))}\n"
        "                </div>\n"
        "              : <div style={{ display:'flex', flexDirection:'column', gap:6 }}>\n"
        "                  {nearbySpots.map((spot, i) => (\n"
        "                    <NearbySpotRow key={i} spot={spot} intensity={intensity}\n"
        "                      onSelect={() => selectLoc(spot)} />\n"
        "                  ))}\n"
        "                </div>\n"
        "            }\n"
        "          </div>\n"
        "        )}"
    ),
    (
        "        {/* ── Nearby spots ── */}\n"
        "        <div style={{ marginTop:28 }}>\n"
        "          <div style={{ display:'flex', alignItems:'center', justifyContent:'space-between', marginBottom:10 }}>\n"
        "            <SectionHeader title=\"Nearby hot spots\" hint=\"Tap to navigate\" inset />\n"
        "            {nearbyLoading && <span style={{ fontSize:10, color:'var(--teal)', letterSpacing:0.5 }}>Scanning…</span>}\n"
        "          </div>\n"
        "          {!userGeoLoc && !nearbyLoading && nearbySpots.length === 0\n"
        "            ? <button onClick={detectLocation} style={{ width:'100%', padding:'14px', background:'rgba(255,255,255,0.03)', border:'1px dashed rgba(255,255,255,0.12)', borderRadius:12, color:'var(--muted)', fontSize:12, fontFamily:'inherit', cursor:'pointer', display:'flex', alignItems:'center', justifyContent:'center', gap:8 }}>\n"
        "                <svg width=\"14\" height=\"14\" viewBox=\"0 0 16 16\" fill=\"none\"><circle cx=\"8\" cy=\"8\" r=\"2.8\" stroke=\"currentColor\" strokeWidth=\"1.5\"/><circle cx=\"8\" cy=\"8\" r=\"6.2\" stroke=\"currentColor\" strokeWidth=\"1\" strokeOpacity=\"0.35\"/><path d=\"M8 1.5v2M8 12.5v2M1.5 8h2M12.5 8h2\" stroke=\"currentColor\" strokeWidth=\"1.5\" strokeLinecap=\"round\"/></svg>\n"
        "                Detect location to see nearby spots\n"
        "              </button>\n"
        "            : nearbyLoading && nearbySpots.length === 0\n"
        "              ? <div style={{ display:'flex', flexDirection:'column', gap:6 }}>{[0,1,2].map(i => <div key={i} style={{ height:68, borderRadius:12, background:'rgba(255,255,255,0.03)', animation:'tl-stagger .8s ease infinite alternate' }}/>)}</div>\n"
        "              : nearbySpots.length > 0\n"
        "                ? <div style={{ display:'flex', flexDirection:'column', gap:6 }}>{nearbySpots.map((spot,i) => <NearbySpotRow key={i} spot={spot} intensity={intensity} onSelect={() => selectLoc(spot)} />)}</div>\n"
        "                : <div style={{ padding:'12px', background:'rgba(255,255,255,0.03)', border:'1px solid rgba(255,255,255,0.06)', borderRadius:12, fontSize:12, color:'var(--muted)', textAlign:'center' }}>No spots found nearby — try a different area</div>\n"
        "          }\n"
        "        </div>"
    ),
    "B1-nearby-always-show"
)

# ─────────────────────────────────────────────────────────────────────────────
# B2: Nominatim — add delays + bounded=0 + delta=1.5 + better query
# ─────────────────────────────────────────────────────────────────────────────
rep(
    (
        "  const fetchNearbySpots = React.useCallback(async (lat, lng) => {\n"
        "    setNearbyLoading(true);\n"
        "    const delta = 0.8;\n"
        "    const vb = `${(lng-delta).toFixed(3)},${(lat+delta).toFixed(3)},${(lng+delta).toFixed(3)},${(lat-delta).toFixed(3)}`;\n"
        "    const hdr = { headers: { 'Accept-Language': 'en' } };\n"
        "    const qs = (term) =>\n"
        "      fetch(`https://nominatim.openstreetmap.org/search?q=${encodeURIComponent(term)}&format=json&limit=4&viewbox=${vb}&bounded=1&addressdetails=1`, hdr)\n"
        "        .then(r => r.json()).catch(() => []);\n"
        "    try {\n"
        "      // Stagger requests to respect Nominatim 1req/s policy\n"
        "      const bays    = await qs('bay');\n"
        "      const wharves = await qs('wharf');\n"
        "      const points  = await qs('point');"
    ),
    (
        "  const fetchNearbySpots = React.useCallback(async (lat, lng) => {\n"
        "    setNearbyLoading(true);\n"
        "    setNearbySpots([]);\n"
        "    const delta = 1.5;\n"
        "    const vb = `${(lng-delta).toFixed(3)},${(lat+delta).toFixed(3)},${(lng+delta).toFixed(3)},${(lat-delta).toFixed(3)}`;\n"
        "    const hdr = { headers: { 'Accept-Language': 'en', 'User-Agent': 'TightLinesApp/1.0' } };\n"
        "    const wait = ms => new Promise(r => setTimeout(r, ms));\n"
        "    const qs = async (term) => fetch(`https://nominatim.openstreetmap.org/search?q=${encodeURIComponent(term)}&format=json&limit=6&viewbox=${vb}&bounded=0&addressdetails=1`, hdr).then(r => r.json()).catch(() => []);\n"
        "    try {\n"
        "      const bays    = await qs('bay');\n"
        "      await wait(1100);\n"
        "      const wharves = await qs('wharf');\n"
        "      await wait(1100);\n"
        "      const points  = await qs('jetty pier');"
    ),
    "B2-Nominatim-delays-bounded0-delta15"
)

# ─────────────────────────────────────────────────────────────────────────────
# Done
# ─────────────────────────────────────────────────────────────────────────────
with open(PATH, 'w', encoding='utf-8') as f:
    f.write(src)

print(f"\n=== {len(changes)} patches applied, {len(src)-orig_len:+d} bytes ===")
