from vcstools import GitClient
from vcstools.vcs_base import VcsError

        subprocess.check_call("git init", shell=True, cwd=self.remote_path)
        subprocess.check_call("touch fixed.txt", shell=True, cwd=self.remote_path)
        subprocess.check_call("git add *", shell=True, cwd=self.remote_path)
        subprocess.check_call("git commit -m initial", shell=True, cwd=self.remote_path)
        subprocess.check_call("git tag test_tag", shell=True, cwd=self.remote_path)
        subprocess.check_call("git branch test_branch", shell=True, cwd=self.remote_path)
        po = subprocess.Popen("git log -n 1 --pretty=format:\"%H\"", shell=True, cwd=self.remote_path, stdout=subprocess.PIPE)
        subprocess.check_call("touch modified.txt", shell=True, cwd=self.remote_path)
        subprocess.check_call("touch modified-fs.txt", shell=True, cwd=self.remote_path)
        subprocess.check_call("git add *", shell=True, cwd=self.remote_path)
        subprocess.check_call("git commit -m initial", shell=True, cwd=self.remote_path)
        po = subprocess.Popen("git log -n 1 --pretty=format:\"%H\"", shell=True, cwd=self.remote_path, stdout=subprocess.PIPE)
        subprocess.check_call("touch deleted.txt", shell=True, cwd=self.remote_path)
        subprocess.check_call("touch deleted-fs.txt", shell=True, cwd=self.remote_path)
        subprocess.check_call("git add *", shell=True, cwd=self.remote_path)
        subprocess.check_call("git commit -m modified", shell=True, cwd=self.remote_path)
        po = subprocess.Popen("git log -n 1 --pretty=format:\"%H\"", shell=True, cwd=self.remote_path, stdout=subprocess.PIPE)
        subprocess.check_call("git tag last_tag", shell=True, cwd=self.remote_path)
        subprocess.check_call("git reset --hard test_tag", shell=True, cwd=self.local_path)
        subprocess.check_call("git reset --hard test_tag", shell=True, cwd=self.local_path)
        subprocess.check_call("git config --replace-all branch.master.merge master", shell=True, cwd=self.local_path)
           
        subprocess.check_call("git checkout test_tag -b localbranch", shell=True, cwd=self.local_path)
        subprocess.check_call("touch local.txt", shell=True, cwd=self.local_path)
        subprocess.check_call("git add *", shell=True, cwd=self.local_path)
        subprocess.check_call("git commit -m my_branch", shell=True, cwd=self.local_path)
        subprocess.check_call("git tag my_branch_tag", shell=True, cwd=self.local_path)
        po = subprocess.Popen("git log -n 1 --pretty=format:\"%H\"", shell=True, cwd=self.local_path, stdout=subprocess.PIPE)
        subprocess.check_call("git checkout test_tag", shell=True, cwd=self.local_path)
        subprocess.check_call("touch tagged.txt", shell=True, cwd=self.local_path)
        subprocess.check_call("git add *", shell=True, cwd=self.local_path)
        subprocess.check_call("git commit -m no_branch", shell=True, cwd=self.local_path)
        subprocess.check_call("git tag no_br_tag", shell=True, cwd=self.local_path)
        subprocess.check_call("touch dangling.txt", shell=True, cwd=self.local_path)
        subprocess.check_call("git add *", shell=True, cwd=self.local_path)
        subprocess.check_call("git commit -m dangling", shell=True, cwd=self.local_path)
        po = subprocess.Popen("git log -n 1 --pretty=format:\"%H\"", shell=True, cwd=self.local_path, stdout=subprocess.PIPE)
        subprocess.check_call("git checkout master", shell=True, cwd=self.local_path)
    def test_inject_protection(self):
        client = GitClient(self.local_path)
        try:
            client.is_tag('foo"; bar"', fetch = False)
            self.fail("expected Exception")
        except VcsError: pass
        try:
            client.rev_list_contains('foo"; echo bar"', "foo", fetch = False)
            self.fail("expected Exception")
        except VcsError: pass
        try:
            client.rev_list_contains('foo', 'foo"; echo bar"', fetch = False)
            self.fail("expected Exception")
        except VcsError: pass
        try:
            client.get_version('foo"; echo bar"', fetch = False)
            self.fail("expected Exception")
        except VcsError: pass
        
        subprocess.check_call("rm deleted-fs.txt", shell=True, cwd=self.local_path)
        subprocess.check_call("git rm deleted.txt", shell=True, cwd=self.local_path)
        subprocess.check_call("git add modified.txt", shell=True, cwd=self.local_path)
        subprocess.check_call("git add added.txt", shell=True, cwd=self.local_path)
        self.assertEquals('diff --git ./added.txt ./added.txt\nnew file mode 100644\nindex 0000000..454f6b3\n--- /dev/null\n+++ ./added.txt\n@@ -0,0 +1 @@\n+0123456789abcdef\n\\ No newline at end of file\ndiff --git ./deleted-fs.txt ./deleted-fs.txt\ndeleted file mode 100644\nindex e69de29..0000000\ndiff --git ./deleted.txt ./deleted.txt\ndeleted file mode 100644\nindex e69de29..0000000\ndiff --git ./modified-fs.txt ./modified-fs.txt\nindex e69de29..454f6b3 100644\n--- ./modified-fs.txt\n+++ ./modified-fs.txt\n@@ -0,0 +1 @@\n+0123456789abcdef\n\\ No newline at end of file\ndiff --git ./modified.txt ./modified.txt\nindex e69de29..454f6b3 100644\n--- ./modified.txt\n+++ ./modified.txt\n@@ -0,0 +1 @@\n+0123456789abcdef\n\\ No newline at end of file', client.get_diff().rstrip())
        self.assertEquals('diff --git ros/added.txt ros/added.txt\nnew file mode 100644\nindex 0000000..454f6b3\n--- /dev/null\n+++ ros/added.txt\n@@ -0,0 +1 @@\n+0123456789abcdef\n\\ No newline at end of file\ndiff --git ros/deleted-fs.txt ros/deleted-fs.txt\ndeleted file mode 100644\nindex e69de29..0000000\ndiff --git ros/deleted.txt ros/deleted.txt\ndeleted file mode 100644\nindex e69de29..0000000\ndiff --git ros/modified-fs.txt ros/modified-fs.txt\nindex e69de29..454f6b3 100644\n--- ros/modified-fs.txt\n+++ ros/modified-fs.txt\n@@ -0,0 +1 @@\n+0123456789abcdef\n\\ No newline at end of file\ndiff --git ros/modified.txt ros/modified.txt\nindex e69de29..454f6b3 100644\n--- ros/modified.txt\n+++ ros/modified.txt\n@@ -0,0 +1 @@\n+0123456789abcdef\n\\ No newline at end of file', client.get_diff(basepath=os.path.dirname(self.local_path)).rstrip())