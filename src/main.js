import confetti from 'canvas-confetti';

// Target Wedding Reception Date: Friday, November 13, 2026 5:30:00 PM PST
const WEDDING_DATE = new Date('2026-11-13T17:30:00-08:00');

// Google Apps Script Web App URL for Google Sheets RSVP Integration
let GOOGLE_SHEET_WEB_APP_URL = "https://script.google.com/macros/s/AKfycbx9OAGxd_sK90gR8W-rf4D1hb1YVFZY2xzYw57WcgrN3TFEtaXZ9MQJl36-XGpr3L59JA/exec";

document.addEventListener('DOMContentLoaded', () => {
  initNavbar();
  initCountdown();
  initFoodieForm();
  initRsvpForm();
  initRsvpModal();
  initHeroSlideshow();
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
    const guests = document.getElementById('rsvp-guests') ? document.getElementById('rsvp-guests').value : '1';
    const notes = document.getElementById('rsvp-notes').value.trim();

    if (!fullName || !email) return;

    const payload = {
      formType: 'rsvp',
      fullName: fullName,
      email: email,
      guests: guests,
      attendance: 'yes',
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
    const guestLabel = parseInt(guests, 10) > 1 ? ` (Party of ${guests})` : '';
    feedback.textContent = `Thank you ${fullName}${guestLabel}! Your RSVP has been confirmed. We can't wait to celebrate together! 💌✨`;
    form.reset();
  });
}

/* RSVP Modal Open/Close Controls */
function initRsvpModal() {
  const modal = document.getElementById('rsvp-modal');
  const closeBtn = document.getElementById('rsvp-modal-close');
  const backdrop = document.getElementById('rsvp-modal-backdrop');
  const openButtons = document.querySelectorAll('.open-rsvp-modal-btn, a[href="#rsvp"]');

  function openModal(e) {
    if (e) e.preventDefault();
    if (!modal) return;
    modal.classList.add('active');
    modal.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';
  }

  function closeModal() {
    if (!modal) return;
    modal.classList.remove('active');
    modal.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';
  }

  openButtons.forEach(btn => {
    btn.addEventListener('click', openModal);
  });

  if (closeBtn) closeBtn.addEventListener('click', closeModal);
  if (backdrop) backdrop.addEventListener('click', closeModal);

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && modal && modal.classList.contains('active')) {
      closeModal();
    }
  });
}

/* Picture Slideshow with Dynamic Non-Predictable Transitions & Touch Swipe */
let slideInterval = null;
let currentSlideIndex = 0;
const TRANSITIONS = [
  'effect-zoom-soft',
  'effect-drift-right',
  'effect-glide-up',
  'effect-drift-left',
  'effect-breath-scale',
  'effect-luminous-fade'
];

