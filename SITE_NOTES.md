# Light Portfolio Website

The working website remains in the repository root (React + Vite). The PDF
portfolio is separate and was not changed during the light-theme redesign.

- Theme tokens: `src/styles.css`; editorial theme: `src/light-theme.css`.
- Existing artwork, hero video, Anurati heading, full-resolution image viewer,
  project details, Bilibili embeds, and contact information are preserved.
- `scripts/prepare-web-previews.cjs` accepts a Sharp module path as its first
  argument. It creates WebP display copies without modifying original images.
- `scripts/check-light-site.cjs` accepts a Playwright module path as its first
  argument. It checks three viewport sizes and existing gallery interactions.
- Preview server: `node preview-server.cjs`, serving `dist` at port 4173.
  Run `npm run build` after edits. Do not open preview windows automatically.

## Sites Publication

Use `.sites-release` as the isolated Sites checkout. Its manifest and Git history
belong to the private Site `appgprj_6ab38027664c8191b93fa378a6baab0e`.
Do not register another Site. Do not push the main repository to the Sites remote:
it contains unrelated PDF outputs, temporary files, and the original Git history.

Synchronize only website source, public assets, dependency manifests, entry HTML,
and Vite configuration into `.sites-release` before publishing. Its static
configuration enables SPA fallback for `/projects/...` links. Keep PDF assets,
review screenshots, dependencies, credentials, and temporary artifacts out of
the published source. Obtain temporary credentials through the Sites connector
and pass them only on stdin to the bundled workflow; never save them in files.

The website builds and local interaction checks pass. Two Sites source-push
attempts failed with HTTP 403. The last attempt ended on 2026-09-23 with the
server message "Invalid or expired token" after a long upload. No save/deploy
operation has run, and no hosted URL is verified. Local preview remains available
at http://localhost:4173/. For a future publication retry, reuse the existing Site,
obtain fresh credentials, and let the workflow reconcile the remote source state.
