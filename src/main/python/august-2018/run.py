import toolbox
import sys
import os.path


def run(project, lower_bound=1, upper_bound=-1):
    result = toolbox.get_all_branches_of_bugs(project)
    print lower_bound, upper_bound
    for res in result[lower_bound:upper_bound]:
        print res
        run_one(project, "".join(res.split(" ")))


def run_one(project, branch):
    if branch == "":
        return
    toolbox.current_output_log = os.path.abspath(
        toolbox.prefix_result + project + "/ampl_log_test-selection_" + branch.split("/")[-1] + ".log")
    toolbox.initialize_project_for_branch(project, branch)
    tests_to_be_amplified = toolbox.readTestToBeExecuted(project, branch)
    if len(tests_to_be_amplified) == 0:
        return
    test_classes = []
    test_methods = []
    for test_class in tests_to_be_amplified:
        test_classes.append(test_class)
        test_methods.append(":".join([x for x in tests_to_be_amplified[test_class]]))
    toolbox.print_and_call(
        " ".join([toolbox.java_home + "java", "-XX:-UseGCOverheadLimit",  "-XX:-OmitStackTraceInFastThrow", "-jar",
                  toolbox.absolute_path_dspot,
                  "--path-to-properties", toolbox.prefix_dataset + project + "/" + project + toolbox.suffix_properties,
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
    toolbox.print_and_call(
        " ".join([
            "cp", "-r", "target/dspot/output/", toolbox.prefix_result + project + "/" + branch.split("/")[-1]
        ])
    )
    toolbox.print_and_call(
        " ".join([
            "rm", "-rf", "target"
        ])
    )

if __name__ == '__main__':

    toolbox.init(sys.argv)

    if len(sys.argv) < 2:
        print "usage python select-tests.py <project> <lower_bound> <upper_bound>"
    else:
        if len(sys.argv) > 2:
            run(sys.argv[1], lower_bound=int(sys.argv[2]), upper_bound=int(sys.argv[3]))
        else:
            run(sys.argv[1])
