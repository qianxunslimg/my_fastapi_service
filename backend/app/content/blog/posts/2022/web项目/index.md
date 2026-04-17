---
date: '2022-08-09T09:46:00+08:00'
categories:
- 基础知识
tags:
- 面试
hidden: true
password: '87654123'
---

## 欢迎来到我的魔仙堡

## IO多路复用

### 什么是IO多路复用

IO多路复用是指内核一旦发现进程指定的一个或者多个IO条件准备读取，它就通知该进程。

与多进程和多线程技术相比，`I/O多路复用技术的最大优势是系统开销小，系统不必创建进程/线程`，也不必维护这些进程/线程，从而大大减小了系统的开销。

目前支持I/O多路复用的系统调用有 `select，pselect，poll，epoll`，I/O多路复用就是`通过一种机制，一个进程可以监视多个描述符，一旦某个描述符就绪（一般是读就绪或者写就绪），能够通知程序进行相应的读写操作`。`但select，pselect，poll，epoll本质上都是同步I/O`，因为他们都需要在读写事件就绪后自己负责进行读写，也就是说这个读写过程是阻塞的，而异步I/O则无需自己负责进行读写，异步I/O的实现会负责把数据从内核拷贝到用户空间。



### 为什么 I/O 多路复用==内部==需要使用非阻塞I/O

<u>==如果阻塞了还怎么轮询呢~==</u>

I/O 多路复用**内部**会遍历集合中的每个文件描述符，判断其是否就绪：

```c
for fd in read_set
    if(readable(fd)) // 判断 fd 是否就绪
        count++
        FDSET(fd, &res_rset) // 将 fd 添加到就绪集合中
        break
...
return count
```

这里的 `readable(fd)` 就是一个非阻塞 I/O 调用。试想，如果这里使用阻塞 I/O，那么 `fd` 未就绪时，`select` 会阻塞在这个文件描述符上，无法检查下个文件描述符。

注意：这里说的是 I/O 多路复用的==内部实现==，而不是说，使用 I/O 多路复用就必须使用非阻塞 I/O，见下文为什么边缘触发必须使用非阻塞 I/O。



### 为什么`边缘触发`必须使用`非阻塞` I/O？

