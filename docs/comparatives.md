# Comparatives: research notes

*Researched 2026-11-08 from web search results only. Figures below are as reported by those pages and are **not yet checked against primary sources**. Items under *Primary-source check* have since been read; the rest remain unverified until the primary source has been read and the figure entered with the `cite:` filter.*

## Primary-source check (2026-11-08)

What was read directly, and what could not be.

**Read and recorded**

- **Hoek and Palmieri, "Geotechnical risks on large civil engineering projects" (IAEG Congress keynote, 1998).** Read in full from the PDF.
  - Citing the World Bank (1985): actual construction costs of hydropower projects were on average **27% above** estimates, schedules **28% longer**. On average **less than 1%** of total project cost was spent on feasibility, pre-feasibility, reconnaissance and hydrological studies before design.
  - Figure 3, from the US National Committee on Tunnel Technology (1984): interviews with owners, engineers and contractors on **84 tunnels**, plotting contract cost against the ratio of exploration borehole length to tunnel length. The authors say it "suggests that inadequate core drilling for geological investigation results in significant project cost increases".
  - They also say the geotechnical share of overruns "cannot be isolated from the data presented", so do not attribute whole overruns to ground. Long tunnels need interpolation "between widely spaced boreholes or adits".
  - Use as: the same trade, the same problem, a real citation. Do not quote a single overrun percentage as caused by geology.
- **GEBCO, release of the GEBCO_2025 Grid (page dated 6 August 2025).** **27.3%** of the world's ocean floor mapped to modern standards, against **26.1%** for the 2024 release. The page does not define "mapped" or the standard. The Seabed 2030 announcement of 21 June 2025 is the source of the 27.3%. A later 28.7% figure was reported in a search snippet and is unconfirmed.
- **Live Science, "What percentage of the ocean have we mapped?" (24 October 2023, quoting Vicki Ferrini, Columbia University).** As of mid-2023, about a quarter of the seafloor mapped with high-resolution data. The seafloor is mapped mostly by sonar, which sends sound and times the return, so the echo link is literal. Most detail in satellite-derived seafloor maps is modelled from gravity and known depths, not measured directly. Use as: the explanation of why "mapped" needs a definition.
- **ECMWF, "Enter the ensembles" (2024 blog, on the machine-learning AIFS ensemble).** The model has 51 members. Spread plots "highlight where uncertainty is currently large and small". The article gives no quantitative link between spread and error and does not describe how the physics-based ensemble is perturbed. The earlier "one control plus 50 perturbed" wording came from a search snippet of an ECMWF presentation that was not read.

**Not read (blocked or not reached)**

- **Sodir resource report 2018, chapter 7, exploration look-back analyses.** The server returns 403 Forbidden to automated requests, and I did not work around that. **The factor of 2.5, the 58% (Dutch study) and the 78% (Westwood) figures remain unverified** and must not be used until read. Action for you: open the page in a browser and save it, or paste the figures, or point to a PDF of the report.
- **Paraskevopoulou and Boutsis (2020), Channel Tunnel and Olmos Tunnel overruns.** The MDPI page returned 403. The 78% Channel Tunnel overrun is unverified.
- Argo float and biopsy figures: not checked.

## What a comparative must do

The story's claim is: very few samples, a huge volume, every measurement uncertain, and still a confident decision. A good comparative has to share that structure, not just be a big number. Tests applied:

1. Does it also infer a whole from sparse samples?
2. Does it also have an "echo" (an indirect measurement) alongside direct samples?
3. Does it carry uncertainty through to a decision people act on?
4. Is there a public, citable number?

## Candidates

