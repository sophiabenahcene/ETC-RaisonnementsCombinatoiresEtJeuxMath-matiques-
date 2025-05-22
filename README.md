# Résolution du Problème de la Pièce Fausse par Pesées Combinatoires

Ce dépôt contient une implémentation Python de la méthode de détection d’une pièce fausse parmi un ensemble, en utilisant une balance à plateaux et une stratégie de raisonnement combinatoire optimale décrite dans le **Mémoire « ETC Raisonnement Combinatoire »**.

## Table des matières

- [Contexte](#contexte)  
- [Fonctionnalités](#fonctionnalités)   

## Contexte

Dans un jeu de n pièces dont une seule est fausse, elle peut être plus légère ou plus lourde que les autres. L’objectif est de l’identifier en un nombre minimum de pesées en appliquant une stratégie combinatoire.

## Fonctionnalités

- **Découpage optimal** des pièces en trois groupes à chaque étape  
- Simulation de la balance à trois issues (gauche plus léger, équilibré, gauche plus lourd)  
- Recherche récursive de la fausse pièce quand on sait qu’elle est plus légère  
- Procédure en deux phases pour identifier la fausse pièce quand sa nature (lourde/légère) est inconnue

