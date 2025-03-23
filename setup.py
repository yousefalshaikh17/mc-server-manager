from setuptools import setup

def read_version():
    with open("mc_server_manager/version.txt", "r") as f:
        return f.read().strip()

setup(
    name="mc-server-manager",
    version=read_version(),
    install_requires=[
        "process-controller @ git+https://github.com/yousefalshaikh17/system-process-controller.git",
        "python-dotenv",
        "mcstatus"
    ],
    py_modules=['mc_server_manager']
)