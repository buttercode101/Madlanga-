# 60-SECOND DEMO VIDEO SCRIPT
## Madlanga Commission Evidence Room — "R147M vs Free Tool"

**Target:** Native X (Twitter) video upload
**Format:** 60 seconds, 1080x1920 (vertical) or 1920x1080 (horizontal)
**Style:** Screen recording + voiceover, fast-paced, punchy

---

## SHOT LIST (with timestamps)

| Time | Visual | Audio/Voiceover |
|------|--------|-----------------|
| **0:00-0:03** | **HOOK** — Split screen: Left side "R147,000,000" (animated counter), Right side "$0" | *"South Africa spent 147 million rand on the Madlanga Commission. I built a free tool that does their evidence analysis in minutes."* |
| **0:03-0:08** | **EVIDENCE ROOM LOAD** — Browser opens `madlanga-evidence.vercel.app`, header visible with "40 hearing days • 420K chars • 29 witness docs" | *"This is the public Evidence Room. 40 hearing days ingested. 420,000 characters of transcript. 29 witness documents. All free-tier."* |
| **0:08-0:18** | **QUERY 1 (FAIL)** — Type: "What did Mkhwanazi claim about the 121 dockets?" → Hit Enter → Show loading spinner (1.5s) → **NO FINDING: FAIL** card appears with red badge | *"Watch this. Ask about Mkhwanazi's explosive claim — that 121 dockets were removed. The Finding Gate runs 10 conditions... FAIL. Only ONE source. A contradiction exists. Gate says: insufficient evidence."* |
| **0:18-0:25** | **ZOOM INTO FAIL DETAILS** — Hover/click to show: Sources (1 PRIMARY), Contradictions (1), Gaps (1) | *"One PRIMARY source. One unresolved contradiction. One evidence gap. This is what zero-hallucination looks like — it refuses to hallucinate a finding."* |
| **0:25-0:35** | **QUERY 2 (PASS)** — Clear, type: "When was the commission established?" → Enter → Loading → **FINDING: PASS** with green badge | *"Now ask something the Gazette confirms. When was it established? PASS. Two PRIMARY sources: Gazette 53048 and Commission record. All 10 gate conditions met."* |
| **0:35-0:42** | **PROVENANCE CHAIN** — Click "Provenance" → Show sources with tier badges, claims referenced | *"Every sentence traces to a source. Tier 1 = Gazette. Tier 2 = Commission record. Full audit trail."* |
| **0:42-0:50** | **CONTRADICTION EXPLORER** — Click "Show all contradictions" → Show 3 contradiction cards | *"But here's what the Commission's interim reports don't highlight. Three unresolved contradictions. Mkhwanazi vs Sibiya on the dockets. Sindane's medical timeline. Mogotsi's recusal. The Evidence Room flags them automatically."* |
| **0:50-0:55** | **ARCHITECTURE FLASH** — Quick cut to architecture diagram (1 sec) → Stack footer showing "$0/month • Free-tier only" | *"Built on free-tier stack: Tinyfish search, local embeddings, SQLite, Hermes agents. Zero API costs. Open source."* |
| **0:55-1:00** | **CTA** — Evidence Room URL on screen + QR code → "Try it: madlanga-evidence.vercel.app" | *"The Evidence Room is public. Ask it anything. madlanga-evidence.vercel.app. What should I query next?"* |

---

## RECORDING TIPS

### Screen Recording Setup
- **Resolution:** 1920x1080 (horizontal) — crops well to vertical
- **Browser:** Chrome/Edge, full screen, hide bookmarks bar
- **Zoom:** 110-125% for readability
- **Cursor:** Large, high contrast (Settings → Accessibility → Cursor size)

### Recording Tools (Free)
| Tool | Platform | Command |
|------|----------|---------|
| **OBS Studio** | All | `obs` — best quality, set 60fps |
| **SimpleScreenRecorder** | Linux | `simplescreenrecorder` |
| **Kap** | macOS | `brew install kap` |
| **Xbox Game Bar** | Windows | `Win+G` |

### Voiceover
- **Mic:** Any decent USB mic or phone voice memo (sync in edit)
- **Pacing:** 150-160 words/minute
- **Tone:** Urgent but not frantic. "Here's the thing" energy.
- **Record separately:** Cleaner than live narration

### Editing (Free)
| Tool | Platform |
|------|----------|
| **DaVinci Resolve** | All (pro-grade, free) |
| **CapCut Desktop** | All (easy, templates) |
| **Kdenlive** | Linux |
| **iMovie** | macOS |

### Export Settings for X
- **Format:** MP4 (H.264)
- **Resolution:** 1080x1920 (vertical) or 1920x1080 (horizontal)
- **Frame rate:** 30 or 60 fps
- **Bitrate:** 8-12 Mbps
- **Max file:** 512MB (X limit)
- **Duration:** Exactly 60s (X cuts at 2:20 but 60s loops better)

---

## QUICK RECORDING CHECKLIST

```
[ ] Browser: madlanga-evidence.vercel.app loaded, logged out (fresh view)
[ ] Browser zoom: 125%
[ ] Cursor: Large, visible
[ ] Mic: Tested, no background noise
[ ] OBS: 1920x1080 @ 60fps, correct audio input
[ ] Script: Printed or on second screen
[ ] Do 2-3 takes, pick best
[ ] Edit: Cut dead air, speed up typing (2x), add zoom-ins
[ ] Add: Subtitles (critical — 80% watch muted)
[ ] Export: Vertical 1080x1920 for X
[ ] Thumbnail: Custom (split screen R147M vs $0)
```

---

## THUMBNAIL DESIGN (for X video preview)

**Text overlay on split screen:**
```
LEFT (red bg):          RIGHT (green bg):
R147,000,000            $0
SPENT                   COST
MADLANGA                EVIDENCE
COMMISSION              ROOM
```

**Small text bottom:** "madlanga-evidence.vercel.app"

---

## POSTING STRATEGY

| When | What |
|------|------|
| **T+0** | Post video natively to X (not YouTube link) |
| **T+0** | Reply to own tweet with thread (see DAY 1 thread in 7_DAY_VIRAL_PLAN.md) |
| **T+5min** | Quote-tweet with "Thread 🧵" for algorithm |
| **T+30min** | Reply to top comments with finding cards |
| **T+1hr** | Retweet best quote tweets |
| **T+2hr** | Post finding card for "Show me all contradictions" |

---

## BACKUP QUERIES (if main ones fail)

| Query | Expected Result |
|-------|-----------------|
| "What is the budget spent so far?" | FINDING PASS (R147M, Tier 1) |
| "Show me all contradictions" | 3 contradiction cards |
| "What evidence exists for political interference?" | Analysis with sources |
| "Who is Judge Madlanga?" | FINDING PASS (Chairperson) |

---

## FILES READY FOR VIDEO

| Asset | Path |
|-------|------|
| Evidence Room (live) | https://madlanga-commission-architecture.vercel.app |
| Finding Card 1 (Mkhwanazi FAIL) | `finding_cards/finding_card_1.png` |
| Finding Card 2 (Established PASS) | `finding_cards/finding_card_2.png` |
| Finding Card 3 (Contradictions) | `finding_cards/finding_card_3.png` |
| Architecture Diagram | `architecture_diagram.png` |
| 7-Day Plan | `7_DAY_VIRAL_PLAN.md` |

---

**READY TO RECORD.** Open the Evidence Room, hit record, follow the script. Two takes max — ship it.