# Writing Principles

38 rules for clear, precise, data-driven writing. Apply every applicable rule when reviewing or producing a document.

When you lack the information to fix a violation, do not guess. Insert `[⚠️ NEEDS: what is needed]` so the author can fill it in. Flag rather than hallucinate.

## Structure and Purpose

1. TL;DR at the top. Open with 2-3 sentences: the key point and the ask. The reader should know why they are reading before the second paragraph.

   Match the TL;DR structure to the document type:
   - Recommendation/proposal: State the recommendation and key supporting data point. "We recommend X because Y (data)."
   - Investigation/RCA: Size the gap, state how much is explained, what is still open. "Metric dropped X%. We can explain Y%. Investigating Z%."
   - Experiment readout: Lead with the verdict and key metric impact. "Ship/Iterate/Pause: primary metric moved +X%."
   - Status update: Lead with the single most important change since last update. Save details for the body.
   - General/other: Hook (the conclusion) + problem (sized) + ask.

2. Lead with the ask. State what you need (a decision, resources, alignment) in the first paragraph. Do not bury it.
   - ❌ page 3: "Given the above, we would like approval to proceed."
   - ✅ paragraph 1: "We need VP approval by March 20 to launch the pilot."

3. Pass the "so what" test. Every section should answer: what should the reader do with this information? If a section has no answer, cut it or rewrite it.

4. Show your thinking, not your work. Present the causal chain: data → reasoning → recommendation. Move methodology, process details, and intermediate steps to an appendix.
   - ❌ "We ran 14 queries across 3 data sets and normalized for seasonality..."
   - ✅ "Retention dropped 12% QoQ (see Appendix A for methodology), which suggests the onboarding change is not working."

5. Include baseline data. Senior readers are further from details, not closer. Include the obvious numbers; what is obvious to you is new to your reader.
   - ❌ "Conversion improved significantly."
   - ✅ "Conversion rose from 2.1% to 3.4% (baseline was 2.1% in Q3 2025)."

6. State trade-offs explicitly. Present at least two perspectives. If you only show upside, the reader will distrust the analysis.

7. Include a recommendation with rationale. Do not end with an open question. State what you recommend and why.

8. Use toy examples for complex concepts. Before the real data, show a simplified example so the reader builds intuition.

## Sentence-Level Clarity

1. One idea per sentence. If a sentence has "and" or "but" joining two independent ideas, split it.

2. One argument per paragraph. Start with a topic sentence. Support it. End with a hook to the next paragraph.

3. Active voice, subject-verb-object. Name the actor.
   - ❌ "Mistakes were made in the migration."
   - ✅ "The infrastructure team introduced a bug during the migration."

4. ≤30 words per sentence. If longer, split into two. Limitations force clarity.

5. 3-4 sentences per paragraph maximum. Walls of text signal muddled thinking.

6. Cut filler words. Replace cluttered phrases with simpler ones:
   - "in order to" → "to"
   - "utilize" → "use"
   - "due to the fact that" → "because"
   - "at this point in time" → "now"
   - "leverage" → "use"
   - "facilitate" → "help"
   - "prior to" → "before"

7. Cut purposeless adverbs. "Very", "really", "significantly", "almost" — replace with a number or delete. If you do not know the number, flag it: `[⚠️ NEEDS: specific number]`.
   - ❌ "Performance improved significantly."
   - ✅ "p99 latency dropped from 450ms to 120ms."
   - If data unknown: "p99 latency dropped `[⚠️ NEEDS: from X to Y]`."

## Precision and Data

1. Replace adjectives with data. Every qualifier should be backed by a number. If the number is not in the document, flag it.
   - ❌ "Customers love Prime."
   - ✅ "Prime members spend 3x more than non-members, and we retain 90% of them year-over-year."
   - If data unknown: "Prime members spend `[⚠️ NEEDS: multiplier]` more than non-members."

2. No weasel words. "Some", "many", "often", "experts say", "studies show" (without citation) — state the number, name the expert, cite the study, or flag it.
   - ❌ "Many users experienced issues."
   - ✅ "12,400 users (8% of DAU) could not complete checkout."
   - If data unknown: "`[⚠️ NEEDS: number]` users could not complete checkout."

3. No peacock words. "Innovative", "cutting-edge", "world-class", "groundbreaking", "best-in-class" — replace with verifiable facts or flag for the author to supply them.
   - ❌ "Our innovative fraud detection system."
   - ✅ "Our fraud detection system reduced chargebacks by 34% in Q1 2026."

4. Cite every data claim. Include source, date range, and methodology. If the source is not in the document, flag it.
   - ❌ "Revenue increased 25% during the lockdown."
   - ✅ "Revenue increased 25% between Feb and Mar 2020 (source: internal data dashboards, monthly reports)."
   - If source unknown: "Revenue increased 25% between Feb and Mar 2020 `[⚠️ NEEDS: source]`."

5. Include units and currency on every number.
   - ❌ "Raised 35 million." → ✅ "Raised $35M."
   - ❌ "Latency is 120." → ✅ "p99 latency is 120ms."

## Durability and Context

1. Absolute dates. Never use relative time references. Documents outlive the moment they were written. If you cannot determine the absolute date, flag it.
   - ❌ "Next week" → ✅ "Friday, 14 Mar 2026"
   - If date unknown: "`[⚠️ NEEDS: absolute date]`"

2. Absolute references. Never use contextual references that decay. If you cannot determine the specific reference, flag it.
   - ❌ "The new office" → ✅ "The Corporate Plaza (HQ100)"
   - If reference unknown: "The `[⚠️ NEEDS: building name and office code]`"

