/* AROS Wizard ReactOS/Win32 host prototype; read-only, no installation. */
#define WIN32_LEAN_AND_MEAN
#include <windows.h>
static const char CLASS_NAME[] = "AROSWizardReactOS";
static LRESULT CALLBACK WindowProc(HWND hwnd, UINT msg, WPARAM wp, LPARAM lp) {
    switch (msg) {
    case WM_CREATE:
        CreateWindowA("STATIC", "AROS Wizard - ReactOS edition (prototype)",
            WS_CHILD | WS_VISIBLE, 18, 16, 340, 24, hwnd, NULL,
            (HINSTANCE)GetWindowLongPtr(hwnd, GWLP_HINSTANCE), NULL);
        CreateWindowA("STATIC", "Host diagnostics only. AROS installation is not implemented.",
            WS_CHILD | WS_VISIBLE, 18, 48, 350, 44, hwnd, NULL,
            (HINSTANCE)GetWindowLongPtr(hwnd, GWLP_HINSTANCE), NULL);
        CreateWindowA("BUTTON", "About", WS_CHILD | WS_VISIBLE | BS_PUSHBUTTON,
            18, 106, 100, 30, hwnd, (HMENU)(INT_PTR)101,
            (HINSTANCE)GetWindowLongPtr(hwnd, GWLP_HINSTANCE), NULL);
        return 0;
    case WM_COMMAND:
        if (LOWORD(wp) == 101) {
            MessageBoxA(hwnd, "AROS Wizard portable 0.1.0-dev\nReactOS/Win32 preview\nNo changes to the system.", "About", MB_OK | MB_ICONINFORMATION);
            return 0;
        }
        break;
    case WM_DESTROY: PostQuitMessage(0); return 0;
    }
    return DefWindowProcA(hwnd, msg, wp, lp);
}
int WINAPI WinMain(HINSTANCE instance, HINSTANCE previous, LPSTR command, int show) {
    WNDCLASSA wc = {0};
    HWND hwnd;
    MSG msg;
    (void)previous; (void)command;
    wc.lpfnWndProc = WindowProc;
    wc.hInstance = instance;
    wc.lpszClassName = CLASS_NAME;
    wc.hCursor = LoadCursor(NULL, IDC_ARROW);
    wc.hbrBackground = (HBRUSH)(COLOR_WINDOW + 1);
    if (!RegisterClassA(&wc)) return 1;
    hwnd = CreateWindowA(CLASS_NAME, "AROS Wizard for ReactOS", WS_OVERLAPPEDWINDOW,
        CW_USEDEFAULT, CW_USEDEFAULT, 430, 225, NULL, NULL, instance, NULL);
    if (!hwnd) return 2;
    ShowWindow(hwnd, show);
    UpdateWindow(hwnd);
    while (GetMessageA(&msg, NULL, 0, 0) > 0) {
        TranslateMessage(&msg);
        DispatchMessageA(&msg);
    }
    return (int)msg.wParam;
}
