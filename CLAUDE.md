# Pinpoints and Echoes: working rules

A SubScout story about how uncertain geoscience interpretation is. **Status: draft, first slice built** (hook, ladder, error-stack, interpretation spread). Field-independent story; Volve is the
worked case, not the subject. Owner: Adam McCarthy, petroleum geoscience domain expert. Plan in
`docs/plan.md`; `story/story.py` computes every number from the extracts in `story/data/`.

- Built with SubScout (github.com/AdmcCarthy/SubScout). Follow SubScout's CLAUDE.md and styleguide
  for colour, type, registers, confidence language, tables, maps and performance.
- The thesis and voice are in README.md. Keep them: confident about the mechanism, explicit about
  the uncertainty.
- Confidence levels: Observed / Derived / Interpreted. The story itself teaches these three words.
- P90/P50/P10 use the oilfield convention (P90 = low case); say so on the page.
- No numbers in prose until computed from data. every figure in `story/story.md` is a `{{ metric }}`.
- Check dataset licences and terms before downloading anything; record them in data/README.md.
- British English, metric first (Sm³) with boe alongside.
