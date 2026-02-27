# Deck Generation Prompt

A prompt for generating academic slide decks with Claude Code. This prompt encodes best practices for Beamer presentations with embedded code, figures, and multi-agent review.

## Prerequisites

- Claude Code opened in a local directory containing your course materials
- Existing slides, notes, or content to restructure (optional but recommended)
- R installed (or let Claude install it)
- LaTeX/Beamer installed (or let Claude install it)

## The Prompt

Customize the bracketed sections for your context, then paste into Claude Code:

---

```
I want you to design for me an original Beamer style design — something truly original, aesthetically pleasing, but professional for [AUDIENCE: e.g., "an undergraduate course on data science" / "a PhD seminar in applied microeconomics" / "a conference presentation on causal inference"].

I then want you to take [THE CONTENT: e.g., "the first deck" / "my lecture notes on regression discontinuity" / "this paper draft"] and restructure it.

I want you to emphasize a new rhetoric of the same subject matter and key learning points but maintaining my pedagogy as you detect it.

I want [CODE LANGUAGE: R/Python/Stata] scripts embedded in the decks, and also new [CODE LANGUAGE] scripts accompanying it so that I can do walk-throughs and provide those scripts to students.

Remember: to me a deck must be beautiful, it must have a consistent narrative flow that nonetheless maintains technical rigor, it must have beautiful slides with optimal cognitive density across all slides — a smooth delivery, not overloaded at the slide level, but distributed and balanced well so that slides do not become too dense — and I want beautiful figures and beautiful tables as I care about the visualization of data.

And then compile it.

Once you compile, then check and eliminate ALL overfull, underfull, vbox and hbox errors. No matter how small. Recompile.

Then have a second agent evaluate the deck for whether these instructions were met and make adjustments based on that recommendation and criticism.

I want the figures and tables to be based on [CODE LANGUAGE] output (png and tex), so it is critical you run the code first and then be sure to have it inserted well.

Always be aware of labeling issues with Tikz and graphics from ggplot. You can often easily miss the mislabeling positioning because it will not show up as compile overfull etc errors. They are more often due to restrictions you placed inadvertently on positions and coordinate placements being wrong.

Have a third agent check only the graphics for those problems including numerical accuracy.

Then compile a third and last time.
```

---

## The Iterative Workflow

This is a loop, not a linear process. You repeat until all tests pass.

### Step 1: Build and Compile

Create the deck emphasizing:

- **Beautiful slides** - every element earns its presence
- **Beautiful figures** - clear, well-labeled, purposeful
- **Beautiful tables** - clean, readable, highlighted key values
- **Beautiful quantification** - numbers that tell a story
- **MB/MC equivalence** - the marginal benefit to marginal cost ratio should be _equal across all slides_

The goal is NOT to maximize cognitive density. The goal is **smoothness** - a consistent cognitive load throughout, so the audience isn't overwhelmed on slide 7 and bored on slide 12.

Exception: **"Jump scares"** - deliberate spikes in density for rhetorical effect. A sudden, striking statistic. A provocative claim. These must be _intentional_, not accidents of poor distribution.

Compile the deck.

### Step 2: Fix ALL Compilation Warnings

Check for and eliminate:

- Overfull hbox
- Underfull hbox
- Overfull vbox
- Underfull vbox

**No matter how small or inconsequential they seem.** These warnings indicate that LaTeX is making compromises you didn't authorize. Fix every single one.

Recompile.

### Step 3: Check for Silent Visual Errors

This is the critical step that most people skip. **Compilation success does not mean visual success.**

The things that will NOT show up as errors but ARE visual errors:

**Tikz problems:**

- Shape size constraints forcing label misplacement
- Labels not where you think they are
- Coordinate systems misaligned
- Arrows pointing to wrong locations

**Software-generated graphics (ggplot2, matplotlib, etc.):**

- Axis labels cut off or overlapping
- Legend placement obscuring data
- Text sizing inconsistent with slide aesthetic
- Coordinate placements wrong

**How to check:** You must explicitly verify coordinates. Ask:

- "Check whether the placement of labels matches the intended placement by examining the coordinate values"
- "Verify that Tikz node positions correspond to their visual appearance"
- "Confirm ggplot labels are positioned correctly relative to their data points"

