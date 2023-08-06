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

template <typename T>
struct output_streamer {
  inline static std::ostream& put(std::ostream& out, const T& v) { return out; }
};
template<>
struct output_streamer<void*> {
inline static std::ostream& put(std::ostream& out, void* v) { out << std::hex << v; return out; }
};
template<>
struct output_streamer<const void*> {
inline static std::ostream& put(std::ostream& out, const void* v) { out << std::hex << v; return out; }
};

template<>
struct output_streamer<bool> {
  inline static std::ostream& put(std::ostream& out, bool v) { out << std::hex << "<bool " << "0x" << v << std::dec << ">"; return out; }
};

template<>
struct output_streamer<uint8_t> {
  inline static std::ostream& put(std::ostream& out, uint8_t v) { out << std::hex << "<uint8_t " << "0x" << v << std::dec << ">"; return out; }
};

template<>
struct output_streamer<uint16_t> {
  inline static std::ostream& put(std::ostream& out, uint16_t v) { out << std::hex << "<uint16_t " << "0x" << v << std::dec << ">"; return out; }
};

template<>
struct output_streamer<uint32_t> {
  inline static std::ostream& put(std::ostream& out, uint32_t v) { out << std::hex << "<uint32_t " << "0x" << v << std::dec << ">"; return out; }
};

template<>
struct output_streamer<uint64_t> {
  inline static std::ostream& put(std::ostream& out, uint64_t v) { out << std::hex << "<uint64_t " << "0x" << v << std::dec << ">"; return out; }
};


template<>
struct output_streamer<bool*> {
  inline static std::ostream& put(std::ostream& out, bool* v) { out << std::hex << "<bool " << "0x" << *v << std::dec << ">"; return out; }
};

template<>
struct output_streamer<uint8_t*> {
  inline static std::ostream& put(std::ostream& out, uint8_t* v) { out << std::hex << "<uint8_t " << "0x" << *v << std::dec << ">"; return out; }
};

template<>
struct output_streamer<uint16_t*> {
  inline static std::ostream& put(std::ostream& out, uint16_t* v) { out << std::hex << "<uint16_t " << "0x" << *v << std::dec << ">"; return out; }
};

template<>
struct output_streamer<uint32_t*> {
  inline static std::ostream& put(std::ostream& out, uint32_t* v) { out << std::hex << "<uint32_t " << "0x" << *v << std::dec << ">"; return out; }
};

template<>
struct output_streamer<uint64_t*> {
  inline static std::ostream& put(std::ostream& out, uint64_t* v) { out << std::hex << "<uint64_t " << "0x" << *v << std::dec << ">"; return out; }
};

