# Offline report browser review — September 7, 2026

Scope: agent-driven Chromium observation of a real generated **inspection-only**
report. This is not a human study, assistive-technology certification, native
browser-zoom test, or a real-runtime comparison.

The first launch attempts failed on missing native libraries. Thirteen x86_64
AlmaLinux packages were extracted locally without installing host packages.
Chromium still trapped during startup. A syscall trace located the failure near
its temporary SingletonSocket directory; reducing the project-local TMPDIR
length resolved it. This supports a Unix-socket path-length cause. No sandbox
or host security setting was disabled. Diagnostic trace remains in .local.

## Observed steps

1. Open the generated report locally. Status says INSPECTION ONLY and explicitly
   states that original and candidate behavior has not been measured. The
   browser loaded the report with no external resource requests.
2. Set viewport to 390 × 844. Both closed and expanded disclosures report
   scrollWidth 390; text, source hashes and JSON wrap without horizontal page
   overflow. Saved and inspected screenshots: report-mobile-v2.png and
   report-mobile-expanded-v2.png.
3. Use Tab from page load. The skip link receives a visible 3 px focus outline.
   Enter moves to #main; the next Tab reaches the native details summary, and
   Enter opens its contents. These are actual browser keyboard interactions.
4. Set viewport to 1280 × 900. scrollWidth remains 1280. The desktop screenshot
   is report-desktop.png. CSS zoom 2 also preserves page width; the corresponding
   screenshot is report-zoom-200.png. This is CSS zoom, not browser chrome zoom.
5. Follow Results JSON and Review patch from a fresh accessibility snapshot.
   Both navigate to the correct local retained artifact. The JSON explicitly
   retains behavior_measured=false and the inspected file's exact hashes.

## Independent critic result

A fresh-context Astra leaf critic reviewed the stable screenshots and renderer
against the fixed rubric: truthful evidence labels, narrow-screen readability,
keyboard/disclosure clarity, legible non-color status, and actionable recovery.
Its actual model metadata was verified. It found one actionable wording defect:
“0 Sites need review” could imply supported edits require no review. The metric
now reads “Unsupported findings,” while the text still asks maintainers to read
every proposed edit. Original screenshots are retained beside revision-2
captures. No other concrete defect was identified in that evidence.

Human/assistive-technology observations remain pending. On September 8, actual
packaged normal PASS and negative REGRESSION reports were opened in Chromium
at 390 × 844. Both loaded zero resources and had scrollWidth 390. All negative
disclosures were expanded with no horizontal overflow; WRONG.ini remained
visible in the observations. Screenshots report-pass-mobile.png and
report-regression-mobile.png were saved and visually inspected. Status words
and the negative-control explanation distinguish the results without color. Keyboard/browser evidence does not establish
ConfigParser behavioral equivalence or maintainer adoption.
