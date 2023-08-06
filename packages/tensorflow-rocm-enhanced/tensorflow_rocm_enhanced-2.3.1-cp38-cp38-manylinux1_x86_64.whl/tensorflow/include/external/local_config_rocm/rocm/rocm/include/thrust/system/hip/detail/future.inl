// Copyright (c) 2018 NVIDIA Corporation
// Author: Bryce Adelstein Lelbach <brycelelbach@gmail.com>
//
// Distributed under the Boost Software License v1.0 (boost.org/LICENSE_1_0.txt)

// TODO: Split into future.h and detail/future.h

// TODO: Move stream/event classes to another header.

// TODO: Deparameterize pointer.

#pragma once

#include <thrust/detail/config.h>
#include <thrust/detail/cpp11_required.h>

#if THRUST_CPP_DIALECT >= 2011

#include <thrust/optional.h>
#include <thrust/detail/type_deduction.h>
#include <thrust/type_traits/integer_sequence.h>
#include <thrust/detail/type_traits/pointer_traits.h>
#include <thrust/tuple_algorithms.h>
#include <thrust/allocate_unique.h>
#include <thrust/detail/static_assert.h>
#include <thrust/detail/execute_with_dependencies.h>
#include <thrust/system/hip/memory.h>
#include <thrust/system/hip/future.h>
#include <thrust/system/hip/detail/util.h>
#include <thrust/system/hip/detail/get_value.h>

#include <type_traits>
#include <memory>

THRUST_BEGIN_NS

namespace system { namespace hip { namespace detail
{

///////////////////////////////////////////////////////////////////////////////

struct nonowning_t final {};

constexpr nonowning_t nonowning{};

///////////////////////////////////////////////////////////////////////////////

struct event_deleter final
{
  __host__
  void operator()(hipEvent_t e) const
  {
    if (nullptr != e)
      thrust::hip_rocprim::throw_on_error(hipEventDestroy(e), "");
  }
};

///////////////////////////////////////////////////////////////////////////////

struct unique_event final
{
  using native_handle_type = hipEvent_t;

private:
  std::unique_ptr<ihipEvent_t, event_deleter> handle_;

public:
  /// \brief Create a new stream and construct a handle to it. When the handle
  ///        is destroyed, the stream is destroyed.
  __host__
  unique_event()
    : handle_(nullptr, event_deleter())
  {
    native_handle_type e;
    thrust::hip_rocprim::throw_on_error(
      hipEventCreateWithFlags(&e, hipEventDisableTiming),
      ""
    );
    handle_.reset(e);
  }

  __thrust_exec_check_disable__
  unique_event(unique_event const&) = delete;
  __thrust_exec_check_disable__
  unique_event(unique_event&&) = default;
  __thrust_exec_check_disable__
  unique_event& operator=(unique_event const&) = delete;
  __thrust_exec_check_disable__
  unique_event& operator=(unique_event&&) = default;

  __thrust_exec_check_disable__
  ~unique_event() = default;

  __host__
  operator native_handle_type()      const THRUST_RETURNS(handle_.get());
  __host__
  native_handle_type get()           const THRUST_RETURNS(handle_.get());
  __host__
  native_handle_type native_handle() const THRUST_RETURNS(handle_.get());

  bool valid() const THRUST_RETURNS(bool(handle_));

  __host__
  bool ready() const
  {
    hipError_t const err = hipEventQuery(handle_.get());

    if (hipErrorNotReady == err)
      return false;

    // Throw on any other error.
    thrust::hip_rocprim::throw_on_error(err, "");

    return true;
  }

  __host__
  void wait() const
  {
    thrust::hip_rocprim::throw_on_error(hipEventSynchronize(handle_.get()), "");
  }

  __host__
  bool operator==(unique_event const& other) const
  {
    return other.handle_ == handle_;
  }

