# AOProof Context Pack

## 1. What AOProof is
AOProof is a system to prove authenticity and ownership of a specific physical item instance.
It combines an on-chain asset (Solana), an off-chain API + DB, and NFC/QR/link-based user flows.
The goal is anti-counterfeit protection, transparent ownership history, and ownership transfer with a UX that works for both crypto and non-crypto users.

## 2. High-level architecture
Components:
- API: Fastify + PostgreSQL (packages/api)
- SDK: TypeScript wrapper for web (packages/sdk)
- Web:
  - Consumer portal (apps/consumer-web)
  - Brand / Individual portal (apps/brand-web)
- DB tables (examples):
  - items, links (verify/claim/transfer with TTL/revoke/usage), ledger_entries, custody_keys, brands, invoices, mint_jobs

## 3. Code locations
Monorepo: /root/aoproof
- apps/consumer-web
- apps/brand-web
- packages/api
- packages/sdk
- packages/shared

## 4. What is working today (confirmed)
Consumer Web (apps/consumer-web):
- /verify: server wrapper + client UI, calls /v0/verify, shows base item info
- /claim:
  - UI to select method (wallet / custody)
  - custody-claim calls API and works temporarily without account
  - wallet-claim UI exists but wallet connect and tx flow are not implemented

Brand Web (apps/brand-web):
- /mint/one works
- /items displays items (confirmed)

API (packages/api):
- /v0/verify works
- /v0/claim (custody) works
- /v0/claim_wallet + /v0/claim_finalize exist
- mint (one / batch) works
- revoke link works
- ledger_entries exist and record actions
- /v0/transfer returns 501 Not implemented (blocking)

## 5. Key design decisions (fixed)
- Mint:
  - always via minter wallet
  - individual pays themselves
  - brand pays via project deposit
- Claim:
  - wallet claim (crypto user)
  - custody claim (non-crypto user), requires an account
- Transfer:
  - link-based flows (TTL, revoke, single-use)
  - accept via wallet or custody
- Ledger:
  - all actions recorded: mint, claim, transfer, revoke

## 6. What is not working (honest gaps)
- Consumer end-to-end flow is not closed:
  - no transfer accept flow
  - no auth (login/register)
  - no proof endpoint/flow
  - wallet flow not connected (no wallet-adapter providers, no tx signing)
- API transfer is not implemented, DB schema is ready

## 7. Definition of Done (v0)
Consumer v0:
- /verify shows correct status and CTA
- /claim:
  - wallet: sign tx and become owner
  - custody: create account and become owner
- /transfer/accept:
  - accepts ownership (wallet or custody)
  - handles expired / revoked correctly
- /proof: downloadable JSON proof
- Lost/Stolen status reflected in verify

Brand/Individual v0:
- mint one/batch works
- items list + item detail
- offline QR transfer (TTL 15m)
- ledger and invoices readable
- no critical placeholders in core flows

## 8. Constraints
- Must be modular and replaceable components
- Must run on Ubuntu VPS
- Budget: $0 for now
