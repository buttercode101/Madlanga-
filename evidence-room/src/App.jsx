import React, { useState, useEffect } from 'react'

const tierLabels = {
  "PRIMARY": "Tier 1 — Primary Official",
  "PUBLIC RECORD ARCHIVE": "Tier 2 — Commission Record",
  "SWORN TESTIMONY": "Tier 3 — Sworn Testimony",
  "DOCUMENTARY VERIFIED": "Tier 4 — Documentary Verified",
  "MEDIA CORROBORATED": "Tier 5 — Media Corroborated",
  "UNVERIFIED": "Tier 6 — Unverified"
}

const quickQueries = [
  { label: "Establishment", query: "When was the commission established?" },
  { label: "Mkhwanazi dockets", query: "What did Mkhwanazi claim about the 121 dockets?" },
  { label: "Chairperson", query: "Who is Judge Madlanga?" },
  { label: "Contradictions", query: "Show me all contradictions" },
  { label: "Political interference", query: "What evidence exists for political interference?" },
  { label: "Budget R147M", query: "What is the budget spent so far?" }
]

async function fetchSearch(query) {
  const res = await fetch(`/api/search?q=${encodeURIComponent(query)}`)
  if (!res.ok) throw new Error('Search failed')
  return res.json()
}

async function fetchClaim(claimId) {
  const res = await fetch(`/api/claim/${claimId}`)
  if (!res.ok) throw new Error('Claim fetch failed')
  return res.json()
}

async function fetchContradictions() {
  const res = await fetch('/api/contradictions')
  if (!res.ok) throw new Error('Contradictions fetch failed')
  return res.json()
}

function App() {
  const [query, setQuery] = useState('')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)
  const [marqueeText, setMarqueeText] = useState('')

  useEffect(() => {
    const texts = [
      '40 HEARING DAYS INGESTED • 420K TRANSCRIPT CHARACTERS • 29 WITNESS DOCUMENTS • ZERO HALLUCINATION GUARANTEE',
      'FINDING GATE: 10 CONDITIONS • 2+ TIER 1-4 SOURCES • NO UNRESOLVED CONTRADICTIONS • CHAIN OF CUSTODY VERIFIED',
      'R147M COMMISSION BUDGET • FREE-TOOL ALTERNATIVE • PUBLIC EVIDENCE ROOM • OPEN SOURCE • LOOPII BUSINESS SERVICES'
    ]
    setMarqueeText(texts.join('  •  '))
  }, [])

  const handleSearch = async (q) => {
    setQuery(q)
    setLoading(true)
    try {
      // First search for relevant claims
      const searchResult = await fetchSearch(q)
      const claims = searchResult.claims || []
      
      if (claims.length === 0) {
        setResult({
          answer: "I don't have sufficient sourced evidence to answer that.",
          gate: { pass: false, reasons: ['No matching claims found'], sources_used: [], contradictions: [], gaps: [] },
          provenance: { sources_used: [], claims_referenced: [], documents: [], exhibits: [] },
          contradictions: [],
          evidence_gaps: []
        })
        setLoading(false)
        return
      }
      
      // Fetch detailed claim info for the top claim
      const claimId = claims[0]
      const claimDetail = await fetchClaim(claimId)
      const contradictions = await fetchContradictions()
      
      // Build response
      const gate = claimDetail.gate || { pass: false, reasons: [] }
      const claimSources = claimDetail.claim?.sources || []
      
      let answer = ''
      if (gate.pass) {
        answer = `FINDING: ${claimDetail.claim?.statement || 'Claim established'}. — Sources: ${claimSources.join(', ')}`
      } else {
        const reasons = gate.reasons || ['Insufficient evidence']
        const contras = claimDetail.contradictions || []
        answer = `NO FINDING: ${reasons.join('; ')}. Contradictions: ${contras.join(', ')}`
      }
      
      setResult({
        answer,
        gate: {
          pass: gate.pass,
          reasons: reasons,
          sources_used: searchResult.sources,
          contradictions: claimDetail.contradictions || [],
          gaps: gate.gaps || []
        },
        provenance: {
          sources_used: searchResult.sources,
          claims_referenced: [claimId],
          documents: searchResult.documents,
          exhibits: []
        },
        contradictions: contradictions.contradictions || [],
        evidence_gaps: gate.gaps || []
      })
    } catch (err) {
      console.error('Search error:', err)
      setResult({
        answer: "Error retrieving evidence. Please try again.",
        gate: { pass: false, reasons: [err.message], sources_used: [], contradictions: [], gaps: [] },
        provenance: { sources_used: [], claims_referenced: [], documents: [], exhibits: [] },
        contradictions: [],
        evidence_gaps: []
      })
    }
    setLoading(false)
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    if (query.trim()) handleSearch(query.trim())
  }

  const clearResult = () => {
    setResult(null)
    setQuery('')
  }

  if (!result) {
    return <LandingPage onQuickQuery={handleSearch} marqueeText={marqueeText} mobileMenuOpen={mobileMenuOpen} setMobileMenuOpen={setMobileMenuOpen} />
  }

  return (
    <ResultPage
      query={query}
      result={result}
      loading={loading}
      onSearch={handleSearch}
      onClear={clearResult}
      marqueeText={marqueeText}
      mobileMenuOpen={mobileMenuOpen}
      setMobileMenuOpen={setMobileMenuOpen}
    />
  )
}

