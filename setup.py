from setuptools import setup, find_packages

setup(
    name='time-tracker',
    version='0.1.0',
    author='Your Name',
    author_email='your.email@example.com',
    description='A local macOS application for tracking and logging time usage during working hours.',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'pyobjc',
        'pynput',
        'sqlite3',
        'pandas',
        'streamlit',  # or 'dash' if you choose Dash/Plotly
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: MacOS',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.6',
)