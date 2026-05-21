#!/usr/bin/env python3
"""patch7.py — real date/time, auto-detect location on load, local-only nearby spots"""

PATH = '/sessions/cool-nifty-clarke/mnt/outputs/index.html'

with open(PATH, 'r', encoding='utf-8') as f:
    src = f.read()

orig_len = len(src)
changes = []

def rep(old, new, label):
    global src
    if old not in src:
        raise ValueError(f"PATTERN NOT FOUND: {label}\n  -> {repr(old[:160])}")
    c = src.count(old)
    if c > 1:
        raise ValueError(f"AMBIGUOUS ({c} matches): {label}")
    src = src.replace(old, new)
    changes.append(label)
    print(f"  ✓ {label}")

print("=== patch7: real date/time + auto-geo + local spots ===")

# ─────────────────────────────────────────────────────────────────────────────
# C1: generateLocationData — inject real current time at top
# ─────────────────────────────────────────────────────────────────────────────
rep(
    (
        "function generateLocationData(loc) {\n"
        "  const lat = loc.lat != null ? loc.lat : -35.18;\n"
        "  const lng = loc.lng != null ? loc.lng : 174.33;\n"
        "  // deterministic pseudo-random: h(n) → 0..1\n"
        "  const h = n => { let x = Math.sin(lat * 127.1 + lng * 311.7 + n * 74.3) * 43758.5453; return x - Math.floor(x); };\n"
        "  const pad = n => String(Math.floor(n)).padStart(2, '0');\n"
        "  const fmt = (hh, mm) => `${pad(hh % 24)}:${pad(((mm % 60) + 60) % 60)}`;"
    ),
    (
        "function generateLocationData(loc) {\n"
        "  const lat = loc.lat != null ? loc.lat : -35.18;\n"
        "  const lng = loc.lng != null ? loc.lng : 174.33;\n"
        "  // real current time\n"
        "  const _now = new Date();\n"
        "  const _nowH = _now.getHours();\n"
        "  const _nowM = _now.getMinutes();\n"
        "  // deterministic pseudo-random: h(n) → 0..1\n"
        "  const h = n => { let x = Math.sin(lat * 127.1 + lng * 311.7 + n * 74.3) * 43758.5453; return x - Math.floor(x); };\n"
        "  const pad = n => String(Math.floor(n)).padStart(2, '0');\n"
        "  const fmt = (hh, mm) => `${pad(hh % 24)}:${pad(((mm % 60) + 60) % 60)}`;"
    ),
    "C1-inject-real-time"
)

# ─────────────────────────────────────────────────────────────────────────────
# C2: Hourly strip — start from current hour, not hardcoded 8
# ─────────────────────────────────────────────────────────────────────────────
rep(
    "  const hourly = Array.from({ length: 24 }, (_, i) => {\n"
    "    const hr = (8 + i) % 24;",
    "  const hourly = Array.from({ length: 24 }, (_, i) => {\n"
    "    const hr = (_nowH + i) % 24;",
    "C2-hourly-real-hour"
)

# ─────────────────────────────────────────────────────────────────────────────
# C3: Daily forecast — real day names and dates
# ─────────────────────────────────────────────────────────────────────────────
rep(
    (
        "  // Daily\n"
        "  const dNames = ['Today','Tue','Wed','Thu','Fri','Sat','Sun'];\n"
        "  const dDates = ['Mon 18','Tue 19','Wed 20','Thu 21','Fri 22','Sat 23','Sun 24'];\n"
        "  const daily = dNames.map((day, i) => {"
    ),
    (
        "  // Daily — real dates\n"
        "  const _dayNames = Array.from({length:7}, (_,i) => { const d=new Date(_now); d.setDate(d.getDate()+i); return i===0?'Today':d.toLocaleDateString('en-US',{weekday:'short'}); });\n"
        "  const _dayDates = Array.from({length:7}, (_,i) => { const d=new Date(_now); d.setDate(d.getDate()+i); return d.toLocaleDateString('en-US',{weekday:'short',day:'numeric'}).replace(',',''); });\n"
        "  const daily = _dayNames.map((day, i) => {"
    ),
    "C3-real-daily-dates"
)

# ─────────────────────────────────────────────────────────────────────────────
# C4: Daily map body — use _dayDates[i] instead of dDates[i]
# ─────────────────────────────────────────────────────────────────────────────
rep(
    "      day, date: dDates[i],",
    "      day, date: _dayDates[i],",
    "C4-use-real-dDates"
)

# ─────────────────────────────────────────────────────────────────────────────
# C5: Conditions tide header — real date
# ─────────────────────────────────────────────────────────────────────────────
rep(
    '              <span style={{ fontSize: 11, color: \'var(--muted)\' }}>Mon 18 May · LINZ</span>',
    '              <span style={{ fontSize: 11, color: \'var(--muted)\' }}>{new Date().toLocaleDateString(\'en-NZ\',{weekday:\'short\',day:\'numeric\',month:\'short\'})} · LINZ</span>',
    "C5-conditions-tide-real-date"
)

# ─────────────────────────────────────────────────────────────────────────────
# C6: BiteTimeline nowHour — real current hour
# ─────────────────────────────────────────────────────────────────────────────
rep(
    "            <BiteTimeline windows={active.windows} nowHour={9.25} />",
    "            <BiteTimeline windows={active.windows} nowHour={new Date().getHours() + new Date().getMinutes()/60} />",
    "C6-bite-timeline-real-hour"
)

