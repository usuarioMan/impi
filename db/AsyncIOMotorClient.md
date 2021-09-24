
ASYNCIOMOTORCLIENT METHODS.

aggregate
    aggregate(self, pipeline, **kwargs)
    Execute an aggregation pipeline on this database


command
    Issue a MongoDB command
     command(self, 
        command,
        value=1,
        check=True,
        allowable_errors=None,
        read_preference=None,
        codec_options=CodecOptions(
            document_class=dict,
            tz_aware=False,
            uuid_representation=UuidRepresentation.PYTHON_LEGACY,
            unicode_decode_error_handler='strict', 
            tzinfo=None, 
            type_registry=TypeRegistry(
                type_codecs=[], 
                fallback_encoder=None
                )
            ),
            session=None,
            **kwargs
        )


create_collection
    async create_collection(self, name, codec_options=None, read_preference=None, write_concern=None, read_concern=None, session=None, **kwargs)
 |      Create a new :class:`~pymongo.collection.Collection` in this
 |      database.


dereference
    dereference(self, dbref, session=None, **kwargs)
     |      Dereference a :class:`~bson.dbref.DBRef`, getting the
     |      document it points 


drop_collection
     |  drop_collection(self, name_or_collection, session=None)
 |      Drop a collection.
 |      
 |      :Parameters:


get_collection
     |  get_collection(self, name, codec_options=None, read_preference=None, write_concern=None, read_concern=None)
 |      Get a :class:`~pymongo.collection.Collection` with the given name
 |      and options.


get_io_loop
list_collection_names
list_collections

profiling_info
profiling_level
set_profiling_level
validate_collection
watch
with_options
wrap