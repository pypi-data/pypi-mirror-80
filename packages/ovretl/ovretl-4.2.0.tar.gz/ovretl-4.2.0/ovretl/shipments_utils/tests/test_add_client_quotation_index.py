import pandas as pd
import numpy as np

from pandas.util.testing import assert_frame_equal

from ovretl.shipments_utils.add_client_quotation_index import add_client_quotation_index


def test_add_client_quotation_index():
    quotations_df = pd.DataFrame(
        data={"client_name": ["Foo", "Bar", "Foo", "Bar", "Foo"], "created_at": [3, 4, 2, 7, 10]}
    )
    result = add_client_quotation_index(quotations_df)
    result_should_be = pd.DataFrame(
        data={
            "client_name": ["Bar", "Bar", "Foo", "Foo", "Foo"],
            "quotation_number": [1, 2, 1, 2, 3],
            "created_at": [4, 7, 2, 3, 10],
        }
    )
    assert_frame_equal(result, result_should_be)
