document.addEventListener('DOMContentLoaded', () => {

  /* ============================================================
     THEME TOGGLE (Dark / Light Mode)
  ============================================================ */
  const themeToggleBtn = document.querySelector('.theme-toggle');
  const themeIcon      = themeToggleBtn.querySelector('i');

  // Load saved preference (default: dark)
  const savedTheme = localStorage.getItem('theme') || 'dark';
  if (savedTheme === 'light') {
    document.body.classList.add('light');
    themeIcon.className = 'fas fa-sun';
  }

  themeToggleBtn.addEventListener('click', () => {
    const isLight = document.body.classList.toggle('light');
    themeIcon.className = isLight ? 'fas fa-sun' : 'fas fa-moon';
    localStorage.setItem('theme', isLight ? 'light' : 'dark');
  });

  /* ============================================================
     CUSTOM CURSOR
  ============================================================ */
  const cursor  = document.querySelector('.cursor');
  const cursor2 = document.querySelector('.cursor2');

  document.addEventListener('mousemove', e => {
    cursor.style.left  = cursor2.style.left  = e.clientX + 'px';
    cursor.style.top   = cursor2.style.top   = e.clientY + 'px';
  });

  /* ============================================================
     NAVBAR — scroll & active links
  ============================================================ */
  const navbar   = document.querySelector('.navbar');
  const sections = document.querySelectorAll('section[id]');
  const navLinks = document.querySelectorAll('.nav-links a');

  const updateNav = () => {
    // sticky style
    navbar.classList.toggle('scrolled', window.scrollY > 50);

    // active link
    let current = '';
    sections.forEach(sec => {
      if (window.scrollY >= sec.offsetTop - 120) current = sec.id;
    });
    navLinks.forEach(a => {
      a.classList.toggle('active', a.getAttribute('href') === '#' + current);
    });
  };

  window.addEventListener('scroll', updateNav, { passive: true });
  updateNav();

  /* ============================================================
     HAMBURGER MENU
  ============================================================ */
  const hamburger = document.querySelector('.hamburger');
  const navMenu   = document.querySelector('.nav-links');

  hamburger.addEventListener('click', () => {
    navMenu.classList.toggle('active');
    hamburger.classList.toggle('open');
  });

  // close menu on link click
  navLinks.forEach(a => a.addEventListener('click', () => {
    navMenu.classList.remove('active');
    hamburger.classList.remove('open');
  }));

  /* ============================================================
     TYPING EFFECT
  ============================================================ */
  const texts     = ['Cloud Enthusiast', 'B.Tech CS Student', 'AI Explorer', 'Full Stack Developer', 'Google Cloud Legend'];
  const typeEl    = document.querySelector('.type-effect');
  let tIndex = 0, cIndex = 0, deleting = false;

  const typeLoop = () => {
    const word = texts[tIndex];
    typeEl.textContent = deleting
      ? word.slice(0, --cIndex)
      : word.slice(0, ++cIndex);

    let delay = deleting ? 60 : 110;

    if (!deleting && cIndex === word.length) {
      delay = 1800;
      deleting = true;
    } else if (deleting && cIndex === 0) {
      deleting = false;
      tIndex = (tIndex + 1) % texts.length;
      delay = 400;
    }
    setTimeout(typeLoop, delay);
  };
  typeLoop();

  /* ============================================================
     SCROLL REVEAL
  ============================================================ */
  const revealEls = document.querySelectorAll(
    '.skill-card, .project-card, .timeline-item, .about-text, #contact-form, .achievement-card, .cert-card, .c-item, .contact-form-wrap'
  );

  // Add reveal class
  revealEls.forEach((el, i) => {
    el.classList.add('reveal');
    el.style.transitionDelay = (i % 6) * 0.07 + 's';
  });

  const observer = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        e.target.classList.add('visible');
        observer.unobserve(e.target);
      }
    });
  }, { threshold: 0.12 });

  revealEls.forEach(el => observer.observe(el));

  /* ============================================================
     CHATBOT
  ============================================================ */
  const chatbotToggler = document.querySelector('.chatbot-toggler');
  const closeBtn       = document.querySelector('.close-btn');
  const chatbox        = document.querySelector('.chatbox');
  const chatInput      = document.querySelector('.chat-input textarea');
  const sendBtn        = document.querySelector('.chat-input span');

  let userMessage = null;
  const initHeight = chatInput.scrollHeight;

  const createChatLi = (msg, cls) => {
    const li = document.createElement('li');
    li.classList.add('chat', cls);
    li.innerHTML = cls === 'outgoing'
      ? `<p></p>`
      : `<span><i class="fas fa-robot"></i></span><p></p>`;
    li.querySelector('p').textContent = msg;
    return li;
  };

  const generateResponse = el => {
    const p = el.querySelector('p');
    fetch('/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: userMessage })
    })
    .then(r => r.json())
    .then(d => { p.textContent = d.response; })
    .catch(() => { p.textContent = 'Oops! Something went wrong. Please try again.'; })
    .finally(() => chatbox.scrollTo(0, chatbox.scrollHeight));
  };

  const handleChat = () => {
    userMessage = chatInput.value.trim();
    if (!userMessage) return;

    chatInput.value = '';
    chatInput.style.height = initHeight + 'px';

    chatbox.appendChild(createChatLi(userMessage, 'outgoing'));
    chatbox.scrollTo(0, chatbox.scrollHeight);

    setTimeout(() => {
      const incoming = createChatLi('Thinking...', 'incoming');
      chatbox.appendChild(incoming);
      chatbox.scrollTo(0, chatbox.scrollHeight);
      generateResponse(incoming);
    }, 500);
  };

  chatInput.addEventListener('input', () => {
    chatInput.style.height = initHeight + 'px';
    chatInput.style.height = chatInput.scrollHeight + 'px';
  });

  chatInput.addEventListener('keydown', e => {
    if (e.key === 'Enter' && !e.shiftKey && window.innerWidth > 520) {
      e.preventDefault();
      handleChat();
    }
  });

  sendBtn.addEventListener('click', handleChat);
  closeBtn.addEventListener('click', () => document.body.classList.remove('show-chatbot'));
  chatbotToggler.addEventListener('click', () => document.body.classList.toggle('show-chatbot'));

  /* ============================================================
     CONTACT FORM
  ============================================================ */
  const contactForm = document.getElementById('contact-form');
  if (contactForm) {
    contactForm.addEventListener('submit', e => {
      e.preventDefault();
      const payload = {
        name:    document.getElementById('name').value,
        email:   document.getElementById('email').value,
        message: document.getElementById('message').value
      };
      fetch('/contact', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      })
      .then(r => r.json())
      .then(() => {
        alert('Message sent successfully!');
        contactForm.reset();
      })
      .catch(err => console.error(err));
    });
  }
});
