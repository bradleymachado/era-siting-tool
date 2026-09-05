-- era_schema_v1.4.sql
-- Schema for era_rates.db (Electrical Rate Analysis / Data Center Siting Tool).
-- Supersedes v1.3 per brief_ph2_unit2c_open_v1.0.md section B and brief_ph2_report_v1.0.md 3.3,
-- ruled into Unit 2C-b.
--
-- Changes from v1.3 - four, all capability, none of them touching a stored value:
--   1. rate.charge_type gains 'pct_of_base'.  A charge expressed as a PERCENTAGE of some base,
--      stored as the rule rather than multiplied out against every base row.  Georgia Power's
--      ECCR-15 + DSM-C-15 and AEP Ohio's ESRR + DIR + EDCR are the live cases; both remain
--      multiplied out until the costing path can price the charge form (see note below).
--   2. rate.pct_base_scope  'base_bill' | 'base_distribution' | 'energy_only'.  NOT NULL exactly
--      when charge_type = 'pct_of_base', NULL otherwise, enforced in BOTH directions.  A
--      percentage with no stated base is not a chargeable rule.
--   3. rate.unit gains 'pct'.  The only unit a pct_of_base row may take, and no other charge_type
--      may take it.  rate_value is then the percentage as a FRACTION (0.130205 for 13.0205%).
--   4. billing_mechanic.mechanic_type gains 'pf_bill_adjustment'.  A per-kWh bill adjustment whose
--      magnitude depends on the metered power factor.  PG&E B-20's $0.00005/kWh-per-point clause
--      is the type case: the RULE is sourced from the tariff, the MAGNITUDE depends on the
--      project's assumed power factor, and a rate row can express only the second.  Mechanics hold
--      rules; rate rows hold magnitudes.
--
-- WATCH THE 'IS NOT NULL' IN THE pct_base_scope CHECK.  Written as
--   CHECK ((charge_type = 'pct_of_base' AND pct_base_scope IN (...)) OR ...)
-- the constraint is INERT against a NULL scope: `NULL IN (...)` is NULL, the whole CHECK is NULL,
-- and SQLite admits the row.  The explicit IS NOT NULL is what makes it bite.  Found by the Unit
-- 2C-b verifier's check A3, which probes the constraint by attempting the insert rather than by
-- reading the DDL.
--
-- NOTHING IN THE COSTING PATH CAN BILL A pct_of_base ROW YET.  era_acceptance_v1.3.py RAISES on
-- one rather than silently omitting it; era_engine_v1.0.py has no branch for it at all.  Load a
-- pct_of_base row only in the same unit that teaches the engine to price it.
--
-- This file is the authoritative statement of v1.4.  It is used to build a NEW database.
-- An existing v1.3 database is upgraded in place by era_migrate_v13_to_v14_v1.0.py, which must be
-- kept in agreement with this file.
--
-- PRAGMA user_version = 14 marks a v1.4 database.

PRAGMA foreign_keys = ON;

-- One row per utility serving a target metro. Market structure drives how energy is procured.
CREATE TABLE IF NOT EXISTS utility (
  utility_id INTEGER PRIMARY KEY AUTOINCREMENT,
  utility_name TEXT NOT NULL,
  metro TEXT NOT NULL,
  state TEXT NOT NULL,
  eia_utility_id INTEGER,
  urdb_utility_name TEXT,
  market_structure TEXT NOT NULL,
  regulator TEXT,
  notes TEXT,
  UNIQUE (utility_name, state),
  CHECK (length(state) = 2),
  CHECK (market_structure IN ('vertically_integrated','delivery_only','municipal','cooperative'))
);

-- One row per rate schedule REVISION. A new effective_date is a new row, never an update.
CREATE TABLE IF NOT EXISTS schedule (
  schedule_id INTEGER PRIMARY KEY AUTOINCREMENT,
  utility_id INTEGER NOT NULL,
  schedule_code TEXT NOT NULL,
  schedule_name TEXT,
  customer_class TEXT NOT NULL,
  voltage_level TEXT,
  min_demand_kw REAL,
  max_demand_kw REAL,
  effective_date TEXT NOT NULL,
  end_date TEXT,
  source_type TEXT NOT NULL,
  source_url TEXT,
  urdb_label TEXT,
  supply_basis TEXT,
  rider_coverage TEXT NOT NULL DEFAULT 'base_only',
  rider_coverage_authority TEXT,
  verified_against_pdf INTEGER NOT NULL DEFAULT 0,
  verification_date TEXT,
  verification_notes TEXT,
  UNIQUE (utility_id, schedule_code, effective_date),
  CHECK (customer_class IN ('commercial','industrial','residential','other')),
  CHECK (voltage_level IS NULL OR voltage_level IN ('secondary','primary','transmission')),
  CHECK (source_type IN ('urdb','pdf','xlsx','manual')),
  CHECK (supply_basis IS NULL OR supply_basis IN ('bundled','delivery_only')),
  CHECK (rider_coverage IN ('itemised','verified_aggregate','aggregate','base_only')),
  CHECK (verified_against_pdf IN (0,1)),
  FOREIGN KEY (utility_id) REFERENCES utility(utility_id)
);