# ─────────────────────────────────────────────────────────────────────────────
# D1: App — auto-detect location on mount
# ─────────────────────────────────────────────────────────────────────────────
rep(
    (
        "  const handleLocationSelect = loc => {\n"
        "    setActiveLocation(loc);\n"
        "    setLocData(generateLocationData(loc));\n"
        "    if (loc.lat != null && loc.lng != null) setUserGeoLoc({ lat: loc.lat, lng: loc.lng });\n"
        "  };"
    ),
    (
        "  const handleLocationSelect = loc => {\n"
        "    setActiveLocation(loc);\n"
        "    setLocData(generateLocationData(loc));\n"
        "    if (loc.lat != null && loc.lng != null) setUserGeoLoc({ lat: loc.lat, lng: loc.lng });\n"
        "  };\n"
        "\n"
        "  // Auto-detect location on first load\n"
        "  React.useEffect(() => {\n"
        "    if (!navigator.geolocation) return;\n"
        "    navigator.geolocation.getCurrentPosition(\n"
        "      async pos => {\n"
        "        const { latitude: lat, longitude: lng } = pos.coords;\n"
        "        try {\n"
        "          const res = await fetch(\n"
        "            `https://nominatim.openstreetmap.org/reverse?lat=${lat}&lon=${lng}&format=json`,\n"
        "            { headers: { 'Accept-Language': 'en' } }\n"
        "          );\n"
        "          const d = await res.json();\n"
        "          const name = d.name || d.address?.suburb || d.address?.city || d.address?.town || 'Current Location';\n"
        "          const region = [d.address?.state, d.address?.country].filter(Boolean).join(', ');\n"
        "          const cc = d.address?.country_code || '';\n"
        "          handleLocationSelect({ name, region, lat, lng, countryCode: cc });\n"
        "        } catch(e) {\n"
        "          handleLocationSelect({ name: 'Current Location', region: '', lat, lng });\n"
        "        }\n"
        "      },\n"
        "      () => { /* silently ignore if denied */ },\n"
        "      { timeout: 8000, maximumAge: 300000 }\n"
        "    );\n"
        "  }, []); // eslint-disable-line react-hooks/exhaustive-deps"
    ),
    "D1-auto-detect-on-mount"
)

# ─────────────────────────────────────────────────────────────────────────────
# E1: fetchNearbySpots — bounded=1 + filter by distance ≤ 150km
# ─────────────────────────────────────────────────────────────────────────────
rep(
    (
        "    const qs = async (term) => fetch(`https://nominatim.openstreetmap.org/search?q=${encodeURIComponent(term)}&format=json&limit=6&viewbox=${vb}&bounded=0&addressdetails=1`, hdr).then(r => r.json()).catch(() => []);"
    ),
    (
        "    const qs = async (term) => fetch(`https://nominatim.openstreetmap.org/search?q=${encodeURIComponent(term)}&format=json&limit=8&viewbox=${vb}&bounded=1&addressdetails=1`, hdr).then(r => r.json()).catch(() => []);"
    ),
    "E1-bounded1"
)

# ─────────────────────────────────────────────────────────────────────────────
# E2: Filter spots by distance after building list
# ─────────────────────────────────────────────────────────────────────────────
rep(
    (
        "      const spots = unique.slice(0, 7).map(p => {\n"
        "        const plat = parseFloat(p.lat), plng = parseFloat(p.lon);\n"
        "        const dlat = (plat - lat) * 111;\n"
        "        const dlng = (plng - lng) * 111 * Math.cos(lat * Math.PI / 180);\n"
        "        const distKm = Math.round(Math.sqrt(dlat*dlat + dlng*dlng));\n"
        "        const score = Math.round(38 + h(plat, plng, 1) * 57);\n"
        "        const name = p.name || p.display_name.split(',')[0].trim();\n"
        "        const region = [p.address?.suburb, p.address?.city, p.address?.county, p.address?.state].filter(Boolean)[0] || '';\n"
        "        return { name, region, lat: plat, lng: plng, distKm, score };\n"
        "      }).sort((a, b) => b.score - a.score);"
    ),
    (
        "      const spots = unique.map(p => {\n"
        "        const plat = parseFloat(p.lat), plng = parseFloat(p.lon);\n"
        "        const dlat = (plat - lat) * 111;\n"
        "        const dlng = (plng - lng) * 111 * Math.cos(lat * Math.PI / 180);\n"
        "        const distKm = Math.round(Math.sqrt(dlat*dlat + dlng*dlng));\n"
        "        const score = Math.round(38 + h(plat, plng, 1) * 57);\n"
        "        const name = p.name || p.display_name.split(',')[0].trim();\n"
        "        const region = [p.address?.suburb, p.address?.city, p.address?.county, p.address?.state].filter(Boolean)[0] || '';\n"
        "        return { name, region, lat: plat, lng: plng, distKm, score };\n"
        "      }).filter(s => s.distKm <= 150 && s.name.length > 1)\n"
        "        .sort((a, b) => b.score - a.score)\n"
        "        .slice(0, 7);"
    ),
    "E2-filter-by-distance"
)

# ─────────────────────────────────────────────────────────────────────────────
# Done
# ─────────────────────────────────────────────────────────────────────────────
with open(PATH, 'w', encoding='utf-8') as f:
    f.write(src)

print(f"\n=== {len(changes)} patches applied, {len(src)-orig_len:+d} bytes ===")
