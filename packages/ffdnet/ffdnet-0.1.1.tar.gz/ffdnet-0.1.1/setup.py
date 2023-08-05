from distutils.core import setup

setup(
    name = 'ffdnet',
    packages = ['ffdnet'],
    version = '0.1.1',
    license='GPLv3',
    description = 'FFDNet CNN denoiser',
    url = 'https://github.com/kidanger/ffdnet',
    author = 'Jérémy Anger',
    author_email = 'angerj.dev@gmail.com',
    install_requires = [
        'numpy',
        'torch',
    ],
    extras_require = {
        'cli':  ["fire", "imageio"],
    },
    entry_points="""
    [console_scripts]
    ffdnet=ffdnet:cli_main
    """,
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
)
