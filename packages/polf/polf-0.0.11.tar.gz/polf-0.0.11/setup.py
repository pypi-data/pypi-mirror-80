import io
import os
import sys
from shutil import rmtree

from setuptools import setup, Extension, Command

__version__ = "0.0.11"
__title__ = "polf"

HERE = os.path.abspath(os.path.dirname(__file__))

TEST_EXTRAS = ["pytest", "flake8"]
DOC_EXTRAS = [
    'Sphinx>=3.2.1',
    'sphinx-rtd-theme==0.4.3',
]
EXTRAS = {
    "dev": ["twine", "bump2version"] + TEST_EXTRAS + DOC_EXTRAS,
    "test": TEST_EXTRAS,
    "doc": DOC_EXTRAS,
}

with io.open(os.path.join(HERE, "README.md"), encoding="utf-8") as f:
    LONG_DESCRIPTION = "\n" + f.read()

define_macros = []
extra_compile_args = []
if os.environ.get("DEBUG"):
    define_macros.extend([("DEBUG", "1")])
extension = Extension(__title__,
                      language="c",
                      sources=[os.path.join('src', 'pypolf.c')],
                      define_macros=define_macros,
                      extra_compile_args=extra_compile_args)


class UploadCommand(Command):
    """Support setup.py upload."""

    description = "Build and publish the package."
    user_options = [
        ("test", None, "Specify if you want to test your upload to Pypi."),
    ]

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print("\033[1m{0}\033[0m".format(s))

    def initialize_options(self):
        self.test = None

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status("Removing previous builds…")
            rmtree(os.path.join(HERE, "dist"))
        except OSError:
            pass

        self.status("Building Source distribution…")
        os.system("{0} setup.py sdist".format(sys.executable))

        self.status("Uploading the package to PyPI via Twine…")
        cmd = "twine upload%s dist/*" % (
            " --repository-url https://test.pypi.org/legacy/" if self.test
            else ""
        )
        os.system(cmd)
        sys.exit()


setup(
    name=__title__,
    version=__version__,
    description='Calculate points on lines.',
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    license="BSD License",
    classifiers=[
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Scientific/Engineering :: Image Processing",
        "Topic :: Multimedia :: Graphics",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
    ],
    python_requires='>=3.6',
    zip_safe=False,
    ext_modules=[extension],
    include_package_data=True,
    cmdclass={
        "upload": UploadCommand,
    },
    extras_require=EXTRAS,
)
