
 

// This file is autogenerated. DO NOT EDIT

#pragma once
#include <robotpy_build.h>


#include <frc\buttons\POVButton.h>

#include <frc/smartdashboard/SendableBuilder.h>
#include <frc/buttons/Trigger.h>
#include <frc/commands/Command.h>
#include <frc/commands/CommandGroup.h>



#include <rpygen/frc__Button.hpp>

namespace rpygen {

using namespace frc;


template <typename CxxBase>
using PyBasefrc__POVButton = 
    Pyfrc__Button<
        CxxBase
    
    >
;

template <typename CxxBase>
struct Pyfrc__POVButton : PyBasefrc__POVButton<CxxBase> {
    using PyBasefrc__POVButton<CxxBase>::PyBasefrc__POVButton;



#ifndef RPYGEN_DISABLE_Get_v
    bool Get() override {
PYBIND11_OVERLOAD_NAME(PYBIND11_TYPE(bool), CxxBase, "get", Get,);    }
#endif



};

}; // namespace rpygen
