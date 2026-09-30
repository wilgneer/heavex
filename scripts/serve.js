/* Servidor estático para desenvolvimento local (não é usado em produção).
   Uso:  node scripts/serve.js  →  http://localhost:4330
   - brotli/gzip para texto (espelha o que a Vercel entrega)
   - Range requests para o vídeo (sem isso o loop/seek do <video> falha) */
const http = require('http');
const fs = require('fs');
const path = require('path');
const zlib = require('zlib');

const ROOT = path.resolve(__dirname, '..');
const PORT = Number(process.env.PORT) || 4330;

const TYPES = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.svg': 'image/svg+xml',
  '.webp': 'image/webp',
  '.avif': 'image/avif',
  '.png': 'image/png',
  '.mp4': 'video/mp4',
  '.txt': 'text/plain; charset=utf-8',
};
const COMPRESSIBLE = new Set(['.html', '.css', '.js', '.json', '.svg', '.txt']);

http.createServer((req, res) => {
  let rel;
  try { rel = decodeURIComponent(req.url.split('?')[0]); } catch { res.writeHead(400).end(); return; }
  if (rel.endsWith('/')) rel += 'index.html';

  let file = path.join(ROOT, path.normalize(rel));
  if (!file.startsWith(ROOT + path.sep)) { res.writeHead(403).end('403'); return; }
  // cleanUrls como na Vercel: /api-whatsapp serve api-whatsapp.html
  if (!path.extname(file) && fs.existsSync(`${file}.html`)) file += '.html';

  fs.stat(file, (err, stat) => {
    if (err || !stat.isFile()) { res.writeHead(404, { 'Content-Type': 'text/plain' }).end('404'); return; }

    const ext = path.extname(file).toLowerCase();
    const headers = {
      'Content-Type': TYPES[ext] || 'application/octet-stream',
      'Cache-Control': ext === '.html' || ext === '.js' ? 'no-store' : 'public, max-age=31536000, immutable',
      'X-Content-Type-Options': 'nosniff',
      'Accept-Ranges': 'bytes',
    };

    const range = /^bytes=(\d*)-(\d*)$/.exec(req.headers.range || '');
    if (range && ext === '.mp4') {
      const start = range[1] ? Number(range[1]) : Math.max(0, stat.size - Number(range[2]));
      const end = range[1] && range[2] ? Math.min(Number(range[2]), stat.size - 1) : stat.size - 1;
      if (start > end || start >= stat.size) {
        res.writeHead(416, { 'Content-Range': `bytes */${stat.size}` }).end();
        return;
      }
      res.writeHead(206, { ...headers, 'Content-Range': `bytes ${start}-${end}/${stat.size}`, 'Content-Length': end - start + 1 });
      fs.createReadStream(file, { start, end }).pipe(res);
      return;
    }

    const accept = req.headers['accept-encoding'] || '';
    if (COMPRESSIBLE.has(ext) && /\b(br|gzip)\b/.test(accept)) {
      const br = /\bbr\b/.test(accept);
      const body = br
        ? zlib.brotliCompressSync(fs.readFileSync(file), { params: { [zlib.constants.BROTLI_PARAM_QUALITY]: 11 } })
        : zlib.gzipSync(fs.readFileSync(file), { level: 9 });
      res.writeHead(200, { ...headers, 'Content-Encoding': br ? 'br' : 'gzip', 'Content-Length': body.length, Vary: 'Accept-Encoding' });
      res.end(body);
      return;
    }

    res.writeHead(200, { ...headers, 'Content-Length': stat.size });
    fs.createReadStream(file).pipe(res);
  });
}).listen(PORT, () => console.log(`Heavex → http://localhost:${PORT}`));
