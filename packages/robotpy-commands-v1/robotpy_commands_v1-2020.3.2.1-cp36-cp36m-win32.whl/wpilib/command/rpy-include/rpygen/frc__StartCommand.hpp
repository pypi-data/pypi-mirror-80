
 

// This file is autogenerated. DO NOT EDIT

#pragma once
#include <robotpy_build.h>


#include <frc\commands\StartCommand.h>

#include <frc/smartdashboard/SendableBuilder.h>
#include <frc/commands/Command.h>
#include <frc/commands/CommandGroup.h>



#include <rpygen/frc__InstantCommand.hpp>

namespace rpygen {

using namespace frc;


template <typename CxxBase>
using PyBasefrc__StartCommand = 
    Pyfrc__InstantCommand<
        CxxBase
    
    >
;

template <typename CxxBase>
struct Pyfrc__StartCommand : PyBasefrc__StartCommand<CxxBase> {
    using PyBasefrc__StartCommand<CxxBase>::PyBasefrc__StartCommand;



#ifndef RPYGEN_DISABLE_Initialize_v
    void Initialize() override {
PYBIND11_OVERLOAD_NAME(PYBIND11_TYPE(void), CxxBase, "initialize", Initialize,);    }
#endif



};

}; // namespace rpygen