3. Self-contained documents. Do not assume the reader attended the meeting, read the Slack thread, or knows the backstory. Provide enough context for a reader with zero prior knowledge.

4. Write for the future reader. Your document may be read in two years by someone on a different team or org. If it relies on context that will expire, it is already failing.

## Language and Terminology

1. Define every acronym on first use. No exceptions.

   Mechanical check: Scan the entire document for acronym-like sequences (3+ letters with non-standard capitalization, e.g. MKS, SIEM, IaC, PaaS, DevOps). For each occurrence, verify it is defined on first use. Common acronyms (USA, API, URL, HTML) may be left undefined if the audience is technical (check the audience flag if provided).

   All domain-specific, program-specific, and team-specific acronyms MUST be defined. This is the single most commonly missed rule: a typical program document has 10-20 undefined acronyms that the author considers obvious but the audience does not know. Flag every undeclared acronym with `[⚠️ NEEDS: define ACRONYM on first use]`.
   - ❌ "The MAU metric dropped"
   - ✅ "Monthly Active Users (MAU) dropped from 150M to 145M."
   - ❌ "The DAU metric increased after launch" `[⚠️ NEEDS: define DAU on first use]`
   - ✅ "Daily Active Users (DAU) increased from 12M to 14M after launch."

2. No jargon without plain-language explanation. If a term is domain-specific, explain it in one sentence.

3. Consistent terminology. Use the same word for the same thing throughout. Do not cycle synonyms ("the platform", "the tool", "the system", "the product"); it creates ambiguity about whether these are the same thing or different.

4. Action-oriented headers. Headers should tell the reader what the section accomplishes, not just label it.
   - ❌ "Background" → ✅ "Why This Problem Matters Now"
   - ❌ "Details" → ✅ "How the Proposed Solution Works"
   - ❌ "Next Steps" → ✅ "Three Actions Needed by March 20"

## Anti-Patterns

1. No filler openers. Delete any sentence that could start any document on any topic.
   - ❌ "In today's fast-paced world..."
   - ❌ "It's important to note that..."
   - ❌ "As we continue to evolve..."

2. No false profundity. Dramatic one-liners that sound deep but say nothing.
   - ❌ "Everything changed." → State what changed, with data.
   - ❌ "And then it hit me." → State the insight directly.

3. No AI-tell vocabulary. These words are overused by language models and signal unedited output.

   Creative/narrative tells — replace with plain alternatives:
   "delve" → examine; "tapestry" → mix; "leverage" → use; "foster" → encourage; "garner" → earn; "showcase" → show; "underscore" → emphasize; "landscape" → field; "paradigm" → model; "synergy" → cooperation (or state the specific benefit).

   Critical analysis tells — words LLMs overuse when trying to sound rigorous. State the specific thing the word gestures at, or delete. Do not replace with another vague qualifier.
   "honest/honestly" → delete (analysis that labels itself honest isn't demonstrating it); "nuanced" → state the specific distinction; "robust" → cite the specific data or evidence, or delete; "indeed" → delete (filler); "notably" → delete (just state the thing); "crucial" → state why it matters, or delete; "comprehensive" → state what's actually covered; "holistic" → state what's included; "thoughtful" → delete (thoughtfulness is demonstrated, not labeled).

1. No em-dashes. Any em-dashes in a paragraph signals unedited output. Rewrite as separate sentences, or use commas and parentheses.

2. No monotonous structure. If every paragraph is the same length and opens the same way, the writing feels robotic. Vary sentence length and paragraph structure.

## Editorial Integrity

1. No urgency injection. Do not add severity, alarm, or urgency that is not in the original text. If the author wrote a factual statement, do not reframe it as a risk or emergency.
   - ❌ Original: "Not started. Dependent on Q1 items." Rewrite: "Cascading dependency: if Q1 slips, Q2 and May both slip."
   - Keep the original phrasing. The reader can see the dependency.

2. Preserve attribution. When text attributes a statement, decision, or position to a person, preserve the attribution exactly. Do not paraphrase in ways that change who said what or imply positions they did not take.
   - ❌ Original: "The lead discussed with the Product team, who consider it high priority. No committed timeline yet; discussions are early." Rewrite: "No commitment from the Product team."
   - Keep the original. The rewrite implies a refusal; the original describes early-stage discussions.

3. Preserve technical and domain-specific language. When the original uses precise terminology, keep it. Simplification that changes scope or introduces claims the source did not make is worse than jargon. Rule 26 (explain jargon) applies to terms the reader may not know, not to terms the author chose for precision.
   - ❌ Original: "upstream change risk evaluation across the Identity Service, app integrations, and infra dependencies" Rewrite: "could break the Identity Service"
   - Keep the original. "Risk evaluation" is broader than "break," and the scope (core, apps, infra) is lost.

3. No spin or positive reframing. Do not convert neutral or negative facts into positive framing. Internal documentation exists to inform, not to sell. If something has not started, do not call it "on track." If results are mixed, do not lead with the upside.
   - ❌ Original: "Work has not begun. Dependent on Q1 items." Rewrite: "On track - sequenced behind Q1 deliverables."
   - Keep "not started" and state the dependency.

4. No invented proposals or next steps. Do not fabricate actions, timelines, or commitments that are not in the original text. If the author describes a current state, do not generate what should happen next; that is the author's decision.
   - ❌ Original: "Alignment in progress." Rewrite: "Proposing a concrete RACI by next cycle."
   - Keep "alignment in progress." No one proposed a RACI. The LLM generated a plausible-sounding next step and presented it as the plan.
