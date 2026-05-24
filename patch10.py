#!/usr/bin/env python3
"""patch10.py — NZ regs, catch share card, bait & lure suggestions"""

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

print("=== patch10: NZ regs + share card + bait suggestions ===")

# ─────────────────────────────────────────────────────────────────────────────
# A1: NZ_REGS data — before inputSt
# ─────────────────────────────────────────────────────────────────────────────
rep(
    "const inputSt = {",

    "const NZ_REGS = [\n"
    "  { id:'snapper',  name:'Snapper',       maori:'Tāmure',      color:'#FF6B6B', minSize:30, bag:9,  bagNote:'per person/day', measure:'total length', note:'Northland/Hauraki Gulf: check regional limits' },\n"
    "  { id:'kingfish', name:'Kingfish',       maori:'Haku',        color:'#F5A623', minSize:75, bag:3,  bagNote:'per person/day', measure:'total length', note:'Tag & release encouraged for large fish' },\n"
    "  { id:'kahawai',  name:'Kahawai',        maori:'Kahawai',     color:'#7BD4F0', minSize:30, bag:20, bagNote:'per person/day', measure:'total length', note:'' },\n"
    "  { id:'trevally', name:'Trevally',       maori:'Araara',      color:'#C77DFF', minSize:25, bag:20, bagNote:'per person/day', measure:'total length', note:'' },\n"
    "  { id:'hapuka',   name:'Hāpuku / Groper',maori:'Hāpuku',     color:'#4D96FF', minSize:40, bag:3,  bagNote:'combined hāpuku & bass', measure:'total length', note:'' },\n"
    "  { id:'tarakihi', name:'Tarakihi',       maori:'Tarakihi',   color:'#FF9F43', minSize:25, bag:20, bagNote:'per person/day', measure:'total length', note:'' },\n"
    "  { id:'marlin',   name:'Striped Marlin', maori:'Takeketonga', color:'#00C9A7', minSize:null, bag:1, bagNote:'per vessel/day', measure:'LJFL', note:'Tag & release strongly encouraged' },\n"
    "  { id:'johndory', name:'John Dory',      maori:'Kuparu',      color:'#7B8FA1', minSize:25, bag:20, bagNote:'per person/day', measure:'total length', note:'' },\n"
    "  { id:'gurnard',  name:'Gurnard',        maori:'Kumukumu',    color:'#7B8FA1', minSize:25, bag:20, bagNote:'per person/day', measure:'total length', note:'' },\n"
    "  { id:'bluecod',  name:'Blue Cod',       maori:'Rāwaru',      color:'#7BD4F0', minSize:33, bag:20, bagNote:'per person/day', measure:'total length', note:'Varies by region — some areas closed or restricted' },\n"
    "  { id:'crayfish', name:'Rock Lobster',   maori:'Kōura',       color:'#FF6B6B', minSize:54, bag:6,  bagNote:'per person/day', measure:'tail width', note:'Berried / soft-shell females must be returned' },\n"
    "  { id:'paua',     name:'Pāua',           maori:'Pāua',        color:'#00C9A7', minSize:125,bag:10, bagNote:'per person/day', measure:'shell length', note:'Must be prised off underwater, not on rocks' },\n"
    "];\n"
    "\n"
    "const inputSt = {",

    "A1-NZ-regs-data"
)

