# Pinpoints and Echoes: working rules

@../../shared/idiom/CORE.md

Voice, working rules and dataset terms follow Idiom (`CORE.md`, `DATASETS.md`, `house/`; private repo, normally linked at `../../shared/idiom`). The import is harmless when the file is absent (CI).

A SubScout story about how uncertain geoscience interpretation is. **Status: full narrative built** (hook, ladder, observation, echo, tie, error stack, interpretation, depth, volumes, test, therefore). Field-independent story; Volve is the
worked case, not the subject. Owner: Adam McCarthy, petroleum geoscience domain expert. Plan in
`docs/plan.md`; `story/story.py` computes every number from the extracts in `story/data/`.

- Built with SubScout (github.com/AdmcCarthy/SubScout). Follow SubScout's CLAUDE.md and styleguide
  for colour, type, registers, confidence language, tables, maps and performance.
- The thesis and voice are in README.md. Keep them: confident about the mechanism, explicit about
  the uncertainty.
- Confidence levels: Observed / Derived / Interpreted. The story itself teaches these three words.
- P90/P50/P10 use the oilfield convention (P90 = low case); say so on the page.
- No numbers in prose until computed from data. every figure in `story/story.md` is a `{{ metric }}`.
- Dataset terms and attribution lines come from Idiom `DATASETS.md`; they are recorded in `DATA-LICENCE.md`. Raw Volve data is never committed.
- Before showing prose: `python ../../shared/idiom/scripts/check_banned.py story/story.md` and `check_voice.py --mode published`.
- Before publishing: SubScout's readability gate, `uv run --project ../SubScout python ../SubScout/scripts/readability.py _site`,
  must pass on all five viewports. On a 360 px phone a step card gets about 300 px under the pinned figure, so keep
  cards short and custom figures at about 28 % of the viewport height when narrow.
- British English, metric first (Sm³) with boe alongside.

## Idiom (private repo)

Idiom is Adam McCarthy's private repo (`github.com/AdmcCarthy/Idiom`; `gh repo clone AdmcCarthy/Idiom` with access, normally linked at
`../../shared/idiom`) of voice, house style, working rules and the lookup tables agents use first: `DIRECTORY.md` says which repo already
does a job, `DATASETS.md` gives every dataset's terms, attribution line and status. Read the relevant one before choosing a repo or
using data, and update it when you learn something new. Never copy anything from its `personal/` or `working/` folders into this repo
or quote it in public output; if the folder is not available, say so and carry on with this file.
