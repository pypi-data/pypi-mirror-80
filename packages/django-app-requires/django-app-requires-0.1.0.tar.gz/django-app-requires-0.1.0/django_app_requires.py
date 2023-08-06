from fastutils import listutils
from magic_import import import_from_string

def add_requires(apps):
    applists = []
    for app in apps:
        deps_path = app + ".app_requires"
        app_new_requires = import_from_string(deps_path)
        if app_new_requires:
            applists += add_requires(app_new_requires)
        applists.append(app)
    return listutils.unique(applists)
