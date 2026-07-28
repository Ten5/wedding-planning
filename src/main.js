import confetti from 'canvas-confetti';

// Target Wedding Date: November 12, 2026 10:00:00 AM PST
const WEDDING_DATE = new Date('2026-11-12T10:00:00-08:00');

// Theme Configurations for V1, V2, V3
const THEME_CONFIGS = {
  v1: {
    heroBadge: "🌅 GOLDEN HOUR & FLORAL ELEGANCE 🌸",
    heroSubtitle: "Are getting married! Join us for a celebratory weekend of love, golden light, and epic feasts.",
    photoBadge: "🍣 Feasts, Blooms & Sweet Moments",
    confettiColors: ['#E07A5F', '#F4A261', '#D59B27', '#FDEEDC', '#81B29A']
  },
  v2: {
    heroBadge: "✨ MODERN MINIMALIST LUXURY 💍",
    heroSubtitle: "Are getting married! An elegant, ultra-chic indoor celebration of our journey together.",
    photoBadge: "🥂 Modern Elegance & Gourmet Feasts",
    confettiColors: ['#C5A059', '#B8860B', '#F3EFE6', '#111827', '#E5E7EB']
  },
  v3: {
    heroBadge: "🍷 ROMANTIC SUNSET & CULINARY FEASTS 🍣",
    heroSubtitle: "Are getting married! A cozy candlelight celebration centered around fine food, blooms & love.",
    photoBadge: "🕯️ Fine Wine, Sushi Feasts & Loved Ones",
    confettiColors: ['#B85B6C', '#7A2638', '#D49A36', '#F8E3E6', '#FAF2F3']
  }
};

document.addEventListener('DOMContentLoaded', () => {
  initThemeSwitcher();
  initNavbar();
  initCountdown();
  initCalendarHandlers();
  initFoodieForm();
  initRsvpForm();
});

/* Theme Switcher Handler for V1, V2, V3 */
function initThemeSwitcher() {
  const tabs = document.querySelectorAll('.theme-tab-btn');
  const htmlEl = document.documentElement;

  // Check URL hash (#v1, #v2, #v3) or localStorage
  const hash = window.location.hash.replace('#', '').toLowerCase();
  const savedVersion = hash && THEME_CONFIGS[hash] ? hash : (localStorage.getItem('selected_theme_version') || 'v1');

  setThemeVersion(savedVersion);

  tabs.forEach(tab => {
    tab.addEventListener('click', (e) => {
      const version = e.currentTarget.dataset.version;
      setThemeVersion(version);
      triggerConfetti(THEME_CONFIGS[version].confettiColors);
    });
  });

  function setThemeVersion(version) {
    if (!THEME_CONFIGS[version]) version = 'v1';

    htmlEl.setAttribute('data-theme', version);
    localStorage.setItem('selected_theme_version', version);
    window.history.replaceState(null, null, `#${version}`);

    // Update active tab button state
    tabs.forEach(tab => {
      if (tab.dataset.version === version) {
        tab.classList.add('active');
      } else {
        tab.classList.remove('active');
      }
    });

    // Dynamically update text elements for the selected theme
    const cfg = THEME_CONFIGS[version];
    const heroBadge = document.getElementById('hero-badge-tag');
    const heroSubtitle = document.getElementById('hero-subtitle-text');
    const photoBadge = document.getElementById('photo-badge-text');

    if (heroBadge) heroBadge.innerHTML = `<span>${cfg.heroBadge}</span>`;
    if (heroSubtitle) heroSubtitle.textContent = cfg.heroSubtitle;
    if (photoBadge) photoBadge.innerHTML = `<span>${cfg.photoBadge}</span>`;
  }
}

/* Navbar Mobile Toggle & Scroll Effect */
function initNavbar() {
  const navbar = document.getElementById('main-nav');
  const toggle = document.getElementById('mobile-toggle');
  const navLinks = document.querySelector('.nav-links');

  window.addEventListener('scroll', () => {
    if (window.scrollY > 50) {
      navbar.classList.add('scrolled');
    } else {
      navbar.classList.remove('scrolled');
    }
  });

  if (toggle && navLinks) {
    toggle.addEventListener('click', () => {
      navLinks.classList.toggle('active');
    });

    navLinks.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => {
        navLinks.classList.remove('active');
      });
    });
  }
}

