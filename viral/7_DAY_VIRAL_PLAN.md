# 7-DAY VIRAL X (TWITTER) EXECUTION PLAN
## Madlanga Commission Evidence Room — "Free Tool Beats R147M Commission"

---

## THE VIRAL HOOK
> **"South Africa spent R147M on a commission. I built a free tool that does their evidence analysis in minutes. Here's the public Evidence Room where YOU can query the Madlanga Commission yourself..."**

---

## DAY 1 (TODAY): DEPLOY & RECORD
**Goal:** Public Evidence Room live + 60-second demo video

### Deliverables
- [ ] Deploy `evidence_room.html` to Vercel → `madlanga-evidence.vercel.app`
- [ ] Record 60-second screen recording:
  1. Open Evidence Room
  2. Type: "What did Mkhwanazi claim about the 121 dockets?"
  3. Show: **NO FINDING** gate result (1 source, contradiction)
  4. Type: "When was the commission established?"
  5. Show: **FINDING** with 2 PRIMARY sources
  6. Show: Contradiction explorer, provenance chain
- [ ] Export as MP4 + GIF (first 10 seconds)
- [ ] Upload video natively to X (not YouTube link)

### Tweet Thread (Draft)
```
1/ South Africa spent R147 million on the Madlanga Commission. 
178 hearing days. 26,000 transcript pages. 10 evidence leaders.

I built a free tool that ingests their evidence and runs a 10-condition "Finding Gate" in seconds.

Here's the public Evidence Room where anyone can query it: [link]

[VIDEO/GIF]

2/ The commission takes 6 months for an interim report.
My tool cross-references Mkhwanazi's 113,000-character witness statement against all sources in 3 minutes.

It found: Only 1 source supports the "121 dockets removed" claim. A contradiction exists. Gate = FAIL.

[SCREENSHOT: Gate FAIL with reasons]

3/ But for the commission's establishment? 
Gazette 53048 + Commission record = 2 PRIMARY sources. Gate = PASS.

Every answer shows: sources with tier ratings, contradictions, evidence gaps, full provenance chain.

[SCREENSHOT: Gate PASS with sources]

4/ This runs on free-tier stack: Tinyfish search, local embeddings, SQLite, Hermes agents.
Zero API costs. Zero hallucination (gate enforces "insufficient evidence").

The Evidence Room is live. Try it: [link]

Ask: "Show me all contradictions" or "What evidence exists for political interference?"
```

### Tags for Reach
`@MadlangaCommission @PresidencyZA @DailyMaverick @News24 @IOL @GroundUp_News @TechCentral @ITWeb @BarSA @LSSA_Official @JusticeDeptSA #MadlangaCommission #LegalTech #SouthAfrica`

---

## DAY 2: CONTRAST THREAD
**Goal:** "Commission vs Free Tool" comparison that infuriates/inspires

### Content
**Thread: "R147M vs $0 — Same Evidence, Different Results"**

| Commission Process | Free Tool |
|-------------------|-----------|
| 6 months for interim report | 3 minutes for gate-checked finding |
| Manual contradiction hunting | Automated cross-reference |
| Narrative findings (no audit trail) | Every sentence has `[source_id]` |
| Facebook updates for public | Interactive Evidence Room |
| "Trust us" | "Verify yourself" |

**Visual:** Side-by-side screenshot carousel (X supports 4 images)

**CTA:** "The Evidence Room doesn't replace the Commission. It forces transparency. Try finding a contradiction they missed: [link]"

### Target Replies
- Tag journalists who covered Commission delays
- Reply to @DailyMaverick @GroundUp_News threads about Commission
- Quote-tweet IOL article on R147M budget

---

## DAY 3: "ASK THE EVIDENCE" CAMPAIGN
**Goal:** User-generated content — people sharing their queries

### Mechanism
1. Tweet: **"What should I ask the Madlanga Commission Evidence Room? Best question gets a custom Finding Card."**
2. Retweet best questions with results
3. Create "Finding Cards" — shareable images:
   ```
   ┌─────────────────────────────────┐
   │  FINDING: PASS/FAIL             │
   │  Question: [user's question]    │
   │  Sources: s1 (Tier 1), s3 (Tier 1)│
   │  Contradictions: 0              │
   │  Evidence Gaps: 0               │
   │  [madlanga-evidence.vercel.app] │
   └─────────────────────────────────┘
   ```

### Automation Script
```python
# Generate finding card image for any query
# Post as reply with image
```

### Target: 50+ quoted tweets with custom finding cards

---

## DAY 4: EXPOSE THE CONTRADICTIONS
**Goal:** "What the Commission Didn't Resolve" — controversy drives virality

### Content
**Thread: "3 Contradictions the Madlanga Commission Evidence Room Found That Are Still Unresolved"**

1. **Mkhwanazi vs Sibiya on 121 dockets** — Direct testimony conflict
2. **Sindane medical urgency** — Documentary vs oral timeline mismatch  
3. **Mogotsi recusal** — Procedural contradiction

**Each gets:** Screenshot from Evidence Room + source links

**Kicker:** "The Commission's interim reports don't mention these. The Evidence Room flags them automatically. Gate = FAIL until resolved."

**Tag:** `@AdvMkhwebane @PublicProtector @HelenSuzmanFound @OUTASA @CorruptionWatch`

---

## DAY 5: "BUILD IN PUBLIC" — TECHNICAL DEEP DIVE
**Goal:** Dev/legal-tech credibility + "how it works" shareability

### Content
**Thread: "How I Built a Zero-Hallucination Legal AI on Free Tier"**

