#!/usr/bin/env python3
"""patch9_revert.py — undo patch9 AI fish ID changes"""

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

print("=== patch9_revert: removing AI fish ID ===")

# C1 revert: remove identifying + identifyResult state
rep(
    "  const [photo, setPhoto]       = React.useState(null);\n"
    "  const [identifying, setIdentifying] = React.useState(false);\n"
    "  const [identifyResult, setIdentifyResult] = React.useState(null);\n"
    "  const fileRef = React.useRef(null);",

    "  const [photo, setPhoto]       = React.useState(null);\n"
    "  const fileRef = React.useRef(null);",

    "R1-remove-identify-state"
)

# C2 revert: restore handlePhoto without identifyFish call
rep(
    "        const dataUrl = canvas.toDataURL('image/jpeg', 0.82);\n"
    "        setPhoto(dataUrl);\n"
    "        identifyFish(dataUrl);\n"
    "      };\n"
    "      img.src = ev.target.result;\n"
    "    };\n"
    "    reader.readAsDataURL(file);\n"
    "  };",

    "        setPhoto(canvas.toDataURL('image/jpeg', 0.82));\n"
    "      };\n"
    "      img.src = ev.target.result;\n"
    "    };\n"
    "    reader.readAsDataURL(file);\n"
    "  };",

    "R2-restore-handlePhoto"
)

# C3 revert: remove identifyFish function
rep(
    "  const identifyFish = async (dataUrl) => {\n"
    "    const key = localStorage.getItem('tl_claude_api_key') || '';\n"
    "    if (!key.trim()) return;\n"
    "    setIdentifying(true);\n"
    "    setIdentifyResult(null);\n"
    "    try {\n"
    "      const b64 = dataUrl.split(',')[1];\n"
    "      const res = await fetch('https://api.anthropic.com/v1/messages', {\n"
    "        method: 'POST',\n"
    "        headers: {\n"
    "          'Content-Type': 'application/json',\n"
    "          'x-api-key': key.trim(),\n"
    "          'anthropic-version': '2023-06-01',\n"
    "          'anthropic-dangerous-direct-browser-access': 'true',\n"
    "        },\n"
    "        body: JSON.stringify({\n"
    "          model: 'claude-haiku-4-5-20251001',\n"
    "          max_tokens: 120,\n"
    "          messages: [{\n"
    "            role: 'user',\n"
    "            content: [\n"
    "              { type: 'image', source: { type: 'base64', media_type: 'image/jpeg', data: b64 } },\n"
    "              { type: 'text', text: 'Identify the fish species in this photo. Reply with only: the common name, then the scientific name in parentheses. Example: \"Snapper (Chrysophrys auratus)\". If you cannot identify a fish, reply \"Unknown fish\".' }\n"
    "            ]\n"
    "          }]\n"
    "        }),\n"
    "      });\n"
    "      const data = await res.json();\n"
    "      const text = (data.content?.[0]?.text || '').trim();\n"
    "      if (text) {\n"
    "        setIdentifyResult(text);\n"
    "        // Auto-select closest matching species chip\n"
    "        const lower = text.toLowerCase();\n"
    "        const match = window.TL_LOG_SPECIES.find(s =>\n"
    "          lower.includes(s.name.toLowerCase()) ||\n"
    "          lower.includes(s.id.toLowerCase())\n"
    "        );\n"
    "        if (match) setSpecies(match.id);\n"
    "      }\n"
    "    } catch(e) {\n"
    "      console.warn('Fish ID error:', e);\n"
    "    } finally {\n"
    "      setIdentifying(false);\n"
    "    }\n"
    "  };\n"
    "\n"
    "  const handleSave = () => {",

    "  const handleSave = () => {",

    "R3-remove-identifyFish-fn"
)

# C4 revert: un-expose LOG_SPECIES globally
rep(
    "const LOG_SPECIES = window.TL_LOG_SPECIES = [",
    "const LOG_SPECIES = [",
    "R4-unexpose-LOG_SPECIES"
)

# C5 revert: restore original photo UI
rep(
    "          {photo\n"
    "            ? <div>\n"
    "                <div style={{ position:'relative', display:'inline-block' }}>\n"
    "                  <img src={photo} style={{ width:110, height:110, objectFit:'cover', borderRadius:14, border:`1.5px solid ${selSp.color}44` }} alt=\"catch preview\"/>\n"
    "                  <button onClick={()=>{setPhoto(null);setIdentifyResult(null);}} style={{ position:'absolute', top:-7, right:-7, background:'#0D1526', border:'1.5px solid rgba(255,255,255,0.2)', borderRadius:999, width:24, height:24, color:'white', cursor:'pointer', fontSize:14, display:'flex', alignItems:'center', justifyContent:'center', lineHeight:1 }}>×</button>\n"
    "                  {identifying && <div style={{ position:'absolute', inset:0, borderRadius:14, background:'rgba(13,21,38,0.72)', display:'flex', flexDirection:'column', alignItems:'center', justifyContent:'center', gap:6 }}>\n"
    "                    <svg width=\"22\" height=\"22\" viewBox=\"0 0 24 24\" fill=\"none\" style={{ animation:'tl-spin 1s linear infinite' }}><circle cx=\"12\" cy=\"12\" r=\"10\" stroke=\"rgba(255,255,255,0.15)\" strokeWidth=\"2.5\"/><path d=\"M12 2a10 10 0 0 1 10 10\" stroke=\"var(--teal)\" strokeWidth=\"2.5\" strokeLinecap=\"round\"/></svg>\n"
    "                    <span style={{ fontSize:9, color:'var(--teal)', letterSpacing:0.8 }}>ANALYSING</span>\n"
    "                  </div>}\n"
    "                </div>\n"
    "                {identifyResult && !identifying && <div style={{ marginTop:8, padding:'7px 10px', background:'rgba(0,201,167,0.1)', border:'1px solid rgba(0,201,167,0.25)', borderRadius:10, maxWidth:220 }}>\n"
    "                  <div style={{ fontSize:9, letterSpacing:1, color:'var(--teal)', marginBottom:3 }}>AI IDENTIFIED</div>\n"
    "                  <div style={{ fontSize:12, fontWeight:600, color:'var(--ink)', lineHeight:1.4 }}>{identifyResult}</div>\n"
    "                </div>}\n"
    "                {!localStorage.getItem('tl_claude_api_key') && !identifying && !identifyResult && <div style={{ marginTop:8, fontSize:10, color:'var(--muted)', maxWidth:180, lineHeight:1.5 }}>Add your Claude API key in Settings to enable AI fish ID</div>}\n"
    "              </div>",

    "          {photo\n"
    "            ? <div style={{ position:'relative', display:'inline-block' }}>\n"
    "                <img src={photo} style={{ width:110, height:110, objectFit:'cover', borderRadius:14, border:`1.5px solid ${selSp.color}44` }} alt=\"catch preview\"/>\n"
    "                <button onClick={()=>setPhoto(null)} style={{ position:'absolute', top:-7, right:-7, background:'#0D1526', border:'1.5px solid rgba(255,255,255,0.2)', borderRadius:999, width:24, height:24, color:'white', cursor:'pointer', fontSize:14, display:'flex', alignItems:'center', justifyContent:'center', lineHeight:1 }}>×</button>\n"
    "              </div>",

    "R5-restore-photo-ui"
)