/* Dynamic Live Countdown Timer */
function initCountdown() {
  const daysEl = document.getElementById('cd-days');
  const hoursEl = document.getElementById('cd-hours');
  const minsEl = document.getElementById('cd-minutes');
  const secsEl = document.getElementById('cd-seconds');

  function update() {
    const now = new Date();
    const diff = WEDDING_DATE - now;

    if (diff <= 0) {
      if (daysEl) daysEl.textContent = '00';
      if (hoursEl) hoursEl.textContent = '00';
      if (minsEl) minsEl.textContent = '00';
      if (secsEl) secsEl.textContent = '00';
      return;
    }

    const days = Math.floor(diff / (1000 * 60 * 60 * 24));
    const hours = Math.floor((diff / (1000 * 60 * 60)) % 24);
    const mins = Math.floor((diff / 1000 / 60) % 60);
    const secs = Math.floor((diff / 1000) % 60);

    if (daysEl) daysEl.textContent = String(days).padStart(2, '0');
    if (hoursEl) hoursEl.textContent = String(hours).padStart(2, '0');
    if (minsEl) minsEl.textContent = String(mins).padStart(2, '0');
    if (secsEl) secsEl.textContent = String(secs).padStart(2, '0');
  }

  update();
  setInterval(update, 1000);
}

/* Calendar Event Data & Link Generators */
const EVENT_DETAILS = {
  wedding: {
    title: "Subhayu (Dodo) & Tarunima (Rini) - Wedding",
    description: "Save the Date for Subhayu & Tarunima's Wedding Ceremony in San Jose / South Bay Area, CA! Formal invitations with exact venue and timing to follow.",
    location: "San Jose / South Bay Area, CA",
    startDate: "20261112T100000",
    endDate: "20261112T160000",
    isoStart: "2026-11-12T10:00:00-08:00",
    isoEnd: "2026-11-12T16:00:00-08:00"
  },
  reception: {
    title: "Subhayu (Dodo) & Tarunima (Rini) - Grand Reception",
    description: "Save the Date for Subhayu & Tarunima's Grand Reception in San Jose / South Bay Area, CA! Evening dinner, music, dancing, and celebration.",
    location: "San Jose / South Bay Area, CA",
    startDate: "20261113T180000",
    endDate: "20261113T230000",
    isoStart: "2026-11-13T18:00:00-08:00",
    isoEnd: "2026-11-13T23:00:00-08:00"
  }
};

function initCalendarHandlers() {
  const gcalBtn = document.getElementById('btn-gcal');
  const icalBtn = document.getElementById('btn-ical');
  const outlookBtn = document.getElementById('btn-outlook');
  const yahooBtn = document.getElementById('btn-yahoo');

  document.querySelectorAll('.cal-trigger-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      const eventType = e.target.dataset.event || 'wedding';
      triggerConfetti();
      downloadIcs(EVENT_DETAILS[eventType]);
    });
  });

  if (gcalBtn) {
    gcalBtn.addEventListener('click', () => {
      triggerConfetti();
      openGoogleCalendar(EVENT_DETAILS.wedding);
    });
  }

  if (icalBtn) {
    icalBtn.addEventListener('click', () => {
      triggerConfetti();
      downloadIcs(EVENT_DETAILS.wedding);
    });
  }

  if (outlookBtn) {
    outlookBtn.addEventListener('click', () => {
      triggerConfetti();
      openOutlookCalendar(EVENT_DETAILS.wedding);
    });
  }

  if (yahooBtn) {
    yahooBtn.addEventListener('click', () => {
      triggerConfetti();
      openYahooCalendar(EVENT_DETAILS.wedding);
    });
  }
}

function openGoogleCalendar(ev) {
  const url = `https://calendar.google.com/calendar/render?action=TEMPLATE` +
    `&text=${encodeURIComponent(ev.title)}` +
    `&dates=${ev.startDate}/${ev.endDate}` +
    `&details=${encodeURIComponent(ev.description)}` +
    `&location=${encodeURIComponent(ev.location)}`;
  window.open(url, '_blank');
}

