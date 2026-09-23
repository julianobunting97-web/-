const assert = require('node:assert/strict')
const fs = require('node:fs/promises')
const path = require('node:path')
const { chromium } = require(process.argv[2] || 'playwright')

async function main() {
  const browser = await chromium.launch({ channel: 'msedge', headless: true })
  const page = await browser.newPage({ reducedMotion: 'reduce' })
  const output = path.resolve(__dirname, '../tmp/light-site-review')
  await fs.mkdir(output, { recursive: true })

  try {
    for (const width of [1440, 390]) {
      await page.setViewportSize({ width, height: 986 })
      await page.goto('http://localhost:4173/', { waitUntil: 'load' })
      const cards = page.locator('.detail-card, .stat-card, .contact-strip-card')
      assert.ok(await cards.count() > 0)

      for (const card of await cards.all()) {
        await card.scrollIntoViewIfNeeded()
        await card.hover({ position: { x: 12, y: 30 } })
        const geometry = await card.evaluate(el => {
          const edge = el.querySelector(':scope > .edge-light')
          const frame = edge.getBoundingClientRect()
          const rect = el.getBoundingClientRect()
          const style = getComputedStyle(el)
          const padding = parseFloat(style.getPropertyValue('--glow-padding'))
          const borderLeft = parseFloat(style.borderLeftWidth)
          const borderRight = parseFloat(style.borderRightWidth)
          return {
            label: el.textContent.trim(),
            maxWidth: getComputedStyle(edge).maxWidth,
            left: frame.left + padding - rect.left - borderLeft,
            right: frame.right - padding - rect.right + borderRight,
          }
        })
        assert.equal(geometry.maxWidth, 'none', JSON.stringify(geometry))
        assert.ok(Math.abs(geometry.left) < 1 && Math.abs(geometry.right) < 1, JSON.stringify(geometry))
      }

      const gpa = page.locator('.stat-card').filter({ hasText: 'GPA' })
      await gpa.scrollIntoViewIfNeeded()
      const bounds = await gpa.boundingBox()
      await gpa.hover({ position: { x: bounds.width - 8, y: bounds.height / 2 } })
      await page.waitForTimeout(400)
      await gpa.screenshot({ path: path.join(output, `gpa-hover-${width}.png`) })
    }
    console.log('PASS: all information/stat/contact card hover borders align at desktop and mobile widths.')
  } finally {
    await browser.close()
  }
}

main().catch(error => { console.error(error); process.exitCode = 1 })
