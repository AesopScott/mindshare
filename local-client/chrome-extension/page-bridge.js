(function installMindShareLocalClient() {
  if (window.MindShareLocalClient) return;

  const pending = new Map();
  const DEFAULT_TIMEOUT_MS = 300000;

  window.addEventListener('message', (event) => {
    if (event.source !== window) return;
    if (!event.data || event.data.type !== 'MINDSHARE_LOCAL_CLIENT_RESPONSE') return;

    const request = pending.get(event.data.id);
    if (!request) return;

    clearTimeout(request.timer);
    pending.delete(event.data.id);
    request.resolve(event.data);
  });

  function request(method, payload, timeoutMs = DEFAULT_TIMEOUT_MS) {
    const id = crypto.randomUUID();
    return new Promise((resolve) => {
      const timer = setTimeout(() => {
        pending.delete(id);
        resolve({
          id,
          ok: false,
          action: 'timeout',
          error: `MindShare Local Client timed out while running ${method}.`
        });
      }, timeoutMs);

      pending.set(id, { resolve, timer });
      window.postMessage({
        type: 'MINDSHARE_LOCAL_CLIENT_REQUEST',
        id,
        method,
        payload: payload || {}
      }, '*');
    });
  }

  window.MindShareLocalClient = {
    source: 'chrome-extension',
    connectCodex() {
      return request('connectCodex', {}, 30000);
    },
    sendCodexMessage(payload) {
      return request('sendCodexMessage', payload);
    },
    connectClaude() {
      return Promise.resolve({
        ok: false,
        action: 'notWired',
        message: 'Claude connection is not wired yet.'
      });
    }
  };

  window.dispatchEvent(new CustomEvent('mindshare-local-client-ready'));
})();