-- A named TOU period. Energy and demand periods are numbered in separate sequences.
CREATE TABLE IF NOT EXISTS rate_period (
  rate_period_id INTEGER PRIMARY KEY AUTOINCREMENT,
  schedule_id INTEGER NOT NULL,
  applies_to TEXT NOT NULL,
  period_index INTEGER NOT NULL,
  period_name TEXT,
  season TEXT,
  notes TEXT,
  UNIQUE (schedule_id, applies_to, period_index),
  CHECK (applies_to IN ('energy','demand')),
  CHECK (period_index >= 0),
  CHECK (season IS NULL OR season IN ('summer','winter','all')),
  FOREIGN KEY (schedule_id) REFERENCES schedule(schedule_id)
);

-- One month/day-type/hour block belonging to a period. A period owns many windows.
CREATE TABLE IF NOT EXISTS rate_period_window (
  rate_period_window_id INTEGER PRIMARY KEY AUTOINCREMENT,
  rate_period_id INTEGER NOT NULL,
  month_start INTEGER NOT NULL,
  month_end INTEGER NOT NULL,
  day_type TEXT NOT NULL,
  hour_start INTEGER NOT NULL,
  hour_end INTEGER NOT NULL,
  CHECK (month_start BETWEEN 1 AND 12),
  CHECK (month_end BETWEEN 1 AND 12),
  CHECK (day_type IN ('weekday','weekend','holiday','all')),
  CHECK (hour_start BETWEEN 0 AND 23),
  CHECK (hour_end BETWEEN 1 AND 24),
  CHECK (hour_end > hour_start),
  FOREIGN KEY (rate_period_id) REFERENCES rate_period(rate_period_id)
);

-- One row per individual charge. Billed rate = rate_value + rate_adj. Cost engine reads this.
-- is_assumption = 1 : value invented by us, no external source.
-- is_market_price = 1 : value taken from a wholesale index (sourced, not a tariff charge).
-- The two flags are independent; a sourced market price is NOT an assumption.
-- billing_determinant : the metered quantity this charge is applied to. NOT NULL, no default.
-- determinant_is_assumption = 1 : the determinant is a stated default, not read from the sheet.
CREATE TABLE IF NOT EXISTS rate (
  rate_id INTEGER PRIMARY KEY AUTOINCREMENT,
  schedule_id INTEGER NOT NULL,
  rate_period_id INTEGER,
  charge_type TEXT NOT NULL,
  component_name TEXT NOT NULL,
  tier_index INTEGER NOT NULL DEFAULT 0,
  rate_value REAL NOT NULL,
  rate_adj REAL NOT NULL DEFAULT 0,
  unit TEXT NOT NULL,
  billing_determinant TEXT NOT NULL,
  determinant_is_assumption INTEGER NOT NULL DEFAULT 0,
  pct_base_scope TEXT,
  tier_min REAL,
  tier_max REAL,
  tier_unit TEXT,
  applicable_months TEXT,
  effective_date TEXT NOT NULL,
  is_assumption INTEGER NOT NULL DEFAULT 0,
  is_market_price INTEGER NOT NULL DEFAULT 0,
  source_note TEXT,
  CHECK (charge_type IN ('energy','demand','flat_demand','fixed','rider','pct_of_base')),
  CHECK (tier_index >= 0),
  CHECK (unit IN ('USD_per_kWh','USD_per_kW_month','USD_per_month','USD_per_day',
                  'USD_per_kVA_month','USD_per_kVAr_month','pct')),
  CHECK (is_assumption IN (0,1)),
  CHECK (is_market_price IN (0,1)),
  CHECK (determinant_is_assumption IN (0,1)),
  CHECK (tier_unit IS NULL OR tier_unit IN ('kWh','kWh_per_kW','kW','kVA','kVAr')),
  CHECK (billing_determinant IN ('energy_kwh','ncp_kw_15min','ncp_kw_30min',
                                 'cp4_kw','kvar_excess','fixed')),
  -- v1.4: the percentage and its base are inseparable, in both directions. The explicit
  -- IS NOT NULL is load-bearing; see the header note.
  CHECK ((charge_type = 'pct_of_base' AND pct_base_scope IS NOT NULL AND pct_base_scope IN
            ('base_bill','base_distribution','energy_only')) OR
         (charge_type <> 'pct_of_base' AND pct_base_scope IS NULL)),
  -- v1.4: 'pct' is the only unit a pct_of_base row may take, and only it may take 'pct'.
  CHECK ((charge_type = 'pct_of_base' AND unit = 'pct') OR
         (charge_type <> 'pct_of_base' AND unit <> 'pct')),
  CHECK ((charge_type = 'energy' AND unit = 'USD_per_kWh') OR
         (charge_type IN ('demand','flat_demand') AND unit IN ('USD_per_kW_month','USD_per_kVA_month')) OR
         (charge_type = 'fixed' AND unit IN ('USD_per_month','USD_per_day')) OR
         charge_type IN ('rider','pct_of_base')),
  CHECK ((charge_type = 'energy' AND billing_determinant = 'energy_kwh') OR
         (charge_type = 'fixed' AND billing_determinant = 'fixed') OR
         (charge_type IN ('demand','flat_demand') AND
          billing_determinant IN ('ncp_kw_15min','ncp_kw_30min','cp4_kw')) OR
         charge_type IN ('rider','pct_of_base')),
  CHECK (billing_determinant <> 'kvar_excess' OR unit = 'USD_per_kVAr_month'),
  FOREIGN KEY (schedule_id) REFERENCES schedule(schedule_id),
  FOREIGN KEY (rate_period_id) REFERENCES rate_period(rate_period_id)
);