1. **Architecture:** 7 Hermes agents → 12-step workflow → 10-condition Finding Gate
2. **The Gate:** 10 conditions that MUST pass (2+ Tier 1-4 sources, no contradictions, etc.)
3. **Stack:** Tinyfish (search) + sentence-transformers (embeddings) + SQLite + Vercel
4. **Cost:** $0/month. No OpenAI. No Anthropic.
5. **Code:** Open source at github.com/buttercode101/Madlanga-

**Visual:** Architecture diagram (Excalidraw/mermaid)

**CTA:** "Steal this architecture for your inquiry. Deploy in 1 hour: [repo link]"

### Target: Legal tech Twitter, AI Twitter, SA dev Twitter

---

## DAY 6: JOURNALIST/INFLUENCER AMPLIFICATION
**Goal:** Get picked up by media

### Outreach List (DM/Email/Reply)
| Target | Angle |
|--------|-------|
| **Karyn Maughan** (News24 legal) | "Tool that fact-checks Commission testimony in real-time" |
| **Mandy Wiener** (Daily Maverick) | "Public can now cross-examine Commission evidence themselves" |
| **Ferial Haffajee** | "R147M commission vs free tool — what does it say about state capacity?" |
| **TechCentral / ITWeb / MyBroadband** | "SA dev builds legal AI on free tier" |
| **Legal Tech SA newsletter** | "Open source evidence management for commissions" |
| **@TechWithTim @FireshipDev** (if relevant) | "Zero-hallucination AI architecture" |

### Press Kit (One-Pager)
- One-page PDF: Problem, Solution, Evidence Room link, Architecture, Contact
- Pre-written tweet for them to copy-paste

---

## DAY 7: THE "COMMISSION STARTER KIT" LAUNCH
**Goal:** Convert attention → adoption signal

### Content
**Thread: "Every Commission of Inquiry Needs This. Here's the Starter Kit."**

1. **Problem:** 40+ commissions globally use manual processes
2. **Solution:** Deploy Madlanga-grade evidence system in 1 day
3. **Kit includes:** Evidence Room, Ingestion Pipeline, Finding Gate, Profiles
4. **Deploy command:** `git clone && vercel --prod`
5. **Cost:** $0/month (free-tier)

**Visual:** Deploy button screenshot + live demo of fresh deploy

**CTA:** "If you run a commission, inquiry, or investigation — fork this. 
If you're a journalist — use the Evidence Room.
If you're a dev — contribute.

Repo: github.com/buttercode101/Madlanga-
Live: madlanga-evidence.vercel.app"

---

## VIRAL ASSETS TO CREATE (Days 1-2)

| Asset | Format | Use |
|-------|--------|-----|
| **Demo Video** | 60s MP4 + 10s GIF | Day 1 main tweet |
| **Gate PASS/FAIL Screenshots** | 1080x1080 PNG | Thread images |
| **Contradiction Cards** | 1080x1080 PNG | Day 4 thread |
| **Finding Card Template** | Auto-generated PNG | Day 3 UGC |
| **Architecture Diagram** | Excalidraw PNG | Day 5 thread |
| **Side-by-Side Comparison** | 4-image carousel | Day 2 thread |
| **Deploy Demo GIF** | 15s loop | Day 7 thread |

---

## X ALGORITHM OPTIMIZATION

| Tactic | Implementation |
|--------|----------------|
| **Native video** | Upload MP4 directly (not YouTube) |
| **Thread format** | 5-7 tweets, each with image/video |
| **First reply** | Pin your own thread with link |
| **Quote tweets** | Quote journalists' Commission coverage |
| **Tag strategically** | 3-5 relevant accounts per tweet |
| **Post timing** | 7-9 AM SAST (commuter), 7-9 PM SAST (evening) |
| **Engagement bait** | "What should I ask next?" polls |
| **Retweet bait** | "Retweet if you want this for [your country's] commission" |

---

## SUCCESS METRICS (7 Days)

| Metric | Target |
|--------|--------|
| **Impressions** | 500K+ |
| **Profile visits** | 10K+ |
| **Evidence Room visits** | 5K+ unique |
| **GitHub stars** | 100+ |
| **Media mentions** | 3+ (Daily Maverick, TechCentral, legal blog) |
| **Inbound from commissions** | 5+ serious inquiries |

---

## RISK MITIGATION

| Risk | Mitigation |
|------|------------|
| **Commission objects** | Frame as "public transparency tool," not replacement. Disclaimer prominent. |
| **Legal threat** | All sources public. Tool only analyzes public records. No legal advice given. |
| **Technical failure** | Vercel auto-scales. Static HTML = zero backend failure. |
| **Bad faith queries** | Gate returns "insufficient evidence" — can't be gamed. |
| **POPIA/Privacy** | Only public sources ingested. No personal data processed. |

---

## DAILY CHECKLIST

```
[ ] Morning: Post main thread (7-9 AM SAST)
[ ] 30 min: Reply to every comment/quote tweet
[ ] 1 hr: DM 10 relevant accounts with personalized pitch
[ ] 2 hr: Monitor searches for "Madlanga Commission" — reply to top tweets
[ ] Evening: Post follow-up/engagement tweet (7-9 PM SAST)
[ ] Night: Prep next day's assets
```

---

## THE ONE METRIC THAT MATTERS

**Evidence Room unique visitors → Commission secretariat inbound emails**

Everything else is vanity. If 3 commission secretariats email "how do we deploy this?" — viral worked.

---

**START NOW:** Deploy Evidence Room → Record Video → Tweet Thread 1