  __host__
  bool operator!=(unique_event const& other) const
  {
    return !(other == *this);
  }
};

///////////////////////////////////////////////////////////////////////////////

struct stream_deleter final
{
  __host__
  void operator()(hipStream_t s) const
  {
    if (nullptr != s)
      thrust::hip_rocprim::throw_on_error(hipStreamDestroy(s), "");
  }
};

struct stream_conditional_deleter final
{
private:
  bool const cond_ = true;

public:
  __host__
  constexpr stream_conditional_deleter() noexcept
    : cond_(true) {}

  __host__
  constexpr stream_conditional_deleter(nonowning_t) noexcept
    : cond_(false) {}

  __host__
  void operator()(hipStream_t s) const
  {
    if (cond_ && nullptr != s)
    {
      thrust::hip_rocprim::throw_on_error(hipStreamDestroy(s), "");
    }
  }
};

///////////////////////////////////////////////////////////////////////////////

struct unique_stream final
{
  using native_handle_type = hipStream_t;

private:
  std::unique_ptr<ihipStream_t, stream_conditional_deleter> handle_;

public:
  /// \brief Create a new stream and construct a handle to it. When the handle
  ///        is destroyed, the stream is destroyed.
  __host__
  unique_stream()
    : handle_(nullptr, stream_conditional_deleter())
  {
    native_handle_type s;
    thrust::hip_rocprim::throw_on_error(
      hipStreamCreateWithFlags(&s, hipStreamNonBlocking),
      ""
    );
    handle_.reset(s);
  }

  /// \brief Construct a non-owning handle to an existing stream. When the
  ///        handle is destroyed, the stream is not destroyed.
  __host__
  unique_stream(nonowning_t, native_handle_type handle)
    : handle_(handle, stream_conditional_deleter(nonowning))
  {}

  __thrust_exec_check_disable__
  unique_stream(unique_stream const&) = delete;
  __thrust_exec_check_disable__
  unique_stream(unique_stream&&) = default;
  __thrust_exec_check_disable__
  unique_stream& operator=(unique_stream const&) = delete;
  __thrust_exec_check_disable__
  unique_stream& operator=(unique_stream&&) = default;

  __thrust_exec_check_disable__
  ~unique_stream() = default;

  __host__
  operator native_handle_type()      THRUST_RETURNS(handle_.get());
  __host__
  native_handle_type get()           THRUST_RETURNS(handle_.get());
  __host__
  native_handle_type native_handle() THRUST_RETURNS(handle_.get());

  bool valid() const THRUST_RETURNS(bool(handle_));

  __host__
  bool ready() const
  {
    hipError_t const err = hipStreamQuery(handle_.get());

    if (hipErrorNotReady == err)
      return false;

    // Throw on any other error.
    thrust::hip_rocprim::throw_on_error(err, "");

    return true;
  }

  __host__
  void wait() const
  {
    thrust::hip_rocprim::throw_on_error(
      hipStreamSynchronize(handle_.get()),
      ""
    );
  }

  __host__
  void depend_on(unique_event& e)
  {
    thrust::hip_rocprim::throw_on_error(
      hipStreamWaitEvent(handle_.get(), e.get(), 0),
      ""
    );
  }

  __host__
  void depend_on(unique_stream& s)
  {
    if (s != *this)
    {
      unique_event e;
      s.record(e);
      depend_on(e);
    }
  }

  __host__
  void record(unique_event& e)
  {
    thrust::hip_rocprim::throw_on_error(hipEventRecord(e.get(), handle_.get()), "");
  }

  __host__
  bool operator==(unique_stream const& other) const
  {
    return other.handle_ == handle_;
  }

