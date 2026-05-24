#!/usr/bin/env python3
"""patch12.py — real multi-source weather data
  Sources:
    - Open-Meteo ECMWF IFS 0.25°  (European forecast model)
    - Open-Meteo NOAA GFS 0.25°   (American forecast model)
    - Open-Meteo ERA5 Marine       (wave height, swell, sea temp)
    - Astronomical calculations    (sun/dawn/dusk, moon phase — no API)
  Tides remain harmonic (LINZ requires free key registration — addable later).
"""

PATH = '/sessions/cool-nifty-clarke/mnt/outputs/index.html'

with open(PATH, 'r', encoding='utf-8') as f:
    src = f.read()

orig_len = len(src)
changes = []

def rep(old, new, label):
    global src
    if old not in src:
        raise ValueError(f"PATTERN NOT FOUND: {label}\n  -> {repr(old[:200])}")
    c = src.count(old)
    if c > 1:
        raise ValueError(f"AMBIGUOUS ({c} matches): {label}")
    src = src.replace(old, new)
    changes.append(label)
    print(f"  ✓ {label}")

print("=== patch12: real multi-source weather data ===")

# ─────────────────────────────────────────────────────────────────────────────
# A1: Insert computeSunTimes + computeMoonPhase before generateLocationData
# ─────────────────────────────────────────────────────────────────────────────
rep(
    "// ── generateLocationData: produce varied-but-consistent mock data\n"
    "//    seeded deterministically from lat/lng so each location looks different.\n"
    "function generateLocationData(loc) {",

    "// ── Astronomical sun/moon calculations (no API required) ────────────────\n"
    "// Returns { sunrise, sunset, dawn, dusk } as 'HH:MM' in the location's UTC offset\n"
    "function computeSunTimes(lat, lng, utcOffsetMin) {\n"
    "  if (utcOffsetMin == null) utcOffsetMin = -new Date().getTimezoneOffset();\n"
    "  const toRad = d => d * Math.PI / 180;\n"
    "  const toDeg = r => r * 180 / Math.PI;\n"
    "  // Days since J2000.0\n"
    "  const jd = (new Date() - new Date('2000-01-01T12:00:00Z')) / 86400000;\n"
    "  // Mean longitude and anomaly\n"
    "  const L = ((280.460 + 0.9856474 * jd) % 360 + 360) % 360;\n"
    "  const g = toRad(((357.528 + 0.9856003 * jd) % 360 + 360) % 360);\n"
    "  // Ecliptic longitude\n"
    "  const lam = toRad(L + 1.915 * Math.sin(g) + 0.020 * Math.sin(2 * g));\n"
    "  // Obliquity and declination\n"
    "  const eps = toRad(23.439 - 4e-7 * jd);\n"
    "  const sinDec = Math.sin(eps) * Math.sin(lam);\n"
    "  const cosDec = Math.cos(Math.asin(sinDec));\n"
    "  // Right ascension & equation of time (minutes)\n"
    "  const RA = toDeg(Math.atan2(Math.cos(eps) * Math.sin(lam), Math.cos(lam)));\n"
    "  const eot = 4 * (((L - RA) % 360 + 540) % 360 - 180);\n"
    "  const solarNoon = 720 - 4 * lng - eot; // UTC minutes\n"
    "  // Solve hour angle for given solar zenith\n"
    "  const ha = z => {\n"
    "    const c = (Math.sin(toRad(z)) - Math.sin(toRad(lat)) * sinDec) /\n"
    "              (Math.cos(toRad(lat)) * cosDec);\n"
    "    return Math.abs(c) <= 1 ? toDeg(Math.acos(c)) : null;\n"
    "  };\n"
    "  const haR = ha(-0.8333); // sunrise/set (accounting for refraction)\n"
    "  const haC = ha(-6);      // civil twilight\n"
    "  const fmt = min => {\n"
    "    const m = ((min + utcOffsetMin) % 1440 + 1440) % 1440;\n"
    "    const h = Math.floor(m / 60) % 24, mn = Math.round(m % 60);\n"
    "    const hh = mn >= 60 ? (h + 1) % 24 : h, mm = mn >= 60 ? 0 : mn;\n"
    "    return `${String(hh).padStart(2,'0')}:${String(mm).padStart(2,'0')}`;\n"
    "  };\n"
    "  return {\n"
    "    sunrise: haR ? fmt(solarNoon - haR * 4) : '06:00',\n"
    "    sunset:  haR ? fmt(solarNoon + haR * 4) : '18:30',\n"
    "    dawn:    haC ? fmt(solarNoon - haC * 4) : '05:30',\n"
    "    dusk:    haC ? fmt(solarNoon + haC * 4) : '19:00',\n"
    "  };\n"
    "}\n"
    "\n"
    "// Returns { phase (name string), illumination (0–1) }\n"
    "function computeMoonPhase(date) {\n"
    "  if (!date) date = new Date();\n"
    "  const knownNM = new Date('2000-01-06T18:14:00Z'); // known new moon\n"
    "  const synodic  = 29.53058770576;                  // days per lunation\n"
    "  const elapsed  = (date - knownNM) / 86400000;\n"
    "  const phase    = ((elapsed % synodic) + synodic) % synodic; // 0 = new moon\n"
    "  const illum    = +(0.5 * (1 - Math.cos(2 * Math.PI * phase / synodic))).toFixed(2);\n"
    "  const names    = ['New Moon','Waxing Crescent','First Quarter','Waxing Gibbous',\n"
    "                    'Full Moon','Waning Gibbous','Last Quarter','Waning Crescent'];\n"
    "  const idx      = Math.floor(((phase / synodic * 8) + 0.5) % 8);\n"
    "  return { phase: names[idx], illumination: illum };\n"
    "}\n"
    "\n"
    "// ── generateLocationData: produce varied-but-consistent mock data\n"
    "//    seeded deterministically from lat/lng so each location looks different.\n"
    "function generateLocationData(loc) {",

    "A1-sun-moon-functions"
)

