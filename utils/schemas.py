from marshmallow import Schema, fields, post_load
from attrdict import AttrDict


class EntrySchema(Schema):
    """
    Validating entry
    """
    title = fields.Str()
    url = fields.URL()
    summary = fields.Str()
    time_to_read = fields.Int()
    source_site = fields.Str()
    published_date = fields.Date()
    diseases = fields.List(fields.Str())

    @post_load
    def create_entry(self, data, **kwargs):
        return data
