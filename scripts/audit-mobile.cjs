const assert = require('node:assert/strict')
const fs = require('node:fs/promises')
const path = require('node:path')
const { chromium } = require(process.argv[2] || 'playwright')

async function main() {
  const browser = await chromium.launch({ channel: 'msedge', headless: true })
  const out = path.resolve(__dirname, '../tmp/light-site-review/mobile-audit')
  await fs.mkdir(out, { recursive: true })
  try {
    for (const width of [390, 360, 320]) {
      const context = await browser.newContext({ viewport: { width, height: 844 }, deviceScaleFactor: 1, isMobile: true, hasTouch: true, reducedMotion: 'reduce' })
      const page = await context.newPage()
      const errors = []
      page.on('pageerror', error => errors.push(error.message))
      await page.goto('http://localhost:4173/', { waitUntil: 'load' })
      await page.waitForTimeout(300)
      const report = await page.evaluate(() => {
        const selectors = ['.nav-surface', '.nav-links', '.hero', '.hero-title-en', '.hero-caption', '.hero-meta-strip', '.hero-media', '#about', '.portrait-card-shell', '.about-card', '.detail-grid', '.stats-grid', '#projects', '.project-card', '.project-board-strip', '.project-media-preview', '#strengths', '#contact', '.contact-card']
        const entries = Object.fromEntries(selectors.map(selector => {
          const el = document.querySelector(selector)
          if (!el) return [selector, null]
          const rect = el.getBoundingClientRect()
          return [selector, {
            x: Math.round(rect.x), y: Math.round(rect.y + scrollY),
            width: Math.round(rect.width), height: Math.round(rect.height),
            display: getComputedStyle(el).display,
          }]
        }))
        const overflow = [...document.querySelectorAll('body *')]
          .filter(el => {
            const rect = el.getBoundingClientRect()
            return rect.width > 0 && (rect.right > innerWidth + 1 || rect.left < -1)
          })
          .slice(0, 15)
          .map(el => ({ selector: `${el.tagName.toLowerCase()}.${el.className?.baseVal || el.className || ''}`, text: el.textContent.trim().slice(0, 24), right: Math.round(el.getBoundingClientRect().right) }))
        return { scrollWidth: document.documentElement.scrollWidth, viewport: innerWidth, entries, overflow }
      })
      assert.equal(report.scrollWidth, width)
      assert.equal(await page.locator('.nav-links a').count(), 5)
      for (const link of await page.locator('.nav-links a').all()) {
        const rect = await link.boundingBox()
        assert.ok(rect.width >= 44 && rect.height >= 44, `Small navigation target at ${width}: ${JSON.stringify(rect)}`)
      }
      assert.ok(report.entries['.hero-media'].y < 730, `Hero video too low at ${width}`)
      assert.ok(report.entries['.project-board-strip'].height < 450, `Boards too tall at ${width}`)
      await page.screenshot({ path: path.join(out, `hero-${width}.png`) })
      await page.locator('.portrait-card-shell').scrollIntoViewIfNeeded()
      await page.waitForTimeout(350)
      const portrait = await page.evaluate(() => {
        const avatar = document.querySelector('.portrait-card-shell .avatar').getBoundingClientRect()
        const details = document.querySelector('.portrait-card-shell .pc-details').getBoundingClientRect()
        const card = document.querySelector('.portrait-card-shell .pc-card').getBoundingClientRect()
        return { avatarBottom: avatar.bottom, detailsTop: details.top, detailsBottom: details.bottom, cardBottom: card.bottom }
      })
      assert.ok(portrait.detailsTop >= portrait.avatarBottom + 8, `Portrait overlaps name at ${width}: ${JSON.stringify(portrait)}`)
      assert.ok(portrait.detailsBottom <= portrait.cardBottom - 8, `Portrait name leaves card at ${width}: ${JSON.stringify(portrait)}`)
      await page.screenshot({ path: path.join(out, `portrait-${width}.png`) })
      await page.locator('#about').scrollIntoViewIfNeeded()
      await page.waitForTimeout(350)
      await page.screenshot({ path: path.join(out, `about-${width}.png`) })
      await page.locator('#projects').scrollIntoViewIfNeeded()
      await page.waitForTimeout(350)
      await page.screenshot({ path: path.join(out, `projects-${width}.png`) })
      await page.locator('#contact').scrollIntoViewIfNeeded()
      await page.waitForTimeout(350)
      await page.screenshot({ path: path.join(out, `contact-${width}.png`) })
      await page.locator('.project-media-trigger').first().click()
      await page.waitForTimeout(350)
      await page.screenshot({ path: path.join(out, `gallery-${width}.png`) })
      const modal = page.locator('.project-modal-shell')
      await modal.evaluate(el => { el.scrollTop = 550 })
      const modalRect = await modal.boundingBox()
      const closeRect = await page.getByRole('button', { name: '关闭媒体弹层' }).boundingBox()
      assert.ok(closeRect.y >= modalRect.y && closeRect.y < modalRect.y + 60, `Gallery close is not sticky at ${width}`)
      await page.locator('.project-media-slot-copy button').first().click()
      await page.waitForTimeout(350)
      await page.screenshot({ path: path.join(out, `original-${width}.png`) })
      await page.getByRole('button', { name: '放大图片' }).tap()
      assert.equal(await page.locator('.image-preview-zoom').innerText(), '300%')
      await page.getByRole('button', { name: '重置图片缩放' }).tap()
      assert.equal(await page.locator('.image-preview-zoom').innerText(), '100%')
      const canvas = await page.locator('.image-preview-canvas').boundingBox()
      const cdp = await context.newCDPSession(page)
      const centerX = Math.round(canvas.x + canvas.width / 2)
      const centerY = Math.round(canvas.y + canvas.height / 2)
      await cdp.send('Input.dispatchTouchEvent', { type: 'touchStart', touchPoints: [{ x: centerX - 35, y: centerY }, { x: centerX + 35, y: centerY }] })
      await cdp.send('Input.dispatchTouchEvent', { type: 'touchMove', touchPoints: [{ x: centerX - 95, y: centerY }, { x: centerX + 95, y: centerY }] })
      await cdp.send('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: [] })
      await page.waitForTimeout(80)
      assert.ok(Number.parseInt(await page.locator('.image-preview-zoom').innerText(), 10) > 100, `Pinch did not zoom at ${width}`)
      await page.getByRole('button', { name: '关闭原图预览' }).click()
      await page.getByRole('button', { name: '关闭媒体弹层' }).click()
      const href = await page.locator('.project-detail-link').first().getAttribute('href')
      await page.goto(new URL(href, 'http://localhost:4173/').href, { waitUntil: 'load' })
      await page.locator('.project-detail-cover-boards img').first().evaluate(img => img.decode())
      const coverBoard = await page.locator('.project-detail-board').first().boundingBox()
      assert.ok(coverBoard.width > width * .5 && coverBoard.height > width * .6, `Project board too small at ${width}: ${JSON.stringify(coverBoard)}`)
      await page.screenshot({ path: path.join(out, `detail-${width}.png`) })
      assert.deepEqual(errors, [])
      console.log(JSON.stringify({ width, ...report, errors }))
      await context.close()
    }
  } finally {
    await browser.close()
  }
}

main().catch(error => { console.error(error); process.exitCode = 1 })