function LandingPage({ onQuickQuery, marqueeText, mobileMenuOpen, setMobileMenuOpen }) {
  return (
    <div className="min-h-screen bg-[#FFFEFB] font-sans">
      <Header mobileMenuOpen={mobileMenuOpen} setMobileMenuOpen={setMobileMenuOpen} />
      
      <MarqueeBar text={marqueeText} />
      
      <main className="max-w-[1320px] mx-auto px-4 md:px-6 py-12 md:py-20">
        <HeroSection />
        
        <SearchSection onQuickQuery={onQuickQuery} />
        
        <StatsBar />
        
        <HowItWorks />
      </main>
      
      <Footer />
    </div>
  )
}

function Header({ mobileMenuOpen, setMobileMenuOpen }) {
  return (
    <header className="sticky top-0 z-40 bg-[#FFFEFB] border-b border-black">
      <div className="border-b border-black">
        <div className="max-w-[1320px] mx-auto px-4 md:px-6 h-[52px] flex items-center justify-between gap-3">
          <div className="flex items-center gap-3 min-w-0">
            <div className="w-[3px] self-stretch bg-black hidden md:block" />
            <div className="min-w-0">
              <div className="font-mono text-[10px] md:text-[11px] tracking-[0.18em] font-bold leading-none truncate">
                MADLANGA COMMISSION / EVIDENCE ROOM
              </div>
              <div className="font-sans text-[11px] md:text-[12px] tracking-[0.01em] opacity-60 truncate mt-[2px]">
                JUDICIAL COMMISSION OF INQUIRY — CRIMINAL JUSTICE SYSTEM • PUBLIC BETA v2
              </div>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <a href="https://www.gov.za" target="_blank" rel="noopener" className="hidden md:inline-flex font-mono text-[11px] tracking-wide border border-black px-3 py-[6px] hover:bg-black hover:text-white transition-colors focus-ring min-h-[36px] items-center">
              Official Site ↗
            </a>
            <a href="https://github.com/buttercode101/Madlanga-" target="_blank" rel="noopener" className="hidden md:inline-flex font-mono text-[11px] tracking-wide bg-black text-white px-3 py-[6px] border border-black hover:bg-white hover:text-black transition-colors focus-ring min-h-[36px] items-center">
              GitHub ↗
            </a>
            <button
              aria-label="Open menu"
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="md:hidden border border-black w-[44px] h-[44px] flex items-center justify-center focus-ring"
            >
              <div className="space-y-[4px]">
                <div className="w-5 h-[2px] bg-black" />
                <div className="w-5 h-[2px] bg-black" />
                <div className="w-5 h-[2px] bg-black" />
              </div>
            </button>
          </div>
        </div>
      </div>
    </header>
  )
}

