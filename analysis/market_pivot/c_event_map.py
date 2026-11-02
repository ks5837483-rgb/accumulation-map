# Investor-side (market C) outcome labels -> is the investors' evaluation TRIGGERED BY A DEAL? Assigned by reading
# each label (analyst LLM judgment in-session, 2026-10-31; no keyword rules).
# D = deal-triggered (investors judge firms because of an M&A event: announcement, revision, withdrawal, post-deal
#     drift, rival/spillover revaluation) · E = everyday processing (earnings, analysts, lending, trading, IPO,
#     media, issuance) · U = unclear at label level (needs a finding-level read).
D = """acquirer_announcement_return unspecified_announcement_return target_announcement_return target_wealth_gain acquirer_wealth_gain
combined_announcement_return acquirer_share_of_merger_gain rival_announcement_return rival_firm_value combined_merger_wealth_gain
preannouncement_stock_runup acquirer_long_run_stock_return acquirer_post_acquisition_return target_share_of_merger_gain
merger_gain_distribution withdrawal_announcement_return divestiture_announcement_return bid_revision_return new:merger_arbitrage_return
new:merger_arbitrage_spread new:pure_takeover_return new:announcement_period_market_return post_announcement_return_drift
new:market_reaction_completion_predictiveness target_long_run_stock_return stakeholder_announcement_return""".split()
E = """bank_loan_spread forecast_accuracy equity_issuance earnings_information_content stock_price_level loan_terms ipo_likelihood
credit_quality credit_access financing_cost stock_liquidity ipo_proceeds_and_price trading_activity media_coverage loan_covenants
institutional_investor_trading forecast_revision forecast_bias_or_dispersion repurchase_announcement_return systematic_equity_risk
post_ipo_return analyst_coverage stock_return_volatility retail_investor_trading options_trading_intensity media_tone public_bond_financing
new:analyst_downgrade_likelihood new:analyst_stock_recommendation new:delisting_hazard new:investor_interest new:price_incorporation_speed
new:stock_price_synchronicity other_event_announcement_return""".split()
U = """stock_market_reaction_unspecified target_firm_value shareholder_value_general stock_return_unspecified unspecified_long_run_stock_return
other_firm_value acquirer_firm_value combined_firm_value informed_or_suspicious_trading valuation_discount""".split()
EVENT = {**{k: "D" for k in D}, **{k: "E" for k in E}, **{k: "U" for k in U}}