  __host__
  bool operator!=(unique_stream const& other) const
  {
    return !(other == *this);
  }
};

///////////////////////////////////////////////////////////////////////////////

} // detail

template <typename T>
struct ready_future;

namespace detail {

struct async_value_base;

template <typename T, typename Pointer>
struct async_value;

template <typename T, typename Pointer, typename KeepAlives>
struct async_value_with_keep_alives;

template <typename T, typename Pointer>
struct weak_promise;

template <typename X, typename XPointer = pointer<X>>
struct unique_eager_future_promise_pair final
{
  unique_eager_future<X, XPointer> future;
  weak_promise<X, XPointer>        promise;
};

struct acquired_stream final
{
  unique_stream stream;
  optional<std::size_t> const acquired_from;
  // If `acquired_from` is empty, then the stream is newly created.
};

// Precondition: `device` is the current HIP device.
template <typename X, typename Y, typename Deleter>
__host__
optional<unique_stream>
try_acquire_stream(int device, std::unique_ptr<Y, Deleter>&) noexcept;

// Precondition: `device` is the current HIP device.
inline __host__
optional<unique_stream>
try_acquire_stream(int, unique_stream& stream) noexcept;

// Precondition: `device` is the current HIP device.
template <typename T>
__host__
optional<unique_stream>
try_acquire_stream(int device, ready_future<T>&) noexcept;

// Precondition: `device` is the current HIP device.
template <typename X, typename XPointer>
__host__
optional<unique_stream>
try_acquire_stream(int device, unique_eager_future<X, XPointer>& parent) noexcept;

template <typename... Dependencies>
__host__
acquired_stream acquire_stream(int device, Dependencies&... deps) noexcept;

template <
  typename X, typename XPointer
, typename ComputeContent, typename... Dependencies
>
__host__
unique_eager_future_promise_pair<X, XPointer>
depend_on(ComputeContent&& cc, std::tuple<Dependencies...>&& deps);

///////////////////////////////////////////////////////////////////////////////

struct async_value_base
{
protected:
  unique_stream stream_;

public:
  // Constructs an `async_value_base` which uses `stream`.
  __host__
  async_value_base(unique_stream stream)
    : stream_(std::move(stream))
  {}

  __host__
  virtual ~async_value_base() {}

  unique_stream&       stream()       THRUST_RETURNS(stream_);
  unique_stream const& stream() const THRUST_RETURNS(stream_);

  template <typename X, typename XPointer>
  friend __host__
  optional<unique_stream>
  thrust::system::hip::detail::try_acquire_stream(
    int device, unique_eager_future<X, XPointer>& parent
    ) noexcept;
};

template <typename T, typename Pointer>
struct async_value : async_value_base
{
  using pointer
    = typename thrust::detail::pointer_traits<Pointer>::template
      rebind<T>::other;
  using const_pointer
    = typename thrust::detail::pointer_traits<Pointer>::template
      rebind<T const>::other;

protected:
  Pointer content_;

public:
  // Constructs an `async_value` which uses `stream`.
  __host__
  async_value(unique_stream stream)
    : async_value_base(std::move(stream)), content_{}
  {}

  __host__
  virtual ~async_value() {}

  __host__
  pointer       data()       THRUST_RETURNS(content_);
  __host__
  const_pointer data() const THRUST_RETURNS(content_);
};

template <typename Pointer>
struct async_value<void, Pointer> : async_value_base
{
  using pointer
    = typename thrust::detail::pointer_traits<Pointer>::template
      rebind<void>::other;
  using const_pointer
    = typename thrust::detail::pointer_traits<Pointer>::template
      rebind<void const>::other;

  // Constructs an `async_value<void>` which uses `stream`.
  __host__
  async_value(unique_stream stream) : async_value_base(std::move(stream)) {}

  __host__
  virtual ~async_value() {}

