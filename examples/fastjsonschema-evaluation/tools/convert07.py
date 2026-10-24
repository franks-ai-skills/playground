"""Draft 2020-12 -> Draft-07 conversion for Forge's schemas."""
import copy

DRAFT7_URI = "http://json-schema.org/draft-07/schema#"
PREFIX = "urn:harness-forge:schema:"
NOT_IN_DRAFT7 = {"prefixItems", "unevaluatedProperties", "unevaluatedItems", "dependentRequired",
                 "dependentSchemas", "$anchor", "$dynamicRef", "$dynamicAnchor", "minContains", "maxContains"}


def convert(schema, root=True):
    """Draft 2020-12 -> Draft-07 for the keywords Forge's schemas use; refuses the keywords in NOT_IN_DRAFT7
    (an enumerated set, not every keyword Draft-07 lacks) and $ref with siblings."""
    if isinstance(schema, list):
        return [convert(item, False) for item in schema]
    if not isinstance(schema, dict):
        return schema
    if "$ref" in schema and len(set(schema) - {"$ref", "description", "title", "$comment"}) > 0:
        raise ValueError(f"$ref with siblings is ignored in Draft-07: {sorted(schema)}")
    out = {}
    for key, value in schema.items():
        if key in ("properties", "patternProperties", "definitions"):
            out[key] = {name: convert(sub, False) for name, sub in value.items()}
        elif key == "$defs":
            # Draft-07's metaschema does not descend into $defs, so a malformed definition would pass it.
            out["definitions"] = {name: convert(sub, False) for name, sub in value.items()}
        elif key == "$ref":
            out[key] = value.replace("#/$defs/", "#/definitions/")
        elif key in ("enum", "const", "required", "examples", "default"):
            out[key] = copy.deepcopy(value)
        elif key == "prefixItems":
            continue
        else:
            out[key] = convert(value, False)
    if "prefixItems" in schema:
        out["items"] = convert(schema["prefixItems"], False)
        if "items" in schema:
            out["additionalItems"] = convert(schema["items"], False)
    if root and isinstance(schema, dict) and ("$schema" in schema or "$id" in schema):
        out["$schema"] = DRAFT7_URI
    if "$defs" in schema and "definitions" in schema:
        raise ValueError("both $defs and definitions")
    left = NOT_IN_DRAFT7 & set(out)
    if left:
        raise ValueError(f"keywords without a Draft-07 equivalent: {sorted(left)}")
    return out




def absolutize(schema, base=None):
    """Write every local "#..." $ref as "<own $id>#...": fastjsonschema 2.22.2 resolves a local
    ref inside a remotely resolved schema against the root schema instead (see the evaluation report)."""
    if isinstance(schema, dict):
        base = schema.get("$id", base)
        return {key: (base + value if key == "$ref" and isinstance(value, str) and value.startswith("#") and base
                      else absolutize(value, base)) for key, value in schema.items()}
    if isinstance(schema, list):
        return [absolutize(item, base) for item in schema]
    return schema
