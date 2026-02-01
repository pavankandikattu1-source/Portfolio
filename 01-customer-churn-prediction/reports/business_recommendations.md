# Customer Churn – Business Recommendations

## Recommended Retention Actions by Segment

| Segment | Churn risk | Recommended action |
|---------|------------|---------------------|
| **High age, single product** | High | Proactive outreach; offer second product (e.g. savings, card) to increase stickiness. |
| **Germany, low activity** | High | Germany shows higher churn; boost engagement (notifications, rewards) and review fees. |
| **Zero balance, 1 product** | Medium–High | Onboarding and balance-building incentives; reduce friction to use the account. |
| **High salary, low tenure** | Medium | Early loyalty program; personalized offers to increase tenure and product count. |
| **Low credit score** | Medium | Credit education or tailored product (e.g. overdraft); improve satisfaction to reduce exit. |

## Revenue Impact

- **At-risk revenue:** Sum (EstimatedSalary or balance × churn probability) for customers in the top risk decile from the Random Forest model.
- **Target:** Use model scores to prioritize retention; aim to reduce churn in top decile by 10–15% via targeted campaigns (e.g. product bundling, fee waivers, outreach).

## Stakeholder Communication

- **Retail / Product:** Focus on **Age**, **NumOfProducts**, and **Geography** (especially Germany). Design bundles and onboarding for single-product and older customers.
- **Marketing:** Use churn probability scores for segment-specific retention campaigns (email, in-app, offers). Allocate budget to high-risk, high-value segments.
- **Finance:** Use at-risk revenue and expected savings from retention to justify investment in retention programs and measure ROI.

## Next Steps

1. **Validate:** Test model on a holdout period or new cohort; monitor AUC and calibration.
2. **Deploy scores:** Export churn probability per customer; integrate into CRM or campaign tooling.
3. **Define tiers:** Set risk bands (e.g. high / medium / low) and approval rules for offers.
4. **Monitor:** Track monthly churn rate and model performance; set up alerts for drift.
