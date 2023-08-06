"""
ASFPy methods

Say some things about it here.
"""

from operator import itemgetter

#################################################
# Constants
#
# NOTE: These constants refer to data fields that
#	are collected in forms, so may be changed
#	accordingly.
#
#################################################

URM = "urm"
LIM = "lim"
SCHOOL = "du"

#################################################
# APPLICANT-ONLY METHODS
#################################################

def asfp_rank(applicant):
    """
    Rank an applicant by attribute combinations by the standard ASFP method of
    ranking by underrepresented minority (URM) status, whether an applicant has
    limited access (LIM) to mentors in academia and research, and if the applicant
    is affiliated with the University of Denver (DU).

    Parameters
    ----------
    applicant: dict
        An object that represents an applicant (often within a list) with 
        attributes including:
            - "id" a unique string identifier
            - "urm" a boolean designation of URM status
            - "lim" a boolean designation of LIM status
            - "du" a boolean designation of DU affiliation

    Returns
    -------
    rank: integer
        A ranking that represents an applicant's pool relative to an
        ASFP-designed schema, as clarified through boolean logic in code below.
    """
    is_urm = applicant[URM]
    is_lim = applicant[LIM]
    is_school = applicant[SCHOOL]

    if (is_urm and is_lim and is_school):
        rank = 0
    elif (is_urm and is_lim):
        rank = 1
    elif (is_urm or is_lim) and is_school:
        rank = 2
    elif (is_urm or is_lim):
        rank = 3
    elif is_school:
        rank = 4
    else:
        rank = 5

    return rank

def prioritize(applicants, rank_method = asfp_rank):
    """
    Prioritize applicants by rank of attributes.

    Parameters
    ----------
    applicants: list
        The list `applicants` of dicts of each applicant.
    rank_method: function
        The method of assinging ranks under label "rank" based on attributes
        that are necessarily present in items of `applicants`.

    Returns
    -------
    applicants: list
        A copy of applicants is returned, sorted by rank as determined by
        `rank_method`.
    """
    for a in applicants:
        a["rank"] = rank_method(a)
    return sorted(applicants, key = itemgetter("rank"))

#################################################
# EDITOR-ONLY METHODS
#################################################

def editors_by_role(editors, role):
    """
    Get a sublist of editors by role.
    """
    return [e for e in editors if e["role"] == role]

def editors_by_categories(editors, categories):
    """
    Get a sublist of editors by category
    """
    return [e for e in editors if e["categories"].intersection(categories)]

def capacity(editors):
    """
    Compute editing capacity, the number of statements an editor
    can read, for a list of editors.
    """
    return sum(e["capacity"] for e in editors)


def find_highest_capacity_category(applicant, editors):
    """
    Find the highest capacity category based on editors'
    availability given stated category preferences of an applicant.

    Parameters
    ----------
    applicant: dict
        The dict object representing an applicant that has categories
        in a set.
    editors: list
        The editors list of dicts is some subset of editors.

    Returns
    -------
    Returns the highest capacity category given applicant category preferences
    as listed in the set.
    """
    
    capacities = [{
        "capacity": capacity(editors_by_categories(editors, {category})),
        "category": category
    } for category in applicant["categories"]]

    sorted_capacities = sorted(capacities, 
                               key = itemgetter("capacity"), 
                               reverse = True)

    return sorted_capacities[0]["category"]

def find_match(applicant, editors):
    """
    Match an applicant to editors, if possible.
    """
    if capacity(editors) > 0:
    # If at least one editor in a list is available for an applicant,
    # find the best possible match and assign.

        highest_capacity_category = find_highest_capacity_category(applicant, editors)

        highest_capacity_editors = sorted(
            editors_by_categories(editors, {highest_capacity_category}),
            key = itemgetter("capacity"),
            reverse = True
        )

        editor_id = highest_capacity_editors[0]["id"]

        return highest_capacity_editors[0]["id"]

    else:
    # If no editors have capacity within the group, return None
        return None

def update_capacity(editor_id, editors):
    """
    Update capacity of editor within a list by id.
    """
    for editor in editors:
        if editor["id"] == editor_id:
            editor["capacity"] -= 1

def allocate(applicants, editors):
    """
    Allocate applicants to editors.
    """
    unmatched = [applicant["id"] for applicant in applicants]
    matchings = []

    for applicant in applicants:

        potential_editors = editors_by_categories(editors, applicant["categories"])

        if capacity(potential_editors) < 2:
        # If the editing capacity for an applicant is less than 2, continue to next applicant
            continue
        else:

            _match = {
                "applicant": applicant["id"],
                "editors": []
            }

            faculty_editors = editors_by_role(potential_editors, "faculty")
            student_editors = editors_by_role(potential_editors, "student")

            faculty_editor_match = find_match(applicant, faculty_editors)

            if (faculty_editor_match is not None) and (capacity(student_editors) > 0):
            # If a faculty editor match is possible and at least one student editor
            # match is possible, then add a faculty editor match and update capacity.
                _match["editors"].append(faculty_editor_match)
                update_capacity(faculty_editor_match, faculty_editors)
            else:
                if capacity(student_editors) < 2:
                # If fewer than 2 student editors are available, skip to next
                # applicant.
                    continue
                elif applicant["is_flexible"]:
                # If an applicant is flexible and prefers to be matched with two
                # student editors, find first match here.
                    student_editor_match = find_match(applicant, student_editors)
                    if student_editor_match is not None:
                        _match["editors"].append(student_editor_match)
                        update_capacity(student_editor_match, student_editors)
                else:
                # If applicant prefers not to have a match if at least one faculty
                # editor is not available, then continue to next applicant.
                    continue

            # Add a second editor: A student editor match. Then update
            # capacity of that editor.
            student_editor_match = find_match(applicant, student_editors)
            _match["editors"].append(student_editor_match)
            update_capacity(student_editor_match, student_editors)

            # Append the match to matchings and remove this applicant
            # from the list of unmatched applicants.
            matchings.append(_match)
            unmatched.remove(applicant["id"])

    return {
        "matchings": matchings,
        "unmatched": unmatched
    }
