# Scrapy settings for mkrf project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#
# Or you can copy and paste them from where they're defined in Scrapy:
# 
#     scrapy/conf/default_settings.py
#

BOT_NAME = 'mkrf'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['mkrf.spiders']
NEWSPIDER_MODULE = 'mkrf.spiders'
DEFAULT_ITEM_CLASS = 'mkrf.items.FilmItem'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)

DEFAULT_RESPONSE_ENCODING = 'utf-8'

ITEM_PIPELINES = [
    'mkrf.pipelines.FileExportPipeline'
]
EXPORTERS = {
    'mkrf.items.FilmItem': {
        'format':'csv',
        'file': 'films.csv',
        'encoding': 'utf8',
        'fields': ('title',
             'id',
             'genre',
             'firm',
             'country',
             'year',
             'dubbed',
             'category',
             'orig_language',
             'orig_title',
             'format',
             'series',
             'colour',
             'parts',
             'footage',
             'duration',
             'limitation',
             'producer',
             'scenario',
             'director',
             'composer',
             'operator',
             'artist',
             'note',
             'annotation',
             'blocked')
    },
    'mkrf.items.LicenseItem':{
        'format':'csv',
        'file': 'licenses.csv',
        'encoding': 'utf8',
        'fields': ('lic_num',
            'id',
             'lic_date',
             'cat',
             'exp',
             'add',
             'firm',
             'tel',
             'num',
             'date_beg',
             'date_end')
    }
}

