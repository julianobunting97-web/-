// Smaller display images; the original files remain available in the image viewer.
const fs = require('node:fs/promises')
const path = require('node:path')
const sharp = require(process.argv[2] || 'sharp')
const root = path.resolve(__dirname, '..')

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
  const sources = await collect(path.join(root, 'public/portfolio'))
  let total = 0
  for (const source of sources) {
    const output = source.replace(/\.(png|jpe?g)$/i, '.preview.webp')
    await sharp(source).rotate().resize({ width: 1600, withoutEnlargement: true })
      .webp({ quality: 84, effort: 4 }).toFile(output)
    total += (await fs.stat(output)).size
  }
  await sharp(path.join(root, 'src/assets/portrait-cao-shuo.png'))
    .resize({ width: 1000, withoutEnlargement: true })
    .webp({ quality: 88 }).toFile(path.join(root, 'public/portfolio/portrait-cao-shuo.preview.webp'))
  console.log(`Prepared ${sources.length} display previews (${(total / 1024 / 1024).toFixed(1)} MB); originals preserved.`)
}

main().catch((error) => { console.error(error.message); process.exitCode = 1 })