-   每次通过 `read` 系统调用读取数据时，最多只能读取缓冲区大小的字节数；如果某个文件描述符一次性收到的数据超过了缓冲区的大小，那么需要对其 `read` 多次才能全部读取完毕
-   **`select` 可以使用阻塞 I/O**。通过 `select` 获取到所有可读的文件描述符后，遍历每个文件描述符，`read` **一次**数据（见上文 [select 示例](https://imageslr.com/2020/02/27/select-poll-epoll.html#selectdemo)）
    -   这些文件描述符都是可读的，因此即使 `read` 是阻塞 I/O，也一定可以读到数据，不会一直阻塞下去 ==但是 也只是限于读这一次==
    -   `select` 采用水平触发模式，因此如果第一次 `read` 没有读取完全部数据，那么下次调用 `select` 时依然会返回这个文件描述符，可以再次 `read`
    -   **`select` 也可以使用非阻塞 I/O**。当遍历某个可读文件描述符时，使用 `for` 循环调用 `read` **多次**，直到读取完所有数据为止（返回 `EWOULDBLOCK`）。这样做会多一次 `read` 调用，但可以减少调用 `select` 的次数
-   在 `epoll` 的边缘触发模式下，只会在文件描述符的==可读/可写状态发生切换==时，才会收到操作系统的通知
    -   因此，如果使用 `epoll` 的**边缘触发模式**，在收到通知时，**必须使用非阻塞 I/O，并且必须循环调用 `read` 或 `write` 多次，直到返回 `EWOULDBLOCK` 为止**，然后再调用 `epoll_wait` 等待操作系统的下一次通知
    -   如果没有一次性读/写完所有数据，那么在操作系统看来这个文件描述符的状态没有发生改变，将不会再发起通知，调用 `epoll_wait` 会使得该文件描述符一直等待下去，服务端也会一直等待客户端的响应，业务流程无法走完
    -   这样做的好处是每次调用 `epoll_wait` 都是**有效**的——保证数据全部读写完毕了，等待下次通知。在水平触发模式下，如果调用 `epoll_wait` 时数据没有读/写完毕，会直接返回，再次通知。因此边缘触发能显著减少事件被触发的次数
    -   为什么 `epoll` 的**边缘触发模式不能使用阻塞 I/O**？很显然，边缘触发模式需要循环读/写一个文件描述符的所有数据。如果使用阻塞 I/O，那么一定会在最后一次调用（没有数据可读/写）时阻塞，导致无法正常结束





## 线程池问题

### 1\. 线程池设计

使用多线程充分利用多核CPU，并使用线程池避免线程频繁创建、销毁加大系统开销。

-   创建一个线程池来管理多线程，线程池中主要包含**任务队列** 和**工作线程**集合，将任务添加到队列中，然后在创建线程后，自动启动这些任务。使用了一个固定线程数的工作线程，限制线程最大并发数。
-   多个线程共享任务队列，所以需要进行线程间同步，工作线程之间对任务队列的竞争采用**条件变量**和**互斥锁**结合使用
-   一个工作线程**先加互斥锁**，当任务队列中任务数量为0时候，阻塞在条件变量，当任务数量大于0时候，用条件变量通知阻塞在条件变量下的线程，这些线程来继续竞争获取任务
-   对任务队列中任务的调度采用**先来先服务**算法

### 2\. 根据并发量、任务执行时间使用线程池

> **1\. 高并发、任务执行时间短的业务怎样使用线程池？**
>
> **2\. 并发不高、任务执行时间长的业务怎样使用线程池？**
>
> **3\. 并发高、业务执行时间长的业务怎样使用线程池？**

线程池本质上是**生产者和消费者**模型，包括三要素：

-   往线程池队列中投**递任务的生产者**；
-   **任务队列**；
-   从任务队列取出任务执行的**工作线程（消费者）**。

要想合理的配置线程池的大小，得分析线程池任务的特性，可以从以下几个方面来分析：

-   根据任务的性质来分：CPU 密集型任务；IO 密集型任务；混合型任务。

-   根据任务的优先级：高、中、低

-   根据任务的执行时间：长、中、短

不同性质的任务可以交给不同配置的线程池执行。

### 3\. 线程池的`线程数量`

最直接的限制因素是CPU处理器的个数。

-   如果CPU是4核的，那么对于CPU密集的任务，线程池的线程数量`最好也为4`，或者`+1`防止其他因素导致阻塞。

-   如果是IO密集的任务，一般要多于CPU的核数，因为 IO 操作不占用 CPU，线程间竞争的不是CPU资源而是IO，IO的处理一般比较慢，多于核数的线程将为CPU争取更多的任务，不至于在线程处理IO的时候造成CPU空闲导致资源浪费。

-   而对于`混合型的任务`，如果可以拆分，拆分成 IO 密集型和 CPU 密集型分别处理，前提是两者运行的时间是差不多的，如果处理时间相差很大，则没必要拆分了。

如果**任务执行时间长**，在工作线程数量有限的情况下，工作线程很快就很被任务占完，导致后续任务不能及时被处理，此时应适当**增加工作线程数量**；反过来，如果**任务执行时间短**，那么**工作线程数量不用太多**，太多的工作线程会导致过多的时间浪费在线程上下文切换上。

回到这个问题本身来，这里的“高并发”应该是生产者生产任务的速度比较快，此时需要适当**增大任务队列上限**。

但是对于第三个问题并发高、业务执行时间长这种情形单纯靠线程池解决方案是不合适的，即使服务器有再高的资源配置，每个任务长周期地占用着资源，最终服务器资源也会很快被耗尽，因此对于这种情况，应该配合**业务解耦**，做些模块拆分优化整个系统结构。

## web代码流程

### 服务端 webserver

1. 使用config构造webserver实例并初始化

   1. 获取当前路径并初始化资源路径
   2. 初始化 Epoller  数据库连接池 threadPool timer 日志系统
   3. 设置webServer的监听socket  `InitSocket_lfd`
      1. 设置addr:  ipv4协议 和端口号
      2. 设置socket stream SOCK_STREAM提供面向连接的稳定数据传输，即TCP协议。
      3. 设置套接字Linger属性  setsockopt()函数
      4. 设置套接字reuse 重用属性  setsockopt()函数
      5. listen监听fd 并设置同一时刻的最大连接数 backlog
      6. 插入到epoll进行监听
      7. 设置文件描述符为非阻塞

2. Launch 服务运行

   1. 清理超时节点 获取临近的超时间隔t  `timeMS = timer_->nextNodeClock() * 1000;`

   2. 调用epoll_wait 阻塞时间为t  `int eventCnt = epoller_->Wait(timeMS); //等待多少ms`

   3. 遍历处理每一个event  

      > `int fd = epoller_->GetEventFd(i); //得到每一个响应的fd`
      >
      > `uint32_t events = epoller_->GetEvents(i); //感兴趣的事件和被触发的事件`

      1. ==如果为监听文件描述符:== 

         > accept 连接进来 返回fd
         >
         > 判断连接数是否从超过MAXFD 65536 超过的话sendError 关闭fd return掉
         >
         > 如果正常 则`AddClient_(fd, addr);` 添加时间节点, 将fd插入到epoll  设置文件非阻塞

      2. 如果文件描述符发生错误`EPOLLERR`或者被挂断`EPOLLHUP`:  

         > `epoller_->DelFd(client->GetFd());`:
         >
         > ```c++
         >   epoll_event ev = {0};
         >   return 0 == epoll_ctl(epollFd_, EPOLL_CTL_DEL, fd, &ev);
         > ```
         >
         >   `client->Close();` 1. ==取消内存映射== 2. useCount-- 3. 关闭fd

      3. 如果为可读事件`EPOLLIN`:  `DealRead_`

         > 1. 扩充当前客户端对应的定时器事件
         > 2. 线程池AddTask, 线程池唤醒一个线程进行处理
         > 3. 线程执行`WebServer::OnRead_`函数
         >    1. while读取数据 返回读取到的数据的长度
         >    2. 如果数据大小<=0 或者errno不为EAGAIN 关闭客户端 return
         >    3. `OnProcess(client); //处理客户端的请求`  后面全部为HttpConn模块负责
         >       1. 解析数据 `client->processData()`
         >       2. 解析成功 做出响应 `OnProcess`
         >          1. 插入写事件 准备发送数据 `epoller_->ModFd(client->GetFd(), connEvent_ | EPOLLOUT);`
         >             1. 注意 是替换send 因为缓冲区满会gg
         >          2. 如果数据不足以做出响应 继续插入到读事件 `EPOLLIN`
   >          3. 注意 epoll的监听事件是==读写来回切换==的
   
4. 如果为可写事件`EPOLLOUT`:  `DealWrite_`
   
         > 1. 扩充当前客户端对应的定时器事件
         > 2. 线程池AddTask, 线程池唤醒一个线程进行处理
         > 3. 线程执行`WebServer::OnWrite_`函数
         >    1. 写入 对应客户端的响应数据 `iov`
         >    2. 长连接 ? 继续process
         >    3. 没有数据写入, 重新监听?

### 线程池 ThreadPool



```c++
class ThreadPool {
public:
  explicit ThreadPool(size_t threadCount = 8)
      : pool_(std::make_shared<Pool>()) {
    assert(threadCount > 0);
    for (size_t i = 0; i < threadCount; i++) { //循环创建线程
      // lamda
      std::thread([pool = pool_] {
        // unique_lock具有lock_guard的所有功能，而且更为灵活。
        // 虽然二者的对象都不能复制，但是unique_lock可以移动(movable)
        // 因此用unique_lock管理互斥对象，可以作为函数的返回值，也可以放到STL的容器中。
        std::unique_lock<std::mutex> locker(pool->mtx);
        while (true) {
          if (!pool->tasks.empty()) {
            //被唤醒, 执行队列头部的任务
            auto task = std::move(pool->tasks.front());
            pool->tasks.pop();
            locker.unlock();
            task();
            locker.lock();
          } else if (pool->isClosed)
            break;
          else
            pool->cond.wait(locker);
        }
      }).detach();
      //.detach()
      //作用:
      //把线程放在后台运行，线程的所有权和控制权交给 C++ Runtime Library
      //当前对象将不再和任何线程相关联
      //调用后.joinable() 将永远返回 false
    }
  }

  ThreadPool() = default;
  ThreadPool(ThreadPool &&) = default;
  ~ThreadPool() {
    if (static_cast<bool>(pool_)) {
      {
        std::lock_guard<std::mutex> locker(pool_->mtx);
        pool_->isClosed = true;
      }
      //置位关闭 唤醒所有线程 进行清理
      pool_->cond.notify_all();
    }
  }

  template <class F> void AddTask(F &&task) {
    {
      std::lock_guard<std::mutex> locker(pool_->mtx);
      pool_->tasks.emplace(std::forward<F>(task));
    }
    //唤醒一个线程处理task
    pool_->cond.notify_one();
  }

private:
  struct Pool {
    std::mutex mtx;
    std::condition_variable cond;
    bool isClosed;
    std::queue<std::function<void()>> tasks;
  };

  //任务队列
  std::shared_ptr<Pool> pool_;
};
```

#### 注意的几个点

1. 在构造时 使用`std::thread + lamda`创建线程
2. 任务队列存储`function闭包函数指针` 即任务函数
3. 线程内 使用`unique_lock`获取`任务队列的锁`
4. 任务队列为空 被任务队列的条件变量`阻塞`
5. 被唤醒 任务队列非空: 拿到任务队列头部函数指针 `执行` 知道执行完毕 又检测到队列为空 `阻塞`
6. 当线程池调用`AddTask` 时 使用条件变量唤醒一个线程

### 配置 config

config存储配置参数  (可通过命令行启动参数修改)

```c++
config::config() {
  port_ = 9999;   // p  端口
  trigMode_ = 3;  // t  触发模式
  timeoutS_ = 10; // m  超时时间 s
  optLinger_ = false;

  sqlPort_ = 3306;
  sqlUsr_ = "root";
  sqlPSWD_ = "123456";
  dbName_ = "dbkrain";
  sqlPoolNum_ = 6;    // s  sql连接池
  threadPoolNum_ = 8; // n  线程池
  openLog_ = true;    // o  打开日志
  logQueSize_ = 1024; // l  日志队列
}
```

1. 网络相关
   1. epoll触发模式 设置为et
   2. 本机开启的端口号
   3. keepalive超时时间 默认10s
2. mysql相关
   1. 数据库端口号 
   2. 数据库名称  用户及密码
   3. 连接池的额最大数目 6
3. 线程池相关的配置
   2. 线程池最大线程数 8
4. 日志相关
   1. 开启/关闭状态 1
   2. 日志队列大小 1024

### 日志系统 Log

#### 注意的点

1. 使用饿汉单例模式 局部静态首次调用时进行初始化

   ```c++
   Log *Log::Instance() {
     // static实现简单的单例模式
     static Log logObject;
     return &logObject;
   }
   ```

2. 异步写入日志

   1. 目的 : 避免写日志操作 阻塞原本线程

   2. 实现: 队列 互斥锁 条件变量 单一的工作线程

      1. queue< string>存储要写入的日志队列

      2. mutex logmtx_ 对写入日志文件这个临界区进行加锁

      3. 异步写入时 日志队列不为空则唤醒工作线程进行写入操作

         ```c++
         void Log::logAdd(LOG_LEVEL level, const char *format, ...) {
           ......
         	if (isAsync_) {
             logQue_.push(buff_.RecycleAllReturnStr());
             que_not_empty.notify_one(); //唤醒一个线程
           } else
             fputs(buff_.Peek(), fileptr_);
           buff_.RecycleAll();
         }
         
         void Log::asyncWriteLog() {
           while (true) {
             unique_lock<mutex> locker(logmtx_);
             if (logQue_.empty()) {
               que_not_empty.wait(locker);
             }
         
             fputs(logQue_.front().c_str(), fileptr_);
             fflush(fileptr_);
             logQue_.pop();
           }
         }
         ```

      4. 使用`va_list`来解决变参问题
      5. 日志文件太大怎么办: 判断日志行数 如果超过5000行 新建文件+后缀 -1 -2 -3...

### 数据库连接池 SqlConnPool

#### 基本实现

1. 使用饿汉单例模式 局部静态首次调用时进行初始化

   ```c++
   SqlConnPool::Instance()->Init(
         "localhost", cfgObj->sqlPort_, cfgObj->sqlUsr_.c_str(),
         cfgObj->sqlPSWD_.c_str(), cfgObj->dbName_.c_str(), cfgObj->sqlPoolNum_);
   
   SqlConnPool *SqlConnPool::Instance() {
     static SqlConnPool connPool;
     return &connPool;
   }
   ```

2. 初始化10个MSQL实例
   1. 每个MYSQL实例都进行`mysql_init`
   2. 每个MYSQL实例都连接到数据库 sql = `mysql_real_connect`(sql, host, user, pwd, dbName, port, nullptr, 0);
   3. 将每个MYSQL实例压入 ==数据库队列==`connQue_`
   4. 初始化信号量为0 sem_init(&semId_ , 0, MAX_CONN_);

3. 使用
   1. `GetConn` 获取一个MSQL实例 sql队列不为空则 sem_wait -1 加锁取头部sql 返回sql
   2. `FreeConn` 加锁压回sql队列 sem_post +1
   3. `ClosePool` 加锁循环出队列, 依次关闭每个sql连接`mysql_close`
   4. `GetFreeConnCount` 获取当前空闲sql实例的个数

#### RAII实现

使用SqlConnRAII对象实现sql队列的管理: 构造GetConn析构FreeConn

```c++
class SqlConnRAII {
public:
  SqlConnRAII(MYSQL **sql, SqlConnPool *connpool) {
    assert(connpool);
    *sql = connpool->GetConn();
    sql_ = *sql;
    connpool_ = connpool;
  }

  ~SqlConnRAII() {
    if (sql_) {
      connpool_->FreeConn(sql_);
    }
  }

private:
  MYSQL *sql_;
  SqlConnPool *connpool_;
};
```

`为什么要多此一举 使用一个RAII去包装他`

就像stl里面的lock_guard对锁进行包装一样 或者智能指针 <u>为了避免调用了获取sql实例 但是忘记释放的情况</u> 忘记释放连接池就被饿死了



### `Http模块 HttpConn`

#### HttpConn

注: webserver内存储的是一个map 文件描述符int到httpconn的映射 `std::unordered_map<int, HttpConn> users_; //维护所有的http连接`

```c++
class HttpConn {
public:
  HttpConn();  // fd_ = -1;  addr_ = {0};  isClose_ = true;
  ~HttpConn(); // Close();

  void init(int sockFd, const sockaddr_in &addr);
  ssize_t read(int *saveErrno);  //非阻塞 所以循环读
  ssize_t write(int *saveErrno); //非阻塞 所以循环写
  void Close();                  // usercnt-- 关闭fd response_.UnmapFile();

  int GetFd() const;
  int GetPort() const;
  const char *GetIP() const;
  sockaddr_in GetAddr() const;

  bool processData(); // main 主要操作函数

  int ToWriteBytes() {
    return iov_[0].iov_len + iov_[1].iov_len;
  } //返回聚集写 两个缓冲区含有的数据长度之和
  bool IsKeepAlive() const { return request_.IsKeepAlive(); }

  static bool isET;                  //边沿触发
  static const char *srcDir;         //资源文件夹路径
  static std::atomic<int> userCount; //用户数

private:
  int fd_;                  // socket文件描述符
  struct sockaddr_in addr_; // ip和协议族
  bool isClose_;
  int iovCnt_;            // iov缓冲区个数
  struct iovec iov_[2];   //聚集写  内部缓冲区首地址和长度
  Buffer readBuff_;       // 读缓冲
  Buffer writeBuff_;      // 写缓冲
  HttpRequest request_;   //请求类
  HttpResponse response_; //响应类
};
```

==**循环读写忽略 只是while 然后写的话 写完要更新iov内部base指针和长度**==

#### 处理数据

```c++
// main 处理数据
bool HttpConn::processData() {
  request_.Init(); //初始化请求类
  if (readBuff_.ReadableBytes() <= 0) {
    return false;
  } else if (request_.parseData(readBuff_)) { //解析数据
    LOG_DEBUG("%s", request_.path().c_str());
    // 初始化响应的基本信息
    response_.Init(srcDir, request_.path(), request_.IsKeepAlive(), 200);
  } else {
    // 400 bad request
    response_.Init(srcDir, request_.path(), false, 400);
  }

  response_.MakeResponse(writeBuff_); //响应报文
  // 响应报文 存入一个聚集写的缓冲区
  iov_[0].iov_base = const_cast<char *>(writeBuff_.Peek());
  iov_[0].iov_len = writeBuff_.ReadableBytes();
  iovCnt_ = 1;
  // 文件存入第二个iov缓冲区
  if (response_.FileLen() > 0 && response_.File()) {
    iov_[1].iov_base = response_.File();
    iov_[1].iov_len = response_.FileLen();
    iovCnt_ = 2;
  }
  LOG_DEBUG("filesize:%d, %d  to %d", response_.FileLen(), iovCnt_,
            ToWriteBytes());
  return true;
}
```

1. 初始化请求类
2. 请求类解析数据
3. 成功则初始化响应类为200 continue 失败则初始化响应类为400 bad request
4. `响应类阻止响应报文`  并存入一个聚集写的缓冲区
5. 如果存在文件 将文件存入第二个聚集写的缓冲区

#### Http报文

```c++
 //get报文:请求访问的资源。（客户端：我想访问你的某个资源）
 GET /0606/01.php HTTP/1.1\r\n  //请求行:请求方法 空格 URL 空格 协议版本号 回车符 换行符
 Host: localhost\r\n         //首部行 首部行后面还有其他的这里忽略
 \r\n                //空行分割
 空                //实体主体

 //post报文:传输实体主体。（客户端：我要把这条信息告诉你）
 POST /0606/02.php HTTP/1.1 \r\n   //请求行
 Host: localhost\r\n             //首部行 首部行中必须有Contenr-length，告诉服务器我要给你发的实体主体有多少字节 
 Content-type: application/x-www-form-urlencoded\r\n
 Contenr-length: 23\r\n       
  \r\n                           //空行分割
 username=zhangsan&age=9 \r\n    //实体主体 长度23
```

#### HttpRequest类

```c++
bool HttpRequest::parseData(Buffer &buff) {
  const char CRLF[] = "\r\n"; //回车加换行
  if (buff.ReadableBytes() <= 0) {
    return false;
  }
  //四个状态 变换状态 switch切换处理逻辑
  while (buff.ReadableBytes() && master_state_ != FINISH) {
    const char *lineEnd = search(buff.Peek(), buff.BeginWriteConst(), CRLF,
                                 CRLF + 2); //在buff中匹配\r\n
    std::string line(buff.Peek(), lineEnd);
    switch (master_state_) {
    case REQUEST_LINE:
      if (!ParseRequestLine_(line)) { //解析请求行
        return false;
      }
      //方法get/post 路径path version http1.1
      ParsePath_();
      buff.RecycleTo(lineEnd + 2);
      break;
    case HEADERS:
      ParseHeader_(line); //解析请求头
      if (buff.ReadableBytes() <= 2) {
        master_state_ = FINISH;
      }
      buff.RecycleTo(lineEnd + 2);
      break;
    case BODY:
      body_ = &buff;
      //解析请求体 根据post拼接响应文件的路径或者解析上传的文件
      ParseBody_();
      break;
    default:
      break;
    }
  }
  buff.RecycleAll();
  LOG_DEBUG("[%s], [%s], [%s]", method_.c_str(), path_.c_str(),
            version_.c_str());
  return true;
}
```

1. 设置状态机 while中switch切换
2. 解析请求行
3. 解析请求头
4. 解析请求体 根据post拼接响应文件的路径或者解析上传的文件

#### HttpResponse

```c++
class HttpResponse {
public:
  HttpResponse();
  ~HttpResponse();

  void Init(const std::string &srcDir, std::string &path,
            bool isKeepAlive = false, int code = -1);
  void MakeResponse(Buffer &buff);
  void MakeResponse_FILE(Buffer &buff); //响应文件
  void MakeResponse_MENU(Buffer &buff); //响应文件夹
  void UnmapFile();                     //接触文件映射

  char *File();
  size_t FileLen() const;
  void ErrorContent(Buffer &buff, std::string message); //响应一个错误页面
  int Code() const { return code_; }

private:
  void AddStateLine_(Buffer &buff); //状态行
  void AddHeader_(Buffer &buff);    //响应头
  void AddContent_(Buffer &buff);   //添加消息体
  void AddMenuHTML(Buffer &buff);   //在消息主体拼一个目录页面
  void encode_str(std::string &from);
  unsigned char ToHex(unsigned char x);

  void ErrorHtml_();
  std::string GetFileType_();

  int code_; //响应状态码
  bool isKeepAlive_;

  std::string path_;   //响应路径
  std::string srcDir_; //响应文件夹的路径

  char *mmFile_; //文件映射
  struct stat mmFileStat_;

  static const std::unordered_map<std::string, std::string> SUFFIX_TYPE;
  static const std::unordered_map<std::string, std::string> SOURCE_FOLDER;
  static const std::unordered_map<int, std::string> CODE_STATUS;   //状态码
  static const std::unordered_map<int, std::string> ERR_CODE_PATH; //错误页面
};
```

```c++
void HttpResponse::MakeResponse(Buffer &buff) {
  char fileSuffix[10];
  *fileSuffix = '.';
  if (path_ == "upload_ok") {
    code_ = 200;
    buff.Append("upload file ok !");
  } else if (path_ == "upload_err") {
    code_ = 400;
    buff.Append("something error happened !");
  } else if (-1 != sscanf(path_.data(), "%*[^.].%[^.]", fileSuffix + 1)) {
    if (SOURCE_FOLDER.find(fileSuffix) == SOURCE_FOLDER.end())
      code_ = 404;
    else
      path_ = SOURCE_FOLDER.find(fileSuffix)->second + path_;
    MakeResponse_FILE(buff);
  } else {
    MakeResponse_MENU(buff);
  }
  return;
}
```

##### 主要响应两个部分 

1. 对请求的html进行响应
   1. 将响应的html mmap映射到文件描述符 关闭原html
2. 对请求的menu进行响应
   1. 在body中用string组织起html来. 并组织起文件夹下的目录 ==(注意 这里没有将文件压入buff)==
   2. 将string添加到buff中

3. 后序 httpconn中的操作
   1. 第一个iov的缓冲区存储响应报文
   2. 第二个iov的缓冲区存储响应的文件
   3. 最后 两个iov是在webserver中 writev写入写缓冲区的
