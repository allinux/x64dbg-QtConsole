#pragma once

#include "pluginmain.h"

#define plugin_name "QtConsole Launcher" // set plugin name
#define plugin_version 1.0 // set plugin version

//functions
bool pyInit(PLUG_INITSTRUCT* initStruct);
bool pyStop();
void pySetup();
