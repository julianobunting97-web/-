// Keep every pixel dimension for zooming while making original-image viewing lighter on phones.
const fs = require('node:fs/promises')
const path = require('node:path')
const sharp = require(process.argv[2] || 'sharp')

const root = path.resolve(__dirname, '../public/portfolio')

async function collect(directory) {
  const images = []
  for (const entry of await fs.readdir(directory, { withFileTypes: true })) {
    const filename = path.join(directory, entry.name)
    if (entry.isDirectory()) images.push(...await collect(filename))
    else if (/\.(png|jpe?g)$/i.test(entry.name)) images.push(filename)
  }
  return images
}

async function main() {
  const sources = await collect(root)
  let originalBytes = 0
  let outputBytes = 0

  for (const source of sources) {
    const output = source.replace(/\.(png|jpe?g)$/i, '.full.webp')
    const quality = /[\\/]boards[\\/]|-cover\./i.test(source) ? 92 : 91
    await sharp(source).rotate().webp({ quality, effort: 4 }).toFile(output)

    const [original, optimized, sourceMeta, outputMeta] = await Promise.all([
      fs.stat(source), fs.stat(output), sharp(source).metadata(), sharp(output).metadata(),
    ])
    const sourceWidth = [5, 6, 7, 8].includes(sourceMeta.orientation) ? sourceMeta.height : sourceMeta.width
    const sourceHeight = [5, 6, 7, 8].includes(sourceMeta.orientation) ? sourceMeta.width : sourceMeta.height
    if (sourceWidth !== outputMeta.width || sourceHeight !== outputMeta.height) {
      throw new Error(`Pixel dimensions changed: ${source}`)
    }
    originalBytes += original.size
    outputBytes += optimized.size
  }

  console.log(`Prepared ${sources.length} full-size WebP images: ${(originalBytes / 1048576).toFixed(1)} MB -> ${(outputBytes / 1048576).toFixed(1)} MB; pixel dimensions preserved.`)
}

main().catch(error => { console.error(error); process.exitCode = 1 })
