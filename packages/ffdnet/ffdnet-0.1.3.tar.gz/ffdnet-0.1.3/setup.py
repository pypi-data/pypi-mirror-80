from distutils.core import setup

setup(
    name = 'ffdnet',
    packages = ['ffdnet'],
    version = '0.1.3',
    license='GPLv3',
    description = 'FFDNet CNN denoiser',
    url = 'https://github.com/kidanger/ffdnet',
    author = 'Jérémy Anger',
    author_email = 'angerj.dev@gmail.com',
    install_requires = [
        'numpy',
        'torch',
        'fire',
        'imageio',
    ],
    include_package_data=True,
    python_requires=">=3",
    entry_points="""
    [console_scripts]
    ffdnet=ffdnet:cli_main
    """,
)