function MarqueeBar({ text }) {
  return (
    <div className="h-[28px] bg-black text-white overflow-hidden relative flex items-center w-full max-w-full">
      <div className="w-full overflow-hidden">
        <div className="marquee whitespace-nowrap flex items-center gap-8 text-[11px] md:text-[12px] tracking-wide font-mono uppercase">
          {text.split('  •  ').flatMap((t, i) => [
            <span key={i}>{t}</span>,
            <span key={`sep-${i}`} className="opacity-40">◆</span>
          ])}
        </div>
      </div>
    </div>
  )
}

function HeroSection() {
  return (
    <div className="paper relative overflow-hidden rounded-[12px] border border-black p-6 md:p-10 mb-12">
      <div className="absolute inset-0 bg-gradient-to-br from-[#FDE047]/10 to-transparent" />
      <div className="relative z-10 max-w-3xl">
        <div className="font-mono text-[11px] md:text-[12px] tracking-[0.15em] font-bold mb-4 text-black/60">
          R147M COMMISSION • $0 TOOL • SAME EVIDENCE
        </div>
        <h1 className="font-serif text-4xl md:text-5xl lg:text-6xl font-extrabold leading-[1.05] tracking-tight text-black mb-6">
          Query the Evidence.<br />
          <span className="text-[#DC2626]">Verify the Findings.</span>
        </h1>
        <p className="font-serif-body text-lg md:text-xl text-black/70 leading-relaxed mb-8 max-w-xl">
          South Africa spent R147 million on the Madlanga Commission. This free tool ingests their evidence and runs a 10-condition Finding Gate in seconds. Every answer shows sources, contradictions, and evidence gaps — with zero hallucination.
        </p>
        <div className="flex flex-wrap gap-3">
          <a href="https://github.com/buttercode101/Madlanga-" target="_blank" rel="noopener" className="inline-flex items-center gap-2 font-mono text-[11px] tracking-wide bg-black text-white px-5 py-[10px] border border-black hover:bg-white hover:text-black transition-colors focus-ring min-h-[44px]">
            View Source on GitHub
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6" />
              <polyline points="15 3 21 3 21 9" />
              <line x1="10" y1="14" x2="21" y2="3" />
            </svg>
          </a>
          <a href="https://criminaljusticecommission.org.za" target="_blank" rel="noopener" className="inline-flex items-center gap-2 font-mono text-[11px] tracking-wide border border-black px-5 py-[10px] hover:bg-black hover:text-white transition-colors focus-ring min-h-[44px]">
            Official Commission Site
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6" />
              <polyline points="15 3 21 3 21 9" />
              <line x1="10" y1="14" x2="21" y2="3" />
            </svg>
          </a>
        </div>
      </div>
      <div className="absolute bottom-4 right-4 md:bottom-6 md:right-8 opacity-10">
        <div className="stamp font-serif text-2xl md:text-3xl font-extrabold border-2 border-black px-3 py-1 uppercase tracking-widest">
          PUBLIC BETA
        </div>
      </div>
    </div>
  )
}

