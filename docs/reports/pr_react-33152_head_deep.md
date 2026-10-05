graph TD
    Default["Default\n(6 entities)"]
    Babel["Babel\n(3 entities)"]
    Default2["Default2\n(1 entities)"]
    Apps["Apps\n(47 entities)"]
    Packages["Packages\n(1287 entities)"]
    Scripts["Scripts\n(16 entities)"]
    Fixtures["Fixtures\n(56 entities)"]
    Art["Art\n(3 entities)"]
    Attribute_Behavior["Attribute-Behavior\n(12 entities)"]
    Concurrent["Concurrent\n(3 entities)"]
    Devtools["Devtools\n(8 entities)"]
    Dom["Dom\n(189 entities)"]
    Eslint_V6["Eslint-V6\n(1 entities)"]
    Eslint_V7["Eslint-V7\n(1 entities)"]
    Eslint_V8["Eslint-V8\n(1 entities)"]
    Eslint_V9["Eslint-V9\n(2 entities)"]
    Expiration["Expiration\n(6 entities)"]
    Fiber_Debugger["Fiber-Debugger\n(10 entities)"]
    Fizz["Fizz\n(11 entities)"]
    Flight["Flight\n(61 entities)"]
    Flight_Esm["Flight-Esm\n(21 entities)"]
    Flight_Parcel["Flight-Parcel\n(18 entities)"]
    Flight_Vite["Flight-Vite\n(67 entities)"]
    Legacy_Jsx_Runtimes["Legacy-Jsx-Runtimes\n(47 entities)"]
    Nesting["Nesting\n(14 entities)"]
    Owner_Stacks["Owner-Stacks\n(4 entities)"]
    Packaging["Packaging\n(27 entities)"]
    Ssr["Ssr\n(17 entities)"]
    Ssr2["Ssr2\n(16 entities)"]
    Stacks["Stacks\n(21 entities)"]
    View_Transition["View-Transition\n(12 entities)"]
    Packages2["Packages2\n(25 entities)"]
    Dom_Event_Testing_Library["Dom-Event-Testing-Library\n(63 entities)"]
    Eslint_Plugin_React_Hooks["Eslint-Plugin-React-Hooks\n(151 entities)"]
    Internal_Test_Utils["Internal-Test-Utils\n(38 entities)"]
    Jest_React["Jest-React\n(7 entities)"]
    React["React\n(104 entities)"]
    React_Art["React-Art\n(112 entities)"]
    React_Cache["React-Cache\n(9 entities)"]
    React_Client["React-Client\n(151 entities)"]
    React_Debug_Tools["React-Debug-Tools\n(43 entities)"]
    React_Devtools["React-Devtools\n(3 entities)"]
    React_Devtools_Core["React-Devtools-Core\n(34 entities)"]
    React_Devtools_Extensions["React-Devtools-Extensions\n(88 entities)"]
    React_Devtools_Fusebox["React-Devtools-Fusebox\n(5 entities)"]
    React_Devtools_Inline["React-Devtools-Inline\n(15 entities)"]
    React_Devtools_Shared["React-Devtools-Shared\n(633 entities)"]
    React_Devtools_Shell["React-Devtools-Shell\n(146 entities)"]
    React_Devtools_Timeline["React-Devtools-Timeline\n(283 entities)"]
    React_Dom["React-Dom\n(124 entities)"]
    React_Dom_Bindings["React-Dom-Bindings\n(756 entities)"]
    React_Is["React-Is\n(17 entities)"]
    React_Markup["React-Markup\n(27 entities)"]
    React_Native_Renderer["React-Native-Renderer\n(330 entities)"]
    React_Noop_Renderer["React-Noop-Renderer\n(19 entities)"]
    React_Reconciler["React-Reconciler\n(882 entities)"]
    React_Refresh["React-Refresh\n(24 entities)"]
    React_Server["React-Server\n(457 entities)"]
    React_Server_Dom_Esm["React-Server-Dom-Esm\n(62 entities)"]
    React_Server_Dom_Fb["React-Server-Dom-Fb\n(5 entities)"]
    React_Server_Dom_Parcel["React-Server-Dom-Parcel\n(92 entities)"]
    React_Server_Dom_Turbopack["React-Server-Dom-Turbopack\n(87 entities)"]
    React_Server_Dom_Vite["React-Server-Dom-Vite\n(83 entities)"]
    React_Server_Dom_Webpack["React-Server-Dom-Webpack\n(128 entities)"]
    React_Suspense_Test_Utils["React-Suspense-Test-Utils\n(1 entities)"]
    React_Test_Renderer["React-Test-Renderer\n(3 entities)"]
    Scheduler["Scheduler\n(89 entities)"]
    Shared["Shared\n(73 entities)"]
    Use_Subscription["Use-Subscription\n(2 entities)"]
    Use_Sync_External_Store["Use-Sync-External-Store\n(18 entities)"]
    Scripts2["Scripts2\n(6 entities)"]
    Babel2["Babel2\n(6 entities)"]
    Bench["Bench\n(43 entities)"]
    Ci["Ci\n(10 entities)"]
    Devtools2["Devtools2\n(29 entities)"]
    Error_Codes["Error-Codes\n(4 entities)"]
    Eslint_Rules["Eslint-Rules\n(15 entities)"]
    Flags["Flags\n(14 entities)"]
    Flow["Flow\n(15 entities)"]
    Jest["Jest\n(53 entities)"]
    Print_Warnings["Print-Warnings\n(1 entities)"]
    Release["Release\n(65 entities)"]
    Rollup["Rollup\n(85 entities)"]
    Shared2["Shared2\n(10 entities)"]
    Tasks["Tasks\n(6 entities)"]
    Apps --> React_Devtools_Shared
    Dom --> Apps
    Flight --> React_Dom_Bindings
    Packages --> React_Art
    Packages --> React_Devtools_Shared
    React --> Packages
    React --> React_Debug_Tools
    React --> React_Server
    React --> Use_Sync_External_Store
    React_Art --> Packages
    React_Client --> React_Server_Dom_Webpack
    React_Devtools_Shared --> Packages
    React_Devtools_Shared --> React_Devtools_Timeline
    React_Devtools_Shared --> Scheduler
    React_Devtools_Shell --> React_Reconciler
    React_Devtools_Shell --> Ssr
    React_Devtools_Timeline --> React_Devtools_Shared
    React_Dom_Bindings --> Flight
    React_Dom_Bindings --> React_Native_Renderer
    React_Dom_Bindings --> React_Reconciler
    React_Dom_Bindings --> React_Server
    React_Markup --> React_Server
    React_Native_Renderer --> Packages
    React_Native_Renderer --> React_Dom_Bindings
    React_Native_Renderer --> React_Reconciler
    React_Reconciler --> Flight
    React_Reconciler --> Packages
    React_Reconciler --> React_Devtools_Shared
    React_Reconciler --> React_Devtools_Shell
    React_Reconciler --> React_Dom_Bindings
    React_Reconciler --> React_Native_Renderer
    React_Reconciler --> React_Server
    React_Reconciler --> Scheduler
    React_Reconciler --> Ssr2
    React_Server --> React_Dom_Bindings
    React_Server --> React_Markup
    React_Server --> React_Reconciler
    React_Server --> React_Server_Dom_Webpack
    React_Server_Dom_Webpack --> React_Server