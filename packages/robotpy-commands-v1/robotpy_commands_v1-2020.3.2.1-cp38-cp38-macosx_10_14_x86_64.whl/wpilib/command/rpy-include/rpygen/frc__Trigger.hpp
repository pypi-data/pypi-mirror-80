
 

// This file is autogenerated. DO NOT EDIT

#pragma once
#include <robotpy_build.h>


#include <frc/buttons/Trigger.h>

#include <frc/smartdashboard/SendableBuilder.h>
#include <frc/commands/Command.h>
#include <frc/commands/CommandGroup.h>



#include <rpygen/frc__Sendable.hpp>

namespace rpygen {

using namespace frc;


template <typename CxxBase>
using PyBasefrc__Trigger = 
    Pyfrc__Sendable<
        CxxBase
    
    >
;

template <typename CxxBase>
struct Pyfrc__Trigger : PyBasefrc__Trigger<CxxBase> {
    using PyBasefrc__Trigger<CxxBase>::PyBasefrc__Trigger;



#ifndef RPYGEN_DISABLE_Get_v
    bool Get() override {
RPYBUILD_OVERLOAD_PURE_NAME(Trigger,PYBIND11_TYPE(bool), CxxBase, "get", Get,);    }
#endif

#ifndef RPYGEN_DISABLE_InitSendable_RTSendableBuilder
    void InitSendable(SendableBuilder& builder) override {
PYBIND11_OVERLOAD_NAME(PYBIND11_TYPE(void), CxxBase, "initSendable", InitSendable,builder);    }
#endif



};

}; // namespace rpygen
