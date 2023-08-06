/******************************************************************************
 * Copyright (c) 2018, NVIDIA CORPORATION.  All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are met:
 *     * Redistributions of source code must retain the above copyright
 *       notice, this list of conditions and the following disclaimer.
 *     * Redistributions in binary form must reproduce the above copyright
 *       notice, this list of conditions and the following disclaimer in the
 *       documentation and/or other materials provided with the distribution.
 *     * Neither the name of the NVIDIA CORPORATION nor the
 *       names of its contributors may be used to endorse or promote products
 *       derived from this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED. IN NO EVENT SHALL NVIDIA CORPORATION BE LIABLE FOR ANY
 * DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
 * (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
 * LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
 * ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
 * SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 *
 ******************************************************************************/

// TODO: Move into system::hip

#pragma once

#include <thrust/detail/config.h>
#include <thrust/detail/cpp11_required.h>

#if THRUST_CPP_DIALECT >= 2011

#if THRUST_DEVICE_COMPILER == THRUST_DEVICE_COMPILER_HIP

#include <thrust/system/hip/config.h>

#include <thrust/system/hip/detail/async/customization.h>
#include <thrust/system/hip/detail/sort.h>
#include <thrust/detail/alignment.h>
#include <thrust/system/hip/future.h>
#include <thrust/type_traits/is_trivially_relocatable.h>
#include <thrust/type_traits/is_contiguous_iterator.h>
#include <thrust/type_traits/logical_metafunctions.h>
#include <thrust/iterator/iterator_traits.h>
#include <thrust/detail/static_assert.h>
#include <thrust/distance.h>

#include <type_traits>

// rocprim include
#include <rocprim/rocprim.hpp>

THRUST_BEGIN_NS

