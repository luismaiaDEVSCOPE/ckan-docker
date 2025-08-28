# ckanext-dados_cmporto_pt

Custom theme extension for Dados Abertos CM Porto CKAN 2.11

## Description

This extension provides custom templates and functionality for the Dados Abertos CM Porto portal, including:
- Custom dataset display templates
- Enhanced package detail views
- Portal-specific helper functions for statistics
- Portuguese localization support

## Installation

1. Install the extension in development mode:
   ```bash
   pip install -e /srv/app/src_extensions/ckanext-dados_cmporto_pt
   ```

2. Add the plugin to your CKAN configuration file (`ckan.ini` or `development.ini`):
   ```ini
   ckan.plugins = ... dados_cmporto_pt
   ```

3. Restart your CKAN instance.

## Features

The extension includes:
- **Template helpers**: Functions for retrieving statistics about datasets, resources, views, and tags
- **Custom templates**: Enhanced views for dataset display
- **Portal branding**: CM Porto specific styling and layout

## Helper Functions

- `get_recent_datasets()` - Get 5 most recently updated datasets
- `get_most_pop_datasets()` - Get 5 most popular datasets by views
- `get_total_datasets()` - Get total number of datasets
- `get_total_resources()` - Get total number of resources
- `get_total_views()` - Get total view count across all datasets
- `get_top_tags()` - Get top 12 most used tags
- `get_total_tags()` - Get total number of tags

## Compatibility

This extension is compatible with:
- CKAN 2.11+
- Python 3.8+

## Development

This extension follows CKAN 2.11 best practices and uses modern Python patterns for better maintainability.

## License

This project is licensed under the GNU Affero General Public License v3 or later (AGPLv3+).

## Author

ParadigmaXis - mail@ParadigmaXis.pt
