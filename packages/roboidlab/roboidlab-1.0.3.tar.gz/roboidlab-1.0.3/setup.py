from setuptools import setup, find_packages

setup(
	name="roboidlab",
	version="1.0.3",
	author="Kwang-Hyun Park",
	author_email="akaii@kw.ac.kr",
	description="Python Package for Roboid Laboratory",
	long_description=open("README.md").read(),
	long_description_content_type="text/markdown",
	install_requires=["roboid", "pynput", "pandas", "matplotlib"],
	packages=find_packages(exclude=["examples", "tests"]),
	python_requires=">=3",
	zip_safe=False,
	classifiers=[
		"License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)"
	]
)