# ─────────────────────────────────────────────────────────────────────────────
# A2: RegsSheet component — before EmptyCatchLog
# ─────────────────────────────────────────────────────────────────────────────
rep(
    "function EmptyCatchLog({ onAdd }) {",

    "function RegsSheet({ onClose }) {\n"
    "  React.useEffect(() => {\n"
    "    const prev = document.body.style.overflow;\n"
    "    document.body.style.overflow = 'hidden';\n"
    "    return () => { document.body.style.overflow = prev; };\n"
    "  }, []);\n"
    "  return (\n"
    "    <>\n"
    "      <div onClick={onClose} style={{ position:'fixed', inset:0, background:'rgba(0,0,0,0.55)', zIndex:200, backdropFilter:'blur(4px)', WebkitBackdropFilter:'blur(4px)' }}/>\n"
    "      <div style={{ position:'fixed', bottom:0, left:0, right:0, zIndex:201, background:'linear-gradient(180deg,#131B2E,#0D1526)', borderRadius:'22px 22px 0 0', border:'1px solid rgba(255,255,255,0.09)', borderBottom:'none', maxHeight:'88vh', overflowY:'auto', padding:'0 18px max(28px,env(safe-area-inset-bottom,28px))', animation:'tl-screen-in .3s cubic-bezier(.21,.61,.35,1)' }}>\n"
    "        <div style={{ width:36, height:4, borderRadius:2, background:'rgba(255,255,255,0.18)', margin:'14px auto 20px' }}/>\n"
    "        <div style={{ display:'flex', alignItems:'center', justifyContent:'space-between', marginBottom:6 }}>\n"
    "          <div>\n"
    "            <div style={{ fontSize:10, letterSpacing:1.5, textTransform:'uppercase', color:'var(--teal)' }}>MPI Guidelines</div>\n"
    "            <h2 style={{ margin:'4px 0 0', fontSize:21, fontWeight:700, letterSpacing:-0.5 }}>Size & Bag Limits</h2>\n"
    "          </div>\n"
    "          <button onClick={onClose} style={{ background:'rgba(255,255,255,0.07)', border:'none', borderRadius:999, width:34, height:34, color:'var(--muted)', cursor:'pointer', fontSize:20, display:'flex', alignItems:'center', justifyContent:'center' }}>×</button>\n"
    "        </div>\n"
    "        <div style={{ fontSize:11, color:'var(--muted)', marginBottom:20, lineHeight:1.5 }}>Recreational limits for NZ saltwater species. Always verify at <span style={{ color:'var(--teal)' }}>mpi.govt.nz</span> — rules vary by region and change.</div>\n"
    "        <div style={{ display:'flex', flexDirection:'column', gap:10 }}>\n"
    "          {NZ_REGS.map(r => (\n"
    "            <div key={r.id} style={{ background:'rgba(255,255,255,0.03)', border:'1px solid rgba(255,255,255,0.07)', borderRadius:14, padding:'12px 14px' }}>\n"
    "              <div style={{ display:'flex', alignItems:'center', justifyContent:'space-between', marginBottom:r.note?6:0 }}>\n"
    "                <div>\n"
    "                  <span style={{ fontWeight:700, fontSize:15 }}>{r.name}</span>\n"
    "                  {r.maori && <span style={{ fontSize:11, color:'var(--muted)', fontStyle:'italic', marginLeft:8 }}>{r.maori}</span>}\n"
    "                </div>\n"
    "                <div style={{ display:'flex', gap:6, flexShrink:0 }}>\n"
    "                  {r.minSize && (\n"
    "                    <div style={{ textAlign:'center', padding:'4px 10px', borderRadius:8, background:`${r.color}18`, border:`1px solid ${r.color}44` }}>\n"
    "                      <div style={{ fontSize:9, color:r.color, letterSpacing:0.8 }}>MIN SIZE</div>\n"
    "                      <div style={{ fontSize:16, fontWeight:700, color:r.color, fontVariantNumeric:'tabular-nums' }}>{r.minSize}<span style={{ fontSize:9 }}>{r.measure==='tail width'?'mm tail':r.measure==='shell length'?'mm':r.measure==='LJFL'?'cm LJFL':'cm'}</span></div>\n"
    "                    </div>\n"
    "                  )}\n"
    "                  <div style={{ textAlign:'center', padding:'4px 10px', borderRadius:8, background:'rgba(255,255,255,0.04)', border:'1px solid rgba(255,255,255,0.1)' }}>\n"
    "                    <div style={{ fontSize:9, color:'var(--muted)', letterSpacing:0.8 }}>BAG LIMIT</div>\n"
    "                    <div style={{ fontSize:16, fontWeight:700, fontVariantNumeric:'tabular-nums' }}>{r.bag}</div>\n"
    "                    <div style={{ fontSize:9, color:'var(--muted)' }}>{r.bagNote}</div>\n"
    "                  </div>\n"
    "                </div>\n"
    "              </div>\n"
    "              {r.note && <div style={{ fontSize:11, color:'rgba(255,166,35,0.85)', marginTop:4, lineHeight:1.4 }}>⚠ {r.note}</div>}\n"
    "            </div>\n"
    "          ))}\n"
    "        </div>\n"
    "        <div style={{ marginTop:20, padding:'12px 14px', background:'rgba(0,201,167,0.06)', borderRadius:12, border:'1px solid rgba(0,201,167,0.15)', fontSize:11, color:'var(--muted)', lineHeight:1.6 }}>\n"
    "          These are general recreational limits. Regional rules, closed seasons, and special fishing areas may apply. Always check <span style={{ color:'var(--teal)', fontWeight:600 }}>mpi.govt.nz/fishing</span> for current regulations.\n"
    "        </div>\n"
    "      </div>\n"
    "    </>\n"
    "  );\n"
    "}\n"
    "\n"
    "function EmptyCatchLog({ onAdd }) {",

    "A2-RegsSheet-component"
)

