from setuptools import setup, find_packages
# from mc_server_manager import __version__

def read_version():
    with open("mc_server_manager/version.txt", "r") as f:
        return f.read().strip()

setup(
    name="mc-server-manager",
    version=read_version(),
    # packages=find_packages(),
    install_requires=[
        "process-controller @ git+https://github.com/yousefalshaikh17/system-process-controller.git",
        "python-dotenv",
        "mcstatus"
    ],
    py_modules=['mc_server_manager']
)