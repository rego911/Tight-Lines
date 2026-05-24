# 🎣 Tight Lines

A mobile-first fishing weather app built for New Zealand saltwater anglers. Single HTML file — deploy anywhere, works offline once loaded.

---

## Features

### Today
Live fishing score for your location with an at-a-glance gauge, real-time tide height, and a 24-hour hourly strip starting from the current hour. Scroll forward to see wind, swell, and bite conditions throughout the day.

**What's Working** — conditions-aware bait and lure suggestions that update based on wind speed, swell height, water temperature, tide phase, time of day, and season. No guessing required.

### Conditions
Detailed wind and swell breakdown, sun and moon times, and a full tide table with high/low predictions. Sourced from LINZ and NIWA data.

### Forecast
7-day outlook with daily bite window scores and a visual BiteTimeline showing the best feeding windows across the day.

### Catch Log
A personal fishing diary that lives in your browser. Log species, length, weight, date, location, notes, and a photo for every catch.

- **Share card** — tap Share on any entry to generate a styled 1080px card with your fish photo, species, stats and location. Saves to your camera roll or downloads as a PNG.
- **NZ Regulations** — tap Regs to check MPI size limits and daily bag limits for 12 common NZ saltwater species, with notes on regional variations.

### Settings
- Units — metric (kt, °C, m) or imperial (mph, °F, ft)
- Time format — 12-hour or 24-hour
- Watch face — changes the dashboard gauge style
- Nearby fishing spots — auto-detected from your location, ranked by fishing score

---

## Location

The app auto-detects your location on load using the browser geolocation API and reverse-geocodes it via OpenStreetMap Nominatim. You can also search for any location with autocomplete, or tap "Use current location" to re-centre.

All data is generated locally based on your coordinates — no weather API key required.

---

## Deployment

The entire app is a single `index.html` file with no build step, no dependencies to install, and no backend.

**Netlify**
Drop the file into a new site via the Netlify drag-and-drop deploy, or connect your GitHub repo and it deploys automatically on every push.

**GitHub Pages**
Push to a repo, enable Pages from the `main` branch root, and it's live.

**Local**
Open `index.html` directly in a browser. Everything works offline except location search and nearby spots (which use Nominatim).

---

## Stack

- React 18 (via CDN, in-browser JSX with Babel Standalone)
- No build tools, no bundler, no node_modules
- Nominatim (OpenStreetMap) for geocoding and nearby spots
- Canvas API for catch share card generation
- localStorage for catch log persistence
- Web Share API for native share sheet on mobile

---

## Privacy

No data ever leaves your device except:
- Your coordinates are sent to Nominatim (OpenStreetMap) for reverse geocoding and nearby spot search — subject to the [Nominatim usage policy](https://operations.osmfoundation.org/policies/nominatim/)
- Catch log data is stored locally in your browser's localStorage and never uploaded anywhere

---

## NZ Fishing Regulations

The in-app regulations reference is a guide only, based on general MPI recreational limits. Rules vary by region and are updated periodically. Always verify current limits at [mpi.govt.nz/fishing](https://www.mpi.govt.nz/fishing-aquaculture/recreational-fishing/) before heading out.

---

## Licence

MIT — do whatever you like with it.
