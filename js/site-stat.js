(() => {
  const API = '/api/stat'

  const normalizePath = (path) => {
    let p = path || '/'
    try { p = decodeURIComponent(p) } catch (_) {}
    p = p.split('?')[0].split('#')[0]
    const lower = p.toLowerCase()
    if (lower.endsWith('/index.html')) p = p.slice(0, -10)
    else if (lower.endsWith('index.html')) p = p.slice(0, -10) || '/'
    const isFile = /\.(html?|xml|json|txt|js|css|png|jpe?g|gif|webp|ico|svg)$/i.test(p)
    if (p !== '/' && !p.endsWith('/') && !isFile) p += '/'
    return p || '/'
  }

  const setText = (id, value) => {
    const el = document.getElementById(id)
    if (!el || value == null) return
    el.textContent = String(value)
  }

  const fill = (data) => {
    if (!data) return
    setText('busuanzi_value_site_uv', data.site_uv)
    setText('busuanzi_value_site_pv', data.site_pv)
    setText('busuanzi_value_page_pv', data.page_pv)
  }

  const report = () => {
    const path = normalizePath(location.pathname || '/')
    fetch(API, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ path }),
      credentials: 'same-origin',
      keepalive: true
    })
      .then((r) => (r.ok ? r.json() : null))
      .then(fill)
      .catch(() => {})
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', report)
  } else {
    report()
  }

  document.addEventListener('pjax:complete', report)
})()