function SearchSection({ onQuickQuery }) {
  return (
    <div className="mb-12">
      <div className="bg-white rounded-[12px] border border-black p-6 md:p-8 shadow-[4px_4px_0_0_#000]">
        <h2 className="font-serif text-2xl md:text-3xl font-extrabold mb-2">Query the Evidence</h2>
        <p className="font-sans text-black/60 mb-6 max-w-2xl">
          Ask about findings, witnesses, contradictions, or procedural history. Every answer is gate-checked with sources, tiers, and full provenance.
        </p>
        <form onSubmit={(e) => { e.preventDefault(); const q = e.currentTarget.query.value; if (q.trim()) onQuickQuery(q.trim()) }} className="mb-6">
          <div className="flex gap-3">
            <input
              name="query"
              type="text"
              placeholder="e.g., What did Mkhwanazi claim about the 121 dockets? When was the commission established? Show me all contradictions."
              className="flex-1 px-4 py-4 border-2 border-black rounded-[8px] font-sans text-base focus:outline-none focus:ring-2 focus:ring-black focus:border-transparent bg-white placeholder:text-black/30"
              autoComplete="off"
            />
            <button type="submit" className="px-8 py-4 bg-black text-white font-mono text-[11px] tracking-wide border-2 border-black hover:bg-white hover:text-black transition-colors focus-ring min-h-[52px] whitespace-nowrap">
              Search Evidence
            </button>
          </div>
        </form>
        <div className="flex flex-wrap gap-2">
          {quickQueries.map((q) => (
            <button
              key={q.label}
              type="button"
              onClick={() => onQuickQuery(q.query)}
              className="px-4 py-2 text-sm font-mono tracking-wide bg-white border border-black hover:bg-black hover:text-white transition-colors rounded-[6px]"
            >
              {q.label}
            </button>
          ))}
        </div>
      </div>
    </div>
  )
}

function StatsBar() {
  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-16">
      {[
        { label: 'HEARING DAYS', value: '40', desc: 'Ingested from official site' },
        { label: 'TRANSCRIPT CHARS', value: '420K', desc: 'Full-text searchable' },
        { label: 'WITNESS DOCS', value: '29', desc: 'Profiles & testimony' },
        { label: 'GATE CONDITIONS', value: '10', desc: 'Zero-hallucination guarantee' }
      ].map((stat, i) => (
        <div key={i} className="paper border border-black rounded-[12px] p-6 text-center">
          <div className="font-serif text-4xl md:text-5xl font-extrabold text-black">{stat.value}</div>
          <div className="font-mono text-[10px] tracking-[0.15em] uppercase text-black/60 mt-1">{stat.label}</div>
          <div className="font-sans text-[11px] text-black/40 mt-2">{stat.desc}</div>
        </div>
      ))}
    </div>
  )
}

function HowItWorks() {
  const steps = [
    { num: '01', title: 'INGEST', desc: 'Tinyfish searches official Commission site + news. 40 hearing days, 29 witness profiles auto-fetched.' },
    { num: '02', title: 'CLASSIFY', desc: 'Sentence-transformers embeddings map your question to canonical Claim IDs (C-001 to C-005).' },
    { num: '03', title: 'ORCHESTRATE', desc: '12-step workflow: Evidence → Chronology → Network → Contradiction → Verification → Red Team → Gate.' },
    { num: '04', title: 'GATE', desc: '10 conditions checked. 2+ Tier 1-4 sources? No contradictions? Custody verified? PASS = Finding. FAIL = No Finding.' },
    { num: '05', title: 'OUTPUT', desc: 'Finding Card with sources, tiers, contradictions, gaps, full provenance chain. Every sentence traces to [source_id].' }
  ]

  return (
    <section className="mb-16">
      <h2 className="font-serif text-3xl md:text-4xl font-extrabold mb-10 text-center">How It Works</h2>
      <div className="space-y-4">
        {steps.map((step, i) => (
          <div key={i} className="paper border border-black rounded-[12px] p-6 md:p-8 flex flex-col md:flex-row gap-6 items-start md:items-center">
            <div className="font-serif text-3xl md:text-4xl font-extrabold text-black/20 flex-shrink-0 w-[80px] text-right pr-4 border-r border-black/10">
              {step.num}
            </div>
            <div className="flex-1">
              <h3 className="font-serif text-xl md:text-2xl font-extrabold mb-2">{step.title}</h3>
              <p className="font-sans text-black/70 leading-relaxed">{step.desc}</p>
            </div>
          </div>
        ))}
      </div>
    </section>
  )
}

