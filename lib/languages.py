import glob
import os

from lib.shell import shell_out


def noop_build(file):
    return file


def c_build(file):
    bin_file = file.replace(".", "_")
    shell_out(f"gcc -o {bin_file} {file}")
    return bin_file


def c_cmd(file):
    return f"./{file}"


def golang_build(file):
    bin_file = file.replace(".", "_")
    shell_out(f"go build -o {bin_file} {file}")
    return bin_file


def golang_cmd(file):
    return f"./{file}"


def purge_class_files(base_dir):
    class_files = glob.glob(f"{base_dir}/*.class")
    if class_files:
        shell_out(f"rm {' '.join(class_files)}")


def java_build(file):
    def jar_class_arguments(base_dir, class_files):
        args = []
        for file in class_files:
            args.append(f"-C {base_dir} {file[len(base_dir) + 1:]}")
        return args

    base_dir = os.path.dirname(file)
    jar_file = file.replace(".java", ".jar")
    purge_class_files(base_dir)  # Clean up any class files left by Scala compilation
    shell_out(f"javac -sourcepath {base_dir} -classpath ./lib -d {base_dir} {file}")
    class_files = glob.glob(f"{base_dir}/*.class")
    lib_files = glob.glob("lib/**/*.class")
    if not class_files:
        raise Exception("No class files generated by javac")
    jar_classes = jar_class_arguments(base_dir, class_files) + jar_class_arguments(
        "lib", lib_files
    )
    shell_out(f"jar cfe {jar_file} Main {' '.join(jar_classes)}")
    purge_class_files(base_dir)  # Clean up our own class files
    return jar_file


def java_cmd(file):
    return f"java -jar {file}"


def lisp_cmd(file):
    return f"sbcl --script {file}"


def python_cmd(file):
    return f"python {file}"


def ruby_cmd(file):
    return f"ruby {file}"


def rust_build(file):
    bin_file = file.replace(".", "_")
    shell_out(f"rustc -o {bin_file} {file}")
    return bin_file


def rust_cmd(file):
    return f"./{file}"


def scala_build(file):
    base_dir = os.path.dirname(file)
    shell_out(f"scalac -d {base_dir} {file}")
    return base_dir


def scala_cmd(base_dir):
    return f"scala -classpath {base_dir} Main"


def typescript_build(file):
    shell_out(f"yarn tsc {file}")
    return file.replace(".ts", "")


def typescript_cmd(file):
    return f"node index.js ./{file}"


class LanguageConfig(object):
    def __init__(self, extension, cmd_fn, build_fn=noop_build, timing=True):
        self.extension = extension
        self.cmd_fn = cmd_fn
        self.build_fn = build_fn
        self.timing = timing

    def has_build_step(self):
        return self.build_fn != noop_build


LANGUAGES = {
    "c": LanguageConfig("c", c_cmd, c_build, timing=False),
    "golang": LanguageConfig("go", golang_cmd, golang_build, timing=False),
    "java": LanguageConfig("java", java_cmd, java_build),
    "lisp": LanguageConfig("lisp", lisp_cmd, timing=False),
    "python": LanguageConfig("py", python_cmd),
    "ruby": LanguageConfig("rb", ruby_cmd),
    "rust": LanguageConfig("rs", rust_cmd, rust_build, timing=False),
    "scala": LanguageConfig("scala", scala_cmd, scala_build, timing=False),
    "typescript": LanguageConfig("ts", typescript_cmd, typescript_build),
}


def language_config(language):
    if language in LANGUAGES:
        return LANGUAGES[language]
    else:
        raise Exception(f"Unknown language {language}")


def all_languages():
    return [l for l in LANGUAGES.keys()]