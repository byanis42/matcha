# services/matching_service/application/matching_service.py

import math
import httpx

# URLs vers d'autres services
PROFILE_SERVICE_URL = "http://profile_service:8000"
LIKE_SERVICE_URL = "http://profile_service:8000"
# ou un autre service dédié "like_service"

def compute_distance(lat1, lon1, lat2, lon2):
    """
    Calcul distance euclidienne.
    Si un user n'a pas de lat/lon -> distance = 999999
    """
    if lat1 is None or lon1 is None or lat2 is None or lon2 is None:
        return 999999.0
    return math.sqrt((lat1 - lat2)**2 + (lon1 - lon2)**2)

def compute_tags_score(tags1: str, tags2: str):
    """
    Compare deux listes de tags CSV (#vegan,#geek).
    Retourne le nb de tags en commun.
    """
    if not tags1 or not tags2:
        return 0
    set1 = set(t.strip() for t in tags1.split(",") if t.strip())
    set2 = set(t.strip() for t in tags2.split(",") if t.strip())
    return len(set1.intersection(set2))

def orientation_match(user_gender, user_orient, other_gender, other_orient):
    """
    Logique "réciproque" :
    - user A aime B si B correspond à A.orient
    - user B aime A si A correspond à B.orient
    - => A n'est visible par B que s'ils se matchent réciproquement.

    'orientation' étant dynamique, on prend la valeur courante
    du profile (profile_service).
    Les likes existants ne sont pas annulés si l'orientation change,
    mais le user n'apparaîtra plus dans de futurs calculs si la compat ne matche plus.
    """

    # Valeur par défaut = "bi" s'il est vide
    if not user_orient:
        user_orient = "bi"
    if not other_orient:
        other_orient = "bi"

    def prefer(gender, orient):
        """
        Retourne la liste de genres que 'gender' + 'orient' aime.
        """
        if orient == "hetero":
            return ["M"] if gender == "F" else ["F"]
        elif orient == "homo":
            return [gender]
        else:
            return ["M", "F", "O"]  # "bi"

    user_likes = prefer(user_gender, user_orient)
    other_likes = prefer(other_gender, other_orient)

    # On exige la réciprocité : user.gender ∈ other_likes ET other.gender ∈ user_likes
    return (user_gender in other_likes) and (other_gender in user_likes)

def fetch_user_profile(user_id: int):
    """
    GET /profiles/{user_id}.
    """
    try:
        r = httpx.get(f"{PROFILE_SERVICE_URL}/profiles/{user_id}")
        if r.status_code == 200:
            return r.json()
    except:
        pass
    return None

def fetch_all_profiles():
    """
    GET /profiles/all.
    """
    try:
        r = httpx.get(f"{PROFILE_SERVICE_URL}/profiles/all")
        if r.status_code == 200:
            return r.json()
    except:
        pass
    return []

def fetch_likers_for_user(user_id: int):
    """
    GET /likes?target_id=user_id => [ <list of user_ids> ]
    """
    try:
        r = httpx.get(f"{LIKE_SERVICE_URL}/likes?target_id={user_id}")
        if r.status_code == 200:
            return r.json()
    except:
        pass
    return []

def match_profiles(user_profile, all_profiles, likers):
    """
    Calcule un 'score' pour chaque profil parmi all_profiles,
    en tenant compte d'orientation_match.
    + un bonus pour ceux qui ont déjà liké (stocké dans 'likers').
    """
    suggestions = []

    user_id = user_profile.get("user_id")
    user_gender = user_profile.get("gender")
    user_orientation = user_profile.get("orientation", "bi")
    user_tags = user_profile.get("interests", "")
    user_lat = user_profile.get("gps_lat")
    user_lon = user_profile.get("gps_long")

    for prof in all_profiles:
        # ne pas se suggérer soi-même
        if prof["user_id"] == user_id:
            continue

        # orientation check
        if not orientation_match(
            user_gender,
            user_orientation,
            prof.get("gender"),
            prof.get("orientation")
        ):
            # => l'utilisateur n'est pas visible
            continue

        dist = compute_distance(user_lat, user_lon, prof.get("gps_lat"), prof.get("gps_long"))
        tags_score = compute_tags_score(user_tags, prof.get("interests", ""))
        fame = prof.get("fame_rating", 0.0)

        # On construit un "score" simple : dist - 2*tags_score - 0.1*fame
        final_score = dist - (2 * tags_score) - (0.1 * fame)

        # BONUS : si prof["user_id"] ∈ likers => ce user a déjà liké user_id => prioritaire
        if prof["user_id"] in likers:
            final_score -= 5.0

        suggestions.append({
            "user_id": prof["user_id"],
            "distance": dist,
            "tags_score": tags_score,
            "fame": fame,
            "score": final_score
        })

    # tri par "score" croissant
    suggestions.sort(key=lambda x: x["score"])
    return suggestions

def get_suggestions_for_user(user_id: int):
    """
    Récupère le profil (avec orientation courante),
    la liste de tous les profils,
    la liste de user_ids qui ont déjà liké user_id,
    => match_profiles => renvoie top 20.
    """
    user_profile = fetch_user_profile(user_id)
    if not user_profile:
        return []

    all_prof = fetch_all_profiles()
    if not all_prof:
        return []

    # qui a déjà liké user_id ?
    # => user_id apparaitra en top pr ces gens,
    # => bonus -5
    likers = fetch_likers_for_user(user_id)
    suggestions = match_profiles(user_profile, all_prof, likers)
    return suggestions[:20]

def get_swipe_deck_for_user(user_id: int, batch_size=10):
    """
    Renvoie un deck (pile) de 'batch_size' suggestions
    (logique "Tinder swiping").
    """
    suggestions = get_suggestions_for_user(user_id)
    return suggestions[:batch_size]
