(() => {
  const links = document.querySelectorAll('.sidebar-link');
  const sections = document.querySelectorAll('.doc-section');
  const sidebar = document.getElementById('sidebar');
  const toggle = document.getElementById('sidebarToggle');

  function setActive(id) {
    links.forEach(l => {
      l.classList.toggle('active', l.dataset.section === id);
    });
  }

  const observer = new IntersectionObserver((entries) => {
    for (const entry of entries) {
      if (entry.isIntersecting) {
        setActive(entry.target.id);
      }
    }
  }, {
    rootMargin: '-80px 0px -60% 0px',
    threshold: 0
  });

  sections.forEach(s => observer.observe(s));

  links.forEach(link => {
    link.addEventListener('click', () => {
      if (window.innerWidth <= 900) {
        sidebar.classList.remove('open');
      }
    });
  });

  toggle.addEventListener('click', () => {
    sidebar.classList.toggle('open');
  });

  document.addEventListener('click', (e) => {
    if (window.innerWidth <= 900 &&
        sidebar.classList.contains('open') &&
        !sidebar.contains(e.target) &&
        e.target !== toggle) {
      sidebar.classList.remove('open');
    }
  });
})();