namespace system { namespace hip { namespace detail
{

// Non-ContiguousIterator iterators
template <
  typename DerivedPolicy
, typename ForwardIt, typename Size, typename StrictWeakOrdering
>
THRUST_HIP_RUNTIME_FUNCTION
auto async_stable_sort_n(
  execution_policy<DerivedPolicy>& policy,
  ForwardIt                        first,
  Size                             n,
  StrictWeakOrdering               comp
) ->
  typename std::enable_if<
    negation<is_contiguous_iterator<ForwardIt>>::value
  , unique_eager_future<
      void
    , typename thrust::detail::allocator_traits<
        decltype(get_async_device_allocator(policy))
      >::template rebind_traits<void>::pointer
    >
  >::type
{
  THRUST_STATIC_ASSERT_MSG(
    (thrust::detail::depend_on_instantiation<ForwardIt, false>::value)
  , "unimplemented"
  );

  // TODO: Buffer + copy

  THRUST_UNUSEd_VAR(policy);
  THRUST_UNUSEd_VAR(first);
  THRUST_UNUSEd_VAR(n);
  THRUST_UNUSEd_VAR(comp);

  return {};
}

// ContiguousIterator iterators
// Non-Scalar value type
// User-defined StrictWeakOrdering
template <
  typename DerivedPolicy
, typename ForwardIt, typename Size, typename StrictWeakOrdering
>
THRUST_HIP_RUNTIME_FUNCTION
auto async_stable_sort_n(
  execution_policy<DerivedPolicy>& policy,
  ForwardIt                        first,
  Size                             n,
  StrictWeakOrdering               comp
) ->
/*  typename std::enable_if<
    conjunction<
      is_contiguous_iterator<ForwardIt>
    , negation<
        std::is_scalar<
          typename thrust::iterator_traits<ForwardIt>::value_type
        >
      >
    >::value
  ,
*/
    unique_eager_future<
      void
    , typename thrust::detail::allocator_traits<
        decltype(get_async_device_allocator(policy))
      >::template rebind_traits<void>::pointer
    >
//  >::type
{
  auto const device_alloc = get_async_device_allocator(policy);

  using pointer
    = typename thrust::detail::allocator_traits<decltype(device_alloc)>::
      template rebind_traits<void>::pointer;

  unique_eager_future_promise_pair<void, pointer> fp;

  // Determine temporary device storage requirements.

  size_t tmp_size = 0;
  thrust::hip_rocprim::throw_on_error(
    thrust::hip_rocprim::__merge_sort::dispatch<thrust::detail::false_type>::doit(
      nullptr
    , tmp_size
    , first
    , static_cast<thrust::detail::uint8_t*>(nullptr) // Items.
    , n
    , comp
    , nullptr // Null stream, just for sizing.
    , THRUST_HIP_DEBUG_SYNC_FLAG
    )
  , "after merge sort sizing"
  );

  // Allocate temporary storage.

  auto content = uninitialized_allocate_unique_n<thrust::detail::uint8_t>(
    device_alloc, tmp_size
  );

  // The array was dynamically allocated, so we assume that it's suitably
  // aligned for any type of data. `malloc`/`hipMalloc`/`new`/`std::allocator`
  // make this guarantee.
  auto const content_ptr = content.get();

  void* const tmp_ptr = static_cast<void*>(
    thrust::raw_pointer_cast(content_ptr)
  );

  // Set up stream with dependencies.

  hipStream_t const user_raw_stream = thrust::hip_rocprim::stream(policy);

  if (thrust::hip_rocprim::default_stream() != user_raw_stream)
  {
    fp = depend_on<void, pointer>(
      nullptr
    , std::make_tuple(
        std::move(content)
      , unique_stream(nonowning, user_raw_stream)
      )
    );
  }
  else
  {
    fp = depend_on<void, pointer>(
      nullptr
    , std::make_tuple(
        std::move(content)
      )
    );
  }

  // Run merge sort.

  thrust::hip_rocprim::throw_on_error(
    thrust::hip_rocprim::__merge_sort::dispatch<thrust::detail::false_type>::doit(
      tmp_ptr
    , tmp_size
    , first
    , static_cast<thrust::detail::uint8_t*>(nullptr) // Items.
    , n
    , comp
    , fp.future.stream()
    , THRUST_HIP_DEBUG_SYNC_FLAG
    )
  , "after merge sort sizing"
  );

  return std::move(fp.future);
}

// ContiguousIterator iterators
// Scalar value type
// thrust::greater<>
// TODO (hack up rocprim)

// ContiguousIterator iterators
// Scalar value type
// thrust::less<>
template <
  typename DerivedPolicy
, typename ForwardIt, typename Size, typename CompareT
>
THRUST_HIP_RUNTIME_FUNCTION
auto async_stable_sort_n(
  execution_policy<DerivedPolicy>& policy,
  ForwardIt                        first,
  Size                             n,
  thrust::less<CompareT>
) ->
  typename std::enable_if<
    conjunction<
      is_contiguous_iterator<ForwardIt>
    , std::is_scalar<
        typename thrust::iterator_traits<ForwardIt>::value_type
      >
    >::value
  , unique_eager_future<
      void
    , typename thrust::detail::allocator_traits<
        decltype(get_async_device_allocator(policy))
      >::template rebind_traits<void>::pointer
    >
  >::type
{
  using T = typename thrust::iterator_traits<ForwardIt>::value_type;

  auto const device_alloc = get_async_device_allocator(policy);

  using pointer
    = typename thrust::detail::allocator_traits<decltype(device_alloc)>::
      template rebind_traits<void>::pointer;

  unique_eager_future_promise_pair<void, pointer> fp;

  // Determine temporary device storage requirements.

  size_t tmp_size = 0;
  T* first_ptr = raw_pointer_cast(&*first);
  thrust::hip_rocprim::throw_on_error(
    rocprim::radix_sort_keys(
      nullptr
    , tmp_size
    , first_ptr
    , static_cast<T*>(nullptr)
    , n
    , 0
    , sizeof(T) * 8
    , nullptr // Null stream, just for sizing.
    , THRUST_HIP_DEBUG_SYNC_FLAG
    )
  , "after radix sort sizing"
  );

  // Allocate temporary storage.

  size_t keys_temp_storage = thrust::detail::aligned_storage_size(
    sizeof(T) * n, 128
  );

  auto content = uninitialized_allocate_unique_n<thrust::detail::uint8_t>(
    device_alloc, keys_temp_storage + tmp_size
  );

  // The array was dynamically allocated, so we assume that it's suitably
  // aligned for any type of data. `malloc`/`hipMalloc`/`new`/`std::allocator`
  // make this guarantee.
  auto const content_ptr = content.get();

  T* keys_pointer = thrust::detail::aligned_reinterpret_cast<T*>(
    thrust::raw_pointer_cast(content_ptr)
  );

  void* const tmp_ptr = static_cast<void*>(
    thrust::raw_pointer_cast(content_ptr + keys_temp_storage)
  );

  // Set up stream with dependencies.

  hipStream_t const user_raw_stream = thrust::hip_rocprim::stream(policy);

  if (thrust::hip_rocprim::default_stream() != user_raw_stream)
  {
    fp = depend_on<void, pointer>(
      nullptr
    , std::make_tuple(
        std::move(content)
      , unique_stream(nonowning, user_raw_stream)
      )
    );
  }
  else
  {
    fp = depend_on<void, pointer>(
      nullptr
    , std::make_tuple(
        std::move(content)
      )
    );
  }

  // Run radix sort.
  thrust::hip_rocprim::throw_on_error(
    rocprim::radix_sort_keys(
      tmp_ptr
    , tmp_size
    , first_ptr
    , keys_pointer
    , n
    , 0
    , sizeof(T) * 8
    , fp.future.stream()
    , THRUST_HIP_DEBUG_SYNC_FLAG
    )
  , "after radix sort launch"
  );

  // TODO: Temporary hack.
  thrust::hip_rocprim::throw_on_error(
    hipMemcpyAsync(
      reinterpret_cast<T*>(first_ptr)
    , reinterpret_cast<T*>(keys_pointer)
    , sizeof(T) * n
    , hipMemcpyDeviceToDevice
    , fp.future.stream()
    )
  , "radix sort copy back"
  );

  return std::move(fp.future);
}

}}} // namespace system::hip::detail

namespace hip_rocprim
{

// ADL entry point.
template <
  typename DerivedPolicy
, typename ForwardIt, typename Sentinel, typename StrictWeakOrdering
>
THRUST_HIP_RUNTIME_FUNCTION
auto async_stable_sort(
  execution_policy<DerivedPolicy>& policy,
  ForwardIt                        first,
  Sentinel                         last,
  StrictWeakOrdering               comp
)
THRUST_DECLTYPE_RETURNS(
  thrust::system::hip::detail::async_stable_sort_n(
    policy, first, thrust::distance(first, last), comp
  )
);

} // hip_rocprim

THRUST_END_NS

#endif // THRUST_DEVICE_COMPILER == THRUST_DEVICE_COMPILER_HIP

#endif // THRUST_CPP_DIALECT >= 2011
