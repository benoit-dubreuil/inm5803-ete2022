#!/usr/bin/env python

import argparse
import pathlib
import tempfile
import typing

from generate_config import generate_voxsim_geom_params
from simulation_factory import get_simulation_parameters
from simulator.runner.legacy import SimulationRunner

DEFAULT_SINGULARITY_NAME: typing.Final[str] = "voxsim_singularity_latest.sif"


# TODO : Use new runner instead of legacy one.
def run_simulation(output_folder: pathlib.Path):
    geometry_parameters = generate_voxsim_geom_params(output_folder, "runner_test_geometry")

    simulation_parameters = get_simulation_parameters(output_folder, "runner_test_simulation")

    runner = SimulationRunner(
        "runner_test",
        geometry_parameters,
        simulation_parameters,
        output_nifti=True,
    )

    runner.run(output_folder, True)

    simulation_parameters = get_simulation_parameters(output_folder, "runner_test_simulation_standalone")

    standalone_output = output_folder / "standalone_test"

    runner.run_simulation_standalone(standalone_output, output_folder, simulation_parameters, "standalone")


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Simulation Runner Example Script")
    parser.add_argument("singularity_path", type=pathlib.Path, nargs="?", default=DEFAULT_SINGULARITY_NAME)
    parser.add_argument("--out", type=pathlib.Path, help="Output directory for the files")

    args = parser.parse_args()
    args.singularity_path.resolve(strict=True)
    # TODO : pass singularity_path to simulation

    if args.out:
        dest: pathlib.Path = args.out
        dest.mkdir(parents=True, exist_ok=True)
    else:
        dest = pathlib.Path(tempfile.mkdtemp(prefix="sim_runner"))

    print(f"Script execution results are in : {dest}")
    run_simulation(dest)
