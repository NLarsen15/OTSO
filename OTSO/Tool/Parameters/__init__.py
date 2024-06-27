from .functions import cone_inputs, bulk_cone_inputs, trajectory_inputs, planet_inputs, cutoff_inputs, bulk_cutoff_inputs, trace_inputs, bulk_planet_inputs

ConeInputArray = cone_inputs.ConeInputs()
TrajectoryInputArray = trajectory_inputs.TrajectoryInputs()
PlanetInputArray = planet_inputs.PlanetInputs()
CutoffInputArray = cutoff_inputs.CutoffInputs()
TraceInputArray = trace_inputs.TraceInputs()
BulkPlanetInputArraySpace, BulkPlanetInputArrayGauss = bulk_planet_inputs.BulkPlanetInputs()
BulkCutoffInputArraySpace, BulkCutoffInputArrayGauss = bulk_cutoff_inputs.BulkCutoffInputs()
BulkConeInputArraySpace, BulkConeInputArrayGauss = bulk_cone_inputs.BulkConeInputs()


