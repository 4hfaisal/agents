# Portfolio Manager — MCP Tool Reference

Full parameter reference for all 19 tools exposed by the Portfolio Manager MCP server.

---

## Read Tools

### `get_summary`
Top-level portfolio KPIs.
```
Returns: {
  total_value_usd, total_invested_usd,
  unrealized_pl_usd, unrealized_pl_pct,
  realized_pl_usd,
  daily_change_usd, daily_change_pct,
  as_of (ISO datetime)
}
```

### `get_holdings`
Full portfolio tree: asset classes → accounts → positions.
```
Returns: {
  total_value_usd,
  asset_classes: [{
    id, name, display_order, value_usd, pct, pl_usd,
    accounts: [{
      id, name, institution, currency, value_usd, pl_usd, pl_pct,
      positions: [{
        id, name, symbol, asset_type,
        quantity, avg_cost_basis, cost_currency,
        current_value_usd, current_price,
        cost_basis_usd, pl_usd, pl_pct, weight_pct,
        first_acquired, price_updated_at
      }]
    }]
  }]
}
```

### `get_position(position_id: str)`
Full detail for one position.
```
Returns: position fields + {
  transactions: [{ id, type, date, quantity, price, total_amount, currency, notes }],
  account_id, account_name, account_entities,
  metadata: { arbitrary key/value pairs }
}
```

### `get_allocation`
```
Returns: [{ name, value_usd, pct, color }]
```

### `get_performance(days: int = 90)`
Daily portfolio value vs benchmarks, normalised to same start.
```
Returns: [{ date, portfolio_usd, sp500, nasdaq, msci_world }]
```

### `get_top_movers(limit: int = 10)`
```
Returns: [{ id, name, symbol, asset_type, pl_usd, pl_pct, current_value_usd }]
```

### `get_pl_by_class`
```
Returns: [{ name, cost_basis_usd, current_value_usd, pl_usd, pl_pct, color }]
```

### `get_realized_vs_unrealized`
```
Returns: { unrealized_usd, realized_usd, income_usd, total_return_usd }
```

### `get_wacc`
```
Returns: {
  wacc_pct,
  total_debt_usd,
  loans: [{ id, name, balance_usd, interest_rate_pct, currency, weight_pct }]
}
```

### `list_contacts`
```
Returns: [{ id, name, position, email, mobile, linkedin_url, notes, created_at }]
```

### `list_loans`
```
Returns: [{
  id, name, principal, interest_rate, balance,
  currency, start_date, maturity_date, is_active
}]
```

### `list_reports`
```
Returns: [{ filename, size_kb, generated_at }]
```
`generated_at` format: `YYYYMMDD_HHMMSS`

### `list_ingestion_logs(limit: int = 20)`
```
Returns: [{
  id, filename, report_type, status,
  records_extracted, error_message, processed_at
}]
```
`status`: `success` | `failed` | `quarantined` | `processing`

---

## Write Tools

### `add_transaction`
```
Parameters:
  position_id: str          # UUID from get_holdings
  type: str                 # buy | sell | dividend | distribution | interest
                            # capital_call | nav_update | cost_entry
  date: str                 # YYYY-MM-DD
  total_amount: float       # cash value (required)
  currency: str             # USD | BHD | SAR | EUR  (default: USD)
  quantity: float | None    # units bought/sold (optional)
  price: float | None       # per-unit price (optional)
  notes: str | None         # free text (optional)

Returns: { id: str, ok: bool }
```

### `update_position`
```
Parameters (all optional except position_id):
  position_id: str
  name: str | None
  symbol: str | None
  asset_type: str | None    # stock|etf|mutual_fund|crypto|real_estate|pe|vc|private_credit|gold
  quantity: float | None
  avg_cost_basis: float | None
  cost_currency: str | None
  current_value: float | None   # manual override for illiquid assets
  first_acquired: str | None    # YYYY-MM-DD

Returns: { id: str, ok: bool }
```

### `add_position`
```
Parameters:
  account_id: str           # UUID from get_holdings
  name: str
  asset_type: str           # see asset types reference
  cost_currency: str        # default: USD
  symbol: str | None
  quantity: float | None
  avg_cost_basis: float | None
  current_value: float | None
  first_acquired: str | None    # YYYY-MM-DD

Returns: { id: str, ok: bool }
```

### `add_loan`
```
Parameters:
  name: str
  principal: float          # original loan amount
  balance: float            # current outstanding balance
  interest_rate: float      # annual % (e.g. 5.25 for 5.25%)
  start_date: str           # YYYY-MM-DD
  currency: str             # default: USD
  maturity_date: str | None # YYYY-MM-DD

Returns: { id: str, ok: bool }
```

### `add_contact`
```
Parameters:
  name: str
  position: str | None          # job title
  email: str | None
  mobile: str | None
  linkedin_url: str | None
  notes: str | None
  link_to_position_id: str | None   # auto-link on creation
  link_to_account_id: str | None    # auto-link on creation

Returns: { id: str, ok: bool }
```

### `generate_report`
```
Parameters: none

Returns: { ok: bool, filename: str }
```
File saved to `/app/data/reports/` on the server. External agent picks it up for delivery.
