import subprocess
import csv
import subprocess

absolute_path_dspot = "/tmp/dspot/dspot/target/dspot-1.1.1-SNAPSHOT-jar-with-dependencies.jar"
prefix_dataset = "dataset/august-2018/"
prefix_bug_dot_jar = prefix_dataset + "bugs-dot-jar/"
suffix_properties = ".properties"
prefix_result = "results/august-2018/"
suffix_project_buggy = "_buggy"
suffix_project_fixed = "_fixed"
relative_test_path = ".bugs-dot-jar/test-results.txt"
relative_patch_path = ".bugs-dot-jar/developer-patch.diff"
maven_home = ""
java_home = ""
current_output_log = ""
single_module_projects = ["commons-math"]

def readTestToBeExecuted(project, branch):
    tests_to_be_amplified = {}
    path_to_csv_file = prefix_dataset + project + "/" + "data_test-selection_" + branch.split("/")[-1] + ".csv"
    with open(path_to_csv_file, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';')
        for row in spamreader:
            print row[1:]
            print list(set(row[1:]))
            tests_to_be_amplified[row[0]] = list(set(row[1:]))
    return tests_to_be_amplified


def get_all_branches_of_bugs(project):
    result = subprocess.check_output(
        " ".join(["cd", prefix_bug_dot_jar + project, "&&", "git", "branch", "-a", "|", "grep", "remotes/origin/bugs-dot-jar"]),
        shell=True)
    return [x.split("/")[-1] for x in result.split("\n")]


def get_module(project):
    if project in single_module_projects:
        return ""
    with open(prefix_bug_dot_jar + project + "/"+ relative_test_path, 'r') as test_result:
        for line in test_result:
            if line.startswith("[INFO] Surefire report directory:"):
                splitted_line = line.split(" ")[-1].split("/")
                for element in splitted_line:
                    if element == "target":
                        candidate = splitted_line[splitted_line.index(element) - 1]
                        if candidate == project:
                            return ""
                        else:
                            return candidate

def print_and_call(cmd):
    global current_output_log
    print cmd
    with open(current_output_log, "a") as f:
        f.write(cmd + "\n")
        return subprocess.call(cmd, shell=True, stdout=f, stderr=f)

# this method clean, checkout the correct branch and install.
# then it copies the project into ../project_fixed and apply the developer patch
def initialize_project_for_branch(project, branch):
    global maven_home
    # copy the buggy version to keep it clean...
    path_to_project = prefix_bug_dot_jar + project
    print_and_call(" ".join(["rm", "-rf", prefix_bug_dot_jar + project + suffix_project_buggy]))
    print_and_call(" ".join(["cd", path_to_project, "&&", "git", "checkout", branch]))
    print_and_call(" ".join(["cp", "-r", path_to_project, prefix_bug_dot_jar + project + suffix_project_buggy]))
    path_to_project = prefix_bug_dot_jar + project + suffix_project_buggy
    # setting the branch
    print_and_call(" ".join(["cd", path_to_project, "&&", maven_home + "mvn", "versions:use-latest-versions", "-Dincludes=junit:junit"]))
    print_and_call(" ".join(["rm", "-rf", prefix_bug_dot_jar + project + suffix_project_fixed]))
    print_and_call(" ".join(["cp", "-r", path_to_project, prefix_bug_dot_jar + project + suffix_project_fixed]))
    # patching the second version
    print_and_call(
        " ".join(["cd", prefix_bug_dot_jar + project + suffix_project_fixed, "&&", "patch", "-p1", "<", relative_patch_path]))

def initialize_project_for_branch_with_build(project, branch):
    global maven_home
    # copy the buggy version to keep it clean...
    path_to_project = prefix_bug_dot_jar + project
    print_and_call(" ".join(["rm", "-rf", prefix_bug_dot_jar + project + suffix_project_buggy]))
    print_and_call(" ".join(["cd", path_to_project, "&&", "git", "checkout", branch]))
    print_and_call(" ".join(["cp", "-r", path_to_project, prefix_bug_dot_jar + project + suffix_project_buggy]))
    path_to_project = prefix_bug_dot_jar + project + suffix_project_buggy
    # setting the branch
    print_and_call(" ".join(["cd", path_to_project, "&&", maven_home + "mvn", "clean", "install", "-DskipTests"]))
    print_and_call(" ".join(["rm", "-rf", prefix_bug_dot_jar + project + suffix_project_fixed]))
    print_and_call(" ".join(["cp", "-r", path_to_project, prefix_bug_dot_jar + project + suffix_project_fixed]))
    # patching the second version
    print_and_call(
        " ".join(["cd", prefix_bug_dot_jar + project + suffix_project_fixed, "&&", "patch", "-p1", "<", relative_patch_path]))




def init(argv):
    global maven_home
    global java_home
    if "onClusty" in argv:
        maven_home = "~/apache-maven-3.3.9/bin/"
        java_home = "~/jdk1.8.0_121/bin/"
    else:
        maven_home = ""

if __name__ == '__main__':
    print get_module(project="accumulo")