# ─────────────────────────────────────────────────────────────────────────────
# A3: generateShareCard — before CatchCard
# ─────────────────────────────────────────────────────────────────────────────
rep(
    "function CatchCard({ entry, intensity, expanded, onToggle, onDelete }) {",

    "async function generateShareCard(entry, sp) {\n"
    "  const W = 1080, H = 580;\n"
    "  const c = document.createElement('canvas');\n"
    "  c.width = W; c.height = H;\n"
    "  const ctx = c.getContext('2d');\n"
    "  await document.fonts.ready;\n"
    "  // Background\n"
    "  const bg = ctx.createLinearGradient(0, 0, W, H);\n"
    "  bg.addColorStop(0, '#0A0F1E'); bg.addColorStop(1, '#131B2E');\n"
    "  ctx.fillStyle = bg; ctx.fillRect(0, 0, W, H);\n"
    "  // Grid\n"
    "  ctx.strokeStyle = 'rgba(0,201,167,0.05)'; ctx.lineWidth = 0.5;\n"
    "  for (let x=0;x<W;x+=40){ctx.beginPath();ctx.moveTo(x,0);ctx.lineTo(x,H);ctx.stroke();}\n"
    "  for (let y=0;y<H;y+=40){ctx.beginPath();ctx.moveTo(0,y);ctx.lineTo(W,y);ctx.stroke();}\n"
    "  // Photo or colour slab on left\n"
    "  const slabW = 440;\n"
    "  if (entry.photo) {\n"
    "    await new Promise(r => {\n"
    "      const img = new Image();\n"
    "      img.onload = () => {\n"
    "        ctx.save();\n"
    "        ctx.beginPath(); ctx.rect(0, 0, slabW, H); ctx.clip();\n"
    "        const scale = Math.max(slabW/img.width, H/img.height);\n"
    "        ctx.drawImage(img, (slabW-img.width*scale)/2, (H-img.height*scale)/2, img.width*scale, img.height*scale);\n"
    "        ctx.restore();\n"
    "        // fade right edge into dark\n"
    "        const fade = ctx.createLinearGradient(slabW-100, 0, slabW, 0);\n"
    "        fade.addColorStop(0, 'rgba(10,15,30,0)'); fade.addColorStop(1, 'rgba(10,15,30,1)');\n"
    "        ctx.fillStyle = fade; ctx.fillRect(slabW-100, 0, 100, H);\n"
    "        r();\n"
    "      };\n"
    "      img.src = entry.photo;\n"
    "    });\n"
    "  } else {\n"
    "    const grad = ctx.createLinearGradient(0, 0, slabW, H);\n"
    "    grad.addColorStop(0, sp.color+'44'); grad.addColorStop(1, sp.color+'08');\n"
    "    ctx.fillStyle = grad; ctx.fillRect(0, 0, slabW, H);\n"
    "    ctx.fillStyle = sp.color+'33';\n"
    "    ctx.font = 'bold 200px Inter,system-ui';\n"
    "    ctx.textAlign = 'center'; ctx.textBaseline = 'middle';\n"
    "    ctx.fillText(sp.name[0], slabW/2, H/2);\n"
    "    const fade2 = ctx.createLinearGradient(slabW-80, 0, slabW, 0);\n"
    "    fade2.addColorStop(0, 'rgba(10,15,30,0)'); fade2.addColorStop(1, 'rgba(11,18,32,1)');\n"
    "    ctx.fillStyle = fade2; ctx.fillRect(slabW-80, 0, 80, H);\n"
    "  }\n"
    "  // Teal left bar\n"
    "  ctx.fillStyle = 'rgba(0,201,167,0.9)'; ctx.fillRect(0, 0, 5, H);\n"
    "  // Right text area\n"
    "  ctx.textAlign = 'left'; ctx.textBaseline = 'alphabetic';\n"
    "  const tx = slabW + 44;\n"
    "  let ty = 90;\n"
    "  // App label\n"
    "  ctx.fillStyle = 'rgba(0,201,167,0.85)';\n"
    "  ctx.font = '600 14px Inter,system-ui';\n"
    "  ctx.fillText('TIGHT LINES', tx, ty); ty += 52;\n"
    "  // Species\n"
    "  ctx.fillStyle = '#FFFFFF';\n"
    "  ctx.font = 'bold 70px Inter,system-ui';\n"
    "  ctx.fillText(sp.name, tx, ty); ty += 20;\n"
    "  if (sp.maori) {\n"
    "    ctx.fillStyle = 'rgba(255,255,255,0.4)';\n"
    "    ctx.font = 'italic 26px Inter,system-ui';\n"
    "    ctx.fillText(sp.maori, tx, ty+26); ty += 54;\n"
    "  } else { ty += 30; }\n"
    "  ty += 22;\n"
    "  // Stats\n"
    "  if (entry.length) {\n"
    "    ctx.fillStyle = 'rgba(0,201,167,1)';\n"
    "    ctx.font = 'bold 52px Inter,system-ui';\n"
    "    ctx.fillText(entry.length+' cm', tx, ty); ty += 64;\n"
    "  }\n"
    "  if (entry.weight) {\n"
    "    ctx.fillStyle = 'rgba(245,166,35,1)';\n"
    "    ctx.font = 'bold 52px Inter,system-ui';\n"
    "    ctx.fillText(entry.weight+' kg', tx, ty); ty += 64;\n"
    "  }\n"
    "  ty += 8;\n"
    "  ctx.fillStyle = 'rgba(255,255,255,0.4)';\n"
    "  ctx.font = '500 22px Inter,system-ui';\n"
    "  if (entry.location) { ctx.fillText('\\u{1F4CD} '+entry.location, tx, ty); ty += 34; }\n"
    "  if (entry.date) {\n"
    "    const d = new Date(entry.date);\n"
    "    ctx.fillText(d.toLocaleDateString('en-NZ',{weekday:'long',day:'numeric',month:'long',year:'numeric'}), tx, ty);\n"
    "  }\n"
    "  // Bottom teal line\n"
    "  ctx.fillStyle = 'rgba(0,201,167,0.35)'; ctx.fillRect(0, H-3, W, 3);\n"
    "  return c.toDataURL('image/png');\n"
    "}\n"
    "\n"
    "function CatchCard({ entry, intensity, expanded, onToggle, onDelete }) {",

    "A3-generateShareCard"
)

