const http = require("http");
const fs = require("fs");
const path = require("path");

const root = path.join(__dirname, "dist");
const port = 4173;

const types = {
  ".html": "text/html; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".png": "image/png",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".svg": "image/svg+xml",
  ".mp4": "video/mp4",
  ".woff": "font/woff",
  ".woff2": "font/woff2",
};

http
  .createServer((req, res) => {
    const url = new URL(req.url, `http://localhost:${port}`);
    const pathname = decodeURIComponent(url.pathname);
    let file = path.join(root, pathname === "/" ? "index.html" : pathname);

    if (!file.startsWith(root)) {
      res.writeHead(403);
      res.end("Forbidden");
      return;
    }

    fs.stat(file, (statError, stat) => {
      if (statError || !stat.isFile()) {
        file = path.join(root, "index.html");
      }

      const extension = path.extname(file).toLowerCase();
      const range = req.headers.range;

      if (extension === ".mp4" && range) {
        fs.stat(file, (videoStatError, videoStat) => {
          if (videoStatError) {
            res.writeHead(500);
            res.end(String(videoStatError));
            return;
          }

          const fileSize = videoStat.size;
          const parts = range.replace(/bytes=/, "").split("-");
          const start = Number.parseInt(parts[0], 10);
          const end = parts[1] ? Number.parseInt(parts[1], 10) : fileSize - 1;
          const chunkSize = end - start + 1;
          const stream = fs.createReadStream(file, { start, end });

          res.writeHead(206, {
            "Content-Range": `bytes ${start}-${end}/${fileSize}`,
            "Accept-Ranges": "bytes",
            "Content-Length": chunkSize,
            "Content-Type": "video/mp4",
          });
          stream.pipe(res);
        });
        return;
      }

      fs.readFile(file, (readError, data) => {
        if (readError) {
          res.writeHead(500);
          res.end(String(readError));
          return;
        }

        res.writeHead(200, {
          "Content-Type": types[extension] || "application/octet-stream",
          "Accept-Ranges": extension === ".mp4" ? "bytes" : "none",
        });
        res.end(data);
      });
    });
  })
  .listen(port, "0.0.0.0", () => {
    console.log(`Portfolio preview: http://localhost:${port}/`);
  });