| Candidate | Fits which test | Strongest point | What the search found | Weak point |
|---|---|---|---|---|
| **Seafloor mapping** | 1, 2, 4 | The seabed is itself mapped by echo (sonar), so the echo beat is literal. We know the surface of other planets better than the floor of our own sea. | Seabed 2030 reports vary by date: 23.4% (June 2022), 24.9% (Eos), 27.3% (undated), about a quarter by mid-2023. | "High resolution" is defined differently for the seabed and for Mars imagery, so the Moon/Mars line needs care. Figures date quickly; use the current Seabed 2030 page. |
| **Tunnel and civil ground investigation** | 1, 3, 4 | Same trade, same problem: infer the ground between boreholes, then commit large sums. Hoek (1998) plots cost against the ratio of exploration borehole length to tunnel length. | Channel Tunnel total cost overran by 78%; Olmos Tunnel construction cost by 6.7-9.6% (Paraskevopoulou and Boutsis 2020). Melbourne West Gate Tunnel: up to AU$2bn overruns blamed partly on ground characterisation. Reports argue one borehole says little about ground a few metres away. | Overruns have several causes; the sources attribute only part to ground. Say so. |
| **Weather ensembles** | 3 | Maps straight onto P90/P50/P10 and onto "several valid picks": run many plausible versions, show the spread. Calibration (spread should match actual error) is a good lesson for P-values. | ECMWF runs 51 members (one control, 50 perturbed). Narrow spread means higher predictability. | The spread covers only some uncertainty sources; it does not give samples-versus-volume. Use for the volumes beat, not the scale beat. |
| **Ocean sampling (Argo floats)** | 1, 4 | About 4,000 floats profile an ocean to roughly 2,000 m; a real "few points, vast volume" case. | WHOI fact sheet: about 4,000 active floats, over 800 deployments a year; about 120,000 profiles a year. | No published coverage fraction found. Multiplying floats by depth would overstate it. We would compute our own ratio and state the method. |
| **Needle biopsy** | 1, 2 | Needle sample against an ultrasound image is the pinpoint-and-echo pair in medicine. | A patent filing estimates 12 cores take about 0.096 mL from a gland of 25-50 mL. A review cites a 35% false-negative rate for the old sextant method. An MRI-fusion study says about 1.6 mm RMS needle error is needed to sample 95% of tumours with one core. | Figures are from weak or specialised sources. The topic is sensitive for readers. Use qualitatively, or only with a verified clinical source. |
| **Opinion polling** | 1 | Familiar to every reader. | Not researched. | It samples people who can answer; the subsurface cannot. Probably too glib. Hold in reserve. |

## A stronger link than any analogy: the industry's own track record

The same search turned up published look-backs on pre-drill estimates against drilling results. These belong in the **test** beat as direct evidence, not as comparatives, and they may be the best answer to open question 3 (what to use for pre/post-drill):

- Sodir's resource report has a chapter on exploration look-back analyses. It is the same provider as our wellbore data. Per the search, the 2008 NPD study found companies overstated resource estimates by a factor of 2.5. Read the chapter before relying on this.
- A Dutch study (Hoetz et al. 2020; 215 projects) reports about 58% of promised pre-drill volumes matured, and suggests survival bias as one cause.
- Westwood's wildcat database reports 78% of discoveries since 2008 found less than the pre-drill P50, across 220 with both estimates. This is a commercial database summary.
- Milkov and co-authors have published related studies (including LaCosta and Milkov 2022 on Mexico, with Norwegian and Dutch history). I did not reach their numbers.

These need primary-source reading. If they hold, the story can say, with a citation, that the industry's own P50 has tended to be optimistic. That is the "explicit about the uncertainty" voice at its strongest.

## Recommendation

Use three comparatives, one per section of the story, plus the track record:

1. **Seafloor mapping** for the *scale* and *echo* beats: sonar is an echo too, and the ratio is simple to show.
2. **Tunnel ground investigation** for the *interpretation between the wells* and *depth/cost* beats: another trade making expensive decisions between boreholes.
3. **Weather ensembles** for the *volumes* beat: spread as a deliberate output.
4. **Sodir and published look-backs** for the *test* beat, as evidence.

Hold Argo and biopsy as alternates. If Argo is chosen, compute the ratio ourselves.

## Rules for using them

- Each comparative is drawn at the same ratio as the subsurface figure beside it, so the reader compares like with like.
- Every outside figure goes in as `{{ x | cite:<source> }}` and in the appendix ledger with its date.
- Where a figure changes with time (seafloor coverage), state the date on the page.
- Analogies illustrate; they do not prove. Tag each Derived or Interpreted as the style guide requires.

## Next steps

1. Read the primary sources for the four recommended items and record exact figures and dates here.
2. Read the Sodir look-back chapter and decide if it settles the test beat.
3. Decide which two or three to keep.