  __host__
  pointer       data()       THRUST_RETURNS(pointer{});
  __host__
  const_pointer data() const THRUST_RETURNS(pointer{});
};

template <typename T, typename Pointer, typename... KeepAlives>
struct async_value_with_keep_alives<T, Pointer, std::tuple<KeepAlives...>> final
  : async_value<T, Pointer>
{
  THRUST_STATIC_ASSERT_MSG(
    (0 < sizeof...(KeepAlives))
  , "non-void async_value_with_keep_alives must have at least one keep alive"
  );

  using pointer = typename async_value<T, Pointer>::pointer;
  using const_pointer = typename async_value<T, Pointer>::const_pointer;

  using keep_alives_type = std::tuple<KeepAlives...>;

protected:
  keep_alives_type keep_alives_;

public:
  // Constructs an `async_value_with_keep_alives` which uses `stream`, keeps
  // the objects in the tuple `keep_alives` alive until the asynchronous value
  // is destroyed, and has a content pointer determined by calling
  // `ComputeContent` on the first element of `keep_alives_`.
  template <typename ComputeContent>
  __host__
  async_value_with_keep_alives(
    unique_stream stream, ComputeContent&& cc, keep_alives_type&& keep_alives
  )
    : async_value<T, Pointer>(std::move(stream))
    , keep_alives_(std::move(keep_alives))
  {
    this->content_ = THRUST_FWD(cc)(std::get<0>(keep_alives_));
  }
};

template <typename Pointer, typename... KeepAlives>
struct async_value_with_keep_alives<void, Pointer, std::tuple<KeepAlives...>> final
  : async_value<void, Pointer>
{
  using pointer = typename async_value<void, Pointer>::pointer;
  using const_pointer = typename async_value<void, Pointer>::const_pointer;

  using keep_alives_type = std::tuple<KeepAlives...>;

protected:
  keep_alives_type keep_alives_;

public:
  // Constructs an `async_value_with_keep_alives` which uses `stream` and keeps
  // the objects in the tuple `keep_alives` alive until the asynchronous value
  // is destroyed.
  __host__
  async_value_with_keep_alives(
    unique_stream stream, std::nullptr_t, keep_alives_type&& keep_alives
  )
    : async_value<void, Pointer>(std::move(stream))
    , keep_alives_(std::move(keep_alives))
  {}
};

///////////////////////////////////////////////////////////////////////////////

template <typename T, typename Pointer>
struct weak_promise final
{
  using pointer = typename async_value<T, Pointer>::pointer;
  using const_pointer = typename async_value<T, Pointer>::const_pointer;

private:
  pointer content_;

  __host__ __device__
  weak_promise(pointer content)
    : content_(content)
  {}

public:
  weak_promise() : content_{} {}

  __thrust_exec_check_disable__
  weak_promise(weak_promise const&) = default;
  __thrust_exec_check_disable__
  weak_promise(weak_promise&&) = default;
  __thrust_exec_check_disable__
  weak_promise& operator=(weak_promise const&) = default;
  __thrust_exec_check_disable__
  weak_promise& operator=(weak_promise&&) = default;

  template <typename U>
  __host__ __device__
  void set_value(U&& value) &&
  {
    *content_ = THRUST_FWD(value);
  }

  template <
    typename X, typename XPointer
  , typename ComputeContent, typename... Dependencies
  >
  friend __host__
  unique_eager_future_promise_pair<X, XPointer>
  thrust::system::hip::detail::depend_on(
    ComputeContent&& cc, std::tuple<Dependencies...>&& deps
  );
};

template <typename Pointer>
struct weak_promise<void, Pointer> final
{
  using pointer       = typename async_value<void, Pointer>::pointer;
  using const_pointer = typename async_value<void, Pointer>::const_pointer;

private:
  __host__ __device__
  weak_promise(pointer p)
  {
    THRUST_UNUSED_VAR(p);
    assert(pointer{} == p);
  }

public:
  weak_promise() {}

  __thrust_exec_check_disable__
  weak_promise(weak_promise const&) = default;
  __thrust_exec_check_disable__
  weak_promise(weak_promise&&) = default;
  __thrust_exec_check_disable__
  weak_promise& operator=(weak_promise const&) = default;
  __thrust_exec_check_disable__
  weak_promise& operator=(weak_promise&&) = default;

