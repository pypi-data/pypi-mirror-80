import json

from django.apps import apps
from jsa_auth_middleware.query_response import Response
from jsa_utils.assets import (
    get_contents,
    get_modifier,
    build_query_filter,
    build_query_sorter,
    build_pagination_markers,
)


def get_property_object(field=None):
    exempted_types = ["FSMField", "AuditlogHistoryField"]

    fld_obj = {}
    if field:
        fld_type = str(field.__class__.__name__)

        if fld_type == "ForeignKey" or fld_type == "ManyToManyField":
            # Capture relations
            fld_obj["label"] = str(field.verbose_name).title()
            fld_obj["key"] = str(field.attname)
            fld_obj["type"] = field.related_model.__name__
            fld_obj["cardinality"] = "FK" if field.many_to_one else "M2M"

        if fld_type != "ForeignKey" and fld_type not in exempted_types:
            fld_obj["label"] = str(field.verbose_name).title()
            fld_obj["key"] = str(field.attname)
            fld_obj["type"] = str(field.__class__.__name__)

    return fld_obj


def get_property_value(entity=None, property=None):

    value = ""
    if entity and property:
        prop_obj = entity._meta.get_field(property)
        prop_type = prop_obj.get_internal_type()

        if prop_type == "DateTimeField":
            value = (
                getattr(entity, property).strftime("%a %b %d,%Y at %I:%M%p")
                if getattr(entity, property)
                else "-"
            )
            return value

        elif prop_type == "DateField":
            value = (
                getattr(entity, property).strftime("%a %b %d,%Y")
                if getattr(entity, property)
                else "-"
            )
            return value

        elif prop_type == "CharField":
            value = getattr(entity, property)
            return value

        elif prop_type == "BooleanField":
            value = getattr(entity, property)
            return value

        elif prop_type == "DecimalField" or prop_type == "AutoField":
            value = getattr(entity, property)
            return str(value)

        elif prop_type == 'FileField':
            value = getattr(entity, property)
            if value:
                return value.url
            else:
                return '-'

        else:
            value = getattr(entity, property)
            return value

    return value


def introspect_entity_action(app_name=None, entity=None):

    if app_name and entity:
        # Get Model
        model = apps.get_model(app_name, entity)
        properties = []
        if model:
            # Return all fields
            fields = model._meta.get_fields()
            properties = [i for i in [get_property_object(x) for x in fields] if i]

        return properties


def read_entity_action(**kwargs):

    app_name = kwargs.get("app_name")
    entity_name = kwargs.get("entity_name")
    properties = kwargs.get("properties")
    resp = kwargs.get("resp", Response())
    page_size = kwargs.get("pageSize")
    page_index = kwargs.get("pageIndex")
    filters = kwargs.get("filter")
    sorter = kwargs.get("sort")

    # Get Model
    query_model = apps.get_model(app_name, entity_name)
    if query_model:
        # args = build_query_sorter(sorter)
        kwargs = build_query_filter(filters)  # Set filters
        pager = build_pagination_markers(page_index, page_size)  # Set pagination

        # Run query
        result_size = query_model.objects.filter(**kwargs).count()  # Get result size
        results = query_model.objects.filter(**kwargs)[pager["lm"]:pager["um"]]
        response_set = []
        for entry in results:
            # Cache attribute values of each instance
            entry_obj = {}
            for prop in properties:
                prop_name = prop.get("field", None)
                if prop_name is not None:
                    entry_obj[prop_name] = get_property_value(entry, prop_name)

            response_set.append(entry_obj)
        # Package results
        resp.passed()
        resp.add_param("result_size", result_size)
        resp.add_param("result", response_set)

    else:
        print("--->> No matching Model found!..")
        resp.failed()
        resp.add_message("-- No matching model found!..")