function openOutlookCalendar(ev) {
  const url = `https://outlook.live.com/calendar/0/deeplink/compose?path=/calendar/action/compose` +
    `&rru=addevent` +
    `&subject=${encodeURIComponent(ev.title)}` +
    `&body=${encodeURIComponent(ev.description)}` +
    `&location=${encodeURIComponent(ev.location)}` +
    `&startdt=${ev.isoStart}` +
    `&enddt=${ev.isoEnd}`;
  window.open(url, '_blank');
}

function openYahooCalendar(ev) {
  const url = `https://calendar.yahoo.com/?v=60` +
    `&title=${encodeURIComponent(ev.title)}` +
    `&st=${ev.startDate}` +
    `&et=${ev.endDate}` +
    `&desc=${encodeURIComponent(ev.description)}` +
    `&in_loc=${encodeURIComponent(ev.location)}`;
  window.open(url, '_blank');
}

function downloadIcs(ev) {
  const icsData = [
    'BEGIN:VCALENDAR',
    'VERSION:2.0',
    'PRODID:-//Dodo & Rini Wedding//Save The Date//EN',
    'CALSCALE:GREGORIAN',
    'BEGIN:VEVENT',
    `SUMMARY:${ev.title}`,
    `DESCRIPTION:${ev.description}`,
    `LOCATION:${ev.location}`,
    `DTSTART:${ev.startDate}`,
    `DTEND:${ev.endDate}`,
    'STATUS:CONFIRMED',
    'END:VEVENT',
    'END:VCALENDAR'
  ].join('\r\n');

  const blob = new Blob([icsData], { type: 'text/calendar;charset=utf-8;' });
  const link = document.createElement('a');
  link.href = window.URL.createObjectURL(blob);
  link.setAttribute('download', `${ev.title.replace(/[^a-zA-Z0-9]/g, '_')}.ics`);
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}

/* Foodie & Activity Suggestion Form */
function initFoodieForm() {
  const form = document.getElementById('foodie-suggestion-form');
  const feedback = document.getElementById('food-form-feedback');

  if (!form) return;

  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const guestName = document.getElementById('food-guest-name').value.trim();
    const spotName = document.getElementById('food-spot-name').value.trim();

    if (!guestName || !spotName) return;

    const saved = JSON.parse(localStorage.getItem('food_suggestions') || '[]');
    saved.push({ name: guestName, spot: spotName, date: new Date().toISOString() });
    localStorage.setItem('food_suggestions', JSON.stringify(saved));

    triggerConfetti();
    feedback.className = 'form-feedback success';
    feedback.textContent = `Thank you ${guestName}! We added "${spotName}" to Dodo & Rini's bucket list! ✨`;
    form.reset();
  });
}

/* Pre-RSVP Form Handler */
function initRsvpForm() {
  const form = document.getElementById('pre-rsvp-form');
  const feedback = document.getElementById('rsvp-feedback');

  if (!form) return;

  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const fullName = document.getElementById('rsvp-full-name').value.trim();
    const email = document.getElementById('rsvp-email').value.trim();
    const attendance = document.getElementById('rsvp-attendance').value;
    const notes = document.getElementById('rsvp-notes').value.trim();

    if (!fullName || !email) return;

    const rsvpEntries = JSON.parse(localStorage.getItem('pre_rsvp_entries') || '[]');
    rsvpEntries.push({ fullName, email, attendance, notes, timestamp: new Date().toISOString() });
    localStorage.setItem('pre_rsvp_entries', JSON.stringify(rsvpEntries));

    triggerConfetti();
    feedback.className = 'form-feedback success';
    feedback.textContent = `Woohoo! Thank you ${fullName}! Your contact details have been saved. Dodo & Rini will keep you posted! 💌✨`;
    form.reset();
  });
}

/* Confetti Helper */
function triggerConfetti(colors) {
  confetti({
    particleCount: 85,
    spread: 75,
    origin: { y: 0.65 },
    colors: colors || ['#E07A5F', '#F4A261', '#D59B27', '#FDEEDC', '#81B29A']
  });
}
