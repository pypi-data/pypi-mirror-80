# Expectation Reflection

The current version of Expectation Reflection is applied for
binary classication. Its extension for regression tasks is in development.

## History

* [Danh-Tai Hoang, Juyong Song, Vipul Periwal, and Junghyo Jo, Network inference in stochastic systems from neurons to currencies: Improved performance at small sample size, Physical Review E, 99, 023311 (2019)](https://journals.aps.org/pre/abstract/10.1103/PhysRevE.99.023311)

* [Danh-Tai Hoang, Junghyo Jo, and Vipul Periwal, Data-driven inference of hidden nodes in networks, Physical Review E, 99, 042114 (2019)](https://journals.aps.org/pre/abstract/10.1103/PhysRevE.99.042114)

## Installation
#### From PyPi

```bash
pip install expectation-reflection
```

#### From Repository

```bash
git clone https://github.com/danhtaihoang/expectation-reflection.git
```

## Usage
* Import `expectation_reflection` package into python script:
```python
from expectation_reflection import classication as ER
```

* Train the model with `(X_train, y_train)` to get the value of intercept `b` and interaction weights `w` from features `X_train` to target `y_train`. In the current version, the target needs to be formatted in form of [0,1].
```python
b,w = ER.fit(X_train, y_train)
print('intercept:', b)
print('interaction weights:', b)
```

* Using the trained `b` and `w`, we can predict outputs `y_pred` and their probability `p_pred` of new inputs `X_test`:
```python
y_pred,p_pred = model.predict(X_test,b,w)
print('predicted output:',y_pred)
print('predicted probability:',y_pred)
```
