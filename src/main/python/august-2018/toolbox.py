import subprocess
import csv
import shlex
import logging
import subprocess
from StringIO import StringIO

absolute_path_dspot = "/home/bdanglot/workspace/dspot/dspot/target/dspot-1.1.1-SNAPSHOT-jar-with-dependencies.jar"
prefix_dataset = "dataset/august-2018/"
prefix_bug_dot_jar = prefix_dataset + "bugs-dot-jar/"
suffix_properties = ".properties"
prefix_result = "results/august-2018/"
suffix_project = "_fixed"
relative_test_path = ".bugs-dot-jar/test-results.txt"
relative_patch_path = ".bugs-dot-jar/developer-patch.diff"
maven_home = ""
current_output_log = ""


def readTestToBeExecuted(project, branch):
    tests_to_be_amplified = {}
    path_to_csv_file = prefix_dataset + project + "_" + branch.split("/")[-1] + ".csv"
    with open(path_to_csv_file, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';')
        for row in spamreader:
            tests_to_be_amplified[row[0]] = row[1:]
    return tests_to_be_amplified


def get_all_branches_of_bugs(project):
    result = subprocess.check_output(
        " ".join(["cd", prefix_bug_dot_jar + project, "&&", "git", "branch", "-a", "|", "grep", "bugs-dot-jar"]),
        shell=True)
    return result.split("\n")


def get_module(project):
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
    with open(current_output_log, "a") as f:
        return subprocess.call(cmd, shell=True, stdout=f, stderr=f)


# this method clean, checkout the correct branch and install.
# then it copies the project into ../project_fixed and apply the developer patch
def initialize_project_for_branch(project, branch):
    output = prefix_dataset + project + "/" + "test-selection_" + branch.split("/")[-1] + ".log"
    global maven_home
    # setting the branch
    print_and_call(" ".join(["cd", prefix_bug_dot_jar + project, "&&",
                             "git", "stash", "&&",
                             "git", "checkout", branch, "&&",
                             maven_home + "mvn", "clean", "install", "-DskipTests"]))
    print_and_call(" ".join(["rm", "-fr", prefix_bug_dot_jar + project + suffix_project]))
    print_and_call(" ".join(["cp", "-r", prefix_bug_dot_jar + project, prefix_bug_dot_jar + project + suffix_project]))
    # patching the second version
    print_and_call(
        " ".join(["cd", prefix_bug_dot_jar + project + suffix_project, "&&", "patch", "-p1", "<", relative_patch_path]))


def init(argv):
    global maven_home
    if len(argv) > 1 and argv[1] == "onClusty":
        maven_home = "~/apache-maven-3.3.9/bin/"
    else:
        maven_home = ""

if __name__ == '__main__':
    print get_module(project="accumulo")
