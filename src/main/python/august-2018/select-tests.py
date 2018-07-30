import sys
import toolbox
import os.path

def run(project):
    result = toolbox.get_all_branches_of_bugs(project)
    for res in result[23:24]:
        run_one(project, res)

def run_one(project, branch):
    path_to_csv = project + "_" + branch.split("/")[-1] + ".csv"
    if os.path.isfile(path_to_csv):
        return
    toolbox.initialize_project_for_branch(project, branch)
    # getting the concerned module
    targetModule = toolbox.get_module(project)
    # run maven plugin to compute the list
    code = toolbox.print_and_call(
        " ".join(
            ["cd", toolbox.prefix_bug_dot_jar + project + "/" + targetModule, "&&",
             toolbox.maven_home + "mvn", "clean",
             "versions:use-latest-versions",
             "-Dincludes=junit:junit",
             "eu.stamp-project:diff-test-selection:0.2:list",
             "-DpathToDiff=" + ("../" if not targetModule == "" else "") + toolbox.relative_patch_path,
             "-DpathToOtherVersion=../" + ("../" if not targetModule == "" else "") + project + toolbox.suffix_project + "/",
             "-DoutputPath=../../" + ("../" if not targetModule == "" else "") + path_to_csv,
             "-Dreport=CSV"]
        )
    )
    print code
    toolbox.print_and_call(" ".join(["rm", "-rf", project + toolbox.suffix_project]))

if __name__ == '__main__':

    toolbox.init(sys.argv)

    if len(sys.argv) < 2:
        print "usage python select-tests.py <project>"
    else:
        run(sys.argv[1])
