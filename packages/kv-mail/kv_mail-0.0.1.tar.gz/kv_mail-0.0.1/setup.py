from setuptools import setup,find_packages
def readme():
    with open('README.md') as f:
        README=f.read()
    return README
setup(
    name='kv_mail',
    version='0.0.1',
    description='simplified code of sending mail',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='',
    author='krupal vora',
    author_email='krupal.vora@sakec.ac.in',
    License='MIT',
    classifiers=[
    'Intended Audience :: Education',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.7',
    ],
    keywords='kv_mail',
    packages=['kv_mail'],
    include_package_data=True,
    install_requires=['smtplib'],
)