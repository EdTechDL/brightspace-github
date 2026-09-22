# Brightspace Support Assistant

Independent support reference and simulator based on the supplied MSU Brightspace capture. It includes ticket lookup, optional click explanations, recorded tours, and editable sample gradebooks. It is not a live D2L instance. Uncaptured screens and simulated behavior are identified in the interface.

## Deploy this repository to Vercel

1. Upload **the contents of this folder** to the root of a GitHub repository. `package.json`, `vercel.json`, and this README should be at the top level alongside `src/`, `data/`, `scripts/`, and `tests/`.
2. In Vercel, choose **Add New → Project**, connect GitHub, and import that repository.
3. Keep **Root Directory** at the repository root. The included `vercel.json` sets:
   - Framework Preset: **Other**
   - Build Command: **npm run build**
   - Output Directory: **dist**
4. Deploy. No API keys, environment variables, database, or paid integration are required by this app.

Vercel builds `dist/index.html` from the source files. Only `dist/` is served. You do not need to upload a generated HTML file or the original archive files separately.

[Vercel configuration documentation](https://vercel.com/docs/project-configuration/vercel-json) · [GitHub integration](https://vercel.com/docs/git/vercel-for-github)

## What to edit

| Change | Source |
| --- | --- |
| Support ticket symptoms, diagnostic checks, and links | `data/ticket-library.json` |
| Course Administration tool explanations | `data/tool-help.json` |
| Interactive walkthrough wording and steps | `data/workflows.json` |
| Layout, typography, spacing, colors | `src/app.css` |
| Page shell, overlays, and walkthrough controls | `src/experience.js` |
| Gradebook, wizard, and course tool forms | `src/grade-ui.js` |
| Setting-specific click explanations | `src/explain.js` |
| Ticket search and result cards | `src/support.js` |
| Recorded-screen rendering and tour parsing | `src/capture.js` |
| Base state, calculations, and application behavior | `src/app.js` |
| Captured source evidence and original recorded tour | `data/capture/` |

`data/capture/` contains imported reference evidence with the live sandbox course identifier replaced by `SANDBOX-COURSE-ID`; preserve its provenance and put corrections in reviewed lesson content. Some original tour statements are corrected by `REVIEWED_REPLAY_CARDS` in `src/experience.js`.

The source files currently use classic JavaScript concatenation. Extension order in `scripts/build.mjs` matters: later view functions override earlier prototype implementations. Preserve that order until an explicit module refactor is tested.

## Future updates

Use a branch or pull request for an update. Vercel can create a preview URL for that branch; after review, merge into the production branch (normally `main`) to update the main site. Changes become live after the deployment finishes, not while a file is being typed. [Vercel Git deployments](https://vercel.com/docs/git)

For an AI-assisted edit, identify the ticket or screen, the expected behavior, and the matching source file from the table. Keep exact captured labels where available and preserve the distinction between real observations and simulated behavior.

## Local build and checks

Use a current Node.js runtime. There are no third-party packages to install.

```sh
npm run build
npm test
```

Open the generated `dist/index.html` directly in a browser. A development server is optional. Do not edit `dist/index.html` as the source of truth; it is regenerated on every build and ignored by Git.

## Hosting and saved data

Sample edits and learning notes are stored in that browser's local storage. Vercel hosting does not synchronize them between devices or write them back to GitHub. Moving from localhost to a Vercel domain starts a separate browser store; export any notes you want to keep before moving. The current app exports notebooks for reuse with an AI; it does not import them to restore app state.

The page makes no API requests. Opening a documentation link leaves the page for that linked site. Ticket search is a local curated keyword lookup, not a model-generated diagnosis.

The static site contains the captured reference text and sample records. Repository visibility and deployed-site access are separate settings: a private GitHub repository does not itself make the website private. Personal notebook exports are excluded by `.gitignore` and are not part of this package.

## Coverage

44 Course Admin explanations, 25 ticket references, 47 captured-screen records, 10 working walkthroughs, and a 20-step recorded tour. Some destinations are documentation-only and the full Brightspace permission, assessment, and integration systems are not reproduced. See `docs/` for the original quick-start and validation notes. Their standalone-filename instructions refer to the earlier HTML delivery; this repository generates `dist/index.html`.
