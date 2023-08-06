import os

from .shared import fix_filenames, normjoin


def fix_junit_filenames(*args, **kwargs):
    return fix_filenames(
        find_xml_filenames,
        [update_report_filenames]
    )(*args, **kwargs)

def find_xml_filenames(tree):
    testcases = tree.findall('./testsuite/testcase/[@file]')
    return {c.get('file') for c in testcases}

def update_report_filenames(tree, source_dir, new_prefix, old_prefix, logger):
    testcases = tree.findall('./testsuite/testcase/[@file]')
    for tc in testcases:
        old_filename = tc.get('file')
        old_classname = tc.get('classname')
        new_filename = normjoin(
            new_prefix,
            os.path.relpath(old_filename, start=old_prefix)
        )
        new_classname = new_filename.replace(os.sep, '.')
        if new_classname.endswith('.py'):
            new_classname = new_classname[:-3]
        tc.set('file', new_filename)
        tc.set('classname', new_classname)
