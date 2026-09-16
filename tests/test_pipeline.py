import pandas as pd
from src.pipeline import transform, validate


def test_transform_normalizes_and_deduplicates():
    df = pd.DataFrame({"Customer Name": [" Alice ", " Alice "], "Amount": [10, 10]})
    result = transform(df)
    assert list(result.columns) == ["customer_name", "amount"]
    assert len(result) == 1
    assert result.iloc[0]["customer_name"] == "Alice"
    validate(result)
