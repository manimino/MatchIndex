## How It Works, Concurrent Edition

ConcurrentDex contains:
 - an instance of Dex
 - a [readerwriterlock](https://github.com/elarivie/pyReaderWriterLock)

It exposes each method of the Dex, wrapped in the appropriate lock type using `with read_lock()` or 
`with write_lock()`.

### Performance Tips

There's a [performance test notebook](/examples/concurrent_perf.ipynb) showing the impact of locking
on single-threaded operation. Each lock operation adds about 5µs. Not huge, but it does add up when doing
many operations in a row.

For this reason, the `read_lock()` and `write_lock()` methods are available. 

This allows patterns like:
```
cfb = ConcurrentDex(...)
with cfb.write_lock()
    for item in a_million_items:
        cfb.box.add(item)  # cfb.box is the underlying Dex.
```
which are faster than calling `cfb.add()` many times.

### Reasons to trust it

Concurrency bugs are notoriously tricky to find. ConcurrentDex is unlikely to have them because:
 - It uses a very simple, coarse-grained concurrency that locks the whole object for every read and write
 - It's built on a widely-used lock library
 - There are concurrent operation tests that succeed on ConcurrentDex and fail on Dex, proving the
  locks are working properly (see `tests/concurrent`).