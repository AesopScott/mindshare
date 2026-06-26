const NATIVE_HOST = 'com.mindshare.local_client';

function sendNativeRequest(request, sendResponse) {
  chrome.runtime.sendNativeMessage(
    NATIVE_HOST,
    {
      id: request.id,
      method: request.method,
      payload: request.payload || {}
    },
    (response) => {
      const lastError = chrome.runtime.lastError;
      if (lastError) {
        sendResponse({
          id: request.id,
          ok: false,
          action: 'installNativeHost',
          message: 'MindShare native host is not installed or is not registered with Chrome.',
          error: lastError.message
        });
        return;
      }

      sendResponse(response || {
        id: request.id,
        ok: false,
        error: 'MindShare native host returned no response.'
      });
    }
  );
}

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (!message || message.type !== 'MINDSHARE_LOCAL_CLIENT_REQUEST') {
    return false;
  }

  sendNativeRequest(message, sendResponse);
  return true;
});

chrome.runtime.onMessageExternal.addListener((message, sender, sendResponse) => {
  if (!sender?.url || !sender.url.startsWith('https://mojoaistudio.com/')) {
    sendResponse({
      id: message?.id,
      ok: false,
      error: 'MindShare Local Client rejected an external request from an unapproved origin.'
    });
    return false;
  }

  if (!message || message.type !== 'MINDSHARE_LOCAL_CLIENT_REQUEST') {
    return false;
  }

  sendNativeRequest(message, sendResponse);
  return true;
});
