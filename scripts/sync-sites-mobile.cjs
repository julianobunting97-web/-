// Copy only the site's runtime assets into its isolated publishing checkout.
const fs = require('node:fs/promises')
const path = require('node:path')

const root = path.resolve(__dirname, '..')
const checkoutName = process.argv[2] || '.sites-mobile'
if (!['.sites-mobile', '.sites-release'].includes(checkoutName)) {
  throw new Error('Expected .sites-mobile or .sites-release checkout')
}
const checkout = path.join(root, checkoutName)

async function copy(relative) {
  const from = path.join(root, relative)
  const to = path.join(checkout, relative)
  await fs.mkdir(path.dirname(to), { recursive: true })
  await fs.copyFile(from, to)
}

async function walk(directory) {
  const files = []
  for (const entry of await fs.readdir(directory, { withFileTypes: true })) {
    const filename = path.join(directory, entry.name)
    if (entry.isDirectory()) files.push(...await walk(filename))
    else files.push(filename)
  }
  return files
}

async function main() {
  const sourceFiles = (await walk(path.join(root, 'src')))
    .map(file => path.relative(root, file))
    .filter(file => !file.startsWith(`src${path.sep}assets${path.sep}`))
  const portfolioFiles = (await walk(path.join(root, 'public/portfolio')))
    .filter(file => /\.(preview|full)\.webp$/i.test(file))
    .map(file => path.relative(root, file))

  const files = [
    'index.html', 'package.json', 'package-lock.json', 'vite.config.js',
    'public/favicon.svg', 'public/_redirects', 'public/fonts/Anurati-Regular.otf',
    'src/assets/hero-background.mp4',
    ...sourceFiles, ...portfolioFiles,
  ]
  for (const relative of files) await copy(relative)

  const full = portfolioFiles.filter(file => file.endsWith('.full.webp')).length
  const preview = portfolioFiles.filter(file => file.endsWith('.preview.webp')).length
  if (full !== 70 || preview < 70) throw new Error(`Missing web images: ${full} full, ${preview} previews`)
  console.log(`Synchronized ${files.length} source and asset files (${full} full-size images, ${preview} previews).`)
}

main().catch(error => { console.error(error); process.exitCode = 1 })
