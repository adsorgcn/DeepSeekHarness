(() => {
  const field = document.getElementById('install-command');
  const toast = document.getElementById('copy-status');
  const copyButtons = [...document.querySelectorAll('[data-copy]')];
  let copyTimer;

  function fitCommand() {
    field.style.height = 'auto';
    field.style.height = `${field.scrollHeight + 2}px`;
  }
  fitCommand();
  window.addEventListener('resize', fitCommand);
  if (document.fonts) document.fonts.ready.then(fitCommand);

  async function copyCommand(event) {
    const trigger = event.currentTarget;
    let copied = false;
    try {
      await navigator.clipboard.writeText(field.value);
      copied = true;
    } catch {
      field.focus({ preventScroll: true });
      field.select();
      try { copied = document.execCommand('copy'); } catch { copied = false; }
      if (copied) trigger.focus({ preventScroll: true });
      else field.scrollIntoView({ block: 'center' });
    }
    clearTimeout(copyTimer);
    copyButtons.forEach(button => {
      button.querySelector('[data-copy-label]').textContent = copied ? '已复制，去 DSH 粘贴' : '复制安装指令';
      button.querySelector('use').setAttribute('href', copied ? '#i-check' : '#i-copy');
    });
    toast.textContent = copied ? '完整指令已复制。粘贴给 DSH，按提示确认即可。' : '已选中完整指令，请按 Ctrl+C 或使用系统复制。';
    toast.dataset.visible = 'true';
    copyTimer = setTimeout(() => {
      copyButtons.forEach(button => {
        button.querySelector('[data-copy-label]').textContent = '复制安装指令';
        button.querySelector('use').setAttribute('href', '#i-copy');
      });
      delete toast.dataset.visible;
      toast.textContent = '';
    }, 3500);
  }
  copyButtons.forEach(button => button.addEventListener('click', copyCommand));

  const header = document.querySelector('.mast');
  const menu = document.querySelector('.menu-toggle');
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
  document.querySelectorAll('.nav a').forEach(link => link.addEventListener('click', () => closeMenu()));
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && menu.getAttribute('aria-expanded') === 'true') closeMenu(true);
  });
  document.addEventListener('click', event => {
    if (!header.contains(event.target)) closeMenu();
  });

  const tabs = [...document.querySelectorAll('[data-step]')];
  function activateTab(tab, focus = false) {
    tabs.forEach(item => {
      const active = item === tab;
      item.setAttribute('aria-selected', String(active));
      item.tabIndex = active ? 0 : -1;
      document.getElementById(item.getAttribute('aria-controls')).hidden = !active;
    });
    if (focus) tab.focus();
  }
  tabs.forEach((tab, index) => {
    tab.addEventListener('click', () => activateTab(tab));
    tab.addEventListener('keydown', event => {
      let next;
      if (event.key === 'ArrowRight') next = (index + 1) % tabs.length;
      if (event.key === 'ArrowLeft') next = (index - 1 + tabs.length) % tabs.length;
      if (event.key === 'Home') next = 0;
      if (event.key === 'End') next = tabs.length - 1;
      if (next === undefined) return;
      event.preventDefault();
      activateTab(tabs[next], true);
    });
  });
})();
