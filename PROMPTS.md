# PROMPTS.md — StaySense AI Week 7

Intern ID: TBI-26100053

## Feature
AI-powered guest-review analysis for StaySense AI.

### Prompt 1 — Concise hospitality analysis
Analyze this guest review and return sentiment, main theme, a one-sentence summary, and a suggested host response.

**Test input:** "The room was clean and the host was very helpful, but the location was a little far from the city."

**Expected type of output:** Structured, concise hospitality feedback analysis.

### Prompt 2 — Action-oriented analysis
Analyze the review from a homestay owner's perspective. Identify what the owner did well, the biggest issue, and three practical actions to improve the guest experience.

**Test input:** "Great food and friendly host, but the bathroom was dirty and check-in took too long."

**Expected type of output:** Prioritized improvement actions.

### Prompt 3 — Response generation
Analyze the review and write a professional, empathetic host response in under 100 words. Do not make promises that are not supported by the review.

**Test input:** "Amazing stay overall. The room was comfortable, although the Wi-Fi was unreliable at night."

**Expected type of output:** Short public-facing host response.

## Which prompt worked best?
Prompt 1 is the best default for StaySense AI because it directly matches the product's main purpose: turning guest feedback into useful sentiment, theme, summary, and response information. Prompt 2 is useful for owners who want operational recommendations, while Prompt 3 is best when the immediate goal is replying to guests.

## System prompt / role used
You are a hospitality feedback assistant. Analyze guest reviews clearly, avoid inventing facts, and keep recommendations practical.

## Notes
The API key is never included in this file. It must be stored in `.env`.
