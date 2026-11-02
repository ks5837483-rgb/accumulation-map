# Market labels for the eval set = the 583-era maps (landscape_ie/market_pivot/{y_market_map,c_event_map}.py, unchanged) +
# an ADDENDUM for outcome groups first seen in the eval set. Addendum assigned by reading each label (analyst LLM judgment
# in-session, 2026-10-31; no keyword rules). Labels not listed anywhere stay "O" (other), exactly as in the 583 pivot.
import sys
import os as _o0; sys.path.insert(0, _o0.path.join(_o0.path.dirname(_o0.path.abspath(__file__)), "..", "market_pivot"))
from y_market_map import MARKET as _M
from c_event_map import EVENT as _E
ADD_F = """NEW:acquisition_overpayment NEW:toehold_acquisition NEW:seller_initiated_deal NEW:strategic_industry_target_choice
NEW:risky_target_acquisition NEW:bidder_consortium_formation NEW:acquisition_versus_licensing_choice NEW:cvc_versus_acquisition_choice
NEW:accounting_information_weight_in_bid_price NEW:fairness_opinion_valuation_inputs new:offer_outcome_quality new:industry_undervaluation_at_bid
new:pollutive_asset_acquisition_likelihood new:bank_client_acquisition new:bank_involvement_in_acquisition NEW:acquirer_target_valuation_similarity
deal_decision_quality valuation_accuracy ipo_versus_acquisition_choice""".split()
ADD_C = """NEW:merger_arbitrage_spread NEW:merger_arbitrage_return NEW:takeover_rumor_accuracy NEW:investor_valuation_judgment
spac_de_spac_return new:price_discovery_efficiency new:demand_for_information_sensitive_securities new:senior_security_value
new:senior_secured_loan_price new:parent_shareholder_gain new:subsidiary_minority_shareholder_gain new:advisory_bank_holdings_strategy_return""".split()
ADD_EVENT = {"NEW:merger_arbitrage_spread": "D", "NEW:merger_arbitrage_return": "D", "NEW:takeover_rumor_accuracy": "D",
             "spac_de_spac_return": "D", "new:parent_shareholder_gain": "D", "new:subsidiary_minority_shareholder_gain": "D",
             "NEW:investor_valuation_judgment": "U", "new:price_discovery_efficiency": "U", "new:senior_security_value": "U",
             "new:demand_for_information_sensitive_securities": "E", "new:senior_secured_loan_price": "E",
             "new:advisory_bank_holdings_strategy_return": "E"}
MARKET = {**_M, **{k: "F" for k in ADD_F}, **{k: "C" for k in ADD_C}}
EVENT = {**_E, **ADD_EVENT}

# RAW-LEVEL OVERRIDES (2026-11-01, user-caught error: Wangerin 2019 CAR "value relevance" was counted as firm-side because its
# outcome group valuation_accuracy mixes both sides). Applied to the raw outcome name BEFORE the group-level map. Judged by reading.
RAW_MARKET = {"value_relevance_of_fair_value_estimates": "C", "value_relevance_of_goodwill": "C",
              "target_valuation_accuracy": "F", "deal_value_observability": "A"}
RAW_EVENT = {"value_relevance_of_fair_value_estimates": "D", "value_relevance_of_goodwill": "D"}

# OUTCOME-LEVEL SIDE JUDGMENTS (2026-11-01, prompt of record outcome_evaluator v1; 919 raw outcomes, blind to the group label;
# 91% agreement with group labels). These supersede the group-level and hand overrides above for every judged outcome.
import json as _json, os as _os
_RS = _json.load(open(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..', '_work_side', 'raw_side.json')))
RAW_MARKET = {**RAW_MARKET, **{k: v['side'] for k, v in _RS.items()}}
RAW_EVENT = {**RAW_EVENT, **{k: (v['event'] or None) for k, v in _RS.items() if v['side'] == 'C'}}
