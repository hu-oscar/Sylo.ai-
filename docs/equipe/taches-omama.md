# Tâches — Omama (pitch, livrables, contenu de démo, mentors, QA)

> **Ta mission** : transformer ce que l'équipe construit en **note** : un pitch de 4 min qui tient, les **livrables exigés par le brief** (playbook de réponse, slide conformité, fiche défense), le contenu réaliste des scènes, et le contrôle qualité de la démo.
> **Pourquoi c'est critique** : conformité (15 %) + pitch (15 %) = 30 % de la note, et le brief exige un **playbook de réponse**. Les 4 autres codent toute la nuit : sans toi, ces livrables seraient faits à 05:30, mal.
> **À lire dans le PRD v4** : §1–3 (problème et chiffres sourcés), §7 (scènes), §12 (playbook), §18 (conformité), §22 (pitch, NIST/ATT&CK, questions préparées), §23 (concurrence et modèle économique).
> **Dossier** : `/docs` (et le deck sur Google Slides/Canva partagé à l'équipe). Tu ne touches pas au code.

## 1. Ce qu'il faut comprendre (10 min)

- **Le cas en une phrase** : un faux e-mail « nos coordonnées ont changé » détourne une facture de 85 000 € de Lyon vers un compte de mule au Ghana ; Sylo.ai le voit avant que l'argent parte, met le paiement sous séquestre, appelle le **vrai** contact du fournisseur, et rembourse — chaque étape prouvée sur la blockchain.
- **Pourquoi les banques le ratent** : c'est le vrai client (Claire) qui autorise le paiement ; la vérification du nom du bénéficiaire (VoP) s'arrête à la frontière européenne.
- **Notre ordre de décision** : normes → risque → coût → commit → action (README §2). C'est la colonne vertébrale du pitch.
- **Ce qui est simulé** : tous les rails et données. On le dit franchement : c'est autorisé par le brief et c'est notre crédibilité.

## 2. Tâches dans l'ordre

| # | Quand | Tâche | Fini quand |
|---|---|---|---|
| 1 | **21:00–21:15** | **Liaison mentors / organisateurs** : (a) mentor Avalanche → **code coupon pour le faucet AVAX Fuji** (Youssef en a besoin tout de suite) ; (b) organisateurs → **heure exacte du code freeze, du passage jury, durée du pitch et format (live ou vidéo)** ; (c) mentors KPMG → « La route stablecoin (EURC via un VASP ghanéen agréé qui crédite la banque nominée) est-elle acceptable pour des recettes d'export au Ghana ? » (PRD §9.3) | Réponses postées dans le canal d'équipe |
| 2 | 21:15–22:00 | **Script de démo minute par minute** `docs/demo/script.md` à partir du §22.1 : qui clique quoi, quelle phrase pendant quel événement, durée de chaque scène | Talal et Devin l'ont lu (ça fixe l'ordre des événements) |
| 3 | 22:00–23:00 | **Contenu des scènes** `docs/demo/contenu.md` : l'e-mail frauduleux (expéditeur `accounts@savanna-shea.com`, ton urgent, « compte en migration »), l'en-tête de la facture SSE-2026-118, les SMS de Kwame et de Claire (**jamais par e-mail**), le texte du brouillon TRACFIN ; en option une image de la facture/e-mail (`docs/demo/assets/`) | Talal et Devin les intègrent |
| 4 | 23:00–01:00 | **Squelette du deck** (≈ 10 slides) : 1 accroche (VoP s'arrête à SEPA, Ghana ≈ 5 % récupéré) · 2 problème BEC · 3 idée (normes → risque → coût → commit) · 4 **démo live** · 5 chiffres (placeholder) · 6 réponse graduée (4 niveaux) · 7 preuve on-chain (avant/après révocation) · 8 **conformité** · 9 marché, concurrence, modèle économique · 10 extension en un fichier + équipe | Squelette partagé |
| 5 | **01:00** | **QA CP1** : rejouer la scène 1 et cocher les critères d'acceptation du §7.2 | Liste des écarts postée |
| 6 | 01:00–02:15 | **Playbook de réponse** `docs/playbook.md` (livrable exigé) : les 4 niveaux (§12.1 : actions automatiques, humaines, qui est alerté, délais, preuves), les surcouches (§12.2), les règles métier (§12.3), qui est responsable si le modèle se trompe (§12.4). Écrit pour un analyste, pas pour un ingénieur | 2 pages max, lisible en 3 min |
| 7 | 02:15–03:30 | **Slide conformité** `docs/conformite.md` (§18.1 : FATF R.16, AML/TRACFIN/FIC, DORA, DSP2, MiCA + travel rule, AI Act, RGPD, lois ghanéennes) + **fiche défense** `docs/fiche-defense.md` (§22.2 NIST CSF 2.0 + MITRE ATT&CK) ; ouvrir les sources citées au pitch (§26 [3], [5]) et vérifier que les chiffres sont exacts | Chaque chiffre du pitch a sa source vérifiée |
| 8 | **03:30** | **QA CP2** : scène 2 contre le §7.3 (MEDIUM ≥ 3 raisons, approbation bloquée, 5 événements on-chain dans l'ordre, SIM swap avant la demande, pas d'e-mail au payeur, dossier cité) | Écarts postés |
| 9 | 03:30–04:15 | **Test « temps analyste »** (§17.3) : 5 cas, 2 testeurs (toi + un mentor ou un autre participant), chronométrés avec et sans le dossier d'enquête ; résultat étiqueté « indicatif » | Chiffre envoyé à Oscar pour `metrics.json` / slide |
| 10 | 04:15–05:00 | Deck final avec les **vrais chiffres** de `ml/metrics.json` ; fiches Q&A (§22.3) réparties : Youssef (blockchain), Oscar (données/modèle), Talal (produit/intégration), toi (conformité/marché) | Deck figé à 05:00 |
| 11 | 05:00–05:30 | Vidéo de secours avec Talal ; chronométrer | MP4 ≤ 3 min |
| 12 | 05:30–06:00 | 2 répétitions chronométrées (4 min pile), puis 5 min de questions pièges | Tout le monde sait sa réplique |

## 3. Pièges

- Ne jamais présenter un coût ou un délai comme réel : « illustratif, rails simulés ».
- Ne pas dire « personne ne fait ça » : la concurrence est au §23 (Wise, Airwallex, Circle CPN, PAPSS, CoP/VoP, Tazama) ; notre angle = intégrité bout-en-bout entre rails + normes des deux pays + réponse vérifiable.
- Track 1 uniquement (pas de « Track 3 »), pas de Jev, pas de L1 dédiée dans le pitch (ou seulement en roadmap).
- Les chiffres du deck viennent **uniquement** de `ml/metrics.json`.

## 4. Ce que tu attends des autres / ce que tu livres

- **Reçois** : chiffres (Oscar, ~04:45), captures de la console (Talal), liens Snowtrace (Youssef/Devin).
- **Livres** : réponses mentors (21:15), script de démo (22:00), contenu des scènes (23:00), playbook + conformité + fiche défense (03:30), deck final (05:00).
