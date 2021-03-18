from cx_Freeze import setup, Executable

base = None

executables = [Executable("bot.py", base=base)]

packages = ['idna', 'datetime', 'os', 'chromedriver_autoinstaller', 'codecs', 'time', 'selenium']
options = {
    'build_exe': {
        'packages': packages,
    },
}

setup(
    name='Lingos BOT - By Kamil G',
    options=options,
    version='0.1',
    description='The lingos bot',
    executables=executables
)
