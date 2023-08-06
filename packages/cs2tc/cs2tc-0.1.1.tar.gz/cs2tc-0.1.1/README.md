# cs2tc

Helper functions for converting Compute Studio parameters to a format compatible with Tax-Calculator.

```
pip install -U cs2tc
```

```python
import cs2tc

adj = {
    "STD": [
        {"MARS": "single", "year": 2019, "value": 10},
        {"MARS": "mjoint", "year": 2019, "value": 1},
        {"MARS": "mjoint", "year": 2022, "value": 10}
    ],
    "STD_checkbox": [{"value": False}]
}

cs2tc.convert_policy_adjustment(adj)

# {'STD': [{'MARS': 'single', 'year': 2019, 'value': 10},
#   {'MARS': 'mjoint', 'year': 2019, 'value': 1},
#   {'MARS': 'mjoint', 'year': 2022, 'value': 10}],
#  'STD-indexed': [{'value': False}]}

```
