# -*- coding: utf-8 -*-

from plone import api
import logging

logger = logging.getLogger('cpskin.agenda')


def install(context):
    if context.readDataFile('cpskin.agenda-default.txt') is None:
        return

    logger.info('Installing')
    portal = api.portal.get()
    addCatalogIndexes(portal)


def addCatalogIndexes(portal):
    """
    Method to add our wanted indexes to the portal_catalog.
    We couldn't do it in the profile directly, see :
        http://maurits.vanrees.org/weblog/archive/2009/12/catalog
    """
    catalog = api.portal.get_tool('portal_catalog')
    indexes = catalog.indexes()
    wanted = (('event_dates', 'FieldIndex'),)
    indexables = []
    for name, meta_type in wanted:
        if name not in indexes:
            catalog.addIndex(name, meta_type)
            indexables.append(name)
            logger.info('Added %s for field %s.', meta_type, name)
    if len(indexables) > 0:
        logger.info('Indexing new indexes %s.', ', '.join(indexables))
        catalog.manage_reindexIndex(ids=indexables)
