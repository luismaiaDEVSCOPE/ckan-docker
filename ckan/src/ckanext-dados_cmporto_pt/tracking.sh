#!/bin/sh
ckan -c /srv/app/production.ini tracking update  && ckan -c /srv/app/production.ini search-index rebuild -r
