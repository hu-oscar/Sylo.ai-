# Tâches — Youssef (chaîne : contrats, Fuji, preuve on-chain)

> **Ta mission** : rendre chaque paiement **infalsifiable et vérifiable par un tiers** sur un explorer public, et faire échouer en direct les tentatives de triche de la scène 2b.
> **Pourquoi c'est critique** : c'est la réponse directe au mentor (immutabilité, attestations, avant/après révocation) et le moment fort du pitch (« appuyez sur un bouton et essayez de tricher »).
> **À lire dans le PRD v4** : §13.1–13.4 (contrats, EIP-712, autorité), §13.8 (RPC), §7.4 (scène 2b), §7.8 (carte des preuves), §19 (menaces).
> **Dossier** : `/contracts` (Foundry). Tu écris aussi **un** fichier dans `/shared` : `shared/eip712_vector.json`.

## 1. Ce qu'il faut comprendre (5 min)

- **Rien de personnel on-chain** : seulement des hash (bénéficiaire et coordonnées en hash **salé**), des statuts, des signatures et, pour la route R3, les tokens en séquestre.
- **Qui signe** : ce n'est pas Claire (elle n'a pas de wallet). Ce sont les **services de la banque** : clé *router* (signe l'intention), clé *verifier* (signe le résultat de la vérification hors bande), clé *analyst* (signe la révocation). Le contrat vérifie la signature EIP-712 contre l'adresse de chaque rôle, fixée au déploiement.
- **Qui paie le gas** : un seul **relayer** (le back de Devin) envoie toutes les tx ; c'est la **signature** dans les données qui compte, pas `msg.sender` (sauf pour les fonctions de rôle comme `freeze`). → **Un seul wallet à financer en AVAX.**
- **EIP-712** : le back (Python, `eth-account`) et le contrat (OpenZeppelin `EIP712`) doivent calculer **exactement** le même digest. D'où le **vecteur de test partagé** : c'est le risque n°2 du PRD, à régler en premier.

## 2. Ce que tu construis

**`PaymentRegistry.sol`** (PRD §13.3) — `commit`, `recordVerification`, `revoke`, `markExecuted`, `intentOf`, `statusOf` + les 4 événements. Machine d'états : `NONE → COMMITTED → CONFIRMED | DENIED` ; `COMMITTED | CONFIRMED | DENIED → REVOKED` (final) ; `CONFIRMED → EXECUTED` (MEDIUM) ; `COMMITTED → EXECUTED` (LOW). Toute autre transition revert. Nonce à usage unique (`NonceUsed`). Domaine `{name:"SyloPaymentRegistry", version:"1", chainId, verifyingContract}`. Types exacts du §13.4.

**`PaymentEscrow.sol`** (Mode A, écrit à la main, OZ 5 n'a pas d'escrow) — `deposit(intent, payer)` (revert `CommitmentMismatch` si bénéficiaire/montant/token ≠ intention enregistrée), `release` (revert `PaymentNotReleasable` sauf si `CONFIRMED`, et si gelé/expiré/en pause), `refund` (analyste à tout moment ; n'importe qui si `REVOKED` ou expiré), `freeze`, `pauseCorridor` + événements. Expiration 24 h. `ReentrancyGuard`, `SafeERC20`, checks-effects-interactions, pas de retrait admin.

**`MockEURC.sol`** — ERC-20 « Sylo Test EURC (simulé) », 6 décimales, `mint` restreint au déployeur (décision par défaut, voir plan §7 ; si l'équipe choisit Circle EURC Fuji `0x5E44db7996c682E92a960b65AC713a54AD815c6B`, le contrat ne change pas, seule l'adresse du token change).

## 3. Tâches dans l'ordre

| # | Quand | Tâche | Fini quand |
|---|---|---|---|
| 1 | 21:00–21:15 | Créer 5 wallets (deployer/relayer, router, verifier, analyst, payer-treasury). **Demander tout de suite de l'AVAX test** (faucet Core : https://core.app/tools/testnet-faucet — demande un solde mainnet **ou un code coupon** → Omama le demande au mentor Avalanche). Clés privées → message privé à Devin, **jamais** dans le dépôt | Le relayer a de l'AVAX Fuji |
| 2 | 21:15–22:00 | `forge init contracts` + OZ 5 ; écrire le struct `PaymentIntent` et un test qui calcule le digest EIP-712 d'une intention fixe (chainId 43113, adresse de registre fixe) → écrire `shared/eip712_vector.json` : `{domain, types, message, structHash, digest}` | Devin obtient le même digest en Python (il te le confirme) |
| 3 | 22:00–00:00 | `PaymentRegistry` + tests (happy path LOW, happy path MEDIUM, chaque transition interdite revert, signature d'un mauvais rôle revert, nonce rejoué revert) | `forge test` vert |
| 4 | 00:00–01:00 | `PaymentEscrow` + `MockEURC` + tests ; script `script/Deploy.s.sol` → déploiement **Fuji** ; écrire `contracts/deployments/fuji.json` : `{chainId, registry, escrow, token, roles:{router,verifier,analyst,relayer}, explorer:"https://testnet.snowtrace.io"}` ; vérifier les contrats sur l'explorer (Routescan/Snowtrace, commande à vérifier) | **CP1** : un `commit` de test visible sur Snowtrace |
| 5 | 01:00–03:30 | Tests des 3 attaques de la scène 2b, reproduites en Foundry : A `release` après `REVOKED` → `PaymentNotReleasable` ; B `deposit` avec un autre bénéficiaire → `CommitmentMismatch` ; C `commit` rejoué → `NonceUsed`. Aider Devin à brancher `web3.py` (ABI, erreurs custom décodées en texte lisible) | Les 3 reverts passent en test **et** sur Fuji (tx en échec visibles) |
| 6 | 03:30–05:00 | Invariants Foundry du §13.3 (au moins 1, 2, 4, 6) ; relecture juridique rapide des règles `api/packs/FR-GH.yaml` écrites par Devin (contenu de ton PRD) | Invariants verts ; OK sur le pack |
| 7 | 05:00–06:00 | Préparer ta réponse aux questions « Pourquoi une blockchain ? », « Les stablecoins sont publics », « Pourquoi pas une chaîne privée ? » (PRD §22.3) | Tu peux y répondre en 20 s chacune |

## 4. Pièges

- **Tx envoyées pour une attaque qui doit échouer** : `eth_estimateGas` refuse d'envoyer une tx qui revert. Pour que l'échec soit **visible sur l'explorer**, il faut forcer l'envoi avec un `gas` fixé (ex. 300 000). Indique-le à Devin.
- Toujours attendre le reçu de chaque tx (Fuji ≈ 2 s).
- Refuser de démarrer si `chainId ≠ 43113` (c'est dans le client de Devin, mais garde-le en tête dans tes scripts).
- Ne pas mettre de chaîne de caractères personnelle dans les événements.
- eERC, guardian, `DecisionAnchor`, L1 dédiée : **P1/P2, gelés cette nuit.** Si CP2 est vert et que tu as fini : `DecisionAnchor` (le plus simple) seulement.

## 5. Ce que tu attends des autres / ce que tu livres

- **Reçois** : coupon AVAX (Omama) ; confirmation du digest (Devin, ~22:15) ; décision MockEURC vs EURC (kick-off).
- **Livres** : `shared/eip712_vector.json` (22:00), `fuji.json` + contrats vérifiés (01:00), reverts 2b sur Fuji (03:30).
