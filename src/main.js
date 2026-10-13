import confetti from 'canvas-confetti';

// Target Wedding Reception Date: Friday, November 13, 2026 5:00:00 PM PST
const WEDDING_DATE = new Date('2026-11-13T17:00:00-08:00');

// Google Apps Script Web App URL for Google Sheets RSVP Integration
// Paste your deployed Google Apps Script URL here to sync responses to Google Sheets
let GOOGLE_SHEET_WEB_APP_URL = "";

document.addEventListener('DOMContentLoaded', () => {
  initNavbar();
  initCountdown();
  initCalendarHandlers();
  initFoodieForm();
  initRsvpForm();
});

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

/* Dynamic Live Countdown Timer to November 13, 2026 5:00 PM PST */
function initCountdown() {
  const daysEl = document.getElementById('cd-days');
  const hoursEl = document.getElementById('cd-hours');
  const minsEl = document.getElementById('cd-minutes');
  const secsEl = document.getElementById('cd-seconds');

  function update() {
    const now = new Date();
    const diff = WEDDING_DATE.getTime() - now.getTime();

    if (diff <= 0) {
      if (daysEl) daysEl.textContent = '00';
      if (hoursEl) hoursEl.textContent = '00';
      if (minsEl) minsEl.textContent = '00';
      if (secsEl) secsEl.textContent = '00';
      return;
    }

    const days = Math.floor(diff / (1000 * 60 * 60 * 24));
    const hours = Math.floor((diff / (1000 * 60 * 60)) % 24);
    const mins = Math.floor((diff / (1000 * 60)) % 60);
    const secs = Math.floor((diff / 1000) % 60);

    if (daysEl) daysEl.textContent = String(days).padStart(2, '0');
    if (hoursEl) hoursEl.textContent = String(hours).padStart(2, '0');
    if (minsEl) minsEl.textContent = String(mins).padStart(2, '0');
    if (secsEl) secsEl.textContent = String(secs).padStart(2, '0');
  }

  update();
  setInterval(update, 1000);
}

/* Calendar Event Data for Reception */
const EVENT_DETAILS = {
  reception: {
    title: "Tarunima & Subhayu - Wedding Reception",
    description: "Tarunima Mandal & Subhayu Chakravorty's Wedding Reception at North Park in San Jose, CA (5:00 PM onwards). We can't wait to celebrate with you!",
    location: "North Park, San Jose, CA",
    startDate: "20261113T170000",
    endDate: "20261113T230000",
    isoStart: "2026-11-13T17:00:00-08:00",
    isoEnd: "2026-11-13T23:00:00-08:00"
  }
};

function initCalendarHandlers() {
  const gcalBtn = document.getElementById('btn-gcal');
  const icalBtn = document.getElementById('btn-ical');

  document.querySelectorAll('.cal-trigger-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      triggerConfetti();
      downloadIcs(EVENT_DETAILS.reception);
    });
  });

  if (gcalBtn) {
    gcalBtn.addEventListener('click', () => {
      triggerConfetti();
      openGoogleCalendar(EVENT_DETAILS.reception);
    });
  }

  if (icalBtn) {
    icalBtn.addEventListener('click', () => {
      triggerConfetti();
      downloadIcs(EVENT_DETAILS.reception);
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

function downloadIcs(ev) {
  const icsData = [
    'BEGIN:VCALENDAR',
    'VERSION:2.0',
    'PRODID:-//Tarunima & Subhayu Wedding Reception//EN',
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

    const payload = {
      formType: 'recommendation',
      fullName: guestName,
      spotName: spotName,
      timestamp: new Date().toLocaleString()
    };

    // Save locally as backup
    const saved = JSON.parse(localStorage.getItem('food_suggestions') || '[]');
    saved.push(payload);
    localStorage.setItem('food_suggestions', JSON.stringify(saved));

    // Send to Google Sheets if Web App URL is configured
    if (GOOGLE_SHEET_WEB_APP_URL) {
      fetch(GOOGLE_SHEET_WEB_APP_URL, {
        method: 'POST',
        mode: 'no-cors',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      }).catch(err => console.log('Google Sheets Sync Note:', err));
    }

    triggerConfetti();
    feedback.className = 'form-feedback success';
    feedback.textContent = `Thank you ${guestName}! We added "${spotName}" to our bucket list! ✨`;
    form.reset();
  });
}

/* RSVP Form Handler */
function initRsvpForm() {
  const form = document.getElementById('rsvp-form');
  const feedback = document.getElementById('rsvp-feedback');

  if (!form) return;

  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const fullName = document.getElementById('rsvp-full-name').value.trim();
    const email = document.getElementById('rsvp-email').value.trim();
    const attendance = document.getElementById('rsvp-attendance').value;
    const notes = document.getElementById('rsvp-notes').value.trim();

    if (!fullName || !email) return;

    const payload = {
      formType: 'rsvp',
      fullName: fullName,
      email: email,
      attendance: attendance,
      notes: notes,
      timestamp: new Date().toLocaleString()
    };

    // Save locally in browser storage as immediate backup
    const rsvpEntries = JSON.parse(localStorage.getItem('rsvp_entries') || '[]');
    rsvpEntries.push(payload);
    localStorage.setItem('rsvp_entries', JSON.stringify(rsvpEntries));

    // Send to Google Sheets if Web App URL is configured
    if (GOOGLE_SHEET_WEB_APP_URL) {
      fetch(GOOGLE_SHEET_WEB_APP_URL, {
        method: 'POST',
        mode: 'no-cors',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      }).catch(err => console.log('Google Sheets Sync Note:', err));
    }

    triggerConfetti();
    feedback.className = 'form-feedback success';
    feedback.textContent = `Thank you ${fullName}! Your RSVP details have been received. We can't wait to celebrate with you! 💌✨`;
    form.reset();
  });
}

/* Confetti Helper with Warm Golden Floral Palette */
function triggerConfetti(colors) {
  confetti({
    particleCount: 85,
    spread: 75,
    origin: { y: 0.65 },
    colors: colors || ['#E07A5F', '#F4A261', '#D59B27', '#FDEEDC', '#81B29A']
  });
}