# ─────────────────────────────────────────────────────────────────────────────
# A4: Add sharing state + handleShare inside CatchCard
# ─────────────────────────────────────────────────────────────────────────────
rep(
    "  const [confirmDel, setConfirmDel] = React.useState(false);",

    "  const [confirmDel, setConfirmDel] = React.useState(false);\n"
    "  const [sharing, setSharing] = React.useState(false);\n"
    "  const handleShare = async () => {\n"
    "    setSharing(true);\n"
    "    try {\n"
    "      const dataUrl = await generateShareCard(entry, sp);\n"
    "      if (navigator.share) {\n"
    "        try {\n"
    "          const res = await fetch(dataUrl);\n"
    "          const blob = await res.blob();\n"
    "          const file = new File([blob], 'tight-lines-catch.png', { type:'image/png' });\n"
    "          if (navigator.canShare && navigator.canShare({ files:[file] })) {\n"
    "            await navigator.share({ files:[file], title:`${sp.name} \\u2014 Tight Lines` });\n"
    "            return;\n"
    "          }\n"
    "        } catch(e) {}\n"
    "      }\n"
    "      const a = document.createElement('a');\n"
    "      a.href = dataUrl;\n"
    "      a.download = `tight-lines-${sp.name.toLowerCase().replace(/\\s+/g,'-')}.png`;\n"
    "      a.click();\n"
    "    } finally { setSharing(false); }\n"
    "  };",

    "A4-handleShare-in-CatchCard"
)

