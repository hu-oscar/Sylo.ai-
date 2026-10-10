from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

Currency = Literal["EUR", "GHS", "NGN", "USD"]
Purpose = Literal["GOODS", "SERVICES_TECHNICAL", "SERVICES_OTHER"]
Tier = Literal["LOW", "MEDIUM", "HIGH", "CRITICAL"]
Provenance = Literal[
    "verified_registry",
    "payment_history",
    "psp_attestation",
    "invoice_pdf_email",
    "inbound_call",
    "user_input",
]


class SharedModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class Party(SharedModel):
    name: str
    accountId: str
    bankBic: str | None = None
    country: str
    region: str | None = None


class Amount(SharedModel):
    value: str
    currency: Currency


class PaymentDocuments(SharedModel):
    invoiceRef: str | None = None
    locRef: str | None = None
    senderDomain: str | None = None


class PaymentChannel(SharedModel):
    deviceId: str
    msisdn: str
    sessionCountry: str


class PaymentOrder(SharedModel):
    id: str
    uetr: str
    debtor: Party
    creditor: Party
    amount: Amount
    purpose: Purpose
    documents: PaymentDocuments
    provenance: dict[str, Provenance]
    channel: PaymentChannel


class PayeeVerification(SharedModel):
    method: Literal["OOB_KNOWN_CONTACT", "PSP_ATTESTATION"]
    at: str
    by: str


class PayeeAccount(SharedModel):
    id: str
    firstSeen: str
    successfulPayments: int
    nominatedForExports: bool | None = None
    verification: PayeeVerification | None = None


class KnownContact(SharedModel):
    msisdn: str
    since: str


class Payee(SharedModel):
    id: str
    legalName: str
    accounts: list[PayeeAccount]
    knownContacts: list[KnownContact]


class NormCheck(SharedModel):
    routeId: str
    ruleId: str
    result: Literal["PASS", "FAIL", "NEEDS_DOCUMENT"]
    legalRef: str


class TaxNotice(SharedModel):
    text: str
    reference: str
    source: str


class RiskReason(SharedModel):
    ref: str
    text: str


class RiskResult(SharedModel):
    score: int = Field(ge=0, le=100)
    tier: Tier
    rulesFired: list[str]
    topReasons: list[RiskReason]
    modelVersion: str


class RouteCandidate(SharedModel):
    routeId: str
    S: float | None = None
    excludedBy: str | None = None


class RouteDecision(SharedModel):
    chosen: str
    candidates: list[RouteCandidate]
    settlement: Literal["DIRECT", "ONCHAIN_ESCROW", "FIAT_HOLD", "NONE"]
    quoteValidUntil: str


class Approval(SharedModel):
    by: list[str]
    method: Literal["SCA", "DUAL_CONTROL"]
    hash: str


class Intent(SharedModel):
    hash: str
    txHash: str


class Decision(SharedModel):
    paymentId: str
    normChecks: list[NormCheck]
    taxNotices: list[TaxNotice]
    risk: RiskResult
    route: RouteDecision
    approval: Approval | None = None
    intent: Intent | None = None


class PaymentLeg(SharedModel):
    uetr: str
    intentHash: str
    nonce: int
    rail: str
    rank: int
    status: Literal[
        "initiated", "pending", "settled", "failed", "returned", "rejected"
    ]
    idempotencyKey: str


class LogEntry(SharedModel):
    seq: int
    prevHash: str
    type: str
    payload: Any
    hash: str
    anchoredRoot: str | None = None


class EventEnvelope(SharedModel):
    id: int
    type: str
    ts: datetime
    paymentId: str
    uetr: str
    scene: str
    data: dict[str, Any]
    explorerUrl: str | None = None


class RiskContext(SharedModel):
    payee_is_new: bool = False
    account_first_seen_days: int | None = None
    account_age_days: int | None = None
    successful_payments_to_account: int = 0
    name_match: float = Field(default=1.0, ge=0, le=1)
    personal_account_for_business: bool = False
    amount_vs_account_capacity: float = 1.0
    provenance: Provenance = "verified_registry"
    lookalike_domain: bool = False
    urgency_cues: bool = False
    payer_sim_swap_72h: bool = False
    payer_new_device_24h: bool = False
    session_country_unusual: bool = False
    account_region: str | None = None
    supplier_region: str | None = None
    region_mismatch: bool = False
    account_near_border: bool = False
    wallet_region_mismatch: bool = False
    impossible_travel: bool = False
    regional_fraud_wave: bool = False
    amount_eur: float = 0
    amount_vs_history_ratio: float = 1.0
    unusual_hour: bool = False
    velocity_24h: int = 0
    fanout_wallets: int = 0
    minutes_credit_to_forward: float | None = None
    shared_cashout_agents: int = 0
    young_fast_cluster: bool = False
    just_below_cap_count: int = 0
    declared_split: bool = False
    norm_r1: bool = False
    sanctions_hit: bool = False
    linked_confirmed_fraud: bool = False
    supplier_contact_sim_swap_7d: bool = False