function Footer() {
  return (
    <footer className="bg-[#FFFEFB] border-t border-black mt-12">
      <div className="max-w-[1320px] mx-auto px-4 md:px-6 py-8 md:py-12">
        <div className="flex flex-col md:flex-row items-center justify-between gap-6">
          <div className="flex flex-col items-start md:items-center text-center md:text-left">
            <div className="font-mono text-[10px] tracking-[0.18em] font-bold mb-2">MADLANGA COMMISSION / EVIDENCE ROOM</div>
            <div className="font-sans text-[11px] text-black/50">Judicial Commission of Inquiry — Criminal Justice System</div>
          </div>
          <div className="flex flex-wrap items-center justify-center gap-4 text-sm font-mono tracking-wide text-black/60">
            <a href="https://github.com/buttercode101/Madlanga-" target="_blank" rel="noopener" className="hover:text-black">GitHub</a>
            <a href="https://criminaljusticecommission.org.za" target="_blank" rel="noopener" className="hover:text-black">Official Site</a>
            <span>Loopii Business Services</span>
            <span>Free-tier Stack</span>
            <span>Zero Hallucination</span>
          </div>
          <div className="font-sans text-[11px] text-black/40 text-center md:text-right">
            <p>Built with evidence-first architecture</p>
            <p className="mt-1">Tinyfish • sentence-transformers • SQLite • Hermes • Vercel</p>
            <p className="mt-1">$0/month • Open Source • No API Keys Required</p>
          </div>
        </div>
        <div className="mt-8 pt-8 border-t border-black/10 flex flex-col md:flex-row items-center justify-between gap-4">
          <p className="font-sans text-[11px] text-black/40">
            <strong>Disclaimer:</strong> Independent evidence analysis tool. All persons presumed innocent until convicted. 
            Findings require 2+ Tier 1-4 sources, no unresolved contradictions. Not affiliated with the official Commission.
          </p>
        </div>
      </div>
    </footer>
  )
}

function ResultPage({ query, result, loading, onSearch, onClear, marqueeText, mobileMenuOpen, setMobileMenuOpen }) {
  const gate = result.gate
  const provenance = result.provenance
  const contradictions = result.contradictions
  const gaps = result.evidence_gaps
  const isFinding = result.answer.startsWith('FINDING:')
  const isNoFinding = result.answer.startsWith('NO FINDING:')

  return (
    <div className="min-h-screen bg-[#FFFEFB] font-sans">
      <Header mobileMenuOpen={mobileMenuOpen} setMobileMenuOpen={setMobileMenuOpen} />
      <MarqueeBar text={marqueeText} />
      
      <main className="max-w-[1320px] mx-auto px-4 md:px-6 py-8 md:py-12">
        {/* Query Bar */}
        <div className="paper border border-black rounded-[12px] p-6 mb-8 shadow-[4px_4px_0_0_#000]">
          <div className="flex flex-col md:flex-row gap-4 items-start md:items-center justify-between mb-4">
            <div className="flex-1">
              <div className="font-mono text-[10px] tracking-[0.15em] font-bold text-black/60 mb-1">YOUR QUERY</div>
              <div className="font-serif-body text-lg md:text-xl text-black">{query}</div>
            </div>
            <button
              onClick={onClear}
              className="px-4 py-2 font-mono text-[11px] tracking-wide border border-black hover:bg-black hover:text-white transition-colors focus-ring min-h-[40px] whitespace-nowrap flex-shrink-0"
            >
              New Search
            </button>
          </div>
          <div className="flex flex-wrap gap-2">
            {quickQueries.map((q) => (
              <button
                key={q.label}
                type="button"
                onClick={() => onSearch(q.query)}
                className="px-4 py-2 text-sm font-mono tracking-wide bg-white border border-black hover:bg-black hover:text-white transition-colors rounded-[6px]"
              >
                {q.label}
              </button>
            ))}
          </div>
        </div>

        {/* Gate Result */}
        <GateCard gate={gate} isFinding={isFinding} isNoFinding={isNoFinding} answer={result.answer} />

        {/* Provenance */}
        <ProvenanceCard provenance={provenance} />

        {/* Contradictions */}
        {contradictions && contradictions.length > 0 && (
          <ContradictionsCard contradictions={contradictions} />
        )}

        {/* Evidence Gaps */}
        {gaps && gaps.length > 0 && (
          <GapsCard gaps={gaps} />
        )}

        {/* Disclaimer */}
        <div className="mt-12 p-6 paper border border-black rounded-[12px] hazard">
          <p className="font-sans text-[12px] text-black/70 leading-relaxed">
            <strong className="font-mono">DISCLAIMER:</strong> This is an independent evidence analysis tool. All persons named in claims are presumed innocent until convicted by a competent court. 
            Findings require minimum 2 independent Tier 1-4 sources with no unresolved contradictions. 
            This tool does not represent the official Madlanga Commission.
          </p>
        </div>
      </main>
      
      <Footer />
    </div>
  )
}