This is where Referee 2 comes in - the adversarial reviewer should specifically check graphics positioning.

### Step 4: Recompile and Re-evaluate

After fixing graphics issues, recompile and check AGAIN for:

- **Flow** - does the narrative still work?
- **MB/MC equivalence** - is cognitive load still balanced?
- **Label positioning** - are all visual elements where they belong?

### Step 5: Repeat Until All Tests Pass

This is a loop:

```
while (not all_tests_pass):
    fix_issues()
    recompile()
    check_flow_and_equivalence()
    check_label_positioning()
```

Only when the deck passes ALL tests do you, as the human, begin walking through it manually.

---

## What Each Phase Accomplishes

### Design Phase

Creates an original Beamer theme rather than using defaults:

- Professional but distinctive
- Consistent color palette
- Clean typography
- Appropriate for the audience

### Rhetoric Restructuring

Takes existing content and applies principles from `rhetoric_of_decks.md`:

- One idea per slide
- Titles as assertions
- Pyramid principle (conclusion first)
- MB/MC equivalence across slides

### Code Integration

- Runs code FIRST to generate figures
- Creates standalone scripts for walkthroughs
- Inserts outputs (PNG, tex tables) into slides
- Embeds executable code where pedagogically useful

### Multi-Agent Review

**Agent 1 (Builder):** Creates the deck

**Agent 2 (Referee 2 / Rhetoric Reviewer):** Evaluates:

- Narrative flow
- MB/MC balance across slides
- Technical rigor maintained
- Pedagogical consistency
- **Graphics coordinate verification**

**Agent 3 (Graphics Specialist):** Checks ONLY:

- Tikz positioning vs. intended positioning
- ggplot/matplotlib label placement
- Numerical accuracy in figures
- Coordinate/position constraint conflicts

## Customization Tips

### For Different Audiences

**Undergraduates:**

```
...professional for an undergraduate course on [SUBJECT].
The students are mostly [YEAR] majors in [FIELD],
many are commuter students with jobs,
and approximately [X]% have prior exposure to [PREREQUISITE].
```

**PhD Students:**

```
...professional for a PhD seminar in [FIELD].
Assume strong mathematical background but varying exposure to [METHOD].
Emphasize intuition alongside formal results.
```

**Conference Presentation:**

```
...professional for a 20-minute conference presentation.
The audience is academic economists familiar with [BROAD AREA]
but not specialists in [YOUR SPECIFIC TOPIC].
Emphasize the identification strategy and key results.
```

### For Different Code Languages

**Stata:**

```
I want Stata do-files embedded in the decks...
figures based on Stata graph export (png)...
```

**Python:**

```
I want Python scripts embedded in the decks...
figures based on matplotlib/seaborn output (png)...
```

### If You Have Student Data

```
Before designing, please review the attached class roster [roster.pdf]
which contains student majors and years.
Tailor the rhetoric to this specific audience composition.
```

## Why This Works

The prompt succeeds because it:

1. **Specifies aesthetics AND function** - "beautiful" but also "professional" and "technically rigorous"

2. **Names the enemy explicitly** - "not overloaded at the slide level, but distributed and balanced"

3. **Demands code-first workflow** - run code → generate figures → insert (not the reverse)

4. **Builds in adversarial review** - second and third agents catch what the first missed

5. **Treats warnings as errors** - "no matter how small" forces Claude to fix LaTeX warnings that humans ignore

6. **Calls out the silent failures** - Tikz/ggplot positioning issues don't throw errors but ruin slides

## Example Output Structure

After running this prompt, you should have:

```
lecture_01/
├── lecture_01.tex          # Main Beamer file
├── lecture_01.pdf          # Compiled deck
├── beamertheme_custom.sty  # Original theme
├── scripts/
│   ├── figure_1.R          # Standalone script
│   ├── figure_2.R
│   └── table_1.R
├── figures/
│   ├── figure_1.png
│   └── figure_2.png
└── tables/
    └── table_1.tex
```

---

_This prompt was developed through iterative refinement across multiple teaching and research presentation projects. The multi-agent review process catches errors that single-pass generation misses._
