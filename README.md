# Sylo.ai

> **La route la moins chère et conforme quand tout va bien. Une fenêtre pour arrêter l'argent quand quelque chose cloche.**

Projet de l'équipe au hackathon **Secure Horizons** (ESSEC Cergy, 10–11 octobre 2026), **Track 1 — Fintech Security: Guardians of Value** (Track 1 uniquement, confirmé par le mentor).

- 📄 **Référence unique : [`prd-final-v4.md`](./prd-final-v4.md)** (PRD fusionné v4, en anglais). En cas de doute, le PRD v4 fait foi.
- 🧾 Ce qui a été gardé/rejeté des 4 PRD sources : [`prd-merge-recap.md`](./prd-merge-recap.md). `prd-final.md` (v3) est **historique** : ne plus s'en servir.
- 👥 Répartition de la nuit et tâches de chacun : [`docs/equipe/`](./docs/equipe/) (commencer par [`plan.md`](./docs/equipe/plan.md)).

> **Pour les agents IA (Devin, Claude, Cursor, Copilot…)** : lisez ce README en entier, puis le fichier de tâches de la personne pour qui vous travaillez (`docs/equipe/taches-<prénom>.md`), puis les sections du PRD v4 qu'il cite. Respectez les **interfaces partagées** (§7) et ne modifiez pas les dossiers des autres (§6). Tout ce qui est simulé doit être **étiqueté « simulé »** dans l'interface. Jamais de secret dans le dépôt.

---

## 1. Le problème (en 4 phrases)

Un paiement d'entreprise **Lyon → Accra** traverse plusieurs institutions qui ne partagent pas ce qu'elles voient (banque française, prestataire de paiement ou CASP crypto, banque ghanéenne, mobile money). La fraude la plus coûteuse pour les entreprises est **l'usurpation de fournisseur (BEC)** : un faux e-mail « nos coordonnées bancaires ont changé » détourne le paiement d'une facture vers un **compte de mule**, vidé en quelques minutes. Les moteurs anti-fraude des banques la ratent parce que **c'est le vrai client qui autorise le paiement**. En Europe, la vérification du nom du bénéficiaire (VoP) **s'arrête à la frontière SEPA**, et au Ghana les banques n'ont récupéré qu'environ **5 %** des montants fraudés en 2025.

## 2. La solution

Sylo.ai est une **couche de décision et de contrôle au-dessus de rails de paiement agréés**. Elle ne détient pas les fonds. Avant que l'argent ne bouge, chaque paiement suit cet ordre (PRD §6.2) :

```
1. NORMES   ne garder que les routes légales dans les deux pays (la règle la plus stricte gagne)
2. RISQUE   score de fraude → niveau (LOW / MEDIUM / HIGH / CRITICAL) → restreint les routes autorisées
3. COÛT     meilleure route restante (frais, change, délai, probabilité d'échec, risque opérationnel du rail)
4. COMMIT   intention approuvée (bénéficiaire, montant, décision) signée en EIP-712 et enregistrée sur Avalanche Fuji
5. ACTION   exécuter / régler sous condition (séquestre ou retenue) / retenir pour un analyste / bloquer et déclarer
```

**Principe directeur** : l'intention approuvée par le payeur est la source de vérité ; chaque composant ne peut que la restreindre ou la vérifier. *Les modèles proposent, les règles disposent, les humains décident.*

**Deux risques séparés** : le **risque de fraude** (du paiement) décide si l'argent peut partir et par quelles routes ; le **risque de route** (panne, connecteur compromis) n'aide qu'à choisir le rail. **Le risque de fraude n'entre jamais dans le score de coût.**

| Niveau | Réponse (PRD §12.1) |
|---|---|
| LOW (0–39) | Commit + exécution sur la meilleure route |
| MEDIUM (40–69) | Commit + **séquestre on-chain** (route R3) ou retenue fiat (R1) ; contrôle SIM swap puis vérification **hors bande** sur le contact **déjà connu** du fournisseur ; libération si confirmé, révocation + remboursement si refusé, remboursement auto à 24 h |
| HIGH (70–89) | Aucune route, approbation bloquée, dossier d'enquête, l'analyste décide |
| CRITICAL (90–100) | Blocage, demande de gel à la banque bénéficiaire, brouillon de déclaration de soupçon (jamais de « tipping-off ») |

