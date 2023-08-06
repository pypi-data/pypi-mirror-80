// automatically generated
/*
Copyright (c) 2018 Advanced Micro Devices, Inc. All rights reserved.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
*/

#ifndef INC_KFD_OSTREAM_OPS_H_
#define INC_KFD_OSTREAM_OPS_H_
#ifdef __cplusplus
#include <iostream>

#include "roctracer.h"

namespace roctracer {
namespace kfd_support {
// begin ostream ops for KFD 
#include "basic_ostream_ops.h"

template<>
struct output_streamer<HsaCounterBlockProperties&> {
  inline static std::ostream& put(std::ostream& out, HsaCounterBlockProperties& v)
{
   roctracer::kfd_support::output_streamer<HsaCounter[1]>::put(out,v.Counters);
   roctracer::kfd_support::output_streamer<HSAuint32>::put(out,v.NumConcurrent);
   roctracer::kfd_support::output_streamer<HSAuint32>::put(out,v.NumCounters);
   roctracer::kfd_support::output_streamer<HSA_UUID>::put(out,v.BlockId);
   return out;
}
};

template<>
struct output_streamer<HsaQueueReport&> {
  inline static std::ostream& put(std::ostream& out, HsaQueueReport& v)
{
   roctracer::kfd_support::output_streamer<HSAuint64>::put(out,v.QueueSize);
   roctracer::kfd_support::output_streamer<HSAuint32>::put(out,v.VMID);
   return out;
}
};

template<>
struct output_streamer<HSA_DEBUG_PROPERTIES&> {
  inline static std::ostream& put(std::ostream& out, HSA_DEBUG_PROPERTIES& v)
{
   roctracer::kfd_support::output_streamer<HSAuint64>::put(out,v.Value);
   return out;
}
};

template<>
struct output_streamer<HsaNodeChange&> {
  inline static std::ostream& put(std::ostream& out, HsaNodeChange& v)
{
   roctracer::kfd_support::output_streamer<HSA_EVENTTYPE_NODECHANGE_FLAGS>::put(out,v.Flags);
   return out;
}
};

template<>
struct output_streamer<HsaDeviceStateChange&> {
  inline static std::ostream& put(std::ostream& out, HsaDeviceStateChange& v)
{
   roctracer::kfd_support::output_streamer<HSA_EVENTTYPE_DEVICESTATECHANGE_FLAGS>::put(out,v.Flags);
   roctracer::kfd_support::output_streamer<HSA_DEVICE>::put(out,v.Device);
   roctracer::kfd_support::output_streamer<HSAuint32>::put(out,v.NodeId);
   return out;
}
};

template<>
struct output_streamer<HSA_LINKPROPERTY&> {
  inline static std::ostream& put(std::ostream& out, HSA_LINKPROPERTY& v)
{
   roctracer::kfd_support::output_streamer<HSAuint32>::put(out,v.LinkProperty);
   return out;
}
};

template<>
struct output_streamer<__fsid_t&> {
  inline static std::ostream& put(std::ostream& out, __fsid_t& v)
{
   roctracer::kfd_support::output_streamer<int[2]>::put(out,v.__val);
   return out;
}
};

template<>
struct output_streamer<HsaMemoryRange&> {
  inline static std::ostream& put(std::ostream& out, HsaMemoryRange& v)
{
   roctracer::kfd_support::output_streamer<HSAuint64>::put(out,v.SizeInBytes);
   return out;
}
};

template<>
struct output_streamer<HsaCounterProperties&> {
  inline static std::ostream& put(std::ostream& out, HsaCounterProperties& v)
{
   roctracer::kfd_support::output_streamer<HsaCounterBlockProperties[1]>::put(out,v.Blocks);
   roctracer::kfd_support::output_streamer<HSAuint32>::put(out,v.NumConcurrent);
   roctracer::kfd_support::output_streamer<HSAuint32>::put(out,v.NumBlocks);
   return out;
}
};

template<>
struct output_streamer<HSA_ENGINE_VERSION&> {
  inline static std::ostream& put(std::ostream& out, HSA_ENGINE_VERSION& v)
{
   roctracer::kfd_support::output_streamer<HSAuint32>::put(out,v.Value);
   return out;
}
};

template<>
struct output_streamer<HsaCComputeProperties&> {
  inline static std::ostream& put(std::ostream& out, HsaCComputeProperties& v)
{
   roctracer::kfd_support::output_streamer<HSAuint32[256]>::put(out,v.SiblingMap);
   return out;
}
};

template<>
struct output_streamer<HsaVersionInfo&> {
  inline static std::ostream& put(std::ostream& out, HsaVersionInfo& v)
{
   roctracer::kfd_support::output_streamer<HSAuint32>::put(out,v.KernelInterfaceMinorVersion);
   roctracer::kfd_support::output_streamer<HSAuint32>::put(out,v.KernelInterfaceMajorVersion);
   return out;
}
};

template<>
struct output_streamer<HsaCacheType&> {
  inline static std::ostream& put(std::ostream& out, HsaCacheType& v)
{
   roctracer::kfd_support::output_streamer<HSAuint32>::put(out,v.Value);
   return out;
}
};

template<>
struct output_streamer<HSA_MEMORYPROPERTY&> {
  inline static std::ostream& put(std::ostream& out, HSA_MEMORYPROPERTY& v)
{
   roctracer::kfd_support::output_streamer<HSAuint32>::put(out,v.MemoryProperty);
   return out;
}
};

template<>
struct output_streamer<HsaCounter&> {
  inline static std::ostream& put(std::ostream& out, HsaCounter& v)
{
   roctracer::kfd_support::output_streamer<HSAuint32>::put(out,v.BlockIndex);
   roctracer::kfd_support::output_streamer<HsaCounterFlags>::put(out,v.Flags);
   roctracer::kfd_support::output_streamer<HSAuint64>::put(out,v.CounterMask);
   roctracer::kfd_support::output_streamer<HSAuint32>::put(out,v.CounterSizeInBits);
   roctracer::kfd_support::output_streamer<HSAuint64>::put(out,v.CounterId);
   roctracer::kfd_support::output_streamer<HSA_PROFILE_TYPE>::put(out,v.Type);
   return out;
}
};

template<>
struct output_streamer<HsaNodeProperties&> {
  inline static std::ostream& put(std::ostream& out, HsaNodeProperties& v)
{
   roctracer::kfd_support::output_streamer<HSAuint8[20]>::put(out,v.Reserved);
   roctracer::kfd_support::output_streamer<HSAuint64>::put(out,v.UniqueID);
   roctracer::kfd_support::output_streamer<HSAuint32>::put(out,v.Domain);
   roctracer::kfd_support::output_streamer<HSAuint8>::put(out,v.Reserved2);
   roctracer::kfd_support::output_streamer<HSAuint8>::put(out,v.NumGws);
   roctracer::kfd_support::output_streamer<HSAuint8>::put(out,v.NumCpQueues);
   roctracer::kfd_support::output_streamer<HSAuint8>::put(out,v.NumSdmaQueuesPerEngine);
   roctracer::kfd_support::output_streamer<HSAuint32>::put(out,v.NumSdmaXgmiEngines);
   roctracer::kfd_support::output_streamer<HSAuint32>::put(out,v.NumSdmaEngines);
   roctracer::kfd_support::output_streamer<HSAuint64>::put(out,v.HiveID);
   roctracer::kfd_support::output_streamer<HSA_DEBUG_PROPERTIES>::put(out,v.DebugProperties);
   roctracer::kfd_support::output_streamer<HSA_ENGINE_VERSION>::put(out,v.uCodeEngineVersions);
   roctracer::kfd_support::output_streamer<HSAuint8[64]>::put(out,v.AMDName);
   roctracer::kfd_support::output_streamer<HSAuint16[64]>::put(out,v.MarketingName);
   roctracer::kfd_support::output_streamer<HSAint32>::put(out,v.DrmRenderMinor);
   roctracer::kfd_support::output_streamer<HSAuint32>::put(out,v.MaxEngineClockMhzCCompute);
   roctracer::kfd_support::output_streamer<HSAuint32>::put(out,v.MaxEngineClockMhzFCompute);
   roctracer::kfd_support::output_streamer<HSAuint64>::put(out,v.LocalMemSize);
   roctracer::kfd_support::output_streamer<HSAuint32>::put(out,v.LocationId);
   roctracer::kfd_support::output_streamer<HSAuint16>::put(out,v.DeviceId);
   roctracer::kfd_support::output_streamer<HSAuint16>::put(out,v.VendorId);
   roctracer::kfd_support::output_streamer<HSA_ENGINE_ID>::put(out,v.EngineId);
   roctracer::kfd_support::output_streamer<HSAuint32>::put(out,v.MaxSlotsScratchCU);
   roctracer::kfd_support::output_streamer<HSAuint32>::put(out,v.NumSIMDPerCU);
   roctracer::kfd_support::output_streamer<HSAuint32>::put(out,v.NumCUPerArray);
   roctracer::kfd_support::output_streamer<HSAuint32>::put(out,v.NumArrays);
   roctracer::kfd_support::output_streamer<HSAuint32>::put(out,v.NumShaderBanks);
   roctracer::kfd_support::output_streamer<HSAuint32>::put(out,v.WaveFrontSize);
   roctracer::kfd_support::output_streamer<HSAuint32>::put(out,v.GDSSizeInKB);
   roctracer::kfd_support::output_streamer<HSAuint32>::put(out,v.LDSSizeInKB);
   roctracer::kfd_support::output_streamer<HSAuint32>::put(out,v.MaxWavesPerSIMD);
   roctracer::kfd_support::output_streamer<HSA_CAPABILITY>::put(out,v.Capability);
   roctracer::kfd_support::output_streamer<HSAuint32>::put(out,v.FComputeIdLo);
   roctracer::kfd_support::output_streamer<HSAuint32>::put(out,v.CComputeIdLo);
   roctracer::kfd_support::output_streamer<HSAuint32>::put(out,v.NumIOLinks);
   roctracer::kfd_support::output_streamer<HSAuint32>::put(out,v.NumCaches);
   roctracer::kfd_support::output_streamer<HSAuint32>::put(out,v.NumMemoryBanks);
   roctracer::kfd_support::output_streamer<HSAuint32>::put(out,v.NumFComputeCores);
   roctracer::kfd_support::output_streamer<HSAuint32>::put(out,v.NumCPUCores);
   return out;
}
};

template<>
struct output_streamer<HsaSystemProperties&> {
  inline static std::ostream& put(std::ostream& out, HsaSystemProperties& v)
{
   roctracer::kfd_support::output_streamer<HSAuint32>::put(out,v.PlatformRev);
   roctracer::kfd_support::output_streamer<HSAuint32>::put(out,v.PlatformId);
   roctracer::kfd_support::output_streamer<HSAuint32>::put(out,v.PlatformOem);
   roctracer::kfd_support::output_streamer<HSAuint32>::put(out,v.NumNodes);
   return out;
}
};

template<>
struct output_streamer<HsaMemoryProperties&> {
  inline static std::ostream& put(std::ostream& out, HsaMemoryProperties& v)
{
   roctracer::kfd_support::output_streamer<HSAuint64>::put(out,v.VirtualBaseAddress);
   roctracer::kfd_support::output_streamer<HSAuint32>::put(out,v.MemoryClockMax);
   roctracer::kfd_support::output_streamer<HSAuint32>::put(out,v.Width);
   roctracer::kfd_support::output_streamer<HSA_MEMORYPROPERTY>::put(out,v.Flags);
   roctracer::kfd_support::output_streamer<HSA_HEAPTYPE>::put(out,v.HeapType);
   return out;
}
};

template<>
struct output_streamer<HSA_ENGINE_ID&> {
  inline static std::ostream& put(std::ostream& out, HSA_ENGINE_ID& v)
{
   roctracer::kfd_support::output_streamer<HSAuint32>::put(out,v.Value);
   return out;
}
};

template<>
struct output_streamer<HSA_CAPABILITY&> {
  inline static std::ostream& put(std::ostream& out, HSA_CAPABILITY& v)
{
   roctracer::kfd_support::output_streamer<HSAuint32>::put(out,v.Value);
   return out;
}
};

template<>
struct output_streamer<HsaQueueInfo&> {
  inline static std::ostream& put(std::ostream& out, HsaQueueInfo& v)
{
   roctracer::kfd_support::output_streamer<HSAuint64>::put(out,v.Reserved2);
   roctracer::kfd_support::output_streamer<HsaUserContextSaveAreaHeader *>::put(out,v.SaveAreaHeader);
   roctracer::kfd_support::output_streamer<HSAuint64>::put(out,v.ControlStackUsedInBytes);
   roctracer::kfd_support::output_streamer<HSAuint32 *>::put(out,v.ControlStackTop);
   roctracer::kfd_support::output_streamer<HSAuint64>::put(out,v.SaveAreaSizeInBytes);
   roctracer::kfd_support::output_streamer<HSAuint32 *>::put(out,v.UserContextSaveArea);
   roctracer::kfd_support::output_streamer<HSAuint32 *>::put(out,v.CUMaskInfo);
   roctracer::kfd_support::output_streamer<HSAuint32>::put(out,v.NumCUAssigned);
   roctracer::kfd_support::output_streamer<HSAuint32>::put(out,v.QueueTypeExtended);
   roctracer::kfd_support::output_streamer<HSAuint32>::put(out,v.QueueDetailError);
   return out;
}
};

template<>
struct output_streamer<HsaIoLinkProperties&> {
  inline static std::ostream& put(std::ostream& out, HsaIoLinkProperties& v)
{
   roctracer::kfd_support::output_streamer<HSA_LINKPROPERTY>::put(out,v.Flags);
   roctracer::kfd_support::output_streamer<HSAuint32>::put(out,v.RecTransferSize);
   roctracer::kfd_support::output_streamer<HSAuint32>::put(out,v.MaximumBandwidth);
   roctracer::kfd_support::output_streamer<HSAuint32>::put(out,v.MinimumBandwidth);
   roctracer::kfd_support::output_streamer<HSAuint32>::put(out,v.MaximumLatency);
   roctracer::kfd_support::output_streamer<HSAuint32>::put(out,v.MinimumLatency);
   roctracer::kfd_support::output_streamer<HSAuint32>::put(out,v.Weight);
   roctracer::kfd_support::output_streamer<HSAuint32>::put(out,v.NodeTo);
   roctracer::kfd_support::output_streamer<HSAuint32>::put(out,v.NodeFrom);
   roctracer::kfd_support::output_streamer<HSAuint32>::put(out,v.VersionMinor);
   roctracer::kfd_support::output_streamer<HSAuint32>::put(out,v.VersionMajor);
   roctracer::kfd_support::output_streamer<HSA_IOLINKTYPE>::put(out,v.IoLinkType);
   return out;
}
};

template<>
struct output_streamer<HsaMemoryAccessFault&> {
  inline static std::ostream& put(std::ostream& out, HsaMemoryAccessFault& v)
{
   roctracer::kfd_support::output_streamer<HSA_EVENTID_MEMORYFLAGS>::put(out,v.Flags);
   roctracer::kfd_support::output_streamer<HsaAccessAttributeFailure>::put(out,v.Failure);
   roctracer::kfd_support::output_streamer<HSAuint64>::put(out,v.VirtualAddress);
   roctracer::kfd_support::output_streamer<HSAuint32>::put(out,v.NodeId);
   return out;
}
};

template<>
struct output_streamer<HsaEvent&> {
  inline static std::ostream& put(std::ostream& out, HsaEvent& v)
{
   roctracer::kfd_support::output_streamer<HsaEventData>::put(out,v.EventData);
   roctracer::kfd_support::output_streamer<HSA_EVENTID>::put(out,v.EventId);
   return out;
}
};

template<>
struct output_streamer<HsaMemMapFlags&> {
  inline static std::ostream& put(std::ostream& out, HsaMemMapFlags& v)
{
   return out;
}
};

template<>
struct output_streamer<HsaDbgWaveMessage&> {
  inline static std::ostream& put(std::ostream& out, HsaDbgWaveMessage& v)
{
   roctracer::kfd_support::output_streamer<HsaDbgWaveMessageAMD>::put(out,v.DbgWaveMsg);
   return out;
}
};

template<>
struct output_streamer<HsaGraphicsResourceInfo&> {
  inline static std::ostream& put(std::ostream& out, HsaGraphicsResourceInfo& v)
{
   roctracer::kfd_support::output_streamer<HSAuint32>::put(out,v.Reserved);
   roctracer::kfd_support::output_streamer<HSAuint32>::put(out,v.MetadataSizeInBytes);
   roctracer::kfd_support::output_streamer<HSAuint64>::put(out,v.SizeInBytes);
   return out;
}
};

template<>
struct output_streamer<HsaEventData&> {
  inline static std::ostream& put(std::ostream& out, HsaEventData& v)
{
   roctracer::kfd_support::output_streamer<HSAuint32>::put(out,v.HWData3);
   roctracer::kfd_support::output_streamer<HSAuint64>::put(out,v.HWData2);
   roctracer::kfd_support::output_streamer<HSAuint64>::put(out,v.HWData1);
   roctracer::kfd_support::output_streamer<HsaMemoryAccessFault>::put(out,v.EventData.MemoryAccessFault);
   roctracer::kfd_support::output_streamer<HsaDeviceStateChange>::put(out,v.EventData.DeviceState);
   roctracer::kfd_support::output_streamer<HsaNodeChange>::put(out,v.EventData.NodeChangeState);
   roctracer::kfd_support::output_streamer<HsaSyncVar>::put(out,v.EventData.SyncVar);
   roctracer::kfd_support::output_streamer<HSA_EVENTTYPE>::put(out,v.EventType);
   return out;
}
};

template<>
struct output_streamer<HsaDbgWaveMessageAMD&> {
  inline static std::ostream& put(std::ostream& out, HsaDbgWaveMessageAMD& v)
{
   roctracer::kfd_support::output_streamer<HsaDbgWaveMsgAMDGen2>::put(out,v.WaveMsgInfoGen2);
   return out;
}
};

template<>
struct output_streamer<HsaPointerInfo&> {
  inline static std::ostream& put(std::ostream& out, HsaPointerInfo& v)
{
   roctracer::kfd_support::output_streamer<const HSAuint32 *>::put(out,v.MappedNodes);
   roctracer::kfd_support::output_streamer<const HSAuint32 *>::put(out,v.RegisteredNodes);
   roctracer::kfd_support::output_streamer<HSAuint32>::put(out,v.NMappedNodes);
   roctracer::kfd_support::output_streamer<HSAuint32>::put(out,v.NRegisteredNodes);
   roctracer::kfd_support::output_streamer<HSAuint64>::put(out,v.SizeInBytes);
   roctracer::kfd_support::output_streamer<HSAuint64>::put(out,v.GPUAddress);
   roctracer::kfd_support::output_streamer<HsaMemFlags>::put(out,v.MemFlags);
   roctracer::kfd_support::output_streamer<HSAuint32>::put(out,v.Node);
   roctracer::kfd_support::output_streamer<HSA_POINTER_TYPE>::put(out,v.Type);
   return out;
}
};

template<>
struct output_streamer<HsaClockCounters&> {
  inline static std::ostream& put(std::ostream& out, HsaClockCounters& v)
{
   roctracer::kfd_support::output_streamer<HSAuint64>::put(out,v.SystemClockFrequencyHz);
   roctracer::kfd_support::output_streamer<HSAuint64>::put(out,v.SystemClockCounter);
   roctracer::kfd_support::output_streamer<HSAuint64>::put(out,v.CPUClockCounter);
   roctracer::kfd_support::output_streamer<HSAuint64>::put(out,v.GPUClockCounter);
   return out;
}
};

template<>
struct output_streamer<HsaEventDescriptor&> {
  inline static std::ostream& put(std::ostream& out, HsaEventDescriptor& v)
{
   roctracer::kfd_support::output_streamer<HsaSyncVar>::put(out,v.SyncVar);
   roctracer::kfd_support::output_streamer<HSAuint32>::put(out,v.NodeId);
   roctracer::kfd_support::output_streamer<HSA_EVENTTYPE>::put(out,v.EventType);
   return out;
}
};

template<>
struct output_streamer<HsaAccessAttributeFailure&> {
  inline static std::ostream& put(std::ostream& out, HsaAccessAttributeFailure& v)
{
   roctracer::kfd_support::output_streamer<unsigned int>::put(out,v.Reserved);
   roctracer::kfd_support::output_streamer<unsigned int>::put(out,v.ErrorType);
   roctracer::kfd_support::output_streamer<unsigned int>::put(out,v.Imprecise);
   roctracer::kfd_support::output_streamer<unsigned int>::put(out,v.ECC);
   roctracer::kfd_support::output_streamer<unsigned int>::put(out,v.GpuAccess);
   roctracer::kfd_support::output_streamer<unsigned int>::put(out,v.NoExecute);
   roctracer::kfd_support::output_streamer<unsigned int>::put(out,v.ReadOnly);
   roctracer::kfd_support::output_streamer<unsigned int>::put(out,v.NotPresent);
   return out;
}
};

template<>
struct output_streamer<HSA_UUID&> {
  inline static std::ostream& put(std::ostream& out, HSA_UUID& v)
{
   roctracer::kfd_support::output_streamer<HSAuint8[8]>::put(out,v.Data4);
   roctracer::kfd_support::output_streamer<HSAuint16>::put(out,v.Data3);
   roctracer::kfd_support::output_streamer<HSAuint16>::put(out,v.Data2);
   roctracer::kfd_support::output_streamer<HSAuint32>::put(out,v.Data1);
   return out;
}
};

template<>
struct output_streamer<HsaQueueResource&> {
  inline static std::ostream& put(std::ostream& out, HsaQueueResource& v)
{
   roctracer::kfd_support::output_streamer<HSA_QUEUEID>::put(out,v.QueueId);
   return out;
}
};

template<>
struct output_streamer<HsaCounterFlags&> {
  inline static std::ostream& put(std::ostream& out, HsaCounterFlags& v)
{
   return out;
}
};

template<>
struct output_streamer<HsaUserContextSaveAreaHeader&> {
  inline static std::ostream& put(std::ostream& out, HsaUserContextSaveAreaHeader& v)
{
   roctracer::kfd_support::output_streamer<HSAuint32>::put(out,v.WaveStateSize);
   roctracer::kfd_support::output_streamer<HSAuint32>::put(out,v.WaveStateOffset);
   roctracer::kfd_support::output_streamer<HSAuint32>::put(out,v.ControlStackSize);
   roctracer::kfd_support::output_streamer<HSAuint32>::put(out,v.ControlStackOffset);
   return out;
}
};

template<>
struct output_streamer<HsaCacheProperties&> {
  inline static std::ostream& put(std::ostream& out, HsaCacheProperties& v)
{
   roctracer::kfd_support::output_streamer<HSAuint32[256]>::put(out,v.SiblingMap);
   roctracer::kfd_support::output_streamer<HsaCacheType>::put(out,v.CacheType);
   roctracer::kfd_support::output_streamer<HSAuint32>::put(out,v.CacheLatency);
   roctracer::kfd_support::output_streamer<HSAuint32>::put(out,v.CacheAssociativity);
   roctracer::kfd_support::output_streamer<HSAuint32>::put(out,v.CacheLinesPerTag);
   roctracer::kfd_support::output_streamer<HSAuint32>::put(out,v.CacheLineSize);
   roctracer::kfd_support::output_streamer<HSAuint32>::put(out,v.CacheSize);
   roctracer::kfd_support::output_streamer<HSAuint32>::put(out,v.CacheLevel);
   roctracer::kfd_support::output_streamer<HSAuint32>::put(out,v.ProcessorIdLow);
   return out;
}
};

template<>
struct output_streamer<HsaMemFlags&> {
  inline static std::ostream& put(std::ostream& out, HsaMemFlags& v)
{
   return out;
}
};

template<>
struct output_streamer<HsaPmcTraceRoot&> {
  inline static std::ostream& put(std::ostream& out, HsaPmcTraceRoot& v)
{
   roctracer::kfd_support::output_streamer<HSATraceId>::put(out,v.TraceId);
   roctracer::kfd_support::output_streamer<HSAuint32>::put(out,v.NumberOfPasses);
   roctracer::kfd_support::output_streamer<HSAuint64>::put(out,v.TraceBufferMinSizeBytes);
   return out;
}
};

template<>
struct output_streamer<HsaGpuTileConfig&> {
  inline static std::ostream& put(std::ostream& out, HsaGpuTileConfig& v)
{
   roctracer::kfd_support::output_streamer<HSAuint32[7]>::put(out,v.Reserved);
   roctracer::kfd_support::output_streamer<HSAuint32>::put(out,v.NumRanks);
   roctracer::kfd_support::output_streamer<HSAuint32>::put(out,v.NumBanks);
   roctracer::kfd_support::output_streamer<HSAuint32>::put(out,v.GbAddrConfig);
   roctracer::kfd_support::output_streamer<HSAuint32>::put(out,v.NumMacroTileConfigs);
   roctracer::kfd_support::output_streamer<HSAuint32>::put(out,v.NumTileConfigs);
   roctracer::kfd_support::output_streamer<HSAuint32 *>::put(out,v.MacroTileConfig);
   roctracer::kfd_support::output_streamer<HSAuint32 *>::put(out,v.TileConfig);
   return out;
}
};

template<>
struct output_streamer<HsaSyncVar&> {
  inline static std::ostream& put(std::ostream& out, HsaSyncVar& v)
{
   roctracer::kfd_support::output_streamer<HSAuint64>::put(out,v.SyncVarSize);
   roctracer::kfd_support::output_streamer<HSAuint64>::put(out,v.SyncVar.UserDataPtrValue);
   return out;
}
};

template<>
struct output_streamer<HsaDbgWaveMsgAMDGen2&> {
  inline static std::ostream& put(std::ostream& out, HsaDbgWaveMsgAMDGen2& v)
{
   roctracer::kfd_support::output_streamer<HSAuint32>::put(out,v.Reserved2);
   roctracer::kfd_support::output_streamer<HSAuint32>::put(out,v.Value);
   return out;
}
};
// end ostream ops for KFD 
};};

#endif //__cplusplus
#endif // INC_KFD_OSTREAM_OPS_H_
 
