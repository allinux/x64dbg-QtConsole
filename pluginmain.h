#ifndef _PLUGINMAIN_H
#define _PLUGINMAIN_H

#include <windows.h>
#include "pluginsdk\_plugins.h"

#ifndef DLL_EXPORT
#define DLL_EXPORT __declspec(dllexport)
#endif //DLL_EXPORT

//superglobal variables
extern int pluginHandle;
extern HWND hwndDlg;
extern int hMenu;
extern int hMenuDisasm;
extern int hMenuDump;
extern int hMenuStack;
extern HINSTANCE hInst;

#ifdef __cplusplus
extern "C"
{
#endif

DLL_EXPORT bool pluginit(PLUG_INITSTRUCT* initStruct);
DLL_EXPORT bool plugstop();
DLL_EXPORT void plugsetup(PLUG_SETUPSTRUCT* setupStruct);

#ifdef __cplusplus
}
#endif

#endif //_PLUGINMAIN_H
