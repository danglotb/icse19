import toolbox
import sys

def run(project):
    branches = toolbox.get_all_branches_of_bugs(toolbox.prefix_bug_dot_jar + project)
    for branch in branches[1:2]:  # skiping the first, which is the HEAD
        run_one(project, "".join(branch.split(" ")))


def run_one(project, branch):
    if branch == "":
        return
    toolbox.initialize_project_for_branch(project, branch)
    tests_to_be_amplified = toolbox.readTestToBeExecuted(project, branch)
    if len(tests_to_be_amplified) == 0:
        return
    test_classes = []
    test_methods = []
    for test_class in tests_to_be_amplified:
        test_classes.append(test_class)
        test_methods.append(":".join([x for x in tests_to_be_amplified[test_class]]))
    toolbox.print_and_call(" ".join(["java", "-jar", toolbox.absolute_path_dspot,
                                     "--path-to-properties", toolbox.prefix_dataset + project + toolbox.suffix_properties,
                                     "--verbose",
                                     "--no-minimize",
                                     "--working-directory",
                                     "--output-path", toolbox.prefix_result + project + "/" + branch.split("/")[-1],
                                     "--amplifiers", "None",
                                     "--test-criterion", "ChangeDetectorSelector",
                                     "--test", ":".join(test_classes),
                                     "--cases", ":".join(test_methods)
                                     ])
                           )


if __name__ == '__main__':

    toolbox.init(sys.argv)

    if len(sys.argv) < 2:
        print "usage python run.py <project>"
    else:
        run(sys.argv[1])
