import collections
import itertools as it
from typing import Counter


def get_counters_product_mapping(
        counter_1: Counter,
        counter_2: Counter,
        product_function,
        key_merge_function,
):
    product_keys = list(it.product(counter_1.keys(), counter_2.keys()))
    product_values = [product_function(counter_1[key_1], counter_2[key_2]) for key_1, key_2 in product_keys]
    product_mapping = collections.defaultdict(lambda: 0)
    for (key_1, key_2), val in zip(product_keys, product_values):
        product_mapping[key_merge_function(key_1, key_2)] += val
    return product_mapping
