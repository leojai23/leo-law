# Leo-Law — Roadmap

An offline-first reference notebook for **Indian lawyers, with a Tamil Nadu focus**.
Single-file PWA, same house style as Leo-Interview / Leo-Health. Live at
<https://leojai23.github.io/leo-law/>.

**Design principle:** every screen must be *reliable enough for a practitioner to
refer to*, not just a study aid. Statutory text only from the Gazette / India Code
(public domain); every fact carries a provenance line; every mapping is reconciled
against the official concordance; case law is citation + own-words ratio only —
never copied notes or headnotes.

Status legend:  ✅ done · 🔜 next · ⬜ planned · ⏸ deferred
Effort: **S** ≈ hours · **M** ≈ a session or two · **L** ≈ multi-session

---

## Phase 0 — Module 1 foundation ✅

- ✅ BNS ⇄ IPC quick converter — two-way section/keyword search, family filters,
  3 status groups (Mapped/Renumbered · New in BNS · Omitted), 4 reading themes,
  offline PWA, deployed to GitHub Pages
- ✅ 152 mapped provisions (the common ones a litigator reaches for)
- ✅ Full verbatim **BNS text for all 358 sections** (Gazette source, parser-QA'd),
  expandable per card — sub-sections, Exceptions, Explanations, Illustrations
- ✅ **BNSS First Schedule classification** (cognizable / bailable / triable-by)
  for 288 sections + sub-sections; compact chips on cards, full table in detail
- ✅ **Compoundability** line (BNSS s.359(1)/(2))
- ✅ **Mapping reconciliation** against the official IPC–BNS concordance —
  6 errors found and fixed (see Changelog)
- ✅ Per-section **provenance** line + top-of-page **"Sources & method"** panel

---

## Phase 1 — finish Module 1 to practitioner grade

| # | Item | Deliverable | Effort | Status |
|---|------|-------------|--------|--------|
| 1.1 | **Full IPC bare-act text** | old IPC section shown verbatim beside the BNS one (currently only the number) | M | 🔜 |
| 1.2 | **Second-source text diff** | diff all 358 BNS texts against India Code / PRS; resolve parser artefacts; stamp each "text verified" | M | 🔜 |
| 1.3 | **Punishment pull-out** | a clean "Punishment" line per sub-section, extracted from the text, not paraphrased | S | ⬜ |
| 1.4 | **Amendment / commencement tracker** | flag provisions not yet in force or later amended (BNS 106(2) etc.); a dated "as in force on…" line | S (ongoing) | ⬜ |
| 1.5 | **Landmark case pointers** | citation + one-line ratio only, for the top ~40 offences (*Mithu*, *Joseph Shine*, *Navtej Johar*, …) | M | ⬜ |
| 1.6 | **In-text cross-reference links** | "see section 122" becomes a tap-through inside the section text | S | ⬜ |

---

## Phase 2 — the other two new-code converters

Same engine and reliability method (Gazette text + official concordance + Schedule).

| # | Item | Notes | Effort | Status |
|---|------|-------|--------|--------|
| 2.1 | **BSA ⇄ Evidence Act** | 170 sections — smallest, fastest confidence-builder | M | ⬜ |
| 2.2 | **BNSS ⇄ CrPC** | 531 sections — procedure, bail provisions, limitation for cognizance, magistrate powers | L | ⬜ |

---

## Phase 3 — practice modules (task-oriented)

| # | Item | Deliverable | Effort | Status |
|---|------|-------------|--------|--------|
| 3.1 | **s.138 NI Act** | notice-period calculator, limitation dates, ingredients, stage checklist, draft skeletons | M | ⬜ |
| 3.2 | **Bail** | regular / anticipatory / default: grounds, checklist, which court, BNSS section map | M | ⬜ |
| 3.3 | **Limitation Act ready-reckoner** | searchable table of the ~137 Articles (period + when time runs) | S | ⬜ |
| 3.4 | **Court-fees & suit valuation** | Central Act first, then TN (see Phase 4) | M | ⬜ |
| 3.5 | **Standard drafts & checklists** | plaint, WS, bail application, 138 complaint, vakalat | M | ⬜ |

---

## Phase 4 — Tamil Nadu layer *(the differentiator)*

| # | Item | Deliverable | Effort | Status |
|---|------|-------------|--------|--------|
| 4.1 | **TN state amendments** | to CPC / CrPC→BNSS / Rent Control / Land Reforms | M | ⬜ |
| 4.2 | **TN Court-Fees & Suits Valuation Act** | ready-reckoner | M | ⬜ |
| 4.3 | **TN enactments index** | TN Prohibition, TN Public Property, Pannaiyal Protection, TNPID, etc. | M | ⬜ |
| 4.4 | **Deep links** | Madras HC cause list & JUDIS, eCourts case status, DLSA | S | ⬜ |
| 4.5 | **Local practice notes** | jurisdiction, presentation, filing quirks — clearly marked "practice note, not law" | M (ongoing) | ⬜ |

---

## Phase 5 — Tamil-language layer

| # | Item | Deliverable | Effort | Status |
|---|------|-------------|--------|--------|
| 5.1 | **Tamil gloss** under each section | plain-language, labelled "not an official translation" | L | ⬜ |
| 5.2 | **Tamil UI toggle** | | S | ⬜ |
| 5.3 | **Bilingual search** | type "கொலை" → murder / BNS 103 | M | ⬜ |

---

## Phase 6 — platform & trust

| # | Item | Deliverable | Effort | Status |
|---|------|-------------|--------|--------|
| 6.1 | **Unified search** across all modules from one box | | M | ⬜ |
| 6.2 | **Versioned changelog** in-app | "what changed since you last opened" + a data-version stamp | S | ⬜ |
| 6.3 | **Update pipeline** | re-run `build-scripts/` when the Gazette/Schedule changes | S | ⬜ |
| 6.4 | **Disclaimer / terms page** | "finding aid, not legal advice, verify the Gazette" | S | ⬜ |
| 6.5 | **Leo-Hub tile** + shared styling | | S | ⬜ |
| 6.6 | Optional: packaged offline bundle / installable desktop | | M | ⏸ |

---

## Cross-cutting rules (in force now)

- Statutory text **only** from Gazette / India Code (public domain, s.52(1)(q)
  Copyright Act 1957). **Never** copy SCC / Manupatra / Devgan notes or headnotes.
- Every fact carries a **provenance** line.
- Every mapping is **reconciled against the official IPC–BNS concordance**.
- Case law = **citation + own-words ratio only**.
- Every module keeps the standing disclaimer: *finding aid, not an authority;
  confirm against the Gazette; check for amendments and commencement notifications.*

---

## Suggested order

**Phase 1** (complete the module people actually rely on) → **2.1 BSA converter**
(fast win) → **3.1 s.138 module** → **Phase 4 TN layer**.

---

## Changelog

### 2026-09-09 — reliability pass
- Reconciled all 152 IPC↔BNS mappings against the official concordance.
  Fixed 6 mapping errors:
  - IPC **116** → BNS **56** (was 51)
  - IPC **120** → BNS **60** (was 55)
  - IPC **145** → BNS **189(3)** (was 189(5))
  - IPC **216** → BNS **253** (was 251)
  - IPC **372 / 373** → BNS **98 / 99** (was 145 / 146 — also wrong subject)
  - IPC **427** → BNS **324(4)** (was 324(3) — reverted a bad earlier fix)
- Added BNSS First Schedule classification (288 sections) + compoundability.
- Added provenance lines + "Sources & method" panel.

### 2026-09-09 — detail view
- Embedded all 358 BNS sections (Gazette text); expandable "bare act" per card
  with sub-sections, Exceptions, Explanations, Illustrations, related-section links.

### 2026-09-09 — launch
- Module 1 BNS⇄IPC converter, 152 provisions, deployed to GitHub Pages.
