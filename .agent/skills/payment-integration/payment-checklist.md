# Payment integration checklist — `/payment-pass`

> Provider-agnostic. Use Stripe, Paddle, Mercado Pago, etc. as **examples** in docs — not as mandatory stack.

## Bootstrap

- [ ] Payment model documented (one-time, subscription, marketplace, usage)
- [ ] PCI scope statement (SAQ level or “provider-hosted checkout”)
- [ ] No card data touches app servers unless explicitly designed and approved

## Security

- [ ] API keys and webhook secrets in env only — never in repo or US examples
- [ ] Webhook signature verification required on every handler
- [ ] Idempotency keys for create/charge operations that retry
- [ ] Replay protection: event ids deduplicated in storage (`06`)
- [ ] Least privilege API keys (restricted permissions per environment)
- [ ] Test vs live mode separation documented in `08`

## Data

- [ ] PII stored for billing listed in `02` / `06` retention
- [ ] Invoice/receipt data minimization
- [ ] Subprocessors row updated when payment provider processes user data

## API / flows

- [ ] Checkout success/cancel URLs documented
- [ ] Failed payment and dunning behavior described (product, not code)
- [ ] Refund/chargeback handling owner identified
- [ ] 07 webhook table lists payment events and auth

## US alignment

- [ ] Must payment US cites 02 payment section in Plan
- [ ] Acceptance includes webhook failure and duplicate event scenarios

## HAR (human)

- [ ] Provider dashboard account and verification
- [ ] Production API keys and webhook endpoint registration
- [ ] Tax/compliance settings in provider (human/legal)