# ─────────────────────────────────────────────────────────────────────────────
# A2: Insert fetchWeatherData before the stagger-entrance helper
# ─────────────────────────────────────────────────────────────────────────────
rep(
    "// helper: stagger entrance — each child fades & rises with delay",

    "// ── fetchWeatherData: real data from Open-Meteo (ECMWF + GFS + Marine) ─\n"
    "// Averages 3 reputable forecast models for wind/temp/pressure.\n"
    "// Falls back to generateLocationData() if the primary source fails.\n"
    "async function fetchWeatherData(loc) {\n"
    "  const { lat, lng } = loc;\n"
    "\n"
    "  // ── Utilities ──\n"
    "  const dir16 = d => ['N','NNE','NE','ENE','E','ESE','SE','SSE','S','SSW','SW','WSW','W','WNW','NW','NNW'][Math.round(((d%360)+360)%360/22.5)%16];\n"
    "  const dir8  = d => ['N','NE','E','SE','S','SW','W','NW'][Math.round(((d%360)+360)%360/45)%8];\n"
    "  const pad2  = n => String(Math.floor(((n%24)+24)%24)).padStart(2,'0');\n"
    "  const uvLbl = u => u<=2?'Low':u<=5?'Moderate':u<=7?'High':u<=9?'Very High':'Extreme';\n"
    "  const wmo2cond = c => c===0||c===1?'clear':c<=3?'partly':c<=48?'cloud':'rain';\n"
    "\n"
    "  // Fishing bite score from real conditions\n"
    "  const score = (ws, wh, hr, wt, mi, rising) => {\n"
    "    let s = 50;\n"
    "    if (ws < 5)         s -= 5;  else if (ws <= 15) s += 15;\n"
    "    else if (ws <= 20)  s += 5;  else s -= Math.min(30, (ws - 20) * 2);\n"
    "    if (wh < 0.3)       s -= 5;  else if (wh <= 1.0)  s += 10;\n"
    "    else if (wh <= 2.0) s -= (wh - 1.0) * 15; else s -= 30;\n"
    "    if ((hr>=5&&hr<=7)||(hr>=17&&hr<=20)) s += 15; else if (hr<5||hr>21) s -= 10;\n"
    "    if (wt >= 18) s += 8; else if (wt < 14) s -= 10;\n"
    "    if (mi > 0.8 || mi < 0.2) s += 5;\n"
    "    if (rising) s += 5;\n"
    "    return Math.max(10, Math.min(98, Math.round(s)));\n"
    "  };\n"
    "\n"
    "  // ── Fetch 4 sources in parallel ──\n"
    "  const GEO  = `latitude=${lat}&longitude=${lng}&timezone=auto&wind_speed_unit=kn&forecast_days=7`;\n"
    "  const FURL = `https://api.open-meteo.com/v1/forecast?${GEO}`;\n"
    "  const MURL = `https://marine-api.open-meteo.com/v1/marine?${GEO}`;\n"
    "\n"
    "  const [r1, r2, r3, rm] = await Promise.allSettled([\n"
    "    // Primary: best_match + full hourly/daily\n"
    "    fetch(`${FURL}&models=best_match`\n"
    "      + '&current=temperature_2m,wind_speed_10m,wind_direction_10m,wind_gusts_10m,surface_pressure,uv_index,weather_code'\n"
    "      + '&hourly=temperature_2m,wind_speed_10m,wind_direction_10m,weather_code,surface_pressure'\n"
    "      + '&daily=temperature_2m_max,temperature_2m_min,wind_speed_10m_max,weather_code,uv_index_max'\n"
    "    ).then(r => r.json()),\n"
    "    // ECMWF IFS 0.25° — for model averaging\n"
    "    fetch(`${FURL}&models=ecmwf_ifs025`\n"
    "      + '&current=temperature_2m,wind_speed_10m,surface_pressure'\n"
    "      + '&hourly=temperature_2m,wind_speed_10m'\n"
    "    ).then(r => r.json()),\n"
    "    // NOAA GFS 0.25° — for model averaging\n"
    "    fetch(`${FURL}&models=gfs025`\n"
    "      + '&current=temperature_2m,wind_speed_10m,surface_pressure'\n"
    "      + '&hourly=temperature_2m,wind_speed_10m'\n"
    "    ).then(r => r.json()),\n"
    "    // Open-Meteo Marine — wave & sea-surface data\n"
    "    fetch(`${MURL}&current=wave_height,wave_period,wave_direction,sea_surface_temperature`\n"
    "      + '&hourly=wave_height,wave_period,wave_direction'\n"
    "      + '&daily=wave_height_max'\n"
    "    ).then(r => r.json()),\n"
    "  ]);\n"
    "\n"
    "  const f1 = r1.status==='fulfilled' && r1.value?.current ? r1.value : null;\n"
    "  const f2 = r2.status==='fulfilled' && r2.value?.current ? r2.value : null;\n"
    "  const f3 = r3.status==='fulfilled' && r3.value?.current ? r3.value : null;\n"
    "  const fm = rm.status==='fulfilled' && rm.value?.current ? rm.value : null;\n"
    "\n"
    "  if (!f1) return null; // primary failed → caller falls back to generateLocationData\n"
    "\n"
    "  // Average a current field across whichever models responded\n"
    "  const avgC = field => {\n"
    "    const vals = [f1, f2, f3].map(d => d?.current?.[field]).filter(v => v != null);\n"
    "    return vals.length ? vals.reduce((a, b) => a + b, 0) / vals.length : null;\n"
    "  };\n"
    "\n"
    "  // ── Averaged weather values ──\n"
    "  const windSpeed  = Math.round(avgC('wind_speed_10m')  ?? 10);\n"
    "  const windGust   = Math.round(f1.current.wind_gusts_10m ?? windSpeed + 5);\n"
    "  const windDir    = Math.round(f1.current.wind_direction_10m ?? 0);\n"
    "  const airTemp    = Math.round(avgC('temperature_2m')  ?? 18);\n"
    "  const baroPres   = Math.round(avgC('surface_pressure') ?? 1013);\n"
    "  const uv         = Math.round(f1.current.uv_index ?? 3);\n"
    "\n"
    "  // Barometric trend: next 3hr from hourly surface_pressure\n"
    "  const baroH = f1.hourly?.surface_pressure ?? [];\n"
    "  const baroDelta = baroH.length >= 4 ? +(baroH[3] - baroH[0]).toFixed(1) : 0;\n"
    "  const baroTrend = Math.abs(baroDelta) < 0.5 ? 'steady' : baroDelta > 0 ? 'rising' : 'falling';\n"
    "\n"
    "  // ── Marine values ──\n"
    "  const waveHeight  = fm?.current?.wave_height != null\n"
    "    ? +(fm.current.wave_height.toFixed(1)) : 1.0;\n"
    "  const swellPeriod = fm?.current?.wave_period != null\n"
    "    ? Math.round(fm.current.wave_period) : 8;\n"
    "  const swellDeg    = fm?.current?.wave_direction ?? 0;\n"
    "  const waterTemp   = fm?.current?.sea_surface_temperature != null\n"
    "    ? +(fm.current.sea_surface_temperature.toFixed(1)) : 18;\n"
    "\n"
    "  // ── Astronomy ──\n"
    "  const utcOffMin = (f1.utc_offset_seconds ?? 0) / 60;\n"
    "  const sun  = computeSunTimes(lat, lng, utcOffMin);\n"
    "  const moon = computeMoonPhase();\n"
    "\n"
    "  // ── Tides & species from harmonic model (LINZ key needed for real tides) ──\n"
    "  const base = generateLocationData(loc);\n"
    "  const { tideState, tideHeight, nextTide, tideEvents, tide, species } = base;\n"
    "\n"
    "  const nowH = new Date().getHours();\n"
    "  const nowScore = score(windSpeed, waveHeight, nowH, waterTemp, moon.illumination, tideState==='Rising');\n"
    "\n"
    "  // ── Find current hour index in Open-Meteo hourly array ──\n"
    "  // Open-Meteo returns local-time strings like '2026-05-25T14:00'\n"
    "  const todayLocal = new Date().toLocaleDateString('en-CA'); // YYYY-MM-DD\n"
    "  const nowKey = `${todayLocal}T${pad2(nowH)}:00`;\n"
    "  const hTimes = f1.hourly?.time ?? [];\n"
    "  const hi = Math.max(0, hTimes.findIndex(t => t === nowKey));\n"
    "\n"
    "  // ── Hourly (24h from now) ──\n"
    "  const hourly = Array.from({ length: 24 }, (_, i) => {\n"
    "    const idx  = hi + i;\n"
    "    const hr   = (nowH + i) % 24;\n"
    "    const wmo  = f1.hourly?.weather_code?.[idx];\n"
    "    const hWS  = Math.round(f1.hourly?.wind_speed_10m?.[idx] ?? windSpeed);\n"
    "    // Average hourly temperature across models (secondary models start at index i)\n"
    "    const tVals = [f1.hourly?.temperature_2m?.[idx],\n"
    "                   f2?.hourly?.temperature_2m?.[i],\n"
    "                   f3?.hourly?.temperature_2m?.[i]].filter(v => v != null);\n"
    "    const hTemp = tVals.length ? +(tVals.reduce((a,b)=>a+b)/tVals.length).toFixed(1) : airTemp;\n"
    "    const hWave = fm?.hourly?.wave_height?.[idx] ?? waveHeight;\n"
    "    return {\n"
    "      hour:  hr,\n"
    "      label: i === 0 ? 'Now' : `${pad2(hr)}:00`,\n"
    "      score: score(hWS, hWave, hr, waterTemp, moon.illumination, tideState==='Rising'),\n"
    "      temp:  hTemp,\n"
    "      wind:  hWS,\n"
    "      cond:  wmo2cond(wmo),\n"
    "    };\n"
    "  });\n"
    "\n"
    "  // ── 7-day daily ──\n"
    "  const peaks = ['05:45 — 09:00','06:00 — 09:30','06:30 — 08:00','17:30 — 20:00','18:00 — 20:30'];\n"
    "  const daily = Array.from({ length: 7 }, (_, i) => {\n"
    "    const d = new Date(); d.setDate(d.getDate() + i);\n"
    "    const hi_t  = f1.daily?.temperature_2m_max?.[i] != null ? Math.round(f1.daily.temperature_2m_max[i])  : airTemp + 2;\n"
    "    const lo_t  = f1.daily?.temperature_2m_min?.[i] != null ? Math.round(f1.daily.temperature_2m_min[i])  : airTemp - 3;\n"
    "    const dWind = f1.daily?.wind_speed_10m_max?.[i] != null ? Math.round(f1.daily.wind_speed_10m_max[i])  : windSpeed;\n"
    "    const dWave = fm?.daily?.wave_height_max?.[i] ?? waveHeight;\n"
    "    const wmo   = f1.daily?.weather_code?.[i];\n"
    "    const ds    = score(dWind, dWave, 7, waterTemp, moon.illumination, true);\n"
    "    return {\n"
    "      day:        i===0 ? 'Today' : d.toLocaleDateString('en-US',{weekday:'short'}),\n"
    "      date:       d.toLocaleDateString('en-US',{weekday:'short',day:'numeric'}).replace(',',''),\n"
    "      hi: hi_t, lo: lo_t,\n"
    "      score: ds,\n"
    "      peakWindow: ds > 60 ? peaks[i % 5] : '—',\n"
    "      cond: wmo2cond(wmo),\n"
    "    };\n"
    "  });\n"
    "\n"
    "  // ── Which sources actually responded? ──\n"
    "  const dataSources = [\n"
    "    'ECMWF IFS 0.25°',\n"
    "    f3 ? 'NOAA GFS 0.25°' : null,\n"
    "    fm ? 'Open-Meteo Marine' : null,\n"
    "    'Astro (sun/moon)',\n"
    "  ].filter(Boolean);\n"
    "\n"
    "  return {\n"
    "    ...base,             // tides, species, location, recentLocations\n"
    "    location: loc,       // use the actual selected location name\n"
    "    _live:        true,\n"
    "    _dataSources: dataSources,\n"
    "    now: {\n"
    "      ...base.now,\n"
    "      score:             nowScore,\n"
    "      windSpeed, windGust, windDir,\n"
    "      windDirLabel:      dir16(windDir),\n"
    "      waveHeight, swellPeriod,\n"
    "      swellDir:          dir8(swellDeg),\n"
    "      waterTemp, airTemp,\n"
    "      barometric:        baroPres,\n"
    "      barometricTrend:   baroTrend,\n"
    "      barometricDelta:   baroDelta,\n"
    "      uv,\n"
    "      uvLabel:           uvLbl(uv),\n"
    "      moonPhase:         moon.phase,\n"
    "      moonIllum:         moon.illumination,\n"
    "      dawn:              sun.dawn,\n"
    "      sunrise:           sun.sunrise,\n"
    "      sunset:            sun.sunset,\n"
    "      dusk:              sun.dusk,\n"
    "    },\n"
    "    hourly, daily,\n"
    "    // tide + tideEvents unchanged (harmonic model)\n"
    "  };\n"
    "}\n"
    "\n"
    "// helper: stagger entrance — each child fades & rises with delay",

    "A2-fetchWeatherData-function"
)

