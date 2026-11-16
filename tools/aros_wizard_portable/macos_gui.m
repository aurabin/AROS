/* Native macOS Cocoa prototype. Read-only; does not install AROS. */
#import <Cocoa/Cocoa.h>
#include "wizard_core.h"
@interface WizardAppDelegate : NSObject <NSApplicationDelegate>
@property (strong) NSWindow *window;
@end
@implementation WizardAppDelegate
- (void)applicationDidFinishLaunching:(NSNotification *)notification {
    (void)notification;
    NSRect frame = NSMakeRect(0, 0, 540, 300);
    self.window = [[NSWindow alloc] initWithContentRect:frame
        styleMask:(NSWindowStyleMaskTitled | NSWindowStyleMaskClosable |
                   NSWindowStyleMaskMiniaturizable | NSWindowStyleMaskResizable)
        backing:NSBackingStoreBuffered defer:NO];
    [self.window setTitle:@"AROS Wizard for macOS"];
    [self.window center];
    NSView *view = [self.window contentView];
    NSTextField *title = [NSTextField labelWithString:@"AROS Wizard for macOS"];
    title.font = [NSFont boldSystemFontOfSize:25];
    title.frame = NSMakeRect(30, 220, 470, 38);
    [view addSubview:title];
    NSString *status = [NSString stringWithFormat:
        @"Host: %s\nVersion: 0.2.0-dev\nMode: read-only diagnostics\nAROS installation: not implemented",
        wizard_platform()];
    NSTextField *details = [NSTextField wrappingLabelWithString:status];
    details.font = [NSFont systemFontOfSize:15];
    details.frame = NSMakeRect(30, 85, 470, 120);
    [view addSubview:details];
    [self.window makeKeyAndOrderFront:nil];
    [NSApp activateIgnoringOtherApps:YES];
}
- (BOOL)applicationShouldTerminateAfterLastWindowClosed:(NSApplication *)sender {
    (void)sender;
    return YES;
}
@end
int main(int argc, const char *argv[]) {
    (void)argc; (void)argv;
    @autoreleasepool {
        NSApplication *app = [NSApplication sharedApplication];
        WizardAppDelegate *delegate = [[WizardAppDelegate alloc] init];
        [app setDelegate:delegate];
        [app run];
    }
    return 0;
}
