"""
打包的工具类
"""
import argparse

from notetool.tool.log import log

from notebuild.shell import run_shell, run_shell_list

logger = log("notebuild")


class PackageBuild:
    """
    打包的工具类
    """

    def __init__(self, name=None):
        res = run_shell("git rev-parse --show-toplevel", printf=False)
        self.name = name or res.split('/')[-1]

    def git_pull(self):
        """
        git pull
        """
        logger.info("{} pull".format(self.name))
        run_shell("git pull")

    def git_push(self):
        """
        git push
        """
        logger.info("{} push".format(self.name))
        run_shell_list([
            'git add -A',
            'git commit -a -m "add"',
            'git push'
        ])

    def git_install(self):
        """
        git install
        """
        logger.info('{} install'.format(self.name))
        run_shell_list([
            'pip uninstall {} -y'.format(self.name),
            'python3 setup.py install',
            'rm -rf {}.egg-info'.format(self.name),
            'rm -rf dist',
            'rm -rf build'
        ])

    def git_build(self):
        """
        git build
        """
        logger.info('{} build'.format(self.name))
        run_shell_list([
            'python3 setup.py build',  # 编译
            'python3 setup.py sdist',  # 生成 tar.gz
            'python3 setup.py bdist_egg',  # 生成 egg 包
            'python3 setup.py bdist_wheel',  # 生成 wheel 包

            # twine register dist/*
            'twine upload dist/*',  # 发布包
            'rm -rf {}.egg-info'.format(self.name),
            'rm -rf dist',
            'rm -rf build',
        ])

    def git_clean_history(self):
        """
        git build
        """
        logger.info('{} clean history'.format(self.name))
        run_shell_list([
            'git checkout --orphan latest_branch',  # 1.Checkout
            'git add -A',  # 2. Add all the files
            'git commit -am "clear history"',  # 3. Commit the changes
            'git branch -D master',  # 4. Delete the branch
            'git branch -m master',  # 5.Rename the current branch to master
            'git push -f origin master',  # 6.Finally, force update your repository
        ])


def command_line_parser():
    parser = argparse.ArgumentParser(description="Test")
    parser.add_argument('command')
    args = parser.parse_args()
    return args


def notebuild():
    """
    build tool
    """
    args = command_line_parser()
    package = PackageBuild()
    if args.command == 'pull':
        package.git_pull()
    elif args.command == 'push':
        package.git_push()
    elif args.command == 'install':
        package.git_install()
    elif args.command == 'build':
        package.git_build()
    elif args.command == 'clean_history':
        package.git_clean_history()