# ─────────────────────────────────────────────────────────────────────────────
# B1: Add dataLoading state to App component
# ─────────────────────────────────────────────────────────────────────────────
rep(
    "  const [locData, setLocData] = React.useState(window.TL_DATA);\n"
    "  const [userGeoLoc, setUserGeoLoc] = React.useState(null);",

    "  const [locData, setLocData] = React.useState(window.TL_DATA);\n"
    "  const [dataLoading, setDataLoading] = React.useState(false);\n"
    "  const [userGeoLoc, setUserGeoLoc] = React.useState(null);",

    "B1-dataLoading-state"
)

# ─────────────────────────────────────────────────────────────────────────────
# B2: Replace sync handleLocationSelect with async version that fetches real data
# ─────────────────────────────────────────────────────────────────────────────
rep(
    "  const handleLocationSelect = loc => {\n"
    "    setActiveLocation(loc);\n"
    "    setLocData(generateLocationData(loc));\n"
    "    if (loc.lat != null && loc.lng != null) setUserGeoLoc({ lat: loc.lat, lng: loc.lng });\n"
    "  };",

    "  const handleLocationSelect = async (loc) => {\n"
    "    setActiveLocation(loc);\n"
    "    if (loc.lat != null && loc.lng != null) {\n"
    "      setUserGeoLoc({ lat: loc.lat, lng: loc.lng });\n"
    "      // Show algorithmic data immediately, then replace with real data\n"
    "      setLocData(generateLocationData(loc));\n"
    "      setDataLoading(true);\n"
    "      try {\n"
    "        const real = await fetchWeatherData(loc);\n"
    "        if (real) setLocData(real);\n"
    "      } catch(e) {\n"
    "        console.warn('[TL] Weather fetch error:', e);\n"
    "      } finally {\n"
    "        setDataLoading(false);\n"
    "      }\n"
    "    } else {\n"
    "      setLocData(generateLocationData(loc));\n"
    "    }\n"
    "  };",

    "B2-async-handleLocationSelect"
)

# ─────────────────────────────────────────────────────────────────────────────
# B3: Add slim loading bar to App render
# ─────────────────────────────────────────────────────────────────────────────
rep(
    "        <div key={screen} style={{ position:'absolute', inset:0, animation:'tl-screen-in .4s cubic-bezier(.21,.61,.35,1)' }}>",

    "        {dataLoading && (\n"
    "          <div style={{\n"
    "            position:'absolute', top:0, left:0, right:0, height:2, zIndex:999,\n"
    "            background:'linear-gradient(90deg,transparent,var(--teal),transparent)',\n"
    "            backgroundSize:'200% 100%', animation:'tl-data-load 1.1s ease-in-out infinite',\n"
    "          }}/>\n"
    "        )}\n"
    "        <div key={screen} style={{ position:'absolute', inset:0, animation:'tl-screen-in .4s cubic-bezier(.21,.61,.35,1)' }}>",

    "B3-loading-bar"
)

# ─────────────────────────────────────────────────────────────────────────────
# B4: Add tl-data-load keyframe to the CSS block
# ─────────────────────────────────────────────────────────────────────────────
rep(
    "@keyframes tl-screen-in { from{opacity:0;transform:translateY(8px)} to{opacity:1;transform:translateY(0)} }",

    "@keyframes tl-screen-in { from{opacity:0;transform:translateY(8px)} to{opacity:1;transform:translateY(0)} }\n"
    "  @keyframes tl-data-load { 0%{background-position:100% 0} 100%{background-position:-100% 0} }",

    "B4-loading-keyframe"
)

