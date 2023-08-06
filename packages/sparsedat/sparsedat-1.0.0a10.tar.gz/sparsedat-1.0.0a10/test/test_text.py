from sparsedat import wrappers
from sparsedat import Data_Type

sdt = wrappers.load_text(
    "01.UMI.txt",
    separator="\t",
    has_header=True,
    has_row_names=True,
    default_value=0,
    data_type=Data_Type.INT
)

sdt.save("01.UMI.sdt")