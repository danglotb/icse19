import sys
import toolbox
import os.path


def run(project, lower_bound=1, upper_bound=-1):
    result = toolbox.get_all_branches_of_bugs(project)
    print lower_bound, upper_bound
    for res in result[lower_bound:upper_bound]:
        run_one(project, res)

def run_one(project, branch):
    # getting the concerned module
    targetModule = toolbox.get_module(project)
    toolbox.current_output_log = os.path.abspath(toolbox.prefix_dataset + project + "/log_test-selection_" + branch.split("/")[-1] + ".log")
    path_to_csv ="../../" + ("../" if not targetModule == "" else "") + project +  "/data_test-selection_" + branch.split("/")[-1] + ".csv"
    if os.path.isfile(path_to_csv):
        return
    toolbox.initialize_project_for_branch(project, branch)
    # run maven plugin to compute the list
    code = toolbox.print_and_call(
        " ".join(
            ["cd", toolbox.prefix_bug_dot_jar + project + toolbox.suffix_project_buggy + "/" + targetModule, "&&",
             toolbox.maven_home + "mvn", "clean",
             "versions:use-latest-versions",
             "-Dincludes=junit:junit",
             "eu.stamp-project:diff-test-selection:0.2:list",
             "-DpathToDiff=" + ("../" if not targetModule == "" else "") + toolbox.relative_patch_path,
             "-DpathToOtherVersion=../" + (
             "../" if not targetModule == "" else "") + project + toolbox.suffix_project_fixed + "/",
             "-DoutputPath=" + path_to_csv,
             "-Dreport=CSV"]
        )
    )
    print code
    toolbox.print_and_call(" ".join(["rm", "-rf", project + toolbox.suffix_project_fixed]))


if __name__ == '__main__':

    toolbox.init(sys.argv)

    if len(sys.argv) < 2:
        print "usage python select-tests.py <project> <lower_bound> <upper_bound>"
    else:
        if len(sys.argv) > 2:
            run(sys.argv[1], lower_bound=int(sys.argv[2]), upper_bound=int(sys.argv[3]))
        else:
            run(sys.argv[1])
