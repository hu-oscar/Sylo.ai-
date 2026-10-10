export type Currency = "EUR" | "GHS" | "NGN" | "USD";
export type Purpose = "GOODS" | "SERVICES_TECHNICAL" | "SERVICES_OTHER";
export type Tier = "LOW" | "MEDIUM" | "HIGH" | "CRITICAL";
export type Provenance =
  | "verified_registry"
  | "payment_history"
  | "psp_attestation"
  | "invoice_pdf_email"
  | "inbound_call"
  | "user_input";

export type Party = {
  name: string;
  accountId: string;
  bankBic?: string;
  country: string;
  region?: string;
};

export type PaymentOrder = {
  id: string;
  uetr: string;
  debtor: Party;
  creditor: Party;
  amount: { value: string; currency: Currency };
  purpose: Purpose;
  documents: { invoiceRef?: string; locRef?: string; senderDomain?: string };
  provenance: Record<string, Provenance>;
  channel: { deviceId: string; msisdn: string; sessionCountry: string };
};

export type Payee = {
  id: string;
  legalName: string;
  accounts: {
    id: string;
    firstSeen: string;
    successfulPayments: number;
    nominatedForExports?: boolean;
    verification?: {
      method: "OOB_KNOWN_CONTACT" | "PSP_ATTESTATION";
      at: string;
      by: string;
    };
  }[];
  knownContacts: { msisdn: string; since: string }[];
};

export type Decision = {
  paymentId: string;
  normChecks: {
    routeId: string;
    ruleId: string;
    result: "PASS" | "FAIL" | "NEEDS_DOCUMENT";
    legalRef: string;
  }[];
  taxNotices: { text: string; reference: string; source: string }[];
  risk: {
    score: number;
    tier: Tier;
    rulesFired: string[];
    topReasons: { ref: string; text: string }[];
    modelVersion: string;
  };
  route: {
    chosen: string;
    candidates: { routeId: string; S?: number; excludedBy?: string }[];
    settlement: "DIRECT" | "ONCHAIN_ESCROW" | "FIAT_HOLD" | "NONE";
    quoteValidUntil: string;
  };
  approval?: { by: string[]; method: "SCA" | "DUAL_CONTROL"; hash: string };
  intent?: { hash: string; txHash: string };
};

export type PaymentLeg = {
  uetr: string;
  intentHash: string;
  nonce: number;
  rail: string;
  rank: number;
  status: "initiated" | "pending" | "settled" | "failed" | "returned" | "rejected";
  idempotencyKey: string;
};

export type LogEntry = {
  seq: number;
  prevHash: string;
  type: string;
  payload: unknown;
  hash: string;
  anchoredRoot?: string;
};

export type EventEnvelope = {
  id: number;
  type: string;
  ts: string;
  paymentId: string;
  uetr: string;
  scene: string;
  data: Record<string, unknown>;
  explorerUrl: string | null;
};

export type RiskContext = {
  payee_is_new: boolean;
  account_first_seen_days: number | null;
  account_age_days: number | null;
  successful_payments_to_account: number;
  name_match: number;
  personal_account_for_business: boolean;
  amount_vs_account_capacity: number;
  provenance: Provenance;
  lookalike_domain: boolean;
  urgency_cues: boolean;
  payer_sim_swap_72h: boolean;
  payer_new_device_24h: boolean;
  session_country_unusual: boolean;
  account_region: string | null;
  supplier_region: string | null;
  region_mismatch: boolean;
  account_near_border: boolean;
  wallet_region_mismatch: boolean;
  impossible_travel: boolean;
  regional_fraud_wave: boolean;
  amount_eur: number;
  amount_vs_history_ratio: number;
  unusual_hour: boolean;
  velocity_24h: number;
  fanout_wallets: number;
  minutes_credit_to_forward: number | null;
  shared_cashout_agents: number;
  young_fast_cluster: boolean;
  just_below_cap_count: number;
  declared_split: boolean;
  norm_r1: boolean;
  sanctions_hit: boolean;
  linked_confirmed_fraud: boolean;
  supplier_contact_sim_swap_7d: boolean;
};

export type RiskResult = {
  score: number;
  tier: Tier;
  rulesFired: string[];
  topReasons: { ref: string; text: string }[];
  modelVersion: string;
};
