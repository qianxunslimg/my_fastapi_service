---
date: '2021-12-02T19:41:34+08:00'
---

A C++ `thread` object generally (but not always) represents a thread of execution, which is an OS or platform concept.

When `thread::join()` is called, the calling thread will block until the thread of execution has completed. Basically, this is one mechanism that can be used to know when a thread has finished. When `thread::join()` returns, the OS thread of execution has completed and the C++ `thread` object can be destroyed.

The `thread::detach()` is called, the thread of execution is "detached" from the `thread` object and is no longer represented by a `thread` object - they are two independent things. The C++ `thread` object can be destroyed and the OS thread of execution can continue on. If the program needs to know when that thread of execution has completed, some other mechanism needs to be used. `join()` cannot be called on that `thread` object any more, since it is no longer associated with a thread of execution.

It is considered an error to destroy a C++ `thread` object while it is still "joinable". That is, in order to destroy a C++ `thread` object either `join()` needs to be called (and completed) or `detach()` must be called. If a C++ `thread` object is still joinable when it's destroyed, an exception will be thrown.

Some other ways that a C++ `thread` object will not represent a thread of execution (ie., can be unjoinable):

- A default constructed `thread` object does not represent a thread of execution, so is not joinable.
- A thread that has been moved from will no longer represent a thread of execution, so is not joinable.

 

`join()` doesn't kill the thread. Actually it waits until thread main function returns. So if your thread main function looks like this:

```cpp
while (true) {
}
```

`join()` is going to wait forever.

`detatch()` doesn't kill thread either. Actually it tells `std::thread` that this thread should continue to run even when `std::thread` object is destroyed. C++ checks in std::thread destructor that thread is either joined or detached and terminates program if this check fails.

So if you uncomment first line in `main` function of the following code it will crash. If you uncomment second or third line it will work ok.

```cpp
#include <thread>

void func() {
}

void fail1() {
    std::thread t(func);
    // will fail when we try to destroy t since it is not joined or detached
}

void works1() {
    std::thread t(func);
    t.join();
}

void works2() {
    std::thread t(func);
    t.detach();
}

int main() {
    // fail1();
    // works1();
    // works2();
}
```
