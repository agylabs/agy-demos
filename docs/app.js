(() => {
  // ── View Switching ──
  const slidesView = document.getElementById('slides-view');
  const docsView = document.getElementById('docs-view');
  const tabSlides = document.getElementById('tabSlides');
  const tabDocs = document.getElementById('tabDocs');
  let currentView = 'slides';

  const docSections = ['skills', 'subagents', 'goal', 'grill-me', 'schedule', 'web', 'workflow', 'imagegen'];

  function switchView(view, scrollTarget) {
    currentView = view;
    slidesView.classList.toggle('active', view === 'slides');
    docsView.classList.toggle('active', view === 'docs');
    tabSlides.classList.toggle('active', view === 'slides');
    tabDocs.classList.toggle('active', view === 'docs');
    document.body.classList.toggle('docs-body', view === 'docs');

    if (view === 'slides') {
      history.replaceState(null, '', '#slides');
    } else {
      history.replaceState(null, '', scrollTarget ? '#' + scrollTarget : '#docs');
      if (scrollTarget) {
        const el = document.getElementById(scrollTarget);
        if (el) setTimeout(() => el.scrollIntoView({ behavior: 'smooth' }), 50);
      }
    }
  }

  tabSlides.addEventListener('click', () => switchView('slides'));
  tabDocs.addEventListener('click', () => switchView('docs'));

  // Handle initial hash
  const hash = location.hash.replace('#', '');
  if (hash === 'docs') {
    switchView('docs');
  } else if (docSections.includes(hash)) {
    switchView('docs', hash);
  }

  // Handle hash changes (back/forward)
  window.addEventListener('hashchange', () => {
    const h = location.hash.replace('#', '');
    if (h === 'slides') switchView('slides');
    else if (h === 'docs') switchView('docs');
    else if (docSections.includes(h)) switchView('docs', h);
  });

  // ── Slide Deck ──
  const slides = document.querySelectorAll('.slide');
  const progress = document.getElementById('progress');
  const counter = document.getElementById('slideCounter');
  const prevBtn = document.getElementById('prevBtn');
  const nextBtn = document.getElementById('nextBtn');
  const total = slides.length;
  let current = 0;
  let transitioning = false;

  function goTo(index) {
    if (index < 0 || index >= total || index === current || transitioning) return;
    transitioning = true;

    const prev = slides[current];
    const next = slides[index];
    const goingForward = index > current;

    prev.classList.remove('active');
    prev.style.transform = goingForward ? 'translateX(-60px)' : 'translateX(60px)';
    prev.style.opacity = '0';

    next.style.transform = goingForward ? 'translateX(60px)' : 'translateX(-60px)';
    next.style.opacity = '0';

    requestAnimationFrame(() => {
      requestAnimationFrame(() => {
        next.classList.add('active');
        next.style.transform = '';
        next.style.opacity = '';
      });
    });

    current = index;
    updateUI();

    setTimeout(() => {
      prev.style.transform = '';
      prev.style.opacity = '';
      transitioning = false;
    }, 500);
  }

  function updateUI() {
    const pct = ((current + 1) / total) * 100;
    progress.style.width = pct + '%';
    counter.textContent = (current + 1) + ' / ' + total;
    prevBtn.disabled = current === 0;
    nextBtn.disabled = current === total - 1;
  }

  function next() { goTo(current + 1); }
  function prev() { goTo(current - 1); }

  prevBtn.addEventListener('click', prev);
  nextBtn.addEventListener('click', next);

  document.addEventListener('keydown', (e) => {
    if (currentView !== 'slides') return;
    if (e.key === 'ArrowRight' || e.key === ' ') {
      e.preventDefault();
      next();
    } else if (e.key === 'ArrowLeft') {
      e.preventDefault();
      prev();
    } else if (e.key === 'Home') {
      e.preventDefault();
      goTo(0);
    } else if (e.key === 'End') {
      e.preventDefault();
      goTo(total - 1);
    }
  });

  let touchStartX = 0;
  let touchStartY = 0;

  document.addEventListener('touchstart', (e) => {
    touchStartX = e.touches[0].clientX;
    touchStartY = e.touches[0].clientY;
  }, { passive: true });

  document.addEventListener('touchend', (e) => {
    if (currentView !== 'slides') return;
    const dx = e.changedTouches[0].clientX - touchStartX;
    const dy = e.changedTouches[0].clientY - touchStartY;
    if (Math.abs(dx) > Math.abs(dy) && Math.abs(dx) > 50) {
      dx < 0 ? next() : prev();
    }
  }, { passive: true });

  updateUI();
})();
