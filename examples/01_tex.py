from mayavi import mlab
from mlabtex import mlabtex

text = (
    r"Sebastian M\"uller, "
    + r"$f(x)=\displaystyle\sum_{n=0}^\infty "
    + r"f^{(n)}(x_0)\cdot\frac{(x-x_0)^n}{n!}$"
)
tex = mlabtex(
    0.0,
    0.0,
    0.0,
    text,
    color=(0.0, 0.0, 0.0),
    orientation=(30.0, 0.0, 0.0),
    dpi=1200,
)
mlab.axes()
mlab.show()
