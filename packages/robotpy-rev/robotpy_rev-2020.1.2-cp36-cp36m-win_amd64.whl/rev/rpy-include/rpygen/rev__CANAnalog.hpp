
 

// This file is autogenerated. DO NOT EDIT

#pragma once
#include <robotpy_build.h>


#include <rev\CANAnalog.h>

#include <rev/CANSparkMax.h>



#include <rpygen/rev__CANSensor.hpp>

namespace rpygen {

using namespace rev;


template <typename CxxBase>
using PyBaserev__CANAnalog = 
    Pyrev__CANSensor<
        CxxBase
    
    >
;

template <typename CxxBase>
struct Pyrev__CANAnalog : PyBaserev__CANAnalog<CxxBase> {
    using PyBaserev__CANAnalog<CxxBase>::PyBaserev__CANAnalog;



#ifndef RPYGEN_DISABLE_SetInverted_b
    CANError SetInverted(bool inverted) override {
PYBIND11_OVERLOAD_NAME(PYBIND11_TYPE(CANError), CxxBase, "setInverted", SetInverted,inverted);    }
#endif

#ifndef RPYGEN_DISABLE_KGetInverted_v
    bool GetInverted() const override {
PYBIND11_OVERLOAD_NAME(PYBIND11_TYPE(bool), CxxBase, "getInverted", GetInverted,);    }
#endif

#ifndef RPYGEN_DISABLE_KGetID_v
    int GetID() const override {
PYBIND11_OVERLOAD_NAME(PYBIND11_TYPE(int), CxxBase, "_getID", GetID,);    }
#endif



};

}; // namespace rpygen
