from distutils.core import setup

setup(
    name='dscpy',
    packages=['dscpy'],
    version='0.1',
    license='MIT',
    description='Simple API for dsc.gg',
    author='iscanyc',
    author_email='yucelumitcan@gmil.com',
    url='https://github.com/iscanyc/dsc.py',
    download_url='https://github.com/iscanyc/dsc.py/archive/master.zip',
    keywords=['DSC.GG', 'API'],
    install_requires=[
        'requests'
    ],
)