# C6 revert: remove spin keyframe
rep(
    "@keyframes tl-spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }\n"
    "      @keyframes tl-screen-in {",
    "@keyframes tl-screen-in {",
    "R6-remove-spin-keyframe"
)

# S1 revert: remove AI Features section from Settings
rep(
    "        {/* AI Features */}\n"
    "        <div style={{ marginBottom:16 }}>\n"
    "          <SectionLabel>AI Features</SectionLabel>\n"
    "          <TLGlass intensity={intensity} style={{ borderRadius:16, overflow:'hidden', padding:'14px 16px' }}>\n"
    "            <div style={{ fontSize:10, letterSpacing:1, textTransform:'uppercase', color:'var(--muted)', marginBottom:6 }}>Claude API Key</div>\n"
    "            <div style={{ fontSize:11, color:'rgba(255,255,255,0.4)', marginBottom:10, lineHeight:1.5 }}>Used for AI fish identification when you add a photo to the catch log. Get a key at console.anthropic.com</div>\n"
    "            <ApiKeyInput />\n"
    "          </TLGlass>\n"
    "        </div>\n"
    "\n"
    "        <div style={{ padding:'24px 0 8px', textAlign:'center', fontSize:10, color:'rgba(255,255,255,0.25)', letterSpacing:1.5 }}>\n"
    "          TIGHT LINES · v2.4 · MADE IN AOTEAROA\n"
    "        </div>",

    "        <div style={{ padding:'24px 0 8px', textAlign:'center', fontSize:10, color:'rgba(255,255,255,0.25)', letterSpacing:1.5 }}>\n"
    "          TIGHT LINES · v2.4 · MADE IN AOTEAROA\n"
    "        </div>",

    "R7-remove-settings-ai-section"
)

# S2 revert: remove ApiKeyInput component
rep(
    "function ApiKeyInput() {\n"
    "  const [val, setVal] = React.useState(() => localStorage.getItem('tl_claude_api_key') || '');\n"
    "  const [saved, setSaved] = React.useState(false);\n"
    "  const save = () => {\n"
    "    localStorage.setItem('tl_claude_api_key', val.trim());\n"
    "    setSaved(true);\n"
    "    setTimeout(() => setSaved(false), 2000);\n"
    "  };\n"
    "  const masked = val.length > 8 ? val.slice(0,4) + '·'.repeat(Math.min(val.length-8,16)) + val.slice(-4) : val;\n"
    "  return (\n"
    "    <div style={{ display:'flex', gap:8, alignItems:'center' }}>\n"
    "      <input\n"
    "        type=\"password\"\n"
    "        value={val}\n"
    "        onChange={e => { setVal(e.target.value); setSaved(false); }}\n"
    "        placeholder=\"sk-ant-…\"\n"
    "        style={{ ...inputSt, flex:1, fontSize:13 }}\n"
    "      />\n"
    "      <button onClick={save} style={{\n"
    "        padding:'11px 14px', borderRadius:10, border:'none',\n"
    "        background: saved ? 'rgba(0,201,167,0.2)' : 'rgba(255,255,255,0.07)',\n"
    "        color: saved ? 'var(--teal)' : 'var(--ink)',\n"
    "        cursor:'pointer', fontSize:12, fontWeight:600,\n"
    "        fontFamily:'Inter,system-ui', flexShrink:0, transition:'all .2s',\n"
    "      }}>{saved ? '✓ Saved' : 'Save'}</button>\n"
    "    </div>\n"
    "  );\n"
    "}\n"
    "\n"
    "function Settings({ tweaks, onLocationSelect, activeLocation, userGeoLoc, setUserGeoLoc, prefs: prefsProp, onPrefsChange }) {",

    "function Settings({ tweaks, onLocationSelect, activeLocation, userGeoLoc, setUserGeoLoc, prefs: prefsProp, onPrefsChange }) {",

    "R8-remove-ApiKeyInput-component"
)

with open(PATH, 'w', encoding='utf-8') as f:
    f.write(src)

print(f"\n=== {len(changes)} reverts applied, {len(src)-orig_len:+d} bytes ===")