function GateCard({ gate, isFinding, isNoFinding, answer }) {
  return (
    <div className={`paper border-2 rounded-[12px] p-6 md:p-8 mb-8 ${gate.pass ? 'border-[#16A34A] bg-[#F0FDF4]' : 'border-[#DC2626] bg-[#FEF2F2]'}`}>
      <div className="flex flex-col md:flex-row gap-6 items-start md:items-center justify-between mb-6">
        <div className="flex items-center gap-4">
          <div className={`stamp px-4 py-2 font-mono text-[11px] md:text-[12px] tracking-[0.15em] font-bold border-2 border-black ${gate.pass ? '' : 'stamp-fail'}`}>
            {gate.pass ? 'GATE: PASS ✅' : 'GATE: FAIL ❌'}
          </div>
          {gate.reasons.length > 0 && (
            <div className="font-sans text-sm text-[#DC2626] max-w-md">
              {gate.reasons.map((r, i) => <div key={i} className="flex items-center gap-1">• {r}</div>)}
            </div>
          )}
        </div>
      </div>
      
      <div className={`paper border border-black rounded-[8px] p-6 ${gate.pass ? 'border-[#16A34A]/30' : 'border-[#DC2626]/30'}`}>
        <div className="font-mono text-[10px] tracking-[0.15em] font-bold text-black/60 mb-3">
          {isFinding ? 'FINDING' : isNoFinding ? 'NO FINDING' : 'ANALYSIS'}
        </div>
        <div className="font-serif-body text-base md:text-lg leading-relaxed text-black whitespace-pre-wrap">
          {answer}
        </div>
      </div>
    </div>
  )
}

function ProvenanceCard({ provenance }) {
  const sources = provenance.sources_used || []
  const claims = provenance.claims_referenced || []
  const docs = provenance.documents || []
  const exhibits = provenance.exhibits || []

  if (sources.length === 0 && claims.length === 0 && docs.length === 0 && exhibits.length === 0) {
    return null
  }

  return (
    <div className="paper border border-black rounded-[12px] p-6 md:p-8 mb-8">
      <div className="font-serif text-xl md:text-2xl font-extrabold mb-6 flex items-center gap-3">
        <div className="w-[3px] h-8 bg-black" />
        PROVENANCE CHAIN
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <ProvenanceSection title="SOURCES" count={sources.length}>
          {sources.map((s, i) => (
            <SourceBadge key={i} source={s} />
          ))}
        </ProvenanceSection>
        <ProvenanceSection title="CLAIMS" count={claims.length}>
          {claims.map((c, i) => (
            <ClaimBadge key={i} claim={c} />
          ))}
        </ProvenanceSection>
        <ProvenanceSection title="DOCUMENTS" count={docs.length}>
          {docs.map((d, i) => (
            <DocBadge key={i} doc={d} />
          ))}
        </ProvenanceSection>
        <ProvenanceSection title="EXHIBITS" count={exhibits.length}>
          {exhibits.map((e, i) => (
            <ExhibitBadge key={i} exhibit={e} />
          ))}
        </ProvenanceSection>
      </div>
    </div>
  )
}

function ProvenanceSection({ title, count, children }) {
  return (
    <div className="space-y-3">
      <div className="flex items-center justify-between">
        <div className="font-mono text-[10px] tracking-[0.15em] font-bold text-black/60">{title}</div>
        <div className="font-mono text-[12px] font-bold bg-black text-white px-2 py-[2px] rounded-[4px] min-w-[28px] text-center">{count}</div>
      </div>
      <div className="space-y-2">{children}</div>
    </div>
  )
}

