const http = require('node:http');
const crypto = require('node:crypto');
const fs = require('node:fs');
const path = require('node:path');
const { connectCodex, sendCodexMessage } = require('./mindshare-local-client');

const HOST = '127.0.0.1';
const PORT = Number(process.env.MINDSHARE_LOCAL_PORT || 8765);
const ALLOWED_ORIGIN = 'https://mojoaistudio.com';
const LOG_PATH = path.join(__dirname, 'mindshare-local-bridge.log');

function corsHeaders() {
  return {
    'Access-Control-Allow-Origin': ALLOWED_ORIGIN,
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Private-Network': 'true',
    'Private-Network-Access-Name': 'mindshare-local',
    'Private-Network-Access-ID': '02:00:00:00:00:01',
    'Access-Control-Max-Age': '600',
    'Vary': 'Origin'
  };
}

function sendOptions(response) {
  response.writeHead(204, {
    ...corsHeaders(),
    'Content-Length': '0'
  });
  response.end();
}

function sendHtml(response, statusCode, html) {
  response.writeHead(statusCode, {
    'Content-Type': 'text/html; charset=utf-8',
    ...corsHeaders()
  });
  response.end(html);
}

function sendJson(response, statusCode, payload) {
  response.writeHead(statusCode, {
    'Content-Type': 'application/json; charset=utf-8',
    ...corsHeaders()
  });
  response.end(JSON.stringify(payload));
}

function bridgeWindowHtml() {
  return `<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>MindShare Local Bridge</title>
  <style>
    body {
      align-items: center;
      background: #0f172a;
      color: #dbeafe;
      display: flex;
      font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      justify-content: center;
      min-height: 100vh;
      margin: 0;
    }
    main {
      border: 1px solid rgba(191, 219, 254, 0.35);
      border-radius: 12px;
      max-width: 34rem;
      padding: 1.25rem;
    }
    h1 {
      font-size: 1rem;
      margin: 0 0 0.5rem;
    }
    p {
      color: #bfdbfe;
      font-size: 0.875rem;
      line-height: 1.45;
      margin: 0;
    }
  </style>
</head>
<body>
  <main>
    <h1>MindShare Local Bridge is connected</h1>
    <p>This window lets the MindShare website communicate with local Codex CLI on this machine. Keep it open while you chat.</p>
  </main>
  <script>
    const allowedOrigin = ${JSON.stringify(ALLOWED_ORIGIN)};

    function postToOpener(payload) {
      if (window.opener && !window.opener.closed) {
        window.opener.postMessage(payload, allowedOrigin);
      }
    }

    async function callLocal(method, payload) {
      const route = method === 'connectCodex' ? '/connect-codex' : '/send-codex-message';
      const response = await fetch(route, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload || {})
      });
      return await response.json();
    }

    window.addEventListener('message', async (event) => {
      if (event.origin !== allowedOrigin) return;
      if (!event.data || event.data.type !== 'MINDSHARE_LOCAL_RELAY_REQUEST') return;

      try {
        postToOpener({
          type: 'MINDSHARE_LOCAL_RELAY_RESPONSE',
          id: event.data.id,
          ...(await callLocal(event.data.method, event.data.payload || {}))
        });
      } catch (error) {
        postToOpener({
          type: 'MINDSHARE_LOCAL_RELAY_RESPONSE',
          id: event.data.id,
          ok: false,
          error: error.message || String(error)
        });
      }
    });

    postToOpener({ type: 'MINDSHARE_LOCAL_RELAY_READY' });
  </script>
</body>
</html>`;
}

function readBody(request) {
  return new Promise((resolve, reject) => {
    let body = '';
    request.on('data', (chunk) => {
      body += chunk.toString();
      if (body.length > 1024 * 1024) {
        reject(new Error('Request body is too large.'));
        request.destroy();
      }
    });
    request.on('end', () => {
      if (!body.trim()) {
        resolve({});
        return;
      }
      try {
        resolve(JSON.parse(body));
      } catch (error) {
        reject(new Error(`Invalid JSON: ${error.message}`));
      }
    });
    request.on('error', reject);
  });
}

async function route(request, response) {
  fs.appendFileSync(LOG_PATH, `${new Date().toISOString()} ${request.method} ${request.url} origin=${request.headers.origin || ''}\n`);

  if (request.method === 'OPTIONS') {
    sendOptions(response);
    return;
  }

  if (request.method === 'GET' && request.url?.startsWith('/bridge-window')) {
    sendHtml(response, 200, bridgeWindowHtml());
    return;
  }

  if (request.method !== 'POST') {
    sendJson(response, 405, { ok: false, error: 'Method not allowed.' });
    return;
  }

  try {
    if (request.url === '/connect-codex') {
      sendJson(response, 200, await connectCodex());
      return;
    }

    if (request.url === '/send-codex-message') {
      const payload = await readBody(request);
      sendJson(response, 200, await sendCodexMessage(payload));
      return;
    }

    sendJson(response, 404, { ok: false, error: 'MindShare local bridge route not found.' });
  } catch (error) {
    sendJson(response, 500, { ok: false, error: error.message || String(error) });
  }
}

const server = http.createServer(route);

function encodeWebSocketFrame(payload) {
  const body = Buffer.from(JSON.stringify(payload));
  if (body.length < 126) {
    return Buffer.concat([Buffer.from([0x81, body.length]), body]);
  }
  if (body.length < 65536) {
    const header = Buffer.alloc(4);
    header[0] = 0x81;
    header[1] = 126;
    header.writeUInt16BE(body.length, 2);
    return Buffer.concat([header, body]);
  }
  const header = Buffer.alloc(10);
  header[0] = 0x81;
  header[1] = 127;
  header.writeBigUInt64BE(BigInt(body.length), 2);
  return Buffer.concat([header, body]);
}

function decodeWebSocketFrame(buffer) {
  const opcode = buffer[0] & 0x0f;
  if (opcode === 0x8) return null;

  let offset = 2;
  let length = buffer[1] & 0x7f;
  if (length === 126) {
    length = buffer.readUInt16BE(offset);
    offset += 2;
  } else if (length === 127) {
    length = Number(buffer.readBigUInt64BE(offset));
    offset += 8;
  }

  const masked = Boolean(buffer[1] & 0x80);
  const mask = masked ? buffer.subarray(offset, offset + 4) : null;
  offset += masked ? 4 : 0;

  const payload = Buffer.from(buffer.subarray(offset, offset + length));
  if (mask) {
    for (let i = 0; i < payload.length; i += 1) {
      payload[i] ^= mask[i % 4];
    }
  }

  return JSON.parse(payload.toString('utf8'));
}

async function handleWebSocketMessage(message) {
  if (message.method === 'connectCodex') {
    return await connectCodex();
  }

  if (message.method === 'sendCodexMessage') {
    return await sendCodexMessage(message.payload || {});
  }

  return { ok: false, error: 'MindShare local bridge WebSocket method not found.' };
}

server.on('upgrade', (request, socket) => {
  fs.appendFileSync(LOG_PATH, `${new Date().toISOString()} UPGRADE ${request.url} origin=${request.headers.origin || ''}\n`);

  if (request.url !== '/socket') {
    socket.destroy();
    return;
  }

  const key = request.headers['sec-websocket-key'];
  const accept = crypto
    .createHash('sha1')
    .update(`${key}258EAFA5-E914-47DA-95CA-C5AB0DC85B11`)
    .digest('base64');

  socket.write([
    'HTTP/1.1 101 Switching Protocols',
    'Upgrade: websocket',
    'Connection: Upgrade',
    `Sec-WebSocket-Accept: ${accept}`,
    `Access-Control-Allow-Origin: ${ALLOWED_ORIGIN}`,
    '',
    ''
  ].join('\r\n'));

  socket.on('data', async (buffer) => {
    try {
      const message = decodeWebSocketFrame(buffer);
      if (!message) {
        socket.end();
        return;
      }

      const payload = await handleWebSocketMessage(message);
      socket.write(encodeWebSocketFrame({ id: message.id, ...payload }));
    } catch (error) {
      socket.write(encodeWebSocketFrame({ ok: false, error: error.message || String(error) }));
    }
  });
});

server.listen(PORT, HOST, () => {
  console.log(`MindShare local bridge listening on http://${HOST}:${PORT}`);
});
