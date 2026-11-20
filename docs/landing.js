(() => {
  'use strict';
  if (window.__DSH_EXTERNAL_BROWSER_REQUIRED__) return;

  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const toast = document.getElementById('copy-status');
  let toastTimer;

  function announce(message) {
    if (!toast) return;
    clearTimeout(toastTimer);
    toast.textContent = message;
    toast.dataset.visible = 'true';
    toastTimer = setTimeout(() => {
      delete toast.dataset.visible;
      toast.textContent = '';
    }, 4000);
  }

  function selectSource(source) {
    if (typeof source.select === 'function') {
      source.focus({ preventScroll: true });
      source.select();
      return true;
    }
    const selection = window.getSelection();
    if (!selection) return false;
    const range = document.createRange();
    range.selectNodeContents(source);
    selection.removeAllRanges();
    selection.addRange(range);
    return true;
  }

  document.querySelectorAll('[data-copy-target]').forEach(button => {
    const label = button.querySelector('[data-copy-label]');
    const originalLabel = label?.textContent;
    let labelTimer;
    let copyRequest = 0;
    button.addEventListener('click', async () => {
      const request = ++copyRequest;
      const source = document.getElementById(button.dataset.copyTarget);
      if (!source) {
        announce('未找到要复制的内容，请刷新页面后重试。');
        return;
      }
      const text = typeof source.value === 'string' ? source.value : source.textContent;
      let copied = false;
      let selected = false;
      try {
        await navigator.clipboard.writeText(text);
        copied = true;
      } catch {
        try {
          selected = selectSource(source);
          copied = selected && document.execCommand('copy');
        } catch {
          copied = false;
        }
        if (copied) button.focus({ preventScroll: true });
        else source.scrollIntoView({ block: 'nearest' });
      }
      if (request !== copyRequest) return;
      clearTimeout(labelTimer);
      if (label) label.textContent = copied ? '已复制' : '请手动复制';
      if (copied) {
        const name = button.dataset.copyName || ({
          'install-command': '完整安装指令',
          'mcp-endpoint': 'MCP 地址',
          'mcp-json': 'JSON 配置',
        }[source.id] || '内容');
        announce(`${name}已复制。`);
      } else {
        announce(selected ? '内容已选中，请按 Ctrl+C（Mac 按 ⌘C）或使用系统复制。' : '自动复制未成功，请手动选中内容后复制。');
      }
      labelTimer = setTimeout(() => {
        if (label) label.textContent = originalLabel;
      }, 3000);
    });
  });

  const installCommand = document.getElementById('install-command');
  function fitCommand() {
    if (!installCommand) return;
    installCommand.style.height = 'auto';
    installCommand.style.height = `${installCommand.scrollHeight + 2}px`;
  }
  fitCommand();
  window.addEventListener('resize', fitCommand, { passive: true });
  document.fonts?.ready.then(fitCommand);

  const header = document.querySelector('.mast');
  const menu = document.querySelector('.menu-toggle');
  const navigation = document.getElementById('site-nav');
  if (header && menu && navigation) {
    function closeMenu(returnFocus = false) {
      header.classList.remove('menu-open');
      menu.setAttribute('aria-expanded', 'false');
      menu.setAttribute('aria-label', '打开导航');
      if (returnFocus) menu.focus();
    }
    menu.addEventListener('click', () => {
      const open = menu.getAttribute('aria-expanded') !== 'true';
      header.classList.toggle('menu-open', open);
      menu.setAttribute('aria-expanded', String(open));
      menu.setAttribute('aria-label', open ? '关闭导航' : '打开导航');
    });
    navigation.addEventListener('click', event => {
      if (event.target.closest('a')) closeMenu();
    });
    document.addEventListener('keydown', event => {
      if (event.key === 'Escape' && menu.getAttribute('aria-expanded') === 'true') closeMenu(true);
    });
    document.addEventListener('click', event => {
      if (!header.contains(event.target)) closeMenu();
    });
    const updateHeader = () => header.classList.toggle('scrolled', window.scrollY > 16);
    updateHeader();
    window.addEventListener('scroll', updateHeader, { passive: true });
  }

  const demo = document.getElementById('demo-window');
  const motionToggle = document.getElementById('motion-toggle');
  const motionLabel = motionToggle?.querySelector('[data-motion-label]');
  const panels = new Map([...document.querySelectorAll('[data-scene-panel]')].map(panel => [panel.dataset.scenePanel, panel]));
  const sceneButtons = [...document.querySelectorAll('[data-scene-button]')].filter(button => panels.has(button.dataset.sceneButton));
  let sceneIndex = Math.max(0, sceneButtons.findIndex(button => button.getAttribute('aria-selected') === 'true'));
  let step = 0;
  let userPaused = reducedMotion.matches;
  let demoVisible = false;
  let pageActive = true;
  let sceneTimer = null;

  function stopTimer() {
    if (sceneTimer !== null) clearInterval(sceneTimer);
    sceneTimer = null;
  }

  function syncMotion() {
    if (!demo || !sceneButtons.length) return;
    const running = !userPaused && demoVisible && !document.hidden && pageActive;
    demo.dataset.paused = String(!running);
    if (motionToggle) {
      motionToggle.setAttribute('aria-pressed', String(userPaused));
      motionToggle.setAttribute('aria-label', userPaused ? '播放演示动画' : '暂停演示动画');
    }
    if (motionLabel) motionLabel.textContent = userPaused ? '播放动画' : '暂停动画';
    if (!running) stopTimer();
    else if (sceneTimer === null) sceneTimer = setInterval(() => {
      if (step < 3) {
        step += 1;
        demo.dataset.step = String(step);
      } else {
        showScene((sceneIndex + 1) % sceneButtons.length);
      }
    }, 2000);
  }

  function showScene(index, focus = false, restart = false) {
    if (!demo || !sceneButtons[index]) return;
    sceneIndex = index;
    step = 0;
    const activeScene = sceneButtons[index].dataset.sceneButton;
    demo.dataset.scene = activeScene;
    demo.dataset.step = '0';
    panels.forEach((panel, scene) => { panel.hidden = scene !== activeScene; });
    sceneButtons.forEach((button, position) => {
      const active = position === index;
      button.setAttribute('aria-selected', String(active));
      button.tabIndex = active ? 0 : -1;
      button.classList.toggle('is-active', active);
    });
    if (focus) sceneButtons[index].focus();
    if (restart) {
      stopTimer();
      syncMotion();
    }
  }

  if (demo && sceneButtons.length) {
    showScene(sceneIndex);
    sceneButtons.forEach((button, index) => {
      button.addEventListener('click', () => showScene(index, false, true));
      button.addEventListener('keydown', event => {
        let next;
        if (event.key === 'ArrowRight') next = (index + 1) % sceneButtons.length;
        else if (event.key === 'ArrowLeft') next = (index - 1 + sceneButtons.length) % sceneButtons.length;
        else if (event.key === 'Home') next = 0;
        else if (event.key === 'End') next = sceneButtons.length - 1;
        if (next === undefined) return;
        event.preventDefault();
        showScene(next, true, true);
      });
    });
    motionToggle?.addEventListener('click', () => {
      userPaused = !userPaused;
      syncMotion();
    });
    if ('IntersectionObserver' in window) {
      const visibilityObserver = new IntersectionObserver(entries => {
        demoVisible = entries[0].isIntersecting;
        syncMotion();
      });
      visibilityObserver.observe(demo);
    } else {
      const updateVisibility = () => {
        const rect = demo.getBoundingClientRect();
        demoVisible = rect.bottom > 0 && rect.top < window.innerHeight && rect.right > 0 && rect.left < window.innerWidth;
        syncMotion();
      };
      updateVisibility();
      window.addEventListener('scroll', updateVisibility, { passive: true });
      window.addEventListener('resize', updateVisibility, { passive: true });
    }
    document.addEventListener('visibilitychange', syncMotion);
    window.addEventListener('pagehide', () => { pageActive = false; syncMotion(); });
    window.addEventListener('pageshow', () => { pageActive = true; syncMotion(); });
    syncMotion();
  }

  const motionPreferenceChanged = event => {
    if (!event.matches) return;
    userPaused = true;
    syncMotion();
  };
  if (typeof reducedMotion.addEventListener === 'function') reducedMotion.addEventListener('change', motionPreferenceChanged);
  else reducedMotion.addListener(motionPreferenceChanged);
})();
