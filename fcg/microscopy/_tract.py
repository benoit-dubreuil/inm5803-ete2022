import csv
import json
import pathlib
import pickle
import typing
import struct

_FIB_FILE_ENCODING: typing.Final[str] = "ascii"


class Tracts(typing.TypedDict):
    x: list[float]
    y: list[float]
    t: list[float]
    id: list[int]


# TODO
def _load_fib_tracts(filename: pathlib.Path) -> Tracts:
    """Loads the tracts of an `.fib` file.

    `.fib` files generated by voXSim are encoded in ASCII and binary with the VTK legacy binary file format_.

    Example of an `.fib` file content when printed on the terminal:

        # vtk DataFile Version 4.2
        vtk output
        BINARY
        DATASET POLYDATA
        POINTS 4 float
        ��?���?�
        LINES 2 6
        
        CELL_DATA 2
        FIELD FieldData 1
        FIBER_WEIGHTS 1 2 float
        ?�?�
        POINT_DATA 4
        FIELD FieldData 1
        FIBER_COLORS 4 4 unsigned_char
        ��������

    Only the points and lines are important.

    Parameters
    ----------
    filename
        Path to an `.fib` filename

    Returns
    -------
    Tracts
        The loaded tracts.

    .. _format: https://kitware.github.io/vtk-examples/site/VTKFileFormats/#binary-files

    """
    tracts: Tracts = {"x": [], "y": [], "t": [], "id": []}

    with open(filename, 'rb') as fib:
        line = fib.readline().decode(_FIB_FILE_ENCODING).lower()
        if not line.startswith("# vtk datafile version"):
            raise ValueError("The supplied `.fib` tract file has the wrong format.")

        fib.readline()  # Line content: "vtk output"

        line = fib.readline().decode(_FIB_FILE_ENCODING).lower()
        if not line.startswith("binary"):
            raise ValueError("The supplied `.fib` tract file has the wrong format.")

        line = fib.readline().decode(_FIB_FILE_ENCODING).lower()
        if not line.startswith("dataset polydata"):
            raise ValueError("The supplied `.fib` tract file has the wrong format.")

        line = fib.readline().decode(_FIB_FILE_ENCODING).lower()
        if not line.startswith("points"):
            raise ValueError("The supplied `.fib` tract file has the wrong format.")
        if "float" != line.split()[-1] != "double":
            raise ValueError("The supplied `.fib` tract file has the wrong format.")

        element_quantity, element_size = line.split()[-2:]
        element_quantity = int(element_quantity)

        data_format: str = element_size[0] * 3  # 3 elements per point
        element_size = struct.calcsize(data_format)

        total_size = element_quantity * element_size
        data = fib.read(total_size)

        points: [(float, float, float)] = []
        for offset in range(0, len(data), element_size):
            points.append(struct.unpack_from(data_format, data, offset))

    pass


def load_tracts(
    filename: pathlib.Path,
    field_x: str = "x",
    field_y: str = "y",
    field_t: str = "t",
    field_id: str = "id",
    file_format: str | None = None,
) -> Tracts:
    """Load the tracts from a `.fib`, `.csv`, `.json` or `.pcl` file.

    Parameters
    ----------
    filename
        Path to a `.fib`, `.csv`, `.json` or `.pcl` filename
    field_x
        Column name in the file corresponding to the tracts X positions.
    field_y
        Column name in the file corresponding to the tracts Y positions.
    field_t
        Column name in the file corresponding to the tracts time.
    field_id
        Column name in the file corresponding to the tracts ID.
    file_format
        Specify the file format (available are fib, cvs, json, pcl). If none is given, it will be inferred from the
        filename.

    """
    tracts: Tracts = {"x": [], "y": [], "t": [], "id": []}

    if pathlib.Path(filename).suffix == ".fib" or file_format == "fib":
        tracts = _load_fib_tracts(filename)
    elif pathlib.Path(filename).suffix == ".csv" or file_format == "csv":
        # Load the csv file
        with open(filename) as csvfile:
            #  Detect the csv format
            dialect = csv.Sniffer().sniff(csvfile.read())

            #  Create a reader
            csvfile.seek(0)
            reader = csv.reader(csvfile, dialect)

            for i, row in enumerate(reader):
                if i == 0:
                    column_names = row
                else:
                    tracts["x"].append(float(row[column_names.index(field_x)]))
                    tracts["y"].append(float(row[column_names.index(field_y)]))
                    tracts["t"].append(float(row[column_names.index(field_t)]))
                    tracts["id"].append(int(row[column_names.index(field_id)]))

    elif pathlib.Path(filename).suffix == ".json" or file_format == "json":
        with open(filename) as f:
            content = json.load(f)
        tracts["x"] = content[field_x]
        tracts["y"] = content[field_y]
        tracts["t"] = content[field_t]
        tracts["id"] = content[field_id]

    elif pathlib.Path(filename).suffix == ".pcl" or file_format == "pcl":
        with open(filename, "rb") as f:
            content = pickle.load(f)
        tracts["x"] = content[field_x]
        tracts["y"] = content[field_y]
        tracts["t"] = content[field_t]
        tracts["id"] = content[field_id]

    return tracts
