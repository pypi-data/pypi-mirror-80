from setuptools import setup
import readonly_docs_theme

setup(
    name='readonly-docs-theme',
    version=readonly_docs_theme.__version__,
    description='Theme for ReadOnly Mods documentation',
    url='https://github.com/ReadOnly-Mods/readonly-docs-theme',
    author='ReadOnly-Mods',
    license='MIT',

    packages=['readonly_docs_theme'],
    install_requires=['sphinx_rtd_theme==0.1.9'],

    message_extractors={
        'src/theme/js': [
            ('**.js', 'javascript', None),
        ]
    },

    zip_safe=False,
    package_data={'readonly_docs_theme': [
        '*.json',
        'favicon.ico',
        'theme.pot',
        'templates/*.html',
        'static/*',
        'static/*/*',
        'extra/*'
    ]},
    scripts=[
        'dist/scripts/build-language',
        'dist/scripts/language-code',
        'dist/scripts/list-translations',
        'dist/scripts/list-versions',
        'dist/scripts/pr-comment',
        'dist/scripts/pr-deploy',
        'dist/scripts/travis-prepare'
    ],

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Framework :: Sphinx',
        'Framework :: Sphinx :: Extension',
    ]
)
