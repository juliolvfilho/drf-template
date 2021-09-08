import json
import logging
from django.conf import settings
from django.utils import timezone
from requestlogs.entries import RequestLogEntry
from requestlogs.storages import BaseStorage
from rest_framework import fields
from rest_framework.serializers import Serializer
from rest_framework.utils.encoders import JSONEncoder

logger = logging.getLogger("requestlogs")


class CustomRequestLogEntry(RequestLogEntry):
    @property
    def user(self):
        return self._user or getattr(self.django_request, "user", None)


class DataShrinkField(fields.DictField):
    """
    This class can abbreviate long JSON logs
    """

    def shrink_dict(self, data):
        shrink_candidates = []
        for key in data:
            field = data[key]
            if isinstance(field, dict) or isinstance(field, list):
                shrink_candidates.append(
                    {
                        "key": key,
                        "size": len(json.dumps(field, cls=JSONEncoder)),
                    }
                )
            if isinstance(field, str) and len(field) > 100:
                shrink_candidates.append({"key": key, "size": len(field) + 2})
        if len(shrink_candidates) > 0:
            shrink = sorted(shrink_candidates, key=lambda k: k["size"], reverse=True)[0]
            shrink_field = data[shrink["key"]]
            if isinstance(shrink_field, dict):
                return (
                    shrink["key"],
                    "(object, size: {}, keys: {})".format(
                        shrink["size"], len(shrink_field.keys())
                    ),
                )
            if isinstance(shrink_field, list):
                return (
                    shrink["key"],
                    "(list, size: {}, count: {})".format(
                        shrink["size"], len(shrink_field)
                    ),
                )
            if isinstance(shrink_field, str):
                return (
                    shrink["key"],
                    shrink_field[:75]
                    + "... (+ {} characters)".format(len(shrink_field) - 75),
                )
        return (None, None)

    def to_representation(self, value):
        while True:
            json_str = json.dumps(value, cls=JSONEncoder)
            data = json.loads(json_str)
            if len(json_str) > settings.REQUESTLOGS.get(
                "SHRINK_JSON_GREATER_THAN", 256
            ):
                if isinstance(data, dict):
                    (key, shrink_value) = self.shrink_dict(data)
                    if key:
                        value[key] = shrink_value
                    else:
                        break
                elif isinstance(data, list):
                    shrink_value = []
                    shrink_value.append(self.to_representation(data[0]))
                    if len(data) > 1:
                        shrink_value.append("(+ {} elements)".format(len(data) - 1))
                    data = shrink_value
                    break
            elif isinstance(data, str):
                data = self.to_representation({"str": data}).get("str")
                break
            else:
                break
        return data


class CustomRequestLogEntrySerializer(Serializer):
    time = fields.SerializerMethodField()
    user_uid = fields.SerializerMethodField()
    method = fields.CharField(source="request.method")
    path = fields.SerializerMethodField()
    query = fields.DictField(source="request.query_params")
    payload = DataShrinkField(source="request.data")
    status = fields.IntegerField(source="response.status_code")
    response = DataShrinkField(source="response.data")
    ip_address = fields.CharField()
    execution_time = fields.DurationField()

    def get_time(self, obj):
        return timezone.now().isoformat()

    def get_user_uid(self, obj):
        return obj.user.get("uid") if obj.user else None

    def get_path(self, obj):
        return obj.request.full_path.split("?", 1)[0]

    @property
    def data(self):
        data = super().data
        return json.dumps(data, cls=JSONEncoder)


class CustomRequestLogStorage(BaseStorage):
    def store(self, entry):
        if entry.request.method not in settings.REQUESTLOGS.get(
            "METHODS", ["GET", "PUT", "PATCH", "POST", "DELETE"]
        ):
            # do not log unwanted methods
            pass
        elif entry.request.method == "GET" and entry.response.data is None:
            # response from cache, ignoring...
            pass
        else:
            logger.info(self.prepare(entry))
