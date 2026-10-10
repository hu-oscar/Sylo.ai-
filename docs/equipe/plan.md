# Plan de nuit à 5 — sam. 21:00 → dim. 06:00

> À lire par toute l'équipe (5 min). Ensuite, chacun ouvre **son** fichier `taches-<prénom>.md`.
> Référence : [`prd-final-v4.md`](../../prd-final-v4.md). Ce plan **remplace le §21 du PRD**, qui supposait un freeze dimanche 12:00.

## 1. Pourquoi ce plan

- Il nous reste **9 h**. Le P0 du PRD fait **29,5 h·p** (heures-personne).
- À 5 (4 humains + Devin qui prend tout le back-end), on a environ **4 × 7 h = 28 h·p humaines** + le back-end en parallèle. Ça passe, **à condition de ne faire que le P0** et de figer les interfaces tôt.
- **Tout le P1 est gelé** (globe, eERC, guardian, panne de rail, pack Lagos, Jev, agent d'intake). Seule exception : si le checkpoint de 03:30 est vert, on ajoute la **scène 3** (réseau de mules + coupe-circuit).

## 2. Qui fait quoi, et pourquoi

| Qui | Mission en une phrase | Modules PRD (§8) | Pourquoi cette personne |
|---|---|---|---|
| **Devin** | Faire tourner tout le cerveau du produit : recevoir un paiement, appliquer les normes, appeler le risque, choisir la route, signer, parler à la chaîne, émettre les événements | M1, M2, M5, M7, M8, M9, scripts | C'est le chemin critique et la colle entre tout le monde ; un agent peut produire vite beaucoup de code back testé |
| **Talal** | Rendre la démo lisible sans narration : le jury doit *voir* le paiement passer, être bloqué, et les attaques échouer | M10 | Ton goût UI (minimaliste, motion) et la démo est 15 % de la note + elle porte la détection/réponse |
| **Youssef** | Rendre la preuve infalsifiable et visible sur un explorer public | M6, M12 (+ vecteur EIP-712, déploiement Fuji) | Auteur du PRD D (EIP-712, escrow, attestations) : réponse directe au mentor |
| **Oscar** | Produire des chiffres de détection crédibles et reproductibles | M3, M4, M11 | Auteur du PRD B (signaux géographiques, protocole seeds A/B) : 30 % de la note = détection |
| **Omama** | Transformer le produit en note : pitch, livrables exigés, contenu des scènes, liaison mentors, contrôle qualité | Livrables §12, §18, §22 + QA | Les livrables (playbook, slide conformité, fiche défense) sont notés (conformité 15 %, pitch 15 %) et personne d'autre n'a le temps de les faire bien |

## 3. Le P0 allégé pour tenir

| Module | Version nuit (ce qu'on simplifie) |
|---|---|
| M3 Données | 20 000 paiements au lieu de 150 000 ; T1 (BEC) + T3 (mules) complets, T2/T4 réduits ; bruit honnête ≈ 3 % ; 300 attaques d'intégrité I1–I3 |
| M4 Risque | LightGBM + calibration isotonic ; raisons via `pred_contrib=True` (pas besoin de SHAP) |
| M6 Contrats | Tests unitaires des happy paths + des 3 reverts de la scène 2b ; fuzz/invariants si temps |
| M8 Orchestration | Mode dégradé = bannière + « rien n'est libéré » ; double contrôle = 2e approbation « Marc » |
| M9 Enquêteur | Mistral live, mais dossiers des scènes **pré-générés et cachés** (étiquetés « cached ») pour que la démo ne dépende pas du réseau |
| M10 Console | Une seule page, 6 zones ; les chiffres vont sur une slide et un petit encart |

**Never cut** : normes FR-GH avec exclusion R4 · approbation bloquée sur coordonnées non fiables · intention sur Fuji · adaptateurs qui refusent les écarts · escrow + vérification + révocation + remboursement · scènes 1, 2, 2b · chiffres mesurés · playbook + slide conformité.

## 4. Comment on travaille en parallèle sans s'attendre

1. **21:15–22:00 : on fige les interfaces** dans `/shared` (types, événements, fixtures, vecteur EIP-712) — voir README §7. Après 22:00, plus personne n'attend personne :
   - Talal code la console contre un **faux flux** d'événements (`shared/fixtures/events-scene*.jsonl`).
   - Oscar travaille sur ses propres données ; Devin utilise une version « règles seules » de `score()` dès 23:00.
   - Youssef teste sur Anvil (chaîne locale) en attendant Fuji ; Devin branche le client chaîne sur Anvil puis Fuji.
2. **Un dossier par personne** (`/api`, `/web`, `/contracts`, `/ml`, `/docs`) → pas de conflits Git. Seul Devin touche `/shared` et le `Makefile`.
3. **Un seul canal d'équipe**, trois types de messages seulement : « ✅ fait : … », « 🔴 bloqué : … (depuis X min) », « ⚠️ j'ai changé l'interface : … ».
4. **Bloqué plus de 30 min → on le dit.** On n'attend pas le checkpoint.

## 5. Planning

| Heure | Devin | Talal | Youssef | Oscar | Omama |
|---|---|---|---|---|---|
| 21:00–21:15 | Squelette repo, Makefile, `.env.example` | Init Next.js dans `/web` | Wallets Fuji, init Foundry | Init `/ml`, lire §10 et §17 | **Mentor Avalanche : coupon AVAX test** ; heures exactes du freeze et du jury |
| 21:15–22:00 | **Interfaces `/shared`** | Maquette des 6 zones | **Vecteur EIP-712** | Schéma `RiskContext` avec Devin | Script de démo minute par minute |
| 22:00–01:00 | Pipeline scène 1 de bout en bout | Console scène 1 sur faux flux | Registry + Escrow + tests ; déploiement Fuji | Simulateur seedé ; `score()` règles seules à 23:00 | Contenu scène 2 (e-mail, facture, SMS) ; squelette du deck |
| **01:00** | **Checkpoint 1** (15 min, tous) : scène 1 de bout en bout, intention visible sur Snowtrace | | | | |
| 01:00–03:30 | Scène 2 : séquestre, SIM swap, hors bande, révocation, remboursement, dossier Mistral | Scène 2 : téléphones, file analyste, panneau preuve | Scripts d'attaque A/B/C ; aide intégration | Entraînement seed A, calibration, raisons, seuils | Playbook, slide conformité, fiche défense |
| **03:30** | **Checkpoint 2** : scène 2 complète, modèle branché | | | | |
| 03:30–05:00 | Scène 2b, kill switch, journal falsifié détecté ; (scène 3 si vert) | Console d'attaque, polish, encart chiffres | Reverts 2b sur Fuji, vérif des contrats sur l'explorer | Éval seed B, ablations, `metrics.json`, model card | QA des scènes, test « temps analyste », deck avec vrais chiffres |
| **05:00** | **CODE FREEZE** — plus aucune feature, seulement des bugs bloquants | | | | |
| 05:00–05:30 | 2 runs complets de la démo + **vidéo de secours** (Talal + Omama) | | | | |
| 05:30–06:00 | 2 répétitions du pitch de 4 min ; Q&A avec PRD §22.3 | | | | |

## 6. Règles de décision aux checkpoints (2 min, pas de débat)

- **CP1 rouge côté chaîne** → Youssef ne fait plus que Fuji ; la démo tourne sur Anvil en attendant ; si Fuji n'est pas là à 03:30, on garde Anvil pour le live et on montre des tx Fuji pré-enregistrées.
- **CP2 : modèle pas prêt** → règles + régression logistique (cut list du PRD), Oscar bascule sur l'éval.
- **CP2 : Mistral instable** → dossiers en cache uniquement, étiquetés « cached ».
- **Console en retard** → on garde le fil texte + le panneau preuve + la console d'attaque ; tout le reste est secondaire.
- **Personne ne commence un P1 avant que CP2 soit vert.**

## 7. Décisions encore ouvertes (à trancher au kick-off)

1. 06:00 = code freeze ou démo/vidéo prêtes ? Heure du jury ? (Omama confirme auprès des organisateurs.)
2. Qui présente le pitch ? (proposition : Omama + Talal en démo live)
3. **Token** : Circle EURC sur Fuji (le faucet donne de petits montants, à vérifier) ou **MockEURC** déployé par nous, 85 000 unités, étiqueté « simulé ». Proposition par défaut : MockEURC.
4. Route R3 légale pour des recettes d'export ? (question aux mentors KPMG, PRD §9.3 ; le pack a un drapeau pour la désactiver.)
