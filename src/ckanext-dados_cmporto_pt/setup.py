from setuptools import setup, find_packages

setup(
    name='ckanext-dados_cmporto_pt',
    version='0.1.0',
    description='Dados Abertos CM Porto theme for CKAN 2.11',
    long_description='Custom theme extension for Dados Abertos CM Porto CKAN 2.11',
    url='https://github.com/ParadigmaXis/ckanext-dados_cmporto_pt',
    author='ParadigmaXis',
    author_email='mail@ParadigmaXis.pt',
    license='AGPL',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    keywords='CKAN dados porto portugal theme',
    packages=find_packages(),
    install_requires=[
        # Let CKAN manage its own dependencies
    ],
    include_package_data=True,
    entry_points={
        'ckan.plugins': [
            'dados_cmporto_pt=ckanext.dados_cmporto_pt.plugin:DadosCMPortoPTPlugin',
        ]
    },
)