# ─────────────────────────────────────────────────────────────────────────────
# A5: Add Share button to expanded CatchCard
# ─────────────────────────────────────────────────────────────────────────────
rep(
    "          <div style={{ display:'flex', gap:8, marginTop:4 }}>\n"
    "            {!confirmDel\n"
    "              ? <button onClick={()=>setConfirmDel(true)}",

    "          <div style={{ display:'flex', gap:8, marginTop:4 }}>\n"
    "            <button onClick={handleShare} disabled={sharing} style={{ padding:'9px 14px', background:'rgba(0,201,167,0.1)', border:'1px solid rgba(0,201,167,0.28)', borderRadius:10, color:'var(--teal)', fontSize:12, fontWeight:600, cursor:'pointer', fontFamily:'Inter,system-ui', display:'flex', alignItems:'center', gap:5, flexShrink:0, opacity:sharing?0.6:1 }}>\n"
    "              <svg width=\"13\" height=\"13\" viewBox=\"0 0 24 24\" fill=\"none\"><path d=\"M4 12v8a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-8M16 6l-4-4-4 4M12 2v13\" stroke=\"currentColor\" strokeWidth=\"2\" strokeLinecap=\"round\" strokeLinejoin=\"round\"/></svg>\n"
    "              {sharing ? '…' : 'Share'}\n"
    "            </button>\n"
    "            {!confirmDel\n"
    "              ? <button onClick={()=>setConfirmDel(true)}",

    "A5-share-button-in-CatchCard"
)

# ─────────────────────────────────────────────────────────────────────────────
# A6: Add showRegs state to CatchLog
# ─────────────────────────────────────────────────────────────────────────────
rep(
    "  const [showForm, setShowForm] = React.useState(false);",
    "  const [showForm, setShowForm] = React.useState(false);\n"
    "  const [showRegs, setShowRegs] = React.useState(false);",
    "A6-showRegs-state"
)

# ─────────────────────────────────────────────────────────────────────────────
# A7: Add Regs button in CatchLog header
# ─────────────────────────────────────────────────────────────────────────────
rep(
    "          <button onClick={()=>setShowForm(true)} style={{\n"
    "            display:'flex', alignItems:'center', gap:6,\n"
    "            background:'var(--teal)', color:'#0A0F1E', border:'none',\n"
    "            borderRadius:999, padding:'10px 16px', fontWeight:700,\n"
    "            fontSize:13, cursor:'pointer', fontFamily:'Inter,system-ui',\n"
    "            boxShadow:'0 4px 16px -4px rgba(0,201,167,0.6)',\n"
    "          }}>\n"
    "            <span style={{ fontSize:19, lineHeight:1, marginTop:-1 }}>+</span> Log\n"
    "          </button>",

    "          <div style={{ display:'flex', gap:8 }}>\n"
    "            <button onClick={()=>setShowRegs(true)} style={{ padding:'10px 14px', background:'rgba(255,255,255,0.06)', border:'1px solid rgba(255,255,255,0.1)', borderRadius:999, color:'var(--muted)', fontSize:12, fontWeight:600, cursor:'pointer', fontFamily:'Inter,system-ui' }}>Regs</button>\n"
    "            <button onClick={()=>setShowForm(true)} style={{ display:'flex', alignItems:'center', gap:6, background:'var(--teal)', color:'#0A0F1E', border:'none', borderRadius:999, padding:'10px 16px', fontWeight:700, fontSize:13, cursor:'pointer', fontFamily:'Inter,system-ui', boxShadow:'0 4px 16px -4px rgba(0,201,167,0.6)' }}>\n"
    "              <span style={{ fontSize:19, lineHeight:1, marginTop:-1 }}>+</span> Log\n"
    "            </button>\n"
    "          </div>",

    "A7-regs-button-in-header"
)

