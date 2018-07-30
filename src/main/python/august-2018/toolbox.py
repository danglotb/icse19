import subprocess
import csv


suffix_project = "_fixed"
relative_patch_path = ".bugs-dot-jar/developer-patch.diff"
maven_home = ""


def readTestToBeExecuted(project, branch):
    tests_to_be_amplified = {}
    path_to_csv_file = project + "_" + branch.split("/")[-1] + ".csv"
    with open(path_to_csv_file, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';')
        for row in spamreader:
            tests_to_be_amplified[row[0]] = row[1:]
    return tests_to_be_amplified

def get_all_branches_of_bugs(project):
    result = subprocess.check_output(
        " ".join(["cd", project, "&&", "git", "branch", "-a", "|", "grep", "bugs-dot-jar"]), shell=True)
    return result.split("\n")

def get_module(project):
    result = subprocess.check_output(
        " ".join(["cat", project + "/" + relative_patch_path, "|",
                  "grep", "\"\\-\\-\\-\"", "|",
                  "cut", "-d", "\" \"", "-f", "2"]), shell=True)
    if result.startswith("a/src/"):
        return ""
    else:
        return result.split("/")[1]

def print_and_call(cmd):
    print cmd
    return subprocess.call(cmd, shell=True)

# this method clean, checkout the correct branch and install.
# then it copies the project into ../project_fixed and apply the developer patch
def initialize_project_for_branch(project, branch):
    global maven_home
    # setting the branch
    print_and_call(" ".join(["cd", project, "&&",
                                   "git", "stash", "&&",
                                   "git", "checkout", branch, "&&",
                             maven_home + "mvn", "clean", "install", "-DskipTests"]))
    print_and_call(" ".join(["rm", "-fr", project + suffix_project]))
    print_and_call(" ".join(["cp", "-r", project, project + suffix_project]))
    # patching the second version
    print_and_call(" ".join(["cd", project + suffix_project, "&&", "patch", "-p1", "<", relative_patch_path]))

def init(argv):
    global maven_home
    if len(argv) > 1 and argv[1] == "onClusty":
        maven_home = "~/apache-maven-3.3.9/bin/"
    else:
        maven_home = ""