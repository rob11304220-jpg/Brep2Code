from importlib.resources import files


def test_contract_schemas_are_packaged() -> None:
    schemas = files("brep2code").joinpath("schemas")

    assert schemas.joinpath("case.schema.json").is_file()
    assert schemas.joinpath("manifest.schema.json").is_file()
