# Video Hero Backup

This folder preserves the homepage video hero immediately before the spatial-diagram test.

- Source commit before the test: `223bbc64d23e9854d71265fb977dfbb6600f7c93`.
- The copied files preserve the original hero markup, styles, opening motion, video component, fluid effect, and MP4 asset.
- Other site files were not changed for this hero test and remain in the main repository.
- To restore the video hero, copy these files back to their matching paths under the project root, then run `npm run build`.

The backup is outside `src` and `public`, so it is not included in the Vite build.
