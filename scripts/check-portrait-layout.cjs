const assert = require('node:assert/strict')
const fs = require('node:fs/promises')
const path = require('node:path')
const { chromium } = require(process.argv[2] || 'playwright')

async function main() {
  const browser = await chromium.launch({ channel: 'msedge', headless: true })
  const output = path.resolve(__dirname, '../tmp/light-site-review/portrait-layout')
  await fs.mkdir(output, { recursive: true })

  try {
    for (const width of [320, 360, 390, 430, 531, 760, 761, 800, 1000]) {
      const page = await browser.newPage({
        viewport: { width, height: 844 },
        deviceScaleFactor: 1,
        reducedMotion: 'reduce',
      })
      await page.goto('http://localhost:4173/#about', { waitUntil: 'load' })
      await page.locator('.portrait-card-shell').scrollIntoViewIfNeeded()
      const bounds = await page.evaluate(() => {
        const rect = selector => {
          const box = document.querySelector(selector).getBoundingClientRect()
          return { top: box.top, bottom: box.bottom, height: box.height }
        }
        return {
          avatar: rect('.portrait-card-shell .avatar'),
          details: rect('.portrait-card-shell .pc-details'),
          card: rect('.portrait-card-shell .pc-card'),
        }
      })

      assert.ok(bounds.details.top >= bounds.avatar.bottom + 8, `Portrait overlaps name at ${width}: ${JSON.stringify(bounds)}`)
      assert.ok(bounds.details.bottom <= bounds.card.bottom - 8, `Portrait caption is clipped at ${width}: ${JSON.stringify(bounds)}`)
      if (width === 390 || width === 531) {
        await page.locator('.portrait-card-shell').screenshot({ path: path.join(output, `portrait-${width}.png`) })
      }
      console.log(`${width}px: ${Math.round(bounds.details.top - bounds.avatar.bottom)}px portrait/name gap`)
      await page.close()
    }
  } finally {
    await browser.close()
  }
}

main().catch(error => {
  console.error(error)
  process.exitCode = 1
})
