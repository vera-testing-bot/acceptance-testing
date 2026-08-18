```
                     _                        _          _   _           
 __ _ __ __ ___ _ __| |_ __ _ _ _  __ ___ ___| |_ ___ __| |_(_)_ _  __ _ 
/ _` / _/ _/ -_) '_ \  _/ _` | ' \/ _/ -_)___|  _/ -_|_-<  _| | ' \/ _` |
\__,_\__\__\___| .__/\__\__,_|_||_\__\___|    \__\___/__/\__|_|_||_\__, |
               |_|                                                 |___/ 
```

# acceptance-testing
<!-- A simple utility README. -->

## Pepperoni estimator

`src.math_utils.calculate_pepperoni_lbs(pizza_diameter, pepperoni_diameter)`
estimates how many pounds of pepperoni are needed to cover a pizza.

Assumptions used by the estimator:
- 0.08 inch overlap between neighboring slices
- 0.1 inch pepperoni thickness
- 0.038 lb/in^3 pepperoni density

## Spec issue replenishment

Use `scripts/create_issues_from_spec.py` to generate GitHub issues for planned (`🚧`) spec items.

- Dry run: `PYTHONPATH=. uv run python scripts/create_issues_from_spec.py --repo vera-testing-bot/acceptance-testing`
- Create issues: `PYTHONPATH=. uv run python scripts/create_issues_from_spec.py --repo vera-testing-bot/acceptance-testing --create`
# acceptance-ping
