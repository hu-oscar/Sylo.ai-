# Tâches — Talal (front-end : la console de démo)

> **Ta mission** : que le jury **comprenne sans narration** ce qui se passe : un paiement qui passe, le même détourné et stoppé, et des tentatives de triche qui échouent sur un explorer public.
> **Pourquoi c'est critique** : le pitch (15 %) se joue sur cet écran, et c'est lui qui rend visibles la détection (30 %) et la réponse (20 %).
> **À lire dans le PRD v4** : §7 (scènes et critères d'acceptation), §15.3 (événements), §18.3 (explicabilité), §22.1 (déroulé du pitch). README §7 pour l'API.
> **Dossier** : `/web` (Next.js App Router, TypeScript, Tailwind, framer-motion). Tu ne touches pas aux autres dossiers.

## 1. Ce qu'il faut comprendre (5 min)

- **La console ne calcule rien.** Elle écoute un seul flux d'événements (SSE, `GET /v1/stream`) et les dessine. Toute la logique est dans le back (Devin). Conséquence : si un événement n'arrive pas, c'est un bug back, pas front.
- **SSE** = `new EventSource(url)` côté navigateur ; chaque message est un JSON avec une enveloppe fixe (README §7) : `id`, `type`, `ts`, `paymentId`, `uetr`, `scene`, `data`, `explorerUrl`.
- **Le faux flux** : jusqu'à ce que le back soit prêt (~01:00), tu rejoues `shared/fixtures/events-scene1.jsonl` / `scene2` / `scene2b` (une ligne = un événement). Avec `NEXT_PUBLIC_MOCK=1`, un petit lecteur les émet avec un délai (ex. 600 ms entre chaque). Le jour J tu passes à `NEXT_PUBLIC_MOCK=0` sans rien changer d'autre.
- **Les boutons** appellent l'API (ils ne modifient jamais l'état local directement) ; le résultat revient par le flux.

## 2. L'écran (une seule page, 6 zones)

| Zone | Ce qu'elle montre | Événements | Actions (POST, base `http://localhost:8000/v1`) |
|---|---|---|---|
| **A. Vue payeur (Claire)** | Ordre (85 000 €, Savanna Shea), carte de décision : normes (R4 exclue + règle citée), notice fiscale, niveau de risque + 3 raisons, routes comparées (choisie / exclues + pourquoi, « prix de la sécurité »), bouton **Approuver** (désactivé + message si vérification requise), 2e approbation Marc | `norms.checked`, `risk.scored`, `route.selected`, `approval.required`, `approval.granted` | `/payments/{id}/approve` `{"by":"claire"}` puis `{"by":"marc"}` |
| **B. Fil texte** | Liste chronologique de tous les événements, une ligne lisible chacun ; refus en rouge avec la raison | tous | — |
| **C. Panneau preuve** | Timeline on-chain : `COMMITTED` → `HELD` → `DENIED` → `REVOKED` → `REFUNDED`, chaque étape avec lien **Snowtrace** ; tx en échec en rouge avec la raison du revert ; bannière rouge « hash mismatch » | `intent.committed`, `escrow.*`, `verification.recorded`, `intent.revoked`, `tx.reverted`, `log.tampered` | — |
| **D. Analyste (Julien)** | Le cas ouvert : niveau, raisons citées, dossier Mistral (≤ 120 mots + timeline), brouillon TRACFIN ; boutons | `alert.raised`, `case.ready` | `/cases/{id}/actions` `{"action":"REVOKE"}` (et `CONFIRM`, `FREEZE`) |
| **E. Téléphones** | Deux faux téléphones côte à côte : **Kwame** reçoit « Avez-vous changé de compte ? » avec boutons Oui / Non ; **Claire** reçoit « Paiement stoppé, fonds retournés » (SMS/in-app, **jamais e-mail**) | `simswap.checked`, `oob.requested`, `intent.revoked`, `escrow.refunded` | `/payees/{id}/verify` `{"result":"DENIED"}` |
| **F. Console d'attaque** | 3 gros boutons que le jury peut presser : **A** « Libérer le paiement révoqué », **B** « Changer le bénéficiaire en transit », **C** « Rejouer / réécrire la décision » ; résultat sous chaque bouton | `tx.reverted`, `leg.rejected`, `killswitch.on`, `log.tampered` | `/sim/attack/A`, `/B`, `/C` |

