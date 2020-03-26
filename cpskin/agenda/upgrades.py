PROFILE_ID = 'profile-cpskin.agenda:default'


def upgrade_1000_to_1001(context):
    context.runImportStepFromProfile(PROFILE_ID, 'cssregistry')


def upgrade_1001_to_1002(context):
    context.runImportStepFromProfile(PROFILE_ID, 'jsregistry')


def upgrade_1002_to_1003(context):
    context.runImportStepFromProfile(PROFILE_ID, 'typeinfo')