function initHeroSlideshow() {
  const slides = document.querySelectorAll('.hero-slideshow-container .slide');
  const dots = document.querySelectorAll('.slide-indicators .dot');
  const prevBtn = document.getElementById('prev-slide');
  const nextBtn = document.getElementById('next-slide');
  const slideshowEl = document.getElementById('hero-slideshow');

  if (!slides.length) return;

  function showSlide(index) {
    if (index >= slides.length) currentSlideIndex = 0;
    else if (index < 0) currentSlideIndex = slides.length - 1;
    else currentSlideIndex = index;

    // Pick a varied transition effect class for this slide
    const chosenEffect = TRANSITIONS[currentSlideIndex % TRANSITIONS.length];

    slides.forEach((slide, i) => {
      // Remove all effect classes
      TRANSITIONS.forEach(cls => slide.classList.remove(cls));

      if (i === currentSlideIndex) {
        slide.classList.add('active', chosenEffect);
      } else {
        slide.classList.remove('active');
      }
    });

    dots.forEach((dot, i) => {
      if (i === currentSlideIndex) {
        dot.classList.add('active');
      } else {
        dot.classList.remove('active');
      }
    });
  }

  function startAutoplay() {
    stopAutoplay();
    slideInterval = setInterval(() => {
      showSlide(currentSlideIndex + 1);
    }, 7500);
  }

  function stopAutoplay() {
    if (slideInterval) clearInterval(slideInterval);
  }

  if (prevBtn) {
    prevBtn.addEventListener('click', (e) => {
      e.preventDefault();
      showSlide(currentSlideIndex - 1);
      startAutoplay();
    });
  }

  if (nextBtn) {
    nextBtn.addEventListener('click', (e) => {
      e.preventDefault();
      showSlide(currentSlideIndex + 1);
      startAutoplay();
    });
  }

  dots.forEach(dot => {
    dot.addEventListener('click', (e) => {
      const idx = parseInt(e.target.dataset.index, 10);
      showSlide(idx);
      startAutoplay();
    });
  });

  if (slideshowEl) {
    slideshowEl.addEventListener('mouseenter', stopAutoplay);
    slideshowEl.addEventListener('mouseleave', startAutoplay);

    // Touch Swipe Gesture Support
    let touchStartX = 0;
    let touchEndX = 0;

    slideshowEl.addEventListener('touchstart', (e) => {
      stopAutoplay();
      touchStartX = e.changedTouches[0].screenX;
    }, { passive: true });

    slideshowEl.addEventListener('touchend', (e) => {
      touchEndX = e.changedTouches[0].screenX;
      handleSwipe();
      startAutoplay();
    }, { passive: true });

    function handleSwipe() {
      const diff = touchEndX - touchStartX;
      if (Math.abs(diff) > 40) {
        if (diff < 0) {
          // Swiped Left -> Next Slide
          showSlide(currentSlideIndex + 1);
        } else {
          // Swiped Right -> Previous Slide
          showSlide(currentSlideIndex - 1);
        }
      }
    }
  }

  // Fullscreen Lightbox Modal for Uncropped Photo View
  const lightbox = document.getElementById('slideshow-lightbox');
  const lightboxImg = document.getElementById('lightbox-img');
  const lightboxTitle = document.getElementById('lightbox-title');
  const lightboxDesc = document.getElementById('lightbox-desc');
  const lightboxPrev = document.getElementById('lightbox-prev');
  const lightboxNext = document.getElementById('lightbox-next');
  const lightboxClose = document.getElementById('lightbox-close');
  let isLightboxOpen = false;

  function updateLightboxContent() {
    const activeSlide = slides[currentSlideIndex];
    if (!activeSlide || !lightbox) return;

    const imgEl = activeSlide.querySelector('.slide-img');
    const titleEl = activeSlide.querySelector('.slide-title');
    const descEl = activeSlide.querySelector('.slide-desc');

    if (imgEl && lightboxImg) {
      lightboxImg.src = imgEl.src;
      lightboxImg.alt = imgEl.alt || '';
    }
    if (titleEl && lightboxTitle) {
      lightboxTitle.textContent = titleEl.textContent;
    }
    if (descEl && lightboxDesc) {
      lightboxDesc.textContent = descEl.textContent;
    }
  }

  function openLightbox() {
    updateLightboxContent();
    if (!lightbox) return;

    lightbox.classList.add('active');
    lightbox.setAttribute('aria-hidden', 'false');
    isLightboxOpen = true;
    stopAutoplay();
  }

  function closeLightbox() {
    if (!lightbox) return;
    lightbox.classList.remove('active');
    lightbox.setAttribute('aria-hidden', 'true');
    isLightboxOpen = false;
    startAutoplay();
  }

  function navigateLightbox(direction) {
    let nextIdx = currentSlideIndex + direction;
    if (nextIdx >= slides.length) nextIdx = 0;
    else if (nextIdx < 0) nextIdx = slides.length - 1;
    showSlide(nextIdx);
    updateLightboxContent();
  }

  // Lightbox Arrow Controls
  if (lightboxPrev) {
    lightboxPrev.addEventListener('click', (e) => {
      e.stopPropagation();
      navigateLightbox(-1);
    });
  }

  if (lightboxNext) {
    lightboxNext.addEventListener('click', (e) => {
      e.stopPropagation();
      navigateLightbox(1);
    });
  }

  if (lightboxClose) {
    lightboxClose.addEventListener('click', (e) => {
      e.stopPropagation();
      closeLightbox();
    });
  }

  // Open modal on tapping/clicking the photo frame or caption card
  slides.forEach(slide => {
    const frame = slide.querySelector('.slide-photo-frame');
    const caption = slide.querySelector('.slide-caption-card');
    if (frame) {
      frame.addEventListener('click', (e) => {
        e.stopPropagation();
        openLightbox();
      });
    }
    if (caption) {
      caption.addEventListener('click', (e) => {
        e.stopPropagation();
        openLightbox();
      });
    }
  });

  // Also allow tapping Family Section cards to view full family portraits in lightbox
  const familyCards = document.querySelectorAll('.family-card');
  familyCards.forEach(card => {
    card.addEventListener('click', (e) => {
      e.stopPropagation();
      const imgEl = card.querySelector('.family-img');
      const titleEl = card.querySelector('.family-card-title');
      const descEl = card.querySelector('.family-card-desc');
      if (!lightbox || !imgEl) return;

      if (lightboxImg) {
        lightboxImg.src = imgEl.src;
        lightboxImg.alt = imgEl.alt || '';
      }
      if (titleEl && lightboxTitle) {
        lightboxTitle.textContent = titleEl.textContent;
      }
      if (descEl && lightboxDesc) {
        lightboxDesc.textContent = descEl.textContent;
      }

      lightbox.classList.add('active');
      lightbox.setAttribute('aria-hidden', 'false');
      isLightboxOpen = true;
      stopAutoplay();
    });
  });

  // Close modal on tapping backdrop or outside controls
  if (lightbox) {
    const backdrop = lightbox.querySelector('.lightbox-backdrop');
    if (backdrop) {
      backdrop.addEventListener('click', (e) => {
        e.stopPropagation();
        closeLightbox();
      });
    }

    const imgWrap = lightbox.querySelector('.lightbox-img-wrap');
    if (imgWrap) {
      imgWrap.addEventListener('click', () => {
        closeLightbox();
      });
    }

    // Touch swipe gesture support for Lightbox
    let lbTouchStartX = 0;
    let lbTouchEndX = 0;

    lightbox.addEventListener('touchstart', (e) => {
      lbTouchStartX = e.changedTouches[0].screenX;
    }, { passive: true });

    lightbox.addEventListener('touchend', (e) => {
      lbTouchEndX = e.changedTouches[0].screenX;
      const diff = lbTouchEndX - lbTouchStartX;
      if (Math.abs(diff) > 40) {
        if (diff < 0) {
          navigateLightbox(1); // Swiped Left -> Next Photo
        } else {
          navigateLightbox(-1); // Swiped Right -> Previous Photo
        }
      }
    }, { passive: true });
  }

  // Keyboard Navigation: Arrow keys for slides/lightbox, Escape to close lightbox
  document.addEventListener('keydown', (e) => {
    if (isLightboxOpen) {
      if (e.key === 'Escape') {
        closeLightbox();
      } else if (e.key === 'ArrowLeft') {
        navigateLightbox(-1);
      } else if (e.key === 'ArrowRight') {
        navigateLightbox(1);
      }
      return;
    }

    if (e.key === 'ArrowLeft') {
      showSlide(currentSlideIndex - 1);
      startAutoplay();
    } else if (e.key === 'ArrowRight') {
      showSlide(currentSlideIndex + 1);
      startAutoplay();
    }
  });

  showSlide(0);
  startAutoplay();
}

/* Confetti Helper with Warm Luxury Gold & Champagne Palette */
function triggerConfetti(colors) {
  confetti({
    particleCount: 85,
    spread: 75,
    origin: { y: 0.65 },
    colors: colors || ['#C5A059', '#B8860B', '#F3EFE6', '#E07A5F', '#D59B27']
  });
}

