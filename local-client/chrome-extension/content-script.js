function injectPageBridge() {
  document.documentElement.setAttribute('data-mindshare-extension', 'content-script-ready');
  const script = document.createElement('script');
  script.src = chrome.runtime.getURL('page-bridge.js');
  script.onload = () => script.remove();
  (document.documentElement || document.head).appendChild(script);
}

window.addEventListener('message', (event) => {
  if (event.source !== window) return;
  if (!event.data || event.data.type !== 'MINDSHARE_LOCAL_CLIENT_REQUEST') return;

  chrome.runtime.sendMessage(event.data, (response) => {
    const lastError = chrome.runtime.lastError;
    window.postMessage({
      type: 'MINDSHARE_LOCAL_CLIENT_RESPONSE',
      id: event.data.id,
      ...(lastError
        ? {
            ok: false,
            action: 'installExtension',
            message: 'MindShare Chrome extension could not reach its background worker.',
            error: lastError.message
          }
        : response)
    }, '*');
  });
});

injectPageBridge();
