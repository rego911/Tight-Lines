// Tight Lines — Mock data for NZ saltwater offshore fishing
// Location: Bay of Islands area (semi-diurnal tides, NZST)

window.TL_DATA = {
  location: {
    name: 'Cape Brett',
    region: 'Bay of Islands',
    country: 'NZ',
    lat: -35.1828,
    lng: 174.3306,
  },
  now: {
    score: 84,
    windSpeed: 11,        // knots
    windGust: 17,
    windDir: 218,          // bearing °, SSW
    windDirLabel: 'SSW',
    waveHeight: 1.2,       // m
    swellPeriod: 9,        // s
    swellDir: 'E',
    waterTemp: 17.8,       // °C
    airTemp: 19,           // °C
    barometric: 1018,      // hPa
    barometricTrend: 'rising', // 'rising' | 'falling' | 'steady'
    barometricDelta: +2.1,
    uv: 6,
    uvLabel: 'High',
    tideState: 'Rising',
    tideHeight: 1.8,
    nextTide: 'High 14:32',
    moonPhase: 'Waxing Gibbous',
    moonIllum: 0.78,
    dawn: '06:12',
    dusk: '19:48',
    sunrise: '06:42',
    sunset: '19:18',
  },
  // hourly forecast — 24 entries from current hour
  hourly: Array.from({ length: 24 }, (_, i) => {
    const h = (8 + i) % 24;
    // simple sinusoidal score with bite peaks at dawn/dusk
    const hourScore = Math.round(
      55 +
      28 * Math.sin((h / 24) * Math.PI * 2 - 0.5) +
      (h === 6 || h === 7 || h === 18 || h === 19 ? 12 : 0) +
      (i === 0 ? 6 : 0)
    );
    return {
      hour: h,
      label: i === 0 ? 'Now' : `${String(h).padStart(2,'0')}:00`,
      score: Math.max(20, Math.min(98, hourScore)),
      temp: 17 + Math.round(4 * Math.sin((h / 24) * Math.PI * 2 - 1.2) * 10) / 10,
      wind: 8 + Math.round(8 * Math.abs(Math.sin(h / 6)) * 10) / 10,
      cond: ['clear','partly','cloud','partly','clear','clear'][i % 6],
    };
  }),
  // 7-day outlook
  daily: [
    { day: 'Today', date: 'Mon 18', hi: 19, lo: 14, score: 84, peakWindow: '06:00 — 09:00', cond: 'partly' },
    { day: 'Tue',   date: 'Tue 19', hi: 20, lo: 13, score: 76, peakWindow: '17:30 — 20:00', cond: 'clear' },
    { day: 'Wed',   date: 'Wed 20', hi: 18, lo: 14, score: 62, peakWindow: '06:30 — 08:00', cond: 'cloud' },
    { day: 'Thu',   date: 'Thu 21', hi: 17, lo: 13, score: 41, peakWindow: '—',             cond: 'rain' },
    { day: 'Fri',   date: 'Fri 22', hi: 18, lo: 12, score: 58, peakWindow: '07:00 — 09:30', cond: 'cloud' },
    { day: 'Sat',   date: 'Sat 23', hi: 20, lo: 14, score: 89, peakWindow: '05:45 — 09:00', cond: 'clear' },
    { day: 'Sun',   date: 'Sun 24', hi: 21, lo: 15, score: 91, peakWindow: '06:00 — 09:30', cond: 'clear' },
  ],
  // tide curve — 24h heights in m, sample every 30 min (48 points)
  tide: Array.from({ length: 48 }, (_, i) => {
    const t = i / 48 * 24;
    // two highs at ~02:18 and 14:32, lows at ~08:25 and 20:45
    const h = 1.0 + 0.95 * Math.sin((t - 2.3) / 12.42 * Math.PI * 2);
    return { t, hour: t, height: +(h.toFixed(2)) };
  }),
  tideEvents: [
    { time: '02:18', label: 'High', height: 1.95 },
    { time: '08:25', label: 'Low',  height: 0.18 },
    { time: '14:32', label: 'High', height: 1.92 },
    { time: '20:45', label: 'Low',  height: 0.22 },
  ],
  // species & bite windows
  species: [
    {
      id: 'snapper', name: 'Snapper', maori: 'Tāmure',
      bestSeason: 'Year-round, peak Oct–May',
      depthRange: '15–80m',
      windows: [
        { start: 5,  end: 8.5, level: 'hot'  },
        { start: 8.5,end: 11,  level: 'warm' },
        { start: 11, end: 16,  level: 'slow' },
        { start: 16, end: 19.5,level: 'hot'  },
        { start: 19.5,end: 22, level: 'warm' },
        { start: 22, end: 24,  level: 'slow' },
        { start: 0,  end: 5,   level: 'slow' },
      ],
      score: 86,
      conf: 'High',
      note: 'Rising barometer + slack tide window at dawn aligns with peak feed.',
    },
    {
      id: 'kingfish', name: 'Kingfish', maori: 'Haku',
      bestSeason: 'Dec–Apr',
      depthRange: '0–50m, structure',
      windows: [
        { start: 0,  end: 6,   level: 'slow' },
        { start: 6,  end: 9,   level: 'warm' },
        { start: 9,  end: 13,  level: 'hot'  },
        { start: 13, end: 17,  level: 'warm' },
        { start: 17, end: 20,  level: 'hot'  },
        { start: 20, end: 24,  level: 'slow' },
      ],
      score: 78,
      conf: 'High',
      note: 'Mid-tide rip lines around Cape Brett pinnacles firing in current.',
    },
    {
      id: 'marlin', name: 'Striped Marlin', maori: 'Takeketonga',
      bestSeason: 'Jan–May',
      depthRange: 'Blue water, 200m+',
      windows: [
        { start: 0,  end: 9,   level: 'slow' },
        { start: 9,  end: 12,  level: 'warm' },
        { start: 12, end: 16,  level: 'hot'  },
        { start: 16, end: 18,  level: 'warm' },
        { start: 18, end: 24,  level: 'slow' },
      ],
      score: 64,
      conf: 'Medium',
      note: 'Water temp 17.8°C borderline — push wider to 18.5°C break, 12nm NE.',
    },
    {
      id: 'kahawai', name: 'Kahawai', maori: 'Kahawai',
      bestSeason: 'Year-round',
      depthRange: 'Surface, schooling',
      windows: [
        { start: 0,  end: 5,   level: 'slow' },
        { start: 5,  end: 8,   level: 'hot'  },
        { start: 8,  end: 12,  level: 'warm' },
        { start: 12, end: 17,  level: 'warm' },
        { start: 17, end: 20,  level: 'hot'  },
        { start: 20, end: 24,  level: 'slow' },
      ],
      score: 81,
      conf: 'High',
      note: 'Workups likely — gannets reported off Piercy Island this morning.',
    },
    {
      id: 'trevally', name: 'Trevally', maori: 'Araara',
      bestSeason: 'Nov–Apr',
      depthRange: '5–40m',
      windows: [
        { start: 0,  end: 6,   level: 'slow' },
        { start: 6,  end: 10,  level: 'warm' },
        { start: 10, end: 14,  level: 'hot'  },
        { start: 14, end: 17,  level: 'warm' },
        { start: 17, end: 20,  level: 'hot'  },
        { start: 20, end: 24,  level: 'slow' },
      ],
      score: 72,
      conf: 'Medium',
      note: 'Following snapper schools — bait fish on side-scan at 22m.',
    },
    {
      id: 'hapuka', name: 'Hāpuku', maori: 'Hāpuku',
      bestSeason: 'Year-round',
      depthRange: '120–400m',
      windows: [
        { start: 0,  end: 24,  level: 'warm' },
      ],
      score: 58,
      conf: 'Medium',
      note: 'Deep drop — sea state below 1.5m makes the run worthwhile.',
    },
    {
      id: 'tarakihi', name: 'Tarakihi', maori: 'Tarakihi',
      bestSeason: 'Year-round',
      depthRange: '40–200m',
      windows: [
        { start: 0,  end: 5,   level: 'warm' },
        { start: 5,  end: 9,   level: 'hot'  },
        { start: 9,  end: 16,  level: 'warm' },
        { start: 16, end: 20,  level: 'hot'  },
        { start: 20, end: 24,  level: 'slow' },
      ],
      score: 75,
      conf: 'High',
      note: 'Foul-ground edges at 60m holding numbers on the sounder.',
    },
  ],
  recentLocations: [
    { name: 'Cape Brett',        region: 'Bay of Islands',    favourite: true,  score: 84 },
    { name: 'Mokohinau Islands', region: 'Hauraki Gulf',      favourite: true,  score: 79 },
    { name: 'Whangaroa Harbour', region: 'Northland',         favourite: false, score: 67 },
    { name: 'Mercury Bay',       region: 'Coromandel',        favourite: false, score: 71 },
    { name: 'Cape Reinga',       region: 'Far North',         favourite: false, score: 58 },
  ],
};
