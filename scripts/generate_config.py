#!/usr/bin/env python

import argparse
import pathlib

from simulator.factory.geometry_factory.handlers import GeometryInfos

import fcg.voxsim
import fcg.voxsim.geom as _geom
import fcg.voxsim.phantom as _fiber
import fcg.voxsim.phantom.generator
import fcg.app


class GenerateStraigthBundle(fcg.app.App):

    def _exec_logic(self) -> None:
        # TODO : Supply the singularity (*.sif) path as a program arg. See SingularityConfig.
        # TODO : Supply the SingularityCE executable path as a program arg. See SingularityConfig.

        parser = argparse.ArgumentParser("Generate a configuration of white matter fibre bundles")
        parser.add_argument(
            "--out", type=pathlib.Path, default=fcg.voxsim.default.ROOT_OUT_DIR, help="Output directory for the files"
        )

        args = parser.parse_args()
        out_dir: pathlib.Path = args.out
        out_dir.mkdir(parents=True, exist_ok=True)
        out_dir = out_dir.resolve(strict=True)

        print(f"Script execution results directory : {out_dir}")
        print("Generating VoxSim geometry parameters ... ")
        voxsim_geom_params: GeometryInfos = _geom.generate_voxsim_geom_params(out_dir)
        # TODO
        _fiber.generator.generate_fiber_tracts(voxsim_geom_params, out_dir)


if __name__ == "__main__":
    app = GenerateStraigthBundle()
    app.start()
