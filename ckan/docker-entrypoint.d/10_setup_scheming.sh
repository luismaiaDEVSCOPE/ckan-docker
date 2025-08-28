#!/bin/bash
set -e

# Set scheming dataset schemas
ckan config-tool ckan.ini "scheming.dataset_schemas = ckanext.scheming:/srv/app/src/ckanext-scheming/scheming/ckan_dataset.json"

# Set scheming presets
ckan config-tool ckan.ini "scheming.presets = ckanext.scheming:/srv/app/src/ckanext-scheming/scheming/presets.json"

# Copy form snippets to templates
cp /srv/app/src/ckanext-scheming/scheming/form_snippets/users_select.html /srv/app/src/ckanext-scheming/ckanext/scheming/templates/scheming/form_snippets/