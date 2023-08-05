import copy
import urllib.parse
from typing import Any, Dict, List

import pandas as pd
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

BASE_URL = "https://api.covidcountydata.org"
POSTGREST_ARGS = {"select", "order", "Range", "Range-Unit", "offset", "limit", "Prefer"}


def setup_session() -> requests.Session:
    retry_strategy = Retry(
        total=5,
        status_forcelist=[429, 500, 502, 503, 504],
        method_whitelist=["HEAD", "GET", "OPTIONS"],
        backoff_factor=0.2,
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    http = requests.Session()
    http.mount("https://", adapter)
    http.mount("http://", adapter)
    return http


def _to_date_str(x):
    return pd.to_datetime(x).strftime("%Y-%m-%d")


def create_filter_rhs(x: Any, k=None) -> str:
    if k is not None and k in POSTGREST_ARGS:
        return x
    inequalities = {">": "gt", "<": "lt", "!=": "neq", ">=": "gte", "<=": "lte"}

    if k == "dt" and isinstance(x, (dict,)):
        extra_keys = set(x.keys()) - set(["start", "end"])
        if len(extra_keys) > 0:
            msg = "Unknown dt filter arguments: {}. Known are `'start'` and `'end'`"
            raise ValueError(msg.format(extra_keys))
        if len(x) == 1:
            # only have 1
            for key, op in zip(["start", "end"], (">=", "<=")):
                if key in x:
                    val = _to_date_str(x[key])
                    return create_filter_rhs(f"{op}{val}", k)
        elif len(x) == 2:
            # must have start and end
            start = _to_date_str(x["start"])
            end = _to_date_str(x["end"])
            return f"(dt.gte.{start},dt.lte.{end})"

    if isinstance(x, (list, tuple, set)):
        # use in
        return f"in.({','.join(map(str, x))})"

    if isinstance(x, str):
        # check for inequality
        for op in inequalities:
            if op in x:
                if f"{op}=" in x:
                    return x.replace(f"{op}=", inequalities[op] + "e.")
                return x.replace(op, inequalities[op] + ".")
    return f"eq.{x}"


def _reshape_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    Reshape a DataFrame from long to wide form, adhering to the following
    rules:

    - If the `meta_date` column exists, replace `variable` column with
      {variable}_{meta_date} and then drop `meta_date`
    - Construct a pivot_table where the columns come from the `variable`
      column, values come from the `value` column, and all other columns are
      used as an index
    """
    if df.shape[0] == 0:
        # empty dataframe
        return df

    cols = list(df)
    for c in ["variable", "value"]:
        if c not in cols:
            gh_issues = (
                "https://github.com/CovidCountyData/covidcountydata.py/issues/new"
            )
            msg = (
                f"Column {c} not found in DataFrame. "
                f"Please report a bug at {gh_issues}"
            )
            raise ValueError(msg)
    if "meta_date" in cols:
        if "variable" in cols:
            df["variable"] = (
                df["variable"].astype(str) + "_" + df["meta_date"].astype(str)
            )
            df.drop("meta_date", axis="columns")

    idx = list(set(cols) - {"variable", "value"})
    return df.pivot_table(index=idx, columns="variable", values="value").reset_index()


def _create_query_string(path: str, filters: Dict[str, Any]) -> str:
    """
    Given a path and filters to apply to that path, construct a query string
    """
    _filters = copy.deepcopy(filters)
    prepped_filters = {}
    # handle dt dict separately
    if "dt" in _filters:
        dt_val = _filters["dt"]
        if isinstance(dt_val, dict):
            if len(dt_val) > 1:
                prepped_filters["and"] = create_filter_rhs(dt_val, "dt")
            else:
                prepped_filters["dt"] = create_filter_rhs(dt_val, "dt")
            _filters.pop("dt")

    prepped_filters.update({k: create_filter_rhs(v, k) for k, v in _filters.items()})
    query = BASE_URL + "/" + path
    if len(prepped_filters) > 0:
        query += "?" + urllib.parse.urlencode(prepped_filters)

    return query


def _combine_dfs(dfs: List[pd.DataFrame]) -> pd.DataFrame:
    """
    Merge all `dfs` on common columns (typically in the index)
    """
    out = dfs[0]
    for right in dfs[1:]:
        out = out.merge(right)
    return out