function SourceBadge({ source }) {
  const tier = source.tier || 'UNVERIFIED'
  const tierColors = {
    "PRIMARY": "bg-[#FEF3C7] text-[#92400E] border-[#F59E0B]",
    "PUBLIC RECORD ARCHIVE": "bg-[#DBEAFE] text-[#1E40AF] border-[#3B82F6]",
    "SWORN TESTIMONY": "bg-[#E0E7FF] text-[#3730A3] border-[#6366F1]",
    "DOCUMENTARY VERIFIED": "bg-[#FCE7F3] text-[#9D174D] border-[#EC4899]",
    "MEDIA CORROBORATED": "bg-[#F3F4F6] text-[#374151] border-[#9CA3AF]",
    "UNVERIFIED": "bg-[#FEE2E2] text-[#991B1B] border-[#EF4444]"
  }
  const colorClass = tierColors[tier] || tierColors["UNVERIFIED"]
  
  return (
    <div className="flex items-center gap-3 p-3 paper border border-black/20 rounded-[8px]">
      <div className="font-mono text-[11px] font-bold px-2 py-1 rounded-[4px] border {colorClass.replace('bg-', 'border-').replace('text-', '')} min-w-[32px] text-center">
        {source.id}
      </div>
      <div className={`font-mono text-[10px] tracking-[0.1em] px-2 py-1 rounded-[4px] ${colorClass}`}>
        {tierLabels[tier] || tier}
      </div>
    </div>
  )
}

function ClaimBadge({ claim }) {
  return (
    <div className="font-mono text-[11px] font-bold px-3 py-2 paper border border-black/20 rounded-[6px] bg-white">
      {claim}
    </div>
  )
}

function DocBadge({ doc }) {
  return (
    <div className="font-mono text-[11px] px-3 py-2 paper border border-black/20 rounded-[6px] bg-white text-black/70">
      {doc}
    </div>
  )
}

function ExhibitBadge({ exhibit }) {
  return (
    <div className="font-mono text-[11px] px-3 py-2 paper border border-black/20 rounded-[6px] bg-white text-black/70">
      {exhibit}
    </div>
  )
}

function ContradictionsCard({ contradictions }) {
  return (
    <div className="paper border-2 border-[#DC2626] rounded-[12px] p-6 md:p-8 mb-8 hazard">
      <div className="font-serif text-xl md:text-2xl font-extrabold mb-6 flex items-center gap-3 text-[#DC2626]">
        <div className="w-[3px] h-8 bg-[#DC2626]" />
        CONTRADICTIONS ({contradictions.length})
      </div>
      <div className="space-y-3">
        {contradictions.map((c, i) => (
          <div key={i} className="paper border border-[#DC2626]/30 rounded-[8px] p-4 relative">
            <div className="font-mono text-[11px] text-[#DC2626] mb-1">{c}</div>
            <div className="font-sans text-sm text-black/60">
              Unresolved contradiction blocking Finding Gate. Requires additional evidence or witness clarification.
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

function GapsCard({ gaps }) {
  return (
    <div className="paper border-2 border-[#F59E0B] rounded-[12px] p-6 md:p-8 mb-8">
      <div className="font-serif text-xl md:text-2xl font-extrabold mb-6 flex items-center gap-3 text-[#F59E0B]">
        <div className="w-[3px] h-8 bg-[#F59E0B]" />
        EVIDENCE GAPS ({gaps.length})
      </div>
      <div className="space-y-3">
        {gaps.map((g, i) => (
          <div key={i} className="paper border border-[#F59E0B]/30 rounded-[8px] p-4">
            <div className="font-mono text-[11px] text-[#F59E0B] mb-1">{g}</div>
            <div className="font-sans text-sm text-black/60">
              Evidence gap identified. Targeted research required to close.
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

export default App