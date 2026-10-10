# Tâches — Devin (back-end : API, orchestration, normes, routage, chaîne, agent)

> **Mission** : faire tourner le cerveau du produit — recevoir un paiement, appliquer les normes, appeler le risque, choisir la route, faire approuver, signer, parler à la chaîne, piloter les adaptateurs et la réponse, émettre tous les événements que la console dessine.
> **Pourquoi c'est critique** : c'est le chemin critique et la colle entre tout le monde. Si le back ne tourne pas, aucune scène ne tourne.
> **PRD v4** : §6, §9, §11, §12, §13.4–13.5, §13.8, §14, §15, §16, §19, §20.
> **Dossiers** : `/api`, `/shared`, `/scripts`, `Makefile`, `.env.example`.

Ce fichier sert surtout aux humains : savoir **ce que Devin livre, quand, et ce dont il a besoin**.

## 1. Livraisons

| # | Quand | Livraison | Débloque |
|---|---|---|---|
| 1 | 21:15 | Squelette du monorepo (`/api`, `/ml`, `/web`, `/contracts`, `/shared`, `/scripts`, `/docs`), `Makefile`, `.env.example`, `.gitignore` | Tout le monde |
| 2 | **22:00** | **Interfaces** : `shared/types.py` + `types.ts` (§16.1), `shared/events.md`, `shared/fixtures/scene1.json`, `scene2.json`, `events-scene1/2/2b.jsonl`, `RiskContext` validé avec Oscar, format des scénarios d'intégrité | Talal (faux flux), Oscar (contexte) |
| 3 | 22:15 | Vérification du vecteur EIP-712 de Youssef avec `eth-account` | Youssef, signer |
| 4 | 22:00–01:00 | **Pipeline scène 1** : `POST /v1/payments` → registre bénéficiaires + provenance + name check → **normes** (`api/profiles/FR.yaml`, `GH.yaml`, `api/packs/FR-GH.yaml`, évaluateur ; règles du §9.3 ; notices fiscales du §9.4) → `ml.score` (règles seules) → **routeur** (R1–R4, éligibilité par niveau, score S du §11.3, fraude exclue du score, raison en une ligne, « prix de la sécurité ») → approbation Claire (+ Marc ≥ 20 k€) → **signer EIP-712** (une clé par rôle) → **client chaîne** (2 RPC, refus si chainId ≠ 43113, attente des reçus ; Anvil puis Fuji) → `commit` → adaptateur R3 (vérifie intent hash, fenêtre, nonce, statut registre, clé d'idempotence) → règlement simulé → journal hash-chaîné → **SSE `/v1/stream`** | **CP1 01:00** |
| 5 | 01:00–03:30 | **Scène 2** : règle R-PV-01 (approbation bloquée), escrow `deposit`, mock SIM swap (forme CAMARA) sur le numéro **connu** de Kwame, demande hors bande, `/payees/{id}/verify` → `recordVerification`, cas analyste, `REVOKE` → `revoke` → `refund`, alerte banque bénéficiaire (UETR + gel) ; **agent enquêteur Mistral** (dossier cité, ≤ 120 mots, brouillon TRACFIN ; chaque phrase cite un `ruleId`/`signalId`, validateur de citations, température 0, timeout 10 s → explication construite depuis les règles ; réponses des scènes en cache étiquetées) | **CP2 03:30** |
| 6 | 03:30–05:00 | **Scène 2b** : `/sim/attack/A` (`release` après révocation, tx forcée pour être visible), `/B` (bénéficiaire changé → adaptateur refuse + `deposit` revert `CommitmentMismatch` + **kill switch**), `/C` (rejeu → nonce consommé ; décision réécrite en « LOW » → chaîne de hash cassée → `log.tampered`) ; **mode dégradé** ; `make eval-integrity` (300 scénarios I1–I3 → taux de détournement = 0) ; `/v1/metrics` ; `/sim/reset` ; si CP2 vert : scène 3 (grappe de mules + coupe-circuit régional) | Freeze 05:00 |
| 7 | 05:00 | `make demo` en une commande, README à jour | Vidéo, répétitions |

## 2. Ce dont Devin a besoin (et de qui)

| Quoi | De qui | Quand |
|---|---|---|
| Clés privées de test (relayer, router, verifier, analyst) + RPC Fuji, **en message privé** (ou ajoutées comme secrets Devin) | Youssef | 22:00 au plus tard |
| `shared/eip712_vector.json` | Youssef | 22:00 |
| `contracts/deployments/fuji.json` + ABI (`contracts/out`) | Youssef | 01:00 (Anvil avant) |
| `ml/score.py` règles seules, puis modèle | Oscar | 23:00, puis 03:30 |
| Script de démo et textes (e-mail, SMS, TRACFIN) | Omama | 22:00 / 23:00 |
| Décision MockEURC vs Circle EURC | Équipe (kick-off) | 21:15 |

## 3. Garde-fous que le back applique (PRD §6.3, §20)

- Nouveau bénéficiaire ou coordonnées changées depuis une source non fiable → **jamais LOW**, approbation bloquée jusqu'à vérification hors bande.
- Toute dépendance en panne (LLM, RPC, modèle) → plus strict, bannière `mode.degraded`, **rien n'est libéré par défaut**.
- Aucune alerte payeur par e-mail ; jamais de tipping-off ; aucun agent ne tient de clé de signature.
- Rien de personnel on-chain : coordonnées en hash salé.
- Décision p95 < 300 ms (chaîne, approbation, vérification et agents passent **après** la décision).
