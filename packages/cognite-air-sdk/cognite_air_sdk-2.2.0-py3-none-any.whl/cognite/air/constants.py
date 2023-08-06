# Model- and schedule asset constants:
SA_EXT_ID = "schedule_asset_ext_id"
SA_FIELD_META_DATA = "data"
MA_FIELD_META_FIELDS = "fields"
MA_FIELD_META_MODELVERSION = "modelVersion"

# Constants related to CDF Event and Time Series resources:
EVENT_EXT_ID = "external_id"
EVENT_TYPE = "type"
EVENT_SUBTYPE = "subtype"
EVENT_ASSET_IDS = "asset_ids"
EVENT_DATA_SET_ID = "data_set_id"
EVENT_DATA_SET_IDS = "data_set_ids"
EVENT_METADATA = "metadata"
AIR_EVENTS_FIELD_TYPE = "AIR"
AIR_EVENTS_FIELD_SUBTYPE = "model_output"
AIR_ALERT_EVENTS_FIELD_SUBTYPE = "ALERT"
AIR_EVENTS_META_KEY_MODEL = "model"
AIR_EVENTS_META_KEY_MODEL_VERSION = "model_version"
AIR_EVENTS_META_KEY_SA_EXT_ID = SA_EXT_ID
AIR_EVENTS_META_KEY_DASHBOARD_ID = "dashboardId"
AIR_EVENTS_META_KEY_SYSTEM_ID = "systemId"
AIR_EVENTS_META_KEY_ORIGINAL_MODEL_VERSION = "original_model_version"
AIR_EVENTS_META_KEY_PROJECT_NAME = "project_name"
AIR_EVENTS_META_KEY_SKIP_NOTIFICATION = "skip_notification"
AIR_EVENTS_META_KEY_ACKNOWLEDGED = "acknowledged"

AIR_TS_FIELD_DATASET = "data_set_id"
AIR_TS_FIELD_ASSET_ID = "asset_id"
AIR_TS_FIELD_METADATA = "metadata"
AIR_TS_META_KEY_MODEL_VERSION = "model_version"


AIR_META_BACKFILL_COMPLETE = "backfill_complete"
AIR_META_BACKFILLED_UNTIL = "backfilled_until"
AIR_META_BACKFILL_LOCK = "backfill_lock"
AIR_META_BACKFILL_LOCK_SET_TIME_UNIX = "backfill_lock_set_time"
AIR_META_BACKFILL_LOCK_MAX_LOCK_TIME = 30 * 60 * 1000  # 30 mins
