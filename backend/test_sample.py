import polars as pl

try:
    df = pl.DataFrame({"a": [1, 2, 3]})
    df.lazy().sample(n=1).collect()
    print("Lazy sample works")
except Exception as e:
    print("Lazy sample error:", e)

try:
    print(df.sample(n=1))
    print("Eager sample works")
except Exception as e:
    print("Eager sample error:", e)
