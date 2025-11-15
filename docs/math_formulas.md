#### 箱子的最高级别不能用于炼金
---
#### Calculate the possibility of specified outcome:
$$
P_j = \frac{N_j}{\sum_{i=1}^n \left(N_i \times N_i' \right)}
$$

其中各符号含义如下：  
- $n$: The number containers included in the trade  
- $N_i$: The number of traded items for the $i$ th container  
- $N_i'$: The number of next rank items for the $i$ th container
---
#### Calculate the wear float of specified outcome:
$$
F_i = (f_{max}^i - f_{min}^i) * f_{avg} + f_{min}^i
$$

其中各符号含义如下：
- $f_{min}^i$: The minimum float value of the specified outcome weapon
- $f_{max}^i$: The maximum float value of the specified outcome weapon
- $f_{avg}$: average flaot value of traded items
