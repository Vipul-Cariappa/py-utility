# py-utility
Utility functions for managing and monitoring python resources.

## installation
<pre><code>pip install py-utility</code></pre>

## Decorator Function

### memoryit
memoryit returns the total memory used by the function at runtime in bytes.
<br>
Example Code:
<br>
<pre><code>from pyutility import memoryit
@memoryit
def prime_check(x):
  for i in range(2, x):
    if x % i == 0:
      return False
  return True</code></pre>

### limit_memory
limit_memory limits the memory consumption of function at runtime. It takes the limit in MB. You will find unexpected behaviour if too low value is set. The default value is 25 MB. It is throw MemoryError if it exceeds the limit.
<br>
Example Code:
<br>
<pre><code>from pyutility import limit_memory
@limit_memory(30)
def prime_check(x):
  for i in range(2, x):
    if x % i == 0:
      return False
  return True</code></pre>
  
### timeit
timeit returns the total time take to execute the function in seconds.
<br>
Example Code:
<br>
<pre><code>from pyutility import timeit
@timeit
def prime_check(x):
  for i in range(2, x):
    if x % i == 0:
      return False
  return True</code></pre>

### limit_time
limit_time limits the time used to execute the function. It takes limit as seconds. The default value is 10 seconds. It throws TimeoutError if it exceeds the limit.
<br>
Example Code:
<br>
<pre><code>from pyutility import limit_time
@limit_time(30)
def prime_check(x):
  for i in range(2, x):
    if x % i == 0:
      return False
  return True</code></pre>
  
  ## Contribution
  All contributions are welcomed. If it is a bug fix or new feature, creating new issue is highly recommend before any pull request.
