#include "plugin.h"
#include "resource.h"
#include "x64dbgpy.h"

enum
{
	RUN_QTCONSOLE,
};

// editor
static void RunQtConsole() // function to call main python app file
{
	ExecutePythonScriptW(L"plugins\\QtConsoleLauncher\\launcher.py"); // execution of main file location (relative to x64dbg.exe)
}

extern "C" __declspec(dllexport) void CBMENUENTRY(CBTYPE cbType, PLUG_CB_MENUENTRY* info)
{
	switch(info->hEntry)
	{
	case RUN_QTCONSOLE: 
		RunQtConsole();
		break;
	}
}

bool pyInit(PLUG_INITSTRUCT* initStruct)
{
	return true;
}

bool pyStop()
{
	return true;
}

void pySetup()
{
	// Set Menu Icon
	ICONDATA pyIcon;
	HRSRC hRes = FindResourceW(hInst, MAKEINTRESOURCEW(IDB_PNG1), L"PNG");
	HGLOBAL hMem = LoadResource(hInst, hRes);
	pyIcon.data = LockResource(hMem);
	pyIcon.size = SizeofResource(hInst, hRes);
	_plugin_menuseticon(hMenu, &pyIcon);
	FreeResource(hMem);

	// Register menu entry
	_plugin_menuaddentry(hMenu, RUN_QTCONSOLE, "Run QtConsole");
}