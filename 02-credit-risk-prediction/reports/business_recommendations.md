# Credit Risk – Business Recommendations

## Risk Tier Definitions

| Tier | Default Probability | Action |
|------|---------------------|--------|
| Low | 0–20% | Standard approval |
| Medium | 20–50% | Enhanced review, possible rate adjustment |
| High | 50–80% | Decline or collateral requirement |
| Critical | 80%+ | Decline |

## RWA & Provisions

- Use model scores for **risk-weighted asset** calculation.
- **Loss provisioning:** Expected loss = PD × LGD × EAD by segment.
- Align with **regulatory requirements** (Basel, IFRS 9).

## Next Steps

1. Validate on holdout portfolio.
2. Integrate into credit decision engine.
3. Monitor model drift and recalibrate.
