# Numba GPU Timer
A helper package to easily time Numba CUDA GPU events.

## Compatibility 
As this package uses Numba, refer to the [Numba compatibility guide](https://numba.pydata.org/numba-doc/dev/user/installing.html#compatibility).

## Installation
To use Pip: `pip install gpu_timer`

Or Conda: `conda install gpu_timer`

## Example
```
from numba_timer import cuda_timer

def increment_by_one(an_array):
    pos = cuda.grid(1)
    if pos < an_array.size:
        an_array[pos] += 1

an_array = [0, 1, 2]
threadsperblock = (16, 16)
blockspergrid_x = math.ceil(an_array.shape[0] / threadsperblock[0])
blockspergrid_y = math.ceil(an_array.shape[1] / threadsperblock[1])
blockspergrid = (blockspergrid_x, blockspergrid_y)

timer = cuda_timer.Timer()

timer.start()
increment_a_2D_array[blockspergrid, threadsperblock](an_array)
timer.stop()

print(f'Elapsed time: {timer.elapsed()} ms')
```
Numba specific code is borrowed from the [Numba documentation](https://numba.pydata.org/numba-doc/latest/cuda/kernels.html).