# ─────────────────────────────────────────────────────────────────────────────
# A8: Render RegsSheet modal in CatchLog
# ─────────────────────────────────────────────────────────────────────────────
rep(
    "      {showForm && <AddCatchSheet intensity={intensity} activeLocation={activeLocation} onSave={addCatch} onClose={()=>setShowForm(false)}/>}",
    "      {showRegs && <RegsSheet onClose={()=>setShowRegs(false)}/>}\n"
    "      {showForm && <AddCatchSheet intensity={intensity} activeLocation={activeLocation} onSave={addCatch} onClose={()=>setShowForm(false)}/>}",
    "A8-render-RegsSheet"
)

# ─────────────────────────────────────────────────────────────────────────────
# B1: getBaitSuggestions function — before Dashboard
# ─────────────────────────────────────────────────────────────────────────────
rep(
    "function Dashboard({ tweaks, activeLocation, onLocationSelect, setUserGeoLoc, prefs }) {",

    "function getBaitSuggestions(nowData, tideEvents) {\n"
    "  const h = new Date().getHours();\n"
    "  const month = new Date().getMonth();\n"
    "  const wind  = nowData.windSpeed  || 0;\n"
    "  const swell = nowData.waveHeight || 0;\n"
    "  const temp  = nowData.waterTemp  || 18;\n"
    "  const isDawn   = h >= 5  && h < 7;\n"
    "  const isDusk   = h >= 17 && h < 20;\n"
    "  const isNight  = h < 5   || h >= 20;\n"
    "  const isCalm   = wind  <= 12;\n"
    "  const isRough  = swell >  1.5;\n"
    "  const isWarm   = temp  >= 20;\n"
    "  const isCold   = temp  <  16;\n"
    "  const isSummer = month === 11 || month <= 1;\n"
    "  const isWinter = month >= 5   && month <= 7;\n"
    "  const nowMs = Date.now();\n"
    "  const upcoming = (tideEvents||[]).filter(e=>e.time>nowMs).sort((a,b)=>a.time-b.time);\n"
    "  const isIncoming = upcoming[0]?.type === 'high';\n"
    "  const sug = [];\n"
    "  if ((isDawn||isDusk) && isCalm && !isRough)\n"
    "    sug.push({ name:'Surface popper / stickbait', tag:'TOP WATER', color:'var(--amber)', reason:'Dawn & dusk trigger surface blitzes — walk-the-dog for kingfish and kahawai' });\n"
    "  if (isWarm && !isRough && (isSummer || month<=2))\n"
    "    sug.push({ name:'Knife jig / speed jig', tag:'PELAGIC', color:'#C77DFF', reason:'Warm water activates kingfish near the surface — drop fast, burn back up' });\n"
    "  if (!isRough && isIncoming)\n"
    "    sug.push({ name:'Soft bait on jig head', tag:'INCOMING TIDE', color:'var(--teal)', reason:'Incoming tide pushes bait over drop-offs — drift paddle tails with the current' });\n"
    "  if (isRough || wind > 20)\n"
    "    sug.push({ name:'Pilchard on ledger rig', tag:'SEEK SHELTER', color:'#7BD4F0', reason:'Rough conditions: find a sheltered bay and fish heavy sinker + fresh pilchard on the bottom' });\n"
    "  if (isCold || isWinter)\n"
    "    sug.push({ name:'Squid strip — slow bottom', tag:'WINTER', color:'#FF9F43', reason:'Cold water slows fish — slow presentation with squid near the seabed triggers snapper' });\n"
    "  if (isNight)\n"
    "    sug.push({ name:'Whole pilchard or squid', tag:'NIGHT', color:'#4D96FF', reason:'Snapper and trevally feed confidently after dark — scent beats sight' });\n"
    "  sug.push({ name:'Kabura / tai rubber', tag:'RELIABLE', color:'rgba(255,255,255,0.45)', reason:'Works in almost any condition — slow spiral drop attracts snapper and trevally all year' });\n"
    "  const seen = new Set();\n"
    "  return sug.filter(s=>{ if(seen.has(s.name)) return false; seen.add(s.name); return true; }).slice(0,3);\n"
    "}\n"
    "\n"
    "function Dashboard({ tweaks, activeLocation, onLocationSelect, setUserGeoLoc, prefs }) {",

    "B1-getBaitSuggestions"
)

