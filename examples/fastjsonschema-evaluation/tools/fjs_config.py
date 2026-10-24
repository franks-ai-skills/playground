"""fastjsonschema in the configuration an adoption would use: metaschema check before every
compile, absolute self-references (workaround), fail-closed local-only references, all errors."""
import json
from pathlib import Path

import fastjsonschema

from convert07 import absolutize

META7 = json.loads((Path(__file__).parent / "draft-07.schema.json").read_text(encoding="utf-8"))
_meta7 = fastjsonschema.compile(META7, use_default=False, use_formats=True)
ERRORS = (fastjsonschema.JsonSchemaValueException, fastjsonschema.JsonSchemaValuesException)


class LocalOnly(dict):
    """Claims every URI scheme, so fastjsonschema never falls back to urllib.request.urlopen;
    resolves only exact local schema ids."""

    def __init__(self, store):
        super().__init__()
        self.store = store

    def __contains__(self, scheme):
        return True

    def __getitem__(self, scheme):
        def resolve(uri):
            base = uri.split("#", 1)[0]
            if base in self.store:
                return self.store[base]
            raise LookupError(f"reference refused: {uri!r}")
        return resolve


def check_schema(schema):
    """Raise unless the (converted) schema satisfies the Draft-07 metaschema."""
    _meta7(schema)


def compile_checked(schema, store, *, absolute=True, fast_fail=False):
    """store: converted schemas by $id (absolutized when absolute)."""
    check_schema(schema)
    return fastjsonschema.compile(absolutize(schema) if absolute else schema, handlers=LocalOnly(store),
                                  use_default=False, use_formats=False, fast_fail=fast_fail)