**Garanties** : pas de substitution (chaque adaptateur de rail recalcule le hash de l'intention et refuse tout écart ; le contrat d'escrow revert) · pas de rejeu (nonces) · journal hash-chaîné · l'IA ne libère jamais de fonds · si une dépendance tombe, le système devient **plus strict**, jamais plus laxiste.

## 3. La démo (ce que le jury voit)

Corridor **France → Ghana**. Claire (CFO de Rhône Cosmétiques, Lyon) paie la facture SSE-2026-118 de **85 000 €** à Savanna Shea Exports (beurre de karité, Tamale/Tema). Kwame est le contact connu du fournisseur ; Julien est l'analyste fraude de la banque de Claire ; Marc co-approuve au-dessus de 20 000 €.

| Scène | Prio | Ce qui se passe | Preuve visible |
|---|---|---|---|
| **1 — Le paiement légitime passe** (≈ 40 s) | P0 | Normes : R4 (mobile money) exclue par la règle ghanéenne sur les recettes d'export ; risque LOW ; R3 (EURC via CASP UE + VASP ghanéen) choisie ; Claire + Marc approuvent ; commit puis règlement | `PaymentCommitted` sur Snowtrace |
| **2 — La facture détournée est stoppée** (≈ 80 s) | P0 | E-mail lookalike `savanna-shea.com` → nouveau compte « K. MENSAH VENTURES » à Aflao. Approbation bloquée → MEDIUM (≥ 3 raisons citées) → R3 + séquestre → contrôle SIM swap → Kwame refuse sur son téléphone → Julien révoque → remboursement ; dossier Mistral cité en < 60 s | `PaymentCommitted` → `Deposited` → `VerificationRecorded(DENIED)` → `PaymentRevoked` → `Refunded` |
| **2b — Le jury essaie de tricher** (≈ 25 s) | P0 | Console d'attaque à 3 boutons : **A** libérer le paiement révoqué ; **B** changer le bénéficiaire en transit ; **C** rejouer / réécrire une décision | Tx en échec sur l'explorer, refus dans le fil, bannière rouge de hash |
| 3 — Le réseau de mules + coupe-circuit régional | P1 | Seulement si le checkpoint 03:30 est vert | — |
| 4, 5 — Guardian on-chain, panne de rail | P1 | Pas cette nuit | — |

**Chiffres affichés** (seed B jamais vue à l'entraînement) : rappel, précision au niveau HIGH, taux de faux positifs, temps de détection, temps analyste gagné, **taux de détournement = 0** sur les attaques d'intégrité. Coûts et délais = **illustratifs** (rails simulés).

## 4. Périmètre de cette nuit (sam. 21:00 → dim. 06:00)

- **P0 uniquement** (PRD §4.2, §8 modules M1–M12), en version allégée (voir [`docs/equipe/plan.md`](./docs/equipe/plan.md)).
- **Never cut** : normes FR-GH avec exclusion R4 ; approbation bloquée sur coordonnées non fiables ; intention sur Fuji ; adaptateurs qui refusent les écarts ; escrow + vérification + révocation + remboursement ; scènes 1, 2, 2b ; chiffres mesurés ; playbook + slide conformité.
- **Hors périmètre** : vrais rails, vraies données, vraies vérifications d'identité, détention de fonds, app grand public, calcul fiscal (la fiscalité est **affichée** en information, jamais calculée), globe 3D, eERC, L1 dédiée, Jev.
- **Freeze code : 05:00.** 05:00–06:00 : vidéo de secours + répétitions.

## 5. Architecture

```
            Ordre de paiement (JSON façon pacs.008) + facture/e-mail (fixtures)
                                      │
┌──────────────────────────── API Sylo.ai (/api, FastAPI) ─────────────────────────────┐
│ Intake + registre bénéficiaires + provenance + name check                            │
│   → Normes (profils FR/GH + pack FR-GH en YAML)                                      │
│   → Risque (/ml : features + règles R-* + LightGBM calibré + top raisons)            │
│   → Routeur (éligibilité par niveau + score S, fraude exclue du score)               │
│   → Approbation (Claire, + Marc ≥ 20 k€) → Signer EIP-712 → Orchestrateur            │
│   → Adaptateurs R1–R4 simulés (vérifient intent hash, nonce, statut on-chain)         │
│   → Réponse (4 niveaux, kill switch, mode dégradé) → Journal hash-chaîné → flux SSE   │
│   Agent enquêteur (Mistral) : dossier cité + explication ≤ 120 mots (après décision) │
└───────────────┬──────────────────────────────────────────────┬───────────────────────┘
                │ web3.py                                        │ SSE GET /v1/stream
     ┌──────────▼──────────┐                         ┌───────────▼───────────────┐
     │ Avalanche Fuji       │                         │ Console (/web, Next.js)   │
     │ PaymentRegistry      │                         │ payeur · fil · analyste · │
     │ PaymentEscrow        │                         │ preuve · attaques · tél.  │
     │ MockEURC (à confirmer)│                        └───────────────────────────┘
     └──────────────────────┘
Monde simulé : annuaire + banque nominée, télécom (SIM swap), canal hors bande (téléphones), rails, générateur de données.
```

Séquence MEDIUM détaillée : PRD §15.2. Événements : PRD §15.3.

| Couche | Choix |
|---|---|
| API, normes, orchestration, signature | Python 3.12, FastAPI (SSE natif), Pydantic, `eth-account` (EIP-712), `web3.py` |
| Règles et profils | YAML + petit évaluateur Python |
| ML | scikit-learn / LightGBM, NetworkX |
| Stockage | En mémoire / SQLite (un fichier, reset en une commande) |
| Contrats | Solidity 0.8.x, Foundry, OpenZeppelin 5 ; réseau **Fuji C-Chain (chainId 43113)** ; Anvil en local pour le dev uniquement |
| Console | Next.js (App Router), TypeScript, Tailwind, framer-motion |
| LLM | Mistral (client agnostique, sortie JSON, cache de réponses) |

## 6. Structure du dépôt et propriétaires

| Dossier | Contenu | Propriétaire |
|---|---|---|
| `/api` | FastAPI : intake, registre, normes (`api/norms/`), routeur, approbation, orchestrateur, adaptateurs (`api/adapters/`), réponse, journal, signer et client chaîne (`api/chain/`), flux SSE, agent enquêteur (`api/agents/`) | **Devin** |
| `/api/profiles`, `/api/packs` | `FR.yaml`, `GH.yaml`, `FR-GH.yaml` | **Devin** (relecture juridique : Youssef) |
| `/shared` | Types, liste d'événements, fixtures des scènes, vecteur de test EIP-712 | **Devin** (le vecteur : Youssef) |
| `/contracts` | Foundry : `PaymentRegistry.sol`, `PaymentEscrow.sol`, `MockEURC.sol`, tests, scripts de déploiement, `deployments/fuji.json` | **Youssef** |
| `/ml` | Simulateur seedé, features, règles, modèle, calibration, évaluation, `score.py`, `metrics.json` | **Oscar** |
| `/web` | Console Next.js | **Talal** |
| `/docs` | Playbook, slide conformité, fiche défense, model card, script de démo, deck | **Omama** (+ chacun pour sa partie) |
| `/scripts`, `Makefile` | Lancement démo, reset, attaques, éval | **Devin** |

Règle : on ne modifie pas le dossier d'un autre sans lui dire. Un changement d'interface (§7) = message à toute l'équipe **avant** de pousser.

## 7. Interfaces partagées (le contrat entre les modules)

Figées à **22:00**. Ce sont elles qui permettent de travailler en parallèle.

| Interface | Où | Produit par → utilisé par |
|---|---|---|
| Types `PaymentOrder`, `Payee`, `Decision`, `PaymentLeg`, `LogEntry` (PRD §16.1) | `shared/types.py`, `shared/types.ts` | Devin → tous |
| Liste des événements SSE + exemple de payload pour chacun | `shared/events.md` | Devin → Talal |
| Flux d'événements attendus par scène (sert de **mock front** et de **test d'acceptation back**) | `shared/fixtures/events-scene1.jsonl`, `events-scene2.jsonl`, `events-scene2b.jsonl` | Devin → Talal |
| Données des scènes : ordres, registre bénéficiaires, compte mule, mocks télécom/annuaire | `shared/fixtures/scene1.json`, `scene2.json` | Devin → tous |
| Vecteur EIP-712 : domaine + un `PaymentIntent` + digest attendu | `shared/eip712_vector.json` | Youssef → Devin (Foundry et `eth-account` doivent donner le même hash) |
| Adresses, ABI, URL explorer | `contracts/deployments/fuji.json` | Youssef → Devin, Talal |
| Fonction de risque | `ml/score.py` : `score(order: dict, ctx: dict) -> dict` | Oscar → Devin |
| Chiffres du pitch | `ml/metrics.json` (seed B) | Oscar → Talal, Omama |

**Enveloppe d'un événement SSE** (tous les événements) :

```json
{ "id": 42, "type": "risk.scored", "ts": "2026-10-11T00:12:03.120Z",
  "paymentId": "pay_scene2", "uetr": "…", "scene": "2",
  "data": { … }, "explorerUrl": null }
```

Types d'événements (PRD §15.3) : `norms.checked`, `risk.scored`, `route.selected`, `approval.required`, `approval.granted`, `intent.committed`, `escrow.deposited`, `simswap.checked`, `oob.requested`, `verification.recorded`, `intent.revoked`, `escrow.refunded`, `escrow.released`, `leg.sent`, `leg.settled`, `leg.rejected`, `alert.raised`, `case.ready`, `killswitch.on`, `tx.reverted`, `log.tampered`, `mode.degraded`.

**API** (`http://localhost:8000/v1`, JSON, en-tête `Idempotency-Key` sur les POST) — PRD §16.2, plus les routes de pilotage de la démo :

| Méthode | Chemin | Rôle |
|---|---|---|
| POST | `/payments` | Soumettre un ordre → décision, approbations et vérifications requises |
| POST | `/payments/{id}/approve` | Approbation payeur (`{"by":"claire"}` puis `{"by":"marc"}` si double contrôle) |
| GET | `/payments/{id}` | Statut jambe par jambe, statut registre, liens explorer |
| GET | `/payments/{id}/proof` | Données EIP-712, signatures, événements, recalcul pour l'auditeur |
| POST | `/payees/{id}/verify` | Réponse hors bande de Kwame (`{"result":"DENIED"}` ou `"CONFIRMED"`) |
| GET, POST | `/cases`, `/cases/{id}/actions` | File analyste ; `CONFIRM` / `REVOKE` / `REFUND` / `FREEZE` / `ESCALATE` / `REPORT` |
| POST | `/sim/scene/{n}` | Lancer la scène 1 ou 2 (crée l'ordre depuis les fixtures) |
| POST | `/sim/attack/{A\|B\|C}` | Boutons de la console d'attaque (scène 2b) |
| POST | `/sim/reset` | Remettre la démo à zéro |
| GET | `/stream` | Flux SSE (reprise via `Last-Event-ID`) |
| GET | `/metrics` | Contenu de `ml/metrics.json` |

## 8. Lancer le projet

> Prévu pour la nuit ; les commandes deviennent réelles au fil des pushes (voir le statut dans `docs/equipe/plan.md`).

Prérequis : Python 3.12, Node 20+ et pnpm, Foundry (`curl -L https://foundry.paradigm.xyz | bash && foundryup`).

```bash
cp .env.example .env          # remplir : MISTRAL_API_KEY, RPC Fuji, clés de rôle (jamais committées)
make setup                    # dépendances api + ml + web + contracts
make data SEED=A && make train && make eval SEED=B   # régénère ml/metrics.json
make demo                     # API sur :8000 + console sur :3000
make reset                    # remet la démo à zéro
cd contracts && forge test    # tests des contrats
```

Variables d'environnement (`.env`, gitignoré) : `MISTRAL_API_KEY`, `FUJI_RPC_URL`, `FUJI_RPC_URL_2`, `RELAYER_PRIVATE_KEY`, `ROUTER_PRIVATE_KEY`, `VERIFIER_PRIVATE_KEY`, `ANALYST_PRIVATE_KEY`, `NEXT_PUBLIC_API_URL=http://localhost:8000`, `NEXT_PUBLIC_MOCK=1` (console sur faux flux).

## 9. Conventions

- **Langue** : docs en français, code et identifiants en anglais, noms d'événements/règles identiques au PRD (`R-FL-01`, `GH_FX_EXPORT_PROCEEDS_NOMINATED_BANK`, …).
- **Git** : petits commits, `git pull --rebase` avant de pousser sur `main` ; branche seulement pour un gros changement. Messages : `api: …`, `web: …`, `ml: …`, `contracts: …`, `docs: …`.
- **Secrets** : uniquement dans `.env` ; les clés privées Fuji circulent en message privé, jamais dans le dépôt ni dans un chat de groupe.
- **Honnêteté** : tout ce qui est simulé porte un badge « simulé » ; les réponses LLM en cache portent « cached » ; aucun chiffre du pitch n'est écrit à la main (tout sort de `ml/metrics.json`).
- **Fail-safe** : une dépendance en panne (LLM, RPC, modèle) → mode dégradé plus strict + bannière ; rien n'est libéré par défaut.

## 10. Glossaire

| Terme | Sens |
|---|---|
| **BEC** | *Business Email Compromise* : usurpation par e-mail (ici, faux fournisseur) |
| **Mule** | Compte qui reçoit l'argent fraudé et le fait sortir vite (ici vers 6 wallets mobile money, cash-out près de la frontière togolaise) |
| **Hors bande (OOB)** | Vérification par un autre canal que celui de la demande : on appelle le contact **déjà connu** du fournisseur, jamais celui donné dans l'e-mail |
| **SIM swap** | Le fraudeur récupère le numéro de la victime ; on le vérifie (API CAMARA simulée) avant de faire confiance au téléphone de Kwame |
| **Provenance** | D'où vient chaque coordonnée : `verified_registry` (fiable) vs `invoice_pdf_email` (non fiable) |
| **Route R1–R4** | R1 SWIFT · R2 prestataire SEPA Instant + payout GHS · R3 EURC sur Avalanche via CASP UE + VASP ghanéen (séquestre possible) · R4 mobile money (exclue pour les recettes d'export) |
| **Signal de norme R1–R4** | ⚠️ À ne pas confondre avec les routes : R1 = recettes d'export versées hors banque nominée (P0) ; R2–R4 en P1 (PRD §9.3) |
| **EIP-712** | Standard de signature de données typées : le hash d'un `PaymentIntent` est le même en Python et en Solidity, et le contrat vérifie qui a signé |
| **Escrow / séquestre** | Le contrat `PaymentEscrow` garde les EURC ; `release` n'est possible que si le registre dit `CONFIRMED` ; sinon remboursement |
| **UETR** | Identifiant unique de bout en bout d'un paiement ISO 20022 ; présent dans chaque événement |
| **pacs.008** | Message ISO 20022 de virement ; notre ordre JSON en reprend la forme |
| **SSE** | *Server-Sent Events* : flux unidirectionnel serveur → navigateur ; la console ne fait que dessiner ces événements |
| **Seed A / seed B** | Deux générations indépendantes du jeu synthétique : A pour entraîner/régler, B (jamais vue) pour les chiffres du pitch |
| **Calibration** | Transformer la sortie du modèle en vraie probabilité (isotonic), affichée en score 0–100 |
| **Kill switch** | Coupure d'un connecteur de rail compromis après des refus répétés |
| **Tipping-off** | Prévenir la personne visée par une déclaration de soupçon : interdit |

## 11. Équipe

| Qui | Rôle cette nuit | Tâches |
|---|---|---|
| **Devin** (agent IA) | Back-end : API, orchestration, normes, routage, signer, SSE, agent Mistral, intégration | [`taches-devin.md`](./docs/equipe/taches-devin.md) |
| **Talal** | Front-end : console de démo | [`taches-talal.md`](./docs/equipe/taches-talal.md) |
| **Youssef** | Chaîne : contrats, Fuji, vecteur EIP-712, attaques on-chain | [`taches-youssef.md`](./docs/equipe/taches-youssef.md) |
| **Oscar** | Données, risque, évaluation | [`taches-oscar.md`](./docs/equipe/taches-oscar.md) |
| **Omama** | Pitch, livrables, contenu de démo, mentors, QA | [`taches-omama.md`](./docs/equipe/taches-omama.md) |

## 12. Statut et limites

Preuve de concept de hackathon : **tous les rails, flux, comptes et contrôles d'identité sont simulés**, aucune donnée réelle. Seuls les indicateurs de sécurité sont mesurés ; coûts et délais sont illustratifs. Questions ouvertes : PRD v4 §25.