# ─────────────────────────────────────────────────────────────────────────────
# B2: "What's Working" bait section in Dashboard — before footer
# ─────────────────────────────────────────────────────────────────────────────
rep(
    "      <div style={{ padding: '20px 18px', textAlign: 'center', fontSize: 10, color: 'rgba(255,255,255,0.25)', letterSpacing: 1.5 }}>\n"
    "        TIDE & METOCEAN · LINZ · NIWA\n"
    "      </div>",

    "      {/* Bait & lure suggestions */}\n"
    "      {(() => {\n"
    "        const baits = getBaitSuggestions(D.now, D.tideEvents);\n"
    "        return (\n"
    "          <div style={{ marginTop:26, padding:'0 18px' }}>\n"
    "            <SectionHeader title=\"What's Working\" hint=\"Conditions-based\" inset />\n"
    "            <div style={{ display:'flex', flexDirection:'column', gap:8, marginTop:8 }}>\n"
    "              {baits.map((b,i) => (\n"
    "                <TLGlass key={i} intensity={intensity} padding={0} style={{ overflow:'hidden' }}>\n"
    "                  <div style={{ display:'flex', alignItems:'center', gap:12, padding:'12px 14px' }}>\n"
    "                    <div style={{ width:40, height:40, borderRadius:10, background:`${b.color}18`, border:`1px solid ${b.color}44`, display:'flex', alignItems:'center', justifyContent:'center', flexShrink:0 }}>\n"
    "                      <svg width='20' height='20' viewBox='0 0 24 24' fill='none'><path d='M2 12C2 12 7 5 12 5C17 5 22 12 22 12C22 12 17 19 12 19C7 19 2 12 2 12Z' stroke='currentColor' strokeWidth='1.5'/><path d='M4 8C6 6 9 4 13 5L22 12L13 19C9 20 6 18 4 16' fill='currentColor' opacity='0.15'/><circle cx='12' cy='12' r='3' stroke='currentColor' strokeWidth='1.5'/></svg>\n"
    "                    </div>\n"
    "                    <div style={{ flex:1, minWidth:0 }}>\n"
    "                      <div style={{ display:'flex', alignItems:'center', gap:6, marginBottom:3 }}>\n"
    "                        <span style={{ fontSize:13, fontWeight:700 }}>{b.name}</span>\n"
    "                        <span style={{ fontSize:9, fontWeight:700, letterSpacing:0.8, color:b.color, background:`${b.color}18`, padding:'2px 6px', borderRadius:4 }}>{b.tag}</span>\n"
    "                      </div>\n"
    "                      <div style={{ fontSize:11, color:'var(--muted)', lineHeight:1.45 }}>{b.reason}</div>\n"
    "                    </div>\n"
    "                  </div>\n"
    "                </TLGlass>\n"
    "              ))}\n"
    "            </div>\n"
    "          </div>\n"
    "        );\n"
    "      })()}\n"
    "\n"
    "      <div style={{ padding: '20px 18px', textAlign: 'center', fontSize: 10, color: 'rgba(255,255,255,0.25)', letterSpacing: 1.5 }}>\n"
    "        TIDE & METOCEAN · LINZ · NIWA\n"
    "      </div>",

    "B2-whats-working-dashboard"
)

# ─────────────────────────────────────────────────────────────────────────────
# Done
# ─────────────────────────────────────────────────────────────────────────────
with open(PATH, 'w', encoding='utf-8') as f:
    f.write(src)

print(f"\n=== {len(changes)} patches applied, {len(src)-orig_len:+d} bytes ===")
