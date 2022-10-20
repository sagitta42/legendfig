# legendfig

## Installation

```console
sudo -H python3 -m pip install git+https://github.com/sagitta42/legendfig
```

## Funcionality

### pretty()

Method `pretty()` allows quick beautification:

- add grid

- increase all fontsize of all labels and text

- increase tick labels

Arguments:

- `large [int]`: controls fontsizes (default 3)

- `stretch [None|float|int]` change x axis range (default None). Useful for cases when the automatic ranges makes the leftmost and rightmost point fall right at the frame and get "eaten up"
    `None`: do not do anything (default)
    `float`: widen the range by N%
    `int`: widen the range by N
    
- `grid ["major"|"minor"]`: only major grid, or also minor; same as the grid argument of the function `ax.grid()`


Compare the same plot with ..........

## Example usage

```python
import legendfig

lfig = legendfig.LegendFig((10,8)) # 10x8 figure

plt.plot(x, y, label = 'shrubbery')
# plot legend outside of plot, find position automatically
lfig.legend(out=True, pos='bottom')
# increase size of tick labels, axis labels, ...; add grid
lfig.pretty()
```
