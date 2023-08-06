import easydev
import os
import tempfile
import subprocess
import sys
from sequana.pipelines_common import get_pipeline_location as getpath

sharedir = getpath('ribofinder')


def test_standalone_subprocess():
    directory = tempfile.TemporaryDirectory()
    cmd = """sequana_pipelines_ribofinder --input-directory {} 
            --working-directory {} --force""".format(sharedir, directory.name)
    subprocess.call(cmd.split())


def test_standalone_script():
    directory = tempfile.TemporaryDirectory()
    import sequana_pipelines.ribofinder.main as m
    sys.argv = ["test", "--input-directory", sharedir, 
            "--working-directory", directory.name, "--force", "--rRNA-file", sharedir+"feature.fasta"]
    m.main()

def test_full():
    with tempfile.TemporaryDirectory() as directory:
        wk = directory

        cmd = "sequana_pipelines_ribofinder --input-directory {} "
        cmd += "--working-directory {}  --force --rRNA-file {}/feature.fasta"
        cmd = cmd.format(sharedir, wk, sharedir)
        print(cmd)
        subprocess.call(cmd.split())

        stat = subprocess.call("sh ribofinder.sh".split(), cwd=wk)

        assert os.path.exists(wk + "/summary.html")

def test_version():
    cmd = "sequana_pipelines_ribofinder --version"
    subprocess.call(cmd.split())


