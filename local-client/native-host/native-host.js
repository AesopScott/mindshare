const client = require('../mindshare-local-client');

let buffer = Buffer.alloc(0);

function writeMessage(message) {
  const body = Buffer.from(JSON.stringify(message), 'utf8');
  const header = Buffer.alloc(4);
  header.writeUInt32LE(body.length, 0);
  process.stdout.write(Buffer.concat([header, body]));
}

async function handleMessage(message) {
  try {
    if (message.method === 'connectCodex') {
      const result = await client.connectCodex();
      writeMessage({ id: message.id, ...result });
      return;
    }

    if (message.method === 'sendCodexMessage') {
      const result = await client.sendCodexMessage(message.payload || {});
      writeMessage({ id: message.id, ...result });
      return;
    }

    writeMessage({
      id: message.id,
      ok: false,
      error: `Unknown MindShare native host method: ${message.method}`
    });
  } catch (error) {
    writeMessage({
      id: message.id,
      ok: false,
      error: error.message || String(error)
    });
  }
}

function pump() {
  while (buffer.length >= 4) {
    const messageLength = buffer.readUInt32LE(0);
    if (buffer.length < messageLength + 4) return;

    const body = buffer.subarray(4, 4 + messageLength).toString('utf8');
    buffer = buffer.subarray(4 + messageLength);

    let message;
    try {
      message = JSON.parse(body);
    } catch (error) {
      writeMessage({ ok: false, error: `Invalid native message JSON: ${error.message}` });
      continue;
    }

    handleMessage(message);
  }
}

process.stdin.on('data', (chunk) => {
  buffer = Buffer.concat([buffer, chunk]);
  pump();
});

process.stdin.on('end', () => {
  process.exit(0);
});
