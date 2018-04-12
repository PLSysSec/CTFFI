if __name__ == '__main__':
    from setuptools import setup
    setup(
        name='ctffi',
        description='FFI for Python to compile and call FaCT code.',
        long_description="""
# CTFFI

Foreign Function Interface for Python calling FaCT code, based on CFFI.

(C) 2018 Riad S. Wahby <rsw@cs.stanford.edu> and the FaCT authors.
""",
        version='0.0.1',
        packages=['ctffi'],
        zip_safe=False,
        url='https://github.com/PLSysSec/CTFFI',
        author='Riad S. Wahby, the FaCT authors',
        author_email='rsw@cs.stanford.edu',
        license='Apache 2.0',
        install_requires=['cffi'],
    )
