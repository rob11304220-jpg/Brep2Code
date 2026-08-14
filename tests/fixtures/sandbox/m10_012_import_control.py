"""M10-012 non-matching control: path correction cannot mask an OCP import failure."""

from OCP.Interface import Interface_Static_SetCVal


input_path = "/input/model.step"
assert Interface_Static_SetCVal is not None, input_path
