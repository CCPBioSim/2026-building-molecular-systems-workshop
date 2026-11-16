# Answers for 0_intro-jupyter.ipynb. `python devtools/make_solutions.py 0_intro-jupyter` builds solutions/0_intro-jupyter_solutions.ipynb
# from them. See devtools/make_solutions.py for the format.

# %% replace ee362e15  (Jupyter notebooks: #define function y2 with shape x*x+c)
#define function y2 with shape x*x+c
def y2(x):
    c = 3
    return x*x + c

#define array x_values_2 and evaluate the function y2 for each value in the array
#look in the example code above to see how
x_values_2 = np.arange(-5, 5.1, 0.1)

#plot the result
plt.plot(x_values_2, y2(x_values_2))
plt.xlabel('x')
plt.ylabel('y2(x)')
plt.show()

# %% [markdown] after ee362e15  (Jupyter notebooks: #define function y2 with shape x*x+c)
# The minimum is at `x = 0`, where `y2(0) = c`. The range has to include negative and positive values of `x` to show it.