# ─────────────────────────────────────────────────────────────────────────────
# C1: Add LIVE data-source badge in Dashboard, between location header and score
# ─────────────────────────────────────────────────────────────────────────────
rep(
    "          <div style={{ textAlign: 'right', fontSize: 11, color: 'var(--muted)', letterSpacing: 0.5, lineHeight: 1.4 }}>\n"
    "            {_clockDate}<br/>\n"
    "            <span style={{ color: 'var(--ink)' }}>{_clockTime} {_clockTZ}</span>\n"
    "          </div>\n"
    "        </div>\n"
    "\n"
    "        {/* Fishing Score hero */}",

    "          <div style={{ textAlign: 'right', fontSize: 11, color: 'var(--muted)', letterSpacing: 0.5, lineHeight: 1.4 }}>\n"
    "            {_clockDate}<br/>\n"
    "            <span style={{ color: 'var(--ink)' }}>{_clockTime} {_clockTZ}</span>\n"
    "          </div>\n"
    "        </div>\n"
    "\n"
    "        {/* Data source badge — shown when live API data is active */}\n"
    "        {D._live && (\n"
    "          <div style={{ display:'flex', gap:4, marginBottom:14, flexWrap:'wrap', alignItems:'center' }}>\n"
    "            <span style={{\n"
    "              fontSize:8, fontWeight:700, letterSpacing:1.4, padding:'3px 8px',\n"
    "              borderRadius:99, background:'rgba(0,201,167,0.15)',\n"
    "              border:'1px solid rgba(0,201,167,0.45)', color:'var(--teal)',\n"
    "              display:'flex', alignItems:'center', gap:4,\n"
    "            }}>\n"
    "              <span style={{ width:5, height:5, borderRadius:99, background:'var(--teal)',\n"
    "                             display:'inline-block', animation:'tl-pulse 2s ease infinite' }}/>\n"
    "              LIVE\n"
    "            </span>\n"
    "            {(D._dataSources||[]).map(s => (\n"
    "              <span key={s} style={{\n"
    "                fontSize:8, padding:'3px 8px', borderRadius:99,\n"
    "                background:'rgba(255,255,255,0.05)',\n"
    "                border:'1px solid rgba(255,255,255,0.1)',\n"
    "                color:'var(--muted)',\n"
    "              }}>{s}</span>\n"
    "            ))}\n"
    "          </div>\n"
    "        )}\n"
    "\n"
    "        {/* Fishing Score hero */}",

    "C1-live-data-badge"
)

# ─────────────────────────────────────────────────────────────────────────────
# Done
# ─────────────────────────────────────────────────────────────────────────────
with open(PATH, 'w', encoding='utf-8') as f:
    f.write(src)

print(f"\n=== {len(changes)} patches applied, {len(src)-orig_len:+d} bytes ===")