-- Tariff mechanics that change the BILLING QUANTITY or the bill floor rather than a price.
-- The cost engine applies these after computing charges from `rate`.
--
-- params is JSON. Documented structure by mechanic_type:
--   demand_ratchet     {"lookback_months": int,
--                       "lookback_pct": float,
--                       "capacity_floors": [{"up_to_kw": float|null,
--                                            "base_kw": float,
--                                            "pct_above_kw": float,
--                                            "above_threshold_kw": float,
--                                            "cap_pct_of_contract_capacity": float|null}],
--                       "ramp_period_max_years": int|null,
--                       "ramp_min_pct_of_ramp_capacity": float|null,
--                       "ramp_capacity_min_pct_by_year": {"<year>": float}|null,
--                       "alt_floor_pct": float|null,   -- e.g. a different floor for legacy load
--                       "notes": str|null}
--   pf_demand_floor    {"pf_threshold": float, "floor_pct_of_max_kva": float}
--   min_monthly_bill   {"amount_usd": float, "basis": "per_metered_service_point"|"per_account"}
--   pf_bill_adjustment {"basis_pf": float,               -- the power factor the tariff measures from
--                       "usd_per_kwh_per_point": float,  -- charge per whole point away from it
--                       "direction": str,                -- e.g. "credit_above_basis_charge_below"
--                       "point_definition": str,
--                       "magnitude_at_project_pf": {"pf": float, "points": int,
--                                                   "usd_per_kwh": float, "usd_per_mwh": float},
--                       "notes": str|null}
CREATE TABLE IF NOT EXISTS billing_mechanic (
  mechanic_id INTEGER PRIMARY KEY AUTOINCREMENT,
  schedule_id INTEGER NOT NULL,
  mechanic_type TEXT NOT NULL,
  params TEXT NOT NULL,
  is_verified INTEGER NOT NULL DEFAULT 0,
  source_note TEXT,
  UNIQUE (schedule_id, mechanic_type),
  CHECK (mechanic_type IN ('demand_ratchet','pf_demand_floor','min_monthly_bill',
                           'pf_bill_adjustment')),
  CHECK (is_verified IN (0,1)),
  FOREIGN KEY (schedule_id) REFERENCES schedule(schedule_id)
);

CREATE INDEX IF NOT EXISTS idx_schedule_utility ON schedule(utility_id);
CREATE INDEX IF NOT EXISTS idx_schedule_effective ON schedule(effective_date);
CREATE INDEX IF NOT EXISTS idx_rate_period_schedule ON rate_period(schedule_id);
CREATE INDEX IF NOT EXISTS idx_window_period ON rate_period_window(rate_period_id);
CREATE INDEX IF NOT EXISTS idx_rate_schedule ON rate(schedule_id);
CREATE INDEX IF NOT EXISTS idx_rate_charge_type ON rate(charge_type);
CREATE INDEX IF NOT EXISTS idx_rate_period ON rate(rate_period_id);
CREATE INDEX IF NOT EXISTS idx_rate_determinant ON rate(billing_determinant);
CREATE INDEX IF NOT EXISTS idx_mechanic_schedule ON billing_mechanic(schedule_id);

PRAGMA user_version = 14;