  template <
    typename X, typename XPointer
  , typename ComputeContent, typename... Dependencies
  >
  friend __host__
  unique_eager_future_promise_pair<X, XPointer>
  thrust::system::hip::detail::depend_on(
    ComputeContent&& cc, std::tuple<Dependencies...>&& deps
  );
};

///////////////////////////////////////////////////////////////////////////////

} // namespace detail

template <typename T>
struct ready_future final
{
  using pointer       = T*;
  using const_pointer = T const*;

private:
  T value_;

public:
  template <typename U>
  explicit ready_future(U&& u)
    : value_(THRUST_FWD(u))
  {}

  ready_future(ready_future&&) = default;
  ready_future(ready_future const&) = default;
  ready_future& operator=(ready_future&&) = default;
  ready_future& operator=(ready_future const&) = default;

  __host__
  const_pointer data() const
  {
    return std::addressof(value_);
  }

  __host__
  T get() &&
  {
    return std::move(value_);
  }
};

template <>
struct ready_future<void> final {};

template <typename T, typename Pointer>
struct unique_eager_future final
{
  using pointer       = typename detail::async_value<T, Pointer>::pointer;
  using const_pointer = typename detail::async_value<T, Pointer>::const_pointer;

private:
  int device_ = 0;
  std::unique_ptr<detail::async_value<T, Pointer>> async_value_;

  __host__
  unique_eager_future(
    int device, std::unique_ptr<detail::async_value<T, Pointer>> av
  )
    : device_(device), async_value_(std::move(av))
  {}

public:
  __host__
  unique_eager_future()
    : device_(0), async_value_()
  {}

  unique_eager_future(unique_eager_future&&) = default;
  unique_eager_future(unique_eager_future const&) = delete;
  unique_eager_future& operator=(unique_eager_future&&) = default;
  unique_eager_future& operator=(unique_eager_future const&) = delete;

  bool valid() const THRUST_RETURNS(bool(async_value_));

  // Precondition: `true == valid()`.
  __host__
  detail::unique_stream& stream()
  {
    assert(true == valid());
    return async_value_->stream();
  }

  __host__
  const_pointer data() const
  {
    if (async_value_)
      return async_value_->data();
    else
      return const_pointer{};
  }

  __host__
  void wait()
  {
    stream().wait();
  }

  __host__
  T get() &&
  {
    stream().wait();
    return std::move(*async_value_->data());
  }

  template <typename X, typename XPointer>
  __host__
  friend optional<detail::unique_stream>
  thrust::system::hip::detail::try_acquire_stream(
    int device, unique_eager_future<X, XPointer>& parent
    ) noexcept;

  template <
    typename X, typename XPointer
  , typename ComputeContent, typename... Dependencies
  >
  friend __host__
  detail::unique_eager_future_promise_pair<X, XPointer>
  thrust::system::hip::detail::depend_on(
    ComputeContent&& cc, std::tuple<Dependencies...>&& deps
  );
};

template <typename Pointer>
struct unique_eager_future<void, Pointer> final
{
  using pointer
    = typename detail::async_value<void, Pointer>::pointer;
  using const_pointer
    = typename detail::async_value<void, Pointer>::const_pointer;

private:
  int device_ = 0;
  std::unique_ptr<detail::async_value<void, Pointer>> async_value_;

  __host__
  unique_eager_future(
    int device, std::unique_ptr<detail::async_value<void, Pointer>> av
  )
    : device_(device), async_value_(std::move(av))
  {}

public:
  __host__
  unique_eager_future()
    : device_(0), async_value_()
  {}

  unique_eager_future(unique_eager_future&&) = default;
  unique_eager_future(unique_eager_future const&) = delete;
  unique_eager_future& operator=(unique_eager_future&&) = default;
  unique_eager_future& operator=(unique_eager_future const&) = delete;

  bool valid() const THRUST_RETURNS(bool(async_value_));

  // Precondition: `true == valid()`.
  __host__
  detail::unique_stream& stream()
  {
    assert(true == valid());
    return async_value_->stream();
  }

  __host__
  void wait()
  {
    stream().wait();
  }

  void get() &&
  {
    stream().wait();
  }