En haut : barre avec **Scène 1**, **Scène 2**, **Reset** (`/sim/scene/1`, `/sim/scene/2`, `/sim/reset`), badge « Données et rails simulés », bannière « Mode dégradé » sur `mode.degraded`. Petit encart chiffres (lu depuis `GET /v1/metrics`) : rappel, précision HIGH, faux positifs, détournement = 0.

## 3. Tâches dans l'ordre

| # | Quand | Tâche | Fini quand |
|---|---|---|---|
| 1 | 21:00–21:15 | `pnpm create next-app web --ts --tailwind --app` ; framer-motion ; garder la DA sobre (fond clair, une couleur d'accent, une couleur rouge pour les refus) | `pnpm dev` tourne sur :3000 |
| 2 | 21:15–22:00 | Maquette statique des 6 zones (wireframe en vrai composants, données en dur) | La page tient sur un écran 1440×900 (écran du pitch) sans scroll |
| 3 | 22:00–22:30 | Hook `useEventStream()` : mode mock (lit les `.jsonl` de `/shared/fixtures`, copiés dans `web/public/fixtures/`) et mode réel (`EventSource`) ; un store (zustand ou `useReducer`) indexé par `paymentId` | Le faux flux scène 1 remplit le fil texte |
| 4 | 22:30–01:00 | Zones A, B, C pour la **scène 1** | Critères §7.2 visibles : R4 exclue avec la règle, LOW, R3 choisie, lien Snowtrace du commit |
| 5 | **01:00** | **CP1** : passer en mode réel contre l'API de Devin | La scène 1 joue en vrai |
| 6 | 01:00–03:30 | Zones D et E pour la **scène 2** ; approbation bloquée avant vérification | Critères §7.3 : MEDIUM + ≥ 3 raisons, approbation bloquée, 5 événements on-chain dans l'ordre, Kwame refuse depuis son téléphone, dossier cité |
| 7 | 03:30–04:30 | Zone F (attaques) + bannière hash mismatch | Les 3 attaques échouent avec une raison nommée et apparaissent dans la timeline |
| 8 | 04:30–05:00 | Polish : micro-animations (entrée des événements, passage au rouge), lisibilité au vidéoprojecteur (police ≥ 16 px), encart chiffres | Omama valide la lisibilité depuis le fond de la salle |
| 9 | 05:00–05:30 | Vidéo de secours avec Omama (enregistrement écran des scènes 1, 2, 2b) | Fichier MP4 ≤ 3 min sur le drive de l'équipe |

## 4. Pièges

- Ne pas recalculer de logique côté front (niveaux, éligibilité) : afficher ce que dit l'événement.
- Les liens explorer viennent de `explorerUrl` dans l'événement : ne pas les construire à la main.
- Prévoir un état vide propre pour chaque zone (au reset, tout repart à zéro).
- Le flux peut se reconnecter : dédupliquer par `id`.
- Pas de globe/carte cette nuit (P1 gelé). Si CP2 est vert et qu'il reste du temps : une petite carte 2D Lyon → Accra (→ Aflao) animée, rien de plus.

## 5. Ce que tu attends des autres / ce que tu livres

- **Reçois** : `shared/events.md` + `shared/fixtures/events-scene*.jsonl` (Devin, 22:00) ; API réelle (Devin, 01:00) ; `fuji.json` pour rien (les liens sont dans les événements) ; textes des SMS/e-mail (Omama, 23:00).
- **Livres** : la console qui joue les 3 scènes ; la vidéo de secours.
