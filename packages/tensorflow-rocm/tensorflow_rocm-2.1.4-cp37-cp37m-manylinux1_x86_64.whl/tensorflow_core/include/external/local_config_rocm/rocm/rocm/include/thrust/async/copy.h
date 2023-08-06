/*
 *  Copyright 2008-2018 NVIDIA Corporation
 *
 *  Licensed under the Apache License, Version 2.0 (the "License");
 *  you may not use this file except in compliance with the License.
 *  You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 *  Unless required by applicable law or agreed to in writing, software
 *  distributed under the License is distributed on an "AS IS" BASIS,
 *  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *  See the License for the specific language governing permissions and
 *  limitations under the License.
 */

/*! \file async/copy.h
 *  \brief Functions for asynchronously copying a range.
 */

#pragma once

#include <thrust/detail/config.h>
#include <thrust/detail/cpp11_required.h>

#if THRUST_CPP_DIALECT >= 2011

#include <thrust/detail/static_assert.h>
#include <thrust/detail/select_system.h>
#include <thrust/system/detail/adl/async/copy.h>

#include <thrust/future.h>

THRUST_BEGIN_NS

namespace async
{

namespace unimplemented
{

template <
  typename DerivedPolicy
, typename ForwardIt, typename Sentinel, typename OutputIt
>
__host__ __device__
future<
  OutputIt, DerivedPolicy
, typename thrust::detail::pointer_traits<
    thrust::host_memory_resource::pointer
  >::template rebind<OutputIt>::other
>
async_copy(
  thrust::execution_policy<DerivedPolicy>& exec
, ForwardIt first, Sentinel last, OutputIt output
)
{
  THRUST_STATIC_ASSERT_MSG(
    (thrust::detail::depend_on_instantiation<ForwardIt, false>::value)
  , "unimplemented for this system"
  );
  return {};
} 

} // namespace unimplemented

struct copy_fn final
{
  __thrust_exec_check_disable__
  template <
    typename DerivedPolicy
  , typename ForwardIt, typename Sentinel, typename OutputIt
  >
  __host__ __device__
  future<
    OutputIt, DerivedPolicy
  , typename thrust::detail::pointer_traits<
      thrust::host_memory_resource::pointer
    >::template rebind<OutputIt>::other
  >
  static call(
    thrust::detail::execution_policy_base<DerivedPolicy> const& exec
  , ForwardIt&& first, Sentinel&& last
  , OutputIt&& output 
  ) 
  {
    // ADL dispatch.
    using thrust::async::unimplemented::async_copy;
    return async_copy(
      thrust::detail::derived_cast(thrust::detail::strip_const(exec))
    , THRUST_FWD(first), THRUST_FWD(last)
    , THRUST_FWD(output)
    );
  } 

  __thrust_exec_check_disable__
  template <typename ForwardIt, typename Sentinel, typename OutputIt>
  __host__ __device__
  static auto call(ForwardIt&& first, Sentinel&& last, OutputIt&& output) 
  THRUST_DECLTYPE_RETURNS(
    copy_fn::call(
      thrust::detail::select_system(
        typename thrust::iterator_system<ForwardIt>::type{}
      , typename thrust::iterator_system<OutputIt>::type{}
      )
    , THRUST_FWD(first), THRUST_FWD(last)
    , THRUST_FWD(output)
    )
  )

  template <typename... Args>
  __host__ __device__
  auto operator()(Args&&... args) const
  THRUST_DECLTYPE_RETURNS(
    call(THRUST_FWD(args)...)
  )
};

THRUST_INLINE_CONSTANT copy_fn copy{};

} // namespace async

THRUST_END_NS

#endif // THRUST_CPP_DIALECT >= 2011