  template <typename X, typename XPointer>
  __host__
  friend optional<detail::unique_stream>
  thrust::system::hip::detail::try_acquire_stream(
    int device, unique_eager_future<X, XPointer>& parent
    ) noexcept;

  template <
    typename X, typename XPointer
  , typename ComputeContent, typename... Dependencies
  >
  friend __host__
  detail::unique_eager_future_promise_pair<X, XPointer>
  thrust::system::hip::detail::depend_on(
    ComputeContent&& cc, std::tuple<Dependencies...>&& deps
  );
};

///////////////////////////////////////////////////////////////////////////////

namespace detail {

template <typename X, typename Deleter>
__host__
optional<unique_stream>
try_acquire_stream(int, std::unique_ptr<X, Deleter>&) noexcept
{
  // There's no stream to acquire!
  return {};
}

inline __host__
optional<unique_stream>
try_acquire_stream(int, unique_stream& stream) noexcept
{
  return {std::move(stream)};
}

template <typename T>
__host__
optional<unique_stream>
try_acquire_stream(int, ready_future<T>&) noexcept
{
  // There's no stream to acquire!
  return {};
}

template <typename X, typename XPointer>
__host__
optional<unique_stream>
try_acquire_stream(int device, unique_eager_future<X, XPointer>& parent) noexcept
{
  // We have unique ownership, so we can always steal the stream if the future
  // has one as long as they are on the same device as us.
  if (parent.async_value_)
    if (device == parent.device_)
      return std::move(parent.async_value_->stream());

  return {};
}

///////////////////////////////////////////////////////////////////////////////

template <typename... Dependencies>
__host__
acquired_stream acquire_stream_impl(
  int, std::tuple<Dependencies...>&, index_sequence<>
) noexcept
{
  // We tried to take a stream from all of our dependencies and failed every
  // time, so we need to make a new stream.
  return {unique_stream(), {}};
}

template <typename... Dependencies, std::size_t I0, std::size_t... Is>
__host__
acquired_stream acquire_stream_impl(
  int device
, std::tuple<Dependencies...>& deps, index_sequence<I0, Is...>
) noexcept
{
  auto tr = try_acquire_stream(device, std::get<I0>(deps));

  if (tr)
    return {std::move(*tr), {I0}};
  else
    return acquire_stream_impl(device, deps, index_sequence<Is...>{});
}

template <typename... Dependencies>
__host__
acquired_stream acquire_stream(
  int device
, std::tuple<Dependencies...>& deps
) noexcept
{
  return acquire_stream_impl(
    device, deps, make_index_sequence<sizeof...(Dependencies)>{}
  );
}

///////////////////////////////////////////////////////////////////////////////

template <typename X, typename Deleter>
__host__
void create_dependency(
  unique_stream&, std::unique_ptr<X, Deleter>&
) noexcept
{}

template <typename T>
__host__
void create_dependency(
  unique_stream&, ready_future<T>&
) noexcept
{}

inline __host__
void create_dependency(
  unique_stream& child, unique_stream& parent
)
{
  child.depend_on(parent);
}

template <typename X, typename XPointer>
__host__
void create_dependency(
  unique_stream& child, unique_eager_future<X, XPointer>& parent
)
{
  child.depend_on(parent.stream());
}

template <typename... Dependencies>
__host__
void create_dependencies_impl(
  acquired_stream&
, std::tuple<Dependencies...>&, index_sequence<>
)
{}

template <typename... Dependencies, std::size_t I0, std::size_t... Is>
__host__
void create_dependencies_impl(
  acquired_stream& as
, std::tuple<Dependencies...>& deps, index_sequence<I0, Is...>
)
{
  // We only need to wait on the current dependency if we didn't steal our
  // stream from it.
  if (!as.acquired_from || *as.acquired_from == I0)
  {
    create_dependency(as.stream, std::get<I0>(deps));
  }

  create_dependencies_impl(as, deps, index_sequence<Is...>{});
}

template <typename... Dependencies>
__host__
void create_dependencies(acquired_stream& as, std::tuple<Dependencies...>& deps)
{
  create_dependencies_impl(
    as, deps, make_index_sequence<sizeof...(Dependencies)>{}
  );
}

///////////////////////////////////////////////////////////////////////////////

// Metafunction that determine which `Dependencies` need to be kept alive.
// Returns the result as an `index_sequence` of indices into the parameter
// pack.
template <std::size_t I, typename... Dependencies>
  struct find_keep_alives_impl;
template <typename... Dependencies>
  using find_keep_alives
    = typename find_keep_alives_impl<0, Dependencies...>::type;

template <std::size_t I>
struct find_keep_alives_impl<I>
{
  using type = index_sequence<>;
};

// User-provided stream.
template <std::size_t I, typename... Dependencies>
struct find_keep_alives_impl<
  I, unique_stream, Dependencies...
>
{
  // Nothing to keep alive, skip this index.
  using type = typename find_keep_alives_impl<I + 1, Dependencies...>::type;
};

template <std::size_t I, typename... Dependencies>
struct find_keep_alives_impl<
  I, ready_future<void>, Dependencies...
>
{
  // Nothing to keep alive, skip this index.
  using type = typename find_keep_alives_impl<I + 1, Dependencies...>::type;
};

template <std::size_t I, typename T, typename... Dependencies>
struct find_keep_alives_impl<
  I, ready_future<T>, Dependencies...
>
{
  // Add this index to the list.
  using type = integer_sequence_push_front<
    std::size_t, I
  , typename find_keep_alives_impl<I + 1, Dependencies...>::type
  >;
};

template <std::size_t I, typename T, typename... Dependencies>
struct find_keep_alives_impl<
  I, unique_eager_future<T>, Dependencies...
>
{
  // Add this index to the list.
  using type = integer_sequence_push_front<
    std::size_t, I
  , typename find_keep_alives_impl<I + 1, Dependencies...>::type
  >;
};

// Content storage.
template <std::size_t I, typename T, typename Deleter, typename... Dependencies>
struct find_keep_alives_impl<
  I, std::unique_ptr<T, Deleter>, Dependencies...
>
{
  // Add this index to the list.
  using type = integer_sequence_push_front<
    std::size_t, I
  , typename find_keep_alives_impl<I + 1, Dependencies...>::type
  >;
};

///////////////////////////////////////////////////////////////////////////////

template <
  typename X, typename XPointer
, typename ComputeContent, typename... Dependencies
>
__host__
unique_eager_future_promise_pair<X, XPointer>
depend_on(ComputeContent&& cc, std::tuple<Dependencies...>&& deps)
{
  int device = 0;
  thrust::hip_rocprim::throw_on_error(hipGetDevice(&device), "");

  // First, either steal a stream from one of our children or make a new one.
  auto as = acquire_stream(device, deps);

  // Then, make the stream we've acquired asynchronously wait on all of our
  // dependencies, except the one we stole the stream from.
  create_dependencies(as, deps);

  // Then, we determine which subset of dependencies need to be kept alive.
  auto ka = tuple_subset(std::move(deps), find_keep_alives<Dependencies...>{});

  // Next, we create the asynchronous value.
  std::unique_ptr<async_value<X, XPointer>> av(
    new async_value_with_keep_alives<X, XPointer, decltype(ka)>(
      std::move(as.stream), std::move(cc), std::move(ka)
    )
  );

  // Finally, we create the promise and future objects.
  weak_promise<X, XPointer> child_prom(av->data());
  unique_eager_future<X, XPointer> child_fut(device, std::move(av));

  return unique_eager_future_promise_pair<X, XPointer>
    {std::move(child_fut), std::move(child_prom)};
}

} // namespace detail

///////////////////////////////////////////////////////////////////////////////

}} // namespace system::hip

THRUST_END_NS

#endif // THRUST_CPP_DIALECT >= 2011
