
 

// This file is autogenerated. DO NOT EDIT

#pragma once
#include <robotpy_build.h>


#include <frc/buttons/HeldButtonScheduler.h>

#include <frc/smartdashboard/SendableBuilder.h>
#include <frc/buttons/Trigger.h>
#include <frc/commands/Command.h>
#include <frc/commands/CommandGroup.h>



#include <rpygen/frc__ButtonScheduler.hpp>

namespace rpygen {

using namespace frc;


template <typename CxxBase>
using PyBasefrc__HeldButtonScheduler = 
    Pyfrc__ButtonScheduler<
        CxxBase
    
    >
;

template <typename CxxBase>
struct Pyfrc__HeldButtonScheduler : PyBasefrc__HeldButtonScheduler<CxxBase> {
    using PyBasefrc__HeldButtonScheduler<CxxBase>::PyBasefrc__HeldButtonScheduler;



#ifndef RPYGEN_DISABLE_Execute_v
    void Execute() override {
PYBIND11_OVERLOAD_NAME(PYBIND11_TYPE(void), CxxBase, "execute", Execute,);    }
#endif



};

}; // namespace rpygen
