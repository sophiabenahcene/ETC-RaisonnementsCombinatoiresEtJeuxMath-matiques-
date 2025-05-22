import math

def split_groupes(indices):
    """
    Pour n = len(indices), renvoie trois listes A, B, C
    telles que la stratégie optimale (voir mémoire) est respectée.
    """
    n = len(indices)
    if n <= 3:
        # Cas de base : on ne split plus
        return indices, [], []

    k = n // 3
    r = n % 3
    if r == 0:
        A = indices[:k]
        B = indices[k:2*k]
        C = indices[2*k:]
    elif r == 1:
        # n = 3k+1  → A = B = k+1,  C = k-1
        A = indices[:k+1]
        B = indices[k+1:2*(k+1)]
        C = indices[2*(k+1):]
    else:  # r == 2
        # n = 3k+2 → A = B = k+1, C = k
        A = indices[:k+1]
        B = indices[k+1:2*(k+1)]
        C = indices[2*(k+1):]
    return A, B, C

def comparer(coins, A, B):
    """
    Simule une pesée A vs B.
    Retourne :
      -1 si A < B (A plus léger),
       1 si A > B (A plus lourd),
       0 si A == B.
    """
    poids_A = sum(coins[i] for i in A)
    poids_B = sum(coins[i] for i in B)
    if poids_A < poids_B: return -1
    if poids_A > poids_B: return 1
    return 0

def chercher_fausse_connu_plus_legere(coins, indices=None, niveau=1):
    """
    Cas 1 : on sait que la fausse pièce est plus légère.
    Retourne l'indice de la fausse pièce et le nombre de pesées utilisées.
    """
    if indices is None:
        indices = list(range(len(coins)))

    n = len(indices)
    # Cas de base
    if n == 1:
        return indices[0], 0
    if n == 2:
        a, b = indices
        return (a, 1) if coins[a] < coins[b] else (b, 1)
    if n == 3:
        a, b, c = indices
        r = comparer(coins, [a], [b])
        if r == -1: return a, 1
        if r == 1:  return b, 1
        return c, 1

    # Cas général : on split en 3 paquets A, B, C
    A, B, C = split_groupes(indices)
    print(f"Niveau {niveau} : on pèse {A} vs {B}")
    r = comparer(coins, A, B)
    if r == -1:
        return chercher_fausse_connu_plus_legere(coins, A, niveau+1)[0], niveau
    if r == 1:
        return chercher_fausse_connu_plus_legere(coins, B, niveau+1)[0], niveau
    # équilibre
    return chercher_fausse_connu_plus_legere(coins, C, niveau+1)[0], niveau

def chercher_fausse_inconnu(coins):
    """
    Cas 2 : on ne sait pas si la fausse pièce est plus légère ou plus lourde.
    On réalise deux premières pesées pour déterminer à la fois
    l'ensemble de travail et la nature (lourd/léger), puis on retombe
    dans le cas 1.
    """
    n = len(coins)
    indices = list(range(n))
    k = n // 3
    r = n % 3

    # 1ère pesée : A vs B
    if r == 0:
        A, B, C = indices[:k], indices[k:2*k], indices[2*k:]
    elif r == 1:
        A, B, C = indices[:k], indices[k:2*k], indices[2*k:]
        # C contient  k+1 pièces, A et B k pièces
    else:  # r == 2
        # on met une pièce à part (D) pour simplifier
        A = indices[:k]
        B = indices[k:2*k]
        C = indices[2*k:2*k+k+1]
        D = indices[-1:]

    print(f"1ᵉʳᵉ pesée : {A} vs {B}")
    r1 = comparer(coins, A, B)

    if r == 2 and r1 == 0 and 'D' in locals():
        # cas mod‐2 et équilibre → seule la pièce D peut être fausse
        fake = D[0]
        nature = 'lourde ou légère ? → pas besoin de pesée'
        return fake, 1

    # si A=B  → la fausse est dans C
    if r1 == 0:
        groupe = C
        # 2ᵉ pesée : C vs A (même taille)
        to_compare = A[:len(C)]
        print(f"2ᵉ pesée : {groupe} vs {to_compare}")
        r2 = comparer(coins, groupe, to_compare)
        nature = 'plus légère' if r2 == -1 else 'plus lourde'
        # on retombe dans cas 1 sur 'groupe', en sachant la nature
        # on adapte les poids pour que la fausse soit plus légère :
        coins2 = [1 if i not in groupe else (0.5 if nature=='plus légère' else 1.5) for i in range(n)]
        fake, pds = chercher_fausse_connu_plus_legere(coins2, groupe)
        return fake, 2 + pds

    # si A≠B  → la fausse est dans A∪B, C authentiques
    groupe = A if r1 != 0 else B
    nature = 'plus légère' if r1 == -1 else 'plus lourde'
    # 2ᵉ pesée : on prend groupe vs C (après ajustement de taille)
    C2 = C[:len(groupe)]
    print(f"2ᵉ pesée : {groupe} vs {C2}")
    r2 = comparer(coins, groupe, C2)
    if r2 == 0:
        fake = B[0] if groupe is A else A[0]
    else:
        fake = groupe[0]  # simplification de l’exemple
    # on sait maintenant l’indice et la nature
    return fake, 2

# --- Exemple d’utilisation : ---
if __name__ == "__main__":
    # Créons 27 pièces, la fausse est la 10ᵉ et est plus légère
    n = 27
    fake_index = 9
    coins = [1.0]*n
    coins[fake_index] = 0.0  # plus légère

    print("=== Cas 1 : faux plus léger ===")
    idx, nb = chercher_fausse_connu_plus_legere(coins)
    print(f"-> Fausse pièce : {idx}, pesées : {nb}\n")

    print("=== Cas 2 : nature inconnue ===")
    # recréons un scénario où la fausse est plus lourde
    coins2 = [1.0]*n
    coins2[fake_index] = 2.0  # plus lourde
    idx2, nb2 = chercher_fausse_inconnu(coins2)
    print(f"-> Fausse pièce : {idx2}, pesées : {nb2}")
