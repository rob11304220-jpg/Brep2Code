# M32 Nested-Cylinder Measured-Fact Audit Review

## Result

The offline reporter found exactly two +Z coaxial cylindrical faces with
strictly ordered radii and one shared adjacent planar shoulder in all three
frozen counterbore rows. It reports this only as
`nested_cylindrical_shoulder`.

Temporary controls confirm the fail-closed boundary: two non-coaxial cylinders
return `cylinders_not_coaxial`; two coaxial cylinders without a shared planar
shoulder return `requires_one_shared_planar_shoulder`.

## Boundary

The result is not a counterbore feature classifier, a history-recovery claim,
or a public probe/runtime change. It applies only to the frozen +Z two-cylinder
relation and does not support additional cylinders, arbitrary axes or imported
topology conditions.
