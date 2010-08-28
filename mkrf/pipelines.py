# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

from scrapy.xlib.pydispatch import dispatcher
from scrapy.core import signals
from scrapy.core.exceptions import NotConfigured
from scrapy.contrib import exporter
from scrapy.conf import settings
from scrapy.utils.misc import load_object
from scrapy import log

def get_exporter_and_file(opts):
    format = opts['format']
    filename = opts['file']
    if not format or not filename:
        raise NotConfigured
    exp_kwargs = {
        'fields_to_export': opts.get('fields') or None,
        'export_empty_fields': opts.get('empty', False),
        'encoding': opts.get('encoding', 'utf-8'),
    }
    file = open(filename, 'wb')
    if format == 'xml':
        exp = exporter.XmlItemExporter(file, **exp_kwargs)
    elif format == 'csv':
        exp = exporter.CsvItemExporter(file, **exp_kwargs)
    elif format == 'csv_headers':
        exp = exporter.CsvItemExporter(file, include_headers_line=True, \
            **exp_kwargs)
    elif format == 'pprint':
        exp = exporter.PprintItemExporter(file, **exp_kwargs)
    elif format == 'pickle':
        exp = exporter.PickleItemExporter(file, **exp_kwargs)
    elif format == 'json':
        from scrapy.contrib.exporter import jsonlines
        exp = jsonlines.JsonLinesItemExporter(file, **exp_kwargs)
    else:
        raise NotConfigured("Unsupported export format: %s" % format)
    return exp, file

class FileExportPipeline(object):

    def __init__(self):
        self.pipelines = {}
        for cls, opts in settings['EXPORTERS'].items():
            item_class = load_object(cls)
            exporter, file = get_exporter_and_file(opts)
            self.pipelines[item_class] = (exporter, file)
            exporter.start_exporting()
        dispatcher.connect(self.engine_stopped, signals.engine_stopped)

    def process_item(self, spider, item):
        item_class = type(item)
        if item_class in self.pipelines:
            exporter, file = self.pipelines[item_class]
            exporter.export_item(item)
        else:
            log.msg("Wrong type of item")
        return item

    def engine_stopped(self):
        for (exporter, file) in self.pipelines.values():
            exporter.finish_exporting()
            file.close()
