from ftest.constants import GENDER_MALE, GENDER_FEMALE, PRONOUN_MALE, PRONOUN_FEMALE


def settings_processor(request):
    """Adds the settings as a variable to all templates"""
    return {
        'gender_female': GENDER_FEMALE,
        'gender_male': GENDER_MALE,
        'pronoun_female': PRONOUN_FEMALE,
        'pronoun_male': PRONOUN_MALE,
    }
