# -*- coding: utf-8 -*-
import os
from ckan import plugins
import ckan.model as model
import ckan.logic as logic
from ckan.plugins import toolkit
from ckan.common import _, g
import json
import copy
import six
from . import auth
import logging
log = logging.getLogger(__name__)


def url_helper(endpoint, **kwargs):
    """
    Custom URL helper for backward compatibility with CKAN 2.11
    Maps old URL patterns to new ones
    """
    if endpoint == 'home':
        return toolkit.h.url_for('home.index')
    else:
        return toolkit.h.url_for(endpoint, **kwargs)


# @timer(seconds=3600)
# def update_views_count(signal_number):
#     """
#     Updates Views Count
#     """
#     os.system(
#         'sh /srv/app/src/ckan/ckanext-dados_cmporto_pt/ckanext/dados_cmporto_pt/tracking.sh')


class DadosCMPortoPTPlugin(plugins.SingletonPlugin):
    '''
    Theme for the dados.cmporto.pt portal - CKAN 2.11 compatible
    '''
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IConfigurable)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IPackageController, inherit=True)

    # IConfigurer
    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('public', 'dados_cmporto_pt')

    # IConfigurable
    def configure(self, config):
        self.is_dcat_plugin_active = 'dcat' in config.get('ckan.plugins', '')

    # ITemplateHelpers
    def get_helpers(self):
        return {'is_dcat_plugin_active': lambda: self.is_dcat_plugin_active,
                'group_list_all_fields': lambda: toolkit.get_action('group_list')(data_dict={'all_fields': True}),
                'get_recent_datasets': get_recent_datasets,
                'get_most_pop_datasets': get_most_pop_datasets,
                'get_top_tags': get_top_tags,
                'get_total_tags': get_total_tags,
                'get_total_views': get_total_views,
                'get_total_datasets': get_total_datasets,
                'get_total_resources' : get_total_resources,
                'get_all_datasets' : get_all_datasets,
                'url': url_helper
                }


def get_recent_datasets():
    try:
        _ctx = {'model': model, 'session': model.Session,
                'user': getattr(g, 'user', None), 'ignore_auth': True}
        result = logic.get_action('package_search')(
            _ctx, {'rows': 5, 'sort': 'metadata_modified desc', 'q': 'type:(dataset OR simples OR composto)'})
        return result['results']
    except Exception as e:
        log.error('Error getting recent datasets: %s', e)
        return []

def get_all_datasets():
    try:
        _ctx = {'model': model, 'session': model.Session,
                'user': getattr(g, 'user', None), 'ignore_auth': True}
        all_datasets = logic.get_action('package_search')(
            _ctx, {'q': 'type:(dataset OR simples OR composto)'})
        return all_datasets['results']
    except Exception as e:
        log.error('Error getting all datasets: %s', e)
        return []

def get_most_pop_datasets():
    try:
        _ctx = {'model': model, 'session': model.Session,
                'user': getattr(g, 'user', None), 'ignore_auth': True}
        result = logic.get_action('package_search')(
            _ctx, {'sort': 'views_recent desc', 'rows': 5, 'q': 'type:(dataset OR simples OR composto)'})
        results = [logic.get_action('package_show')(
            _ctx, {'id': r['id'], 'include_tracking': True}) for r in result['results']]
        return results
    except Exception as e:
        log.error('Error getting most popular datasets: %s', e)
        return []


def get_top_tags():
    try:
        _ctx = {'model': model, 'session': model.Session,
                'user': getattr(g, 'user', None), 'ignore_auth': True}
        tags_list = logic.get_action('tag_list')(_ctx, {})
        if isinstance(tags_list, list) and len(tags_list) > 0 and isinstance(tags_list[0], tuple):
            return sorted(tags_list, key=lambda x: x[1], reverse=True)[0:min(12, len(tags_list))]
        else:
            # Handle case where tag_list returns simple list of tag names
            return tags_list[0:min(12, len(tags_list))]
    except Exception as e:
        log.error('Error getting top tags: %s', e)
        return []


def get_total_tags():
    try:
        _ctx = {'model': model, 'session': model.Session,
                'user': getattr(g, 'user', None), 'ignore_auth': True}
        result = logic.get_action('tag_list')(_ctx, {})
        return len(result)
    except Exception as e:
        log.error('Error getting total tags: %s', e)
        return 0


def get_total_views():
    try:
        _ctx = {'model': model, 'session': model.Session,
                'user': getattr(g, 'user', None), 'ignore_auth': True}
        all_datasets = logic.get_action('package_search')(
            _ctx, {'q': 'type:(dataset OR simples OR composto)'})
        total = 0
        for r in all_datasets['results']:
            d = logic.get_action('package_show')(
                _ctx, {'id': r['id'], 'include_tracking': True})
            tracking = d.get('tracking_summary', {})
            total += tracking.get('total', 0)
        return total
    except Exception as e:
        log.error('Error getting total views: %s', e)
        return 0

def get_total_datasets():
    try:
        # Use proper context for CKAN 2.11
        _ctx = {'model': model, 'session': model.Session, 'ignore_auth': True}
        dataset_count = logic.get_action('package_search')(_ctx, {'include_private': True, "rows": 1})['count']
        return dataset_count
    except Exception as e:
        log.error('Error getting total datasets: %s', e)
        return 0

def get_total_resources():
    try:
        q = model.Session.query(model.Resource) \
            .join(model.Package) \
            .filter(model.Package.state == 'active') \
            .filter(model.Package.private == False) \
            .filter(model.Resource.state == 'active')

        count = q.count()
        return count
    except Exception as e:
        log.error('Error getting total resources: %s', e)
        return 0