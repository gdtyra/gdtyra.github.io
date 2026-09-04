# Potential Deep Dives

## [croc](https://github.com/schollz/croc)
- A low-friction CLI file transfer tool written in Go
- Uses PAKE for end-to-end encryption
- Unique mnemonic code is generated on send and entered elsewhere to receive files
- Participating machines both connect to a relay server, through which the files are transferred
- Supports local network transfers whereby the sender serves its own relay and advertises the relay via local network broadcast

## [Cool Retro Term](https://github.com/Swordfish90/cool-retro-term) - terminal emulator with fun effects

- UI implemented with QML and shader effects
- Built on top of QMLTermWidget, which is a QML port of QTermWidget
- Contains various fonts mimicking 70s and 80s fixed-width fonts

## [noclip.website](https://github.com/magcius/noclip.website/tree/master) - level viewer and arguably partial re-implementation of some game engines

- Supports WebGPU and WebGL2 through an abstraction layer
- Camera and controls appear to be global while scene rendering is game-specific
- Supports VR via WebXR
- Rendering pipeline uses the concept of "render instructions" that capture draw calls and associated resource bindings
- A cache layer prevents redundant creation of GPU objects by hashing descriptors
- A GLSL-like shader language is pre-processed into backend-specific shaders
- A debug-drawing system provides a way to draw lines, text, and shapes in world, view, or screen space
- Debug-drawing aims to efficiently use a dynamic vertex buffer cache for debug geometry
- Font rendering uses a signed distance field font texture
- A plugin architecture allows different "game engines" to implement file parsing and rendering logic
- Source Engine support handles BSP traversal and rendering, lightmaps, VMT/VTK material parsing, and a hierarchical entity/scene system, projected textures / flashlights
- NGC/Wii support includes a re-implementation of Nintendo's GX API, which uses display lists, and support for various model types
- Super Mario Galaxy support involves particle effects, collisions, rail-riding, shadow volumes, and an object/actor system
- Complete reimplementation of Nintendo's J3D framework for loading and rendering models, skeletons, materials, and animations
- N64 support includes F3DEX microcode emulation and translates RDP commands to modern graphics APIs
- Crash Warped PS1 support includes emulation of PS1-style vertex coloring and jitter
- World of Warcraft support handles WMO, M2 models, and ADT terrain tiles, portal culling and frustum culling
- Nintendo DS rendering pipeline implementation, Pokemon map and time-of-day support, Mario Kart course support
- Support for FromSoftware model and map formats, and associated LOD logic
- Integration of RenderWare library for GTA III support
- XNA asset support for Fez
- The Witness uses an uber-shader system
- Morrowind support handles master ESM files and associated landscape records within
- Unity game and asset support with support for file format changes associated with different Unity versions

## [Simitone / FreeSO](https://github.com/riperiperi/Simitone)

- MonoGame/C# re-implementation of The Sims
- Zoom-level management and city/lot state transitions
- Content loading and caching
- Scriptable SimAntics Virtual Machine drives all logic, object behavior, and world state
- VM offers 256 primitive operations to objects
- Simulation loop runs a number of ticks based on speed multiplier and runs scheduled entity behaviors
- Client server state synchronization
- Marshal system for saving state and network synchronization
- Architecture system calculates whether floors are structurally supported and uses flood-fill algorithms to identify enclosed spaces
- Preview system for viewing changes without applying
- Network sync involves an adaptive buffer
- Server uses a MySQL database for persistent storage with a structured migration system
- Development / object editing tools built around the same simulation core
- Two-tiered path finding involving room traversal via portals and A* within a room

## [Stratagus](https://github.com/Wargus/stratagus)

- Modular RTS engine in C++ that uses Lua for configuration and game logic
- Lua is used for map definitions, unit types, UI layouts, triggers, conditions, custom behaviors, AI decision making, and user input or game event callbacks
- Units and buildings have a tile position, direction, action queue, ownership, type definition reference, and state flags
- A* pathfinding with per-unit pathfinding state, terrain cost evaluation, and dynamic obstacle avoidance
- Obstacle avoidance uses a lazy approach where path validity is checked when crossing to the next tile. A unit may wait some time before calculating a new path.
- Renderer built on SDL2 with "automatic" loading and caching of graphics
- Has an immediate mode UI system with panels and widgets, font management and text drawing
- File I/O with compression format determination
- Synchronized random number generation for network games
- C++20-style range algorithms
- World map divided into tiles (or "fields") with flags and a unit cache for fast lookups
- Multiple coordinate representations are used (e.g. tile and pixel)
- Tile rendering is "immediate-mode", but when tile state changes, neighboring tiles need "fixing up" to correct edge boundaries, likely due to the separation of "actual" and "player seen" tile state
- Unit management uses reference counting and storage in reusable "slots"
- Units may have container relationships (transports)
- Unit order system supporting chaining as well as saving/restoring orders when interrupted
- State machines used for complex orders like attacking a moving target
- Attack animation uses a callback to execute attack logic
- Animation is based on wait counters which scale with selected game speed. Certain animation frames have callbacks for attack execution. Animation frames dictate movement and can modify other variables via commands.
- Map visibility can be shared between allied players
- UI system at least partly uses Guichan for retained-mode rendering
- Rendering system supporting images, primitive shapes, clipping to viewport
- Font rendering based on Guichan with support for UTF-8 and DOS codepages
- Adaptive framerate management including tracking of frame timing and dropped frames and frame skipping
- Sound system supports 64 channels with metadata/source tags and completion callbacks
- Spatial audio support
- Supports various types of "missiles", linear, tracer, parabolic, etc.
- Network play "setup phase" involves one player acting as a server to coordinate game settings, then gameplay uses a direct peer-to-peer model
- To synchronize, commands are sent to all players but not executed until a delay has passed. Sync hashes are compared periodically to detect desynchronization
- Contains a map editor as a separate mode within the engine

### [Wargus](https://github.com/Wargus/wargus)
- Extracts WAR and MPQ files into more standardized asset files, using StormLib for MPQ files
- Converts images and tiles to PNG
- Converts ".sud" videos to playable formats
- Converts XMI music to MIDI
- Converts text from language-specific codepages to UTF-8
- Converts the native PUD map format to SMS/SMP
- Uses platform-specific external tools to rip CD audio music tracks
- The Warcraft 2 units specifications, game logic, and campaign sequences seem to be effectively recreated in Lua scripts

## [Frozen Bubble](https://github.com/kthakore/frozen-bubble)
- Written in Perl with C "extensions" and a C networking server
- Uses SDL, SDL_mixer, and Pango for text rendering
- Uses PO files for translations
- Began as an experiment into the performance of using Perl with SDL
- Project history involved evolution from local, single-player to networked multiplayer
- Collision and rebounds on a hexagonal grid
- Uses "dirty rectangles" to redraw only changed portions of the screen
- Transition effects like "waterize" or "plasma"
- Supports replays by capturing inputs and random number generations
- Uses a frame-limited loop targeting a particular speed
- Uses functional paradigms, including a curated subset of functional primitives in MDKCommon
- Network play uses a leader/follower model where the leader determines random seeds and parameters
- To account for floating point drift, the exact bubble position is transmitted to all players when a bubble "sticks" on the leader client
- Lobby chat supports a message system with history and nick completion
- Standalone server is meant to run as a daemon and uses relaying to allow allow communication across NATs

## [C-Dogs](https://github.com/cxong/cdogs-sdl/tree/2.1.0)
- Written in C on SDL, using CMake for builds
- Uses a "screen stack" concept for high-level state changes
- Many game state mutations are routed through an event queue to decouple subsystems and as part of network synchronization
- Common logic and rendering code shared between game and editor via a library artifact
- System for menus and campaign progression screens between gameplay
- The same "command" bitmask drives actor behavior whether the source is AI or human inputs
- Actor state is represented as a bitmask of many possible states
- Some movement is based on simple raycasting or line-of-sight tests, but a "goto" command may fallback to cached A* pathfinding
- "Detouring" logic involves attempting to turn the same direction 4 times before giving up
- Actors, map objects, projectiles, and pickups interact in a unified way as "things" in a tile-based tracking space
- To model vehicles, actors can "pilot" another, in which case commands are forwarded to the vehicle
- Leverages reusable pools of entities
- Uses various "ticks" fields to count duration of various states
- Actor direction, velocity, and interpolated rendering direction are distinct
- Animation frames are sometimes tied strongly to game logic, such as stepping or firing frames
- Actors are tied to character data, loaded from campaign files
- AI does not update every frame, with current command repeated for several frames
- Pickup classes are defined in JSON
- Although visually 2D, some entities have a "Z" dimension influenced by gravity
- Particles individually have a position, may be an image or text, may bounce or stop at walls, and may track an actor
- Map tiles hold a pointer to a shared tile class defining its properties
- Can load Wolfenstein 3D maps
- Four map generation algorithms
- Classic maps are built by randomly placing "features": rectangular floor areas, rectangular wall outlines, "pillar" walls in open spaces, and walls that start at an edge and go a specified length, potentially bending or splitting
- Cave maps use a "two-threshold" cellular automaton to generate organic cave layouts
- Interior maps recursively divide the map area, rooms are placed in each section and then connected by corridors
- Static maps load a hand-designed layout
- Doors are "grouped" such that adjacent doors open and close together
- Multiplayer uses a client-server model over UDP

## [XScreenSaver](https://github.com/Zygo/xscreensaver)
- Multi-platform (iOS/macOS, Android) support built on an Xlib emulation compatibility layer
- Main daemon process is critical and, if it crashes, the screen unlocks
- D-Bus bridge monitors lid events and inhibition requests
- The daemon uses XInput2 to monitor global user activity. When a timeout is reached, it "grabs" the X11 server and launches the visual process
- Includes a Wayland integration layer
- Coordinates with DPMS to manage display power states
- Visuals rendered into windows that cover every monitor on the system, using an `override_redirect` attribute to bypass the window manager
- Authentication to unlock can integrate with PAM, Kerberos, an external validation helper, or shadow password files
- Lock screen and associated process are privileged but isolated and use Xlib and Xft, and captures raw keyboard input events
- Contains 2D Xlib-based screensavers, legacy OpenGL screensavers based on display lists, and support for GLSL and Shadertoy screensavers

## [OpenRA](https://github.com/OpenRA/OpenRA/tree/bleed)
- Customizable engine supporting recreations of Red Alert, Tiberian Dawn, Dune 2000, and Tiberian Sun
- Uses YAML configurations for rulesets, entity and weapon definitions, sprite sequences, and UI layouts
- Written in C# with Lua scripting integration, using bindings for OpenGL and SDL2
- Uses the Actor-Trait-Activity pattern, a variant of Entity Component System
- Network synchronization is achieved through lockstep simulation. Orders are collected from clients, distributed by the server, and executed at specific future frame. Rather than synchronize the unit and world state, identical commands are executed across all clients, with desync detection
- Spatial indexing is used to efficiently find actors in different world or screen regions
- Single-player and replay modes are implemented as types of connection/session and thus multiplayer and single-player are unified logically
- Logic is run at fixed intervals while rendering is done as fast as possible or at a capped rate, decoupled from the logic
- Complex activities can be composed by queue-like "chaining" or stack-like "nesting"
- Traits or attributes are tagged such that they can be used in computing a "sync hash" for network synchronization checks
- Map editor exists as a separate mode
- Synchronized operations use a random generator with a shared seed while other cosmetic effects use a local generator
- Uses reflection to map YAML definitions to objects
- Apparently custom UI implementation involving a tree of widgets, dealing with input handling, modality, and stacking
- Visual asset definitions involve handling "facing" direction rendering, animation rates, Z ramping, baked shadows, and combination through stacking and scaling

## [LinCity-NG](https://github.com/lincity-ng/lincity-ng/)
- City simulation game written in C++ with SDL3 and using CMake for builds
- Operates on a discrete grid and uses a "commodity-based economic model" to simulate resource flow between constructions
- Map tiles track coverage and point back to the "construction" that occupies it
- Pollution spreads through diffusion and dissipates over time
- Game state is saved as compressed XML
- After constructions are placed, "neighborization" links them to related structures
- Animation updates are decoupled from logical ticks
- City grid is updated in a shuffled order each tick to prevent artifacts
- Map generation involves a "diamond-square implementation"
- Contains custom, XML-driven GUI toolkit, modeled as a hierarchy of components with one being in focus
- GUI toolkit contains a signal/slot mechanism and local coordinate transformations
- GUI toolkit contains containers such as table layouts, windows, scrollable views, and a switch component for tabs or multi-page menus
- GUI toolkit contains a "paragraph" component which supports reflowing text and HTML-like styling
- Images are loaded in a secondary thread, but converted to textures on the main thread to avoid rendering context thread safety issues
- Renders the map with an isometric transformation
- Images mapped to in-game resources using XML, with anchor offsets used to orient tiles appropriately in the isometric perspective
- Many assets are renders of Blender models
- Uses gettext for translations
- Uses XLST at build time to preprocess some GUI XML

## [FreeCiv](https://github.com/freeciv/freeciv)
- Written in C, uses Meson for builds with a legacy Autotools build, Lua for modifications
- Multiple options for GUI implementations and database backends
- Networking supports both JSON and binary formats
- Rulesets capture all customizable game configuration in INI-like files
- Client interfaces built on Qt6, GTK4, or custom SDL2 widgets, with common handling for map graphics
- Core tileset handling is GUI-agnostic, but rendering implementations are GUI-specific
- Lua integration provides script access to game state

## [fheroes2](https://github.com/ihhub/fheroes2/tree/master)
- Reimplementation of Heroes of Might and Magic II in C++ with SDL2
- Battles on a hexagonal grid
- Loading of original map format and extended format
- UI implementation with themes, contextual cursor system, and focus system
- Resource loading and caching system
- Redrawing involves flags with a locking mechanism to avoid over-drawing
- Supports keyboard/mouse, controller, and touch
- Can use hardware or software cursor rendering
- Does not appear to use UTF-8 for text, but rather language-specific encodings
- AI pathfinding considers the danger of monsters or armies, whether to interact with objects, and integrates movement spells
- Pathfinding is deeply integrated with other AI decisions and behaviors
- While the original release handled internationalization through different release versions, fheroes2 uses gettext/po files for translations and performs modifications on font images to produce appropriate text
- Unclear how animation or other timing works in relation to the event loop

## [SuperTuxCart](https://github.com/supertuxkart/stk-code)
- Kart racing game in C++ on a modified Irrlicht engine with Bullet for physics
- Uses XML extensively for configuration and data
- Supports "built-in" assets and add-ons
- Depending on frame timing, a variable number of physics steps are executed
- Abstraction layer isolates details of SDL, Wayland, OpenGL, or GLES2
- Implements a shader-based renderer and a legacy fixed-function renderer
- Contains post-processing, lighting, and effect shaders
- Shader pipeline involves rendering to a G-buffer, a lighting pass, shadow pass, transparent object pass, then post-processing
- Lighting is combined with material information for final rendering
- Implements morphological anti-aliasing (MLAA)
- Materials capture texture, shader type, transparency, friction and collision behavior, and sound associations
- Particle system with materials also sometimes dictating the particle effects resulting from collision
- Input system operates in various modes when handling input events, no assignment, player assignment / detection, action assignment, and regular play
- Some assets are loaded from expected relative paths, others are found by searching registered directories
- Uses HTTP to download add-ons (karts, tracks, skins)
- Tracks divided into sectors for progression tracking
- Extends default Bullet physics vehicle system with kart-specific behavior
- Implements skidding/drifting dynamics in addition to material-based friction modification
- Kart collision geometry is built to appeal to the gameplay (beveled edges to avoid getting stuck, lowered center of gravity, angular factors to keep cart upright)
- Kart's maximum turning angle is lowered with increasing speed
- Kart interacts with terrain through physics interactions with wheels, and the current surface material is tracked
- Track system uses quads that form the "driveline" of the track, the center of which is used by AI. It is a directed graph of connected quads
- Track objects may be a 3D model, have no visual representation, be a billboard, be a light,  be a particle, emit a sound, or be an activation trigger
- Track objects may use various collision geometry, or a more expensive "exact" geometry, and may interact with karts in various ways such as flattening
- Primary race AI uses the track's drive graph, randomly choosing paths at forks, steering to avoid track edges and other karts, skidding for sharp turns
- XML-driven GUI implementation built on Irrlicht's, but extended significantly
- UI supports per-player "focus" and includes a "box" layout system that divides a widget into nine sections
- Networking uses a client-server model where either one player's instance or a dedicated server process is the server
- "Address discovery through STUN for NAT traversal"
- Each client signals the server when loading is complete, then clients are instructed to start the race at a fixed time on a synchronized clock
- The server processes all physics and sends authoritative position updates to clients
- Server controls item box generation. When a client collects an item, the server validates this and notifies all clients

## [SuperTux](https://github.com/supertux/supertux)
- 2D platformer in C++ with SDL/OpenGL, with Squirrel for scripting
- Stack-based state/screen manager
- Features installable "add-ons"
- Levels are further divided into sectors, with only one sector being active at a time
- Has a built-in level editor mode
- Systems for swimming, sliding, grabbing enemies
- Uses collision groups to decide what can collide
- Collision detection provides information handed off to a response system rather than being dealt with inline
- Visitor pattern determines collision response based on object type
- Player collisions with the static environment factor in slopes and normals
- When state changes impact bounding boxes (e.g. player tries to duck or stand), the new bounding box is tested for collisions to ensure the change is allowable
- Interactive objects like coins and moving platforms can follow paths of nodes made up of bezier curves
- World and level files written in an S-expression format
- World map is a "special kind of level with a special player implementation", which sounds odd
- A drawing context manages a transformation stack, including translations, scaling, flipping, and transparency
- Drawing operations are represented as requests that are collected and then processed later for ordering and batching purposes made up of bezier curves
- A lightmap is rendered separately from the main scene and combined using multiplicative blending 
- Contains SDL, legacy OpenGL, and "modern" shader-based OpenGL rendering implementations
- Camera system supporting zoom levels, shaking effect, lookahead/peeking, and integration with the path system
- Special multiplayer camera mode aims to keep all players visible
- Culling avoids rendering objects and tiles that don't intersect the camera viewport
- "Autotile" system automatically adjusts tiles based on their surrounding neighbors
- In addition to regular solid tiles, has sloped tiles and "unisolid" tiles allowing movement up through the tile but not downward
- Moving platforms appear to be implemented as tilemaps that follow a path
- Various particle systems for background effects like rain
- "PhysFS" provides a kind of virtual filesystem where different sources and zip file contents can be "mounted" and accessed or searched


## [CorsixTH](https://github.com/CorsixTH/CorsixTH)
- Recreation of Theme Hospital in C++ and SDL with Lua for scripting, CMake for build system
- Entities are either "humanoid" characters or objects
- Variable time / tick rate
- World is made up of tiles which may belong to a room or be generic corridor or outdoor tiles
- Uses tile, world, and screen coordinates (isometric projection of world coordinates)
- Has a temperature system that spreads through tiles
- Map rendering draws floors and shadows, then north/west walls
- Renders "blueprint" overlays of room construction before placement is confirmed
- A-star path finding that leverages directional pass-ability and other flags on tiles
- Has specialized path finders with different heuristics and neighbor-handling for finding paths into a hospital, finding a suitable tile for idling, and finding specific objects
- Path navigation involves door animations and queueing behavior when multiple "humanoids" want to use the door
- Sometimes the pathfinding process is shortened when the destination is directly visible or reachable
- Humanoid visual direction derived from last movement direction
- Humanoids have an action queue with priorities and potential interruptions
- Actions can schedule future callbacks in a given number of ticks
- Supports TrueType and bitmap fonts
- Supports various sprite transformations including palette swapping
- Animation frames can have many layers, and the animation system supports wobbling, heat waves, mirroring, clipping, and color palette remapping
- Video player using FFmpeg for decoding and SDL/SDL_mixer for playback
- Localization / translations use strings embedded in Lua tables rather than something like gettext


## [Warzone 2100](https://github.com/Warzone2100/warzone2100)
- RTS in C++ with JavaScript based AI scripting (QuickJS)
- Uses a client-server networking model where one player serves as the host, processing all game state changes and synchronizing to clients
- Host maintains authoritative game time. Clients maintain a queue of synchronized instructions and execute them at times determined by the host
- Periodic hashes of game state are compared to detect synchronization issues
- Supports OpenGL, OpenGL ES, Vulkan, and DirectX backends
- Virtual file system "PhysicsFS", "PhysFS"
- Template-based Vector2/Vector3 types
- Supports portable mode and standard mode
- Uses INI-style configuration files
- Key abstractions include threading primitives, window management, input for text entry, clipboard access, time, and system resource info.
- Units have a two-layered behavior system, high-level "orders" and lower-level "actions", both of which are updated each frame
- "Indirect" projectiles follow a parabolic arc under simulated gravity, "homing" projectiles adjust to track their target
- To determine whether a projectile "hits", accuracy is calculated based on stats and distance and then a random roll is checked against it
- Potential targets are weighted by the AI system to prefer hostile, nearby, damaged, visible enemies.
- Various projectile and impact rendering effects
- Unit movement is controlled by a state machine (e.g. following path, moving to point, turning, pausing, waiting for route, shuffling to unblock)
- When units are blocked for a short period, they attempt to "shuffle" sideways to get around the obstacle
- In addition to grid based obstacle checks, units attempt to slide around or use perpendicular movement when encountering a dynamic obstacle
- Formation system organizes units into groups, units maintain position relative to assigned slot while formation as a whole moves
- Various complex orders and actions
- Text rendering uses FreeType and HarfBuzz, bidirectional text handling via FriBidi
- Animation uses frames with optional interpolation
- Terrain is tile-based
- Uses texture splatting to blend textures between adjacent tiles, and decals like roads or craters are separate geometry overlaid on the terrain
- Supports "modern" shadow mapping and fallback stencil shadows
- Opaque objects are drawn front-to-back with depth testing enabled while transparent objects are drawn back-to-front with alpha blending
- Water rendering animates texture coordinates to create the illusion of flowing water
- 3D models are stored in a custom, human-readable text format called PIE


## [Xash3D](https://github.com/FWGS/xash3d-fwgs)
- Reimplements the Half-Life GoldSrc engine
- Uses a client-server model allowing for both integrated client-server operation and dedicated server deployment
- Supports dynamic loading of renderers, game logic DLLs, and UI components
- Command system allows modules and components to add commands and register configuration variables
- Each entity contains previous and current state, allowing the client to interpolate between network updates
- Distinguishes between persistent, synchronized entities and "temporary" entities used for things like visual effects
- Implements various particle types as well as support for particles with "custom callbacks"
- Beam system provides "dynamic beam effects" between points or entities
- A lot of details seem to be delegated to game-specific DLLs
- The server runs the authoritative physics simulation and game logic updates
- Server handles distribution of game resources and assets to clients
- Server implements a challenge-response authentication system to prevent spoofing, involving an MD5 hash of IP address and server salt
- Supports "reliable" and "unreliable" data fragments for essential game state and non-critical updates
- Bots are implemented as "fake" clients
- Server processing frame rate is configurable and each frame has a specific duration impacting physics and entity updates
- World state is synchronized with clients via delta compression and "reliable" messaging
- Game logic is implemented via hooks for entity management, AI, game rules, and physics
- Has a "Virtual File System" providing a configurable and searchable view of assets across folders and several archive types (PAK, WAD, ZIP/PK3, PK3DIR)
- VFS abstracts platform-specific file system factors like case-sensitivity, and also supports Android APK assets
- Model system supports BSP files, skeletal "studio models", vertex-based "alias" models, and sprites for UI and effects. BSP supports embedded textures and external references
- BSP models allow for spatial queries through potentially visible sets and potentially hearable sets
- Renderers implement a standard DLL interface, with legacy OpenGL 1.1 and scanline-based software renderer being the available implementations
- Platform-specific code for SDL, Win32, Linux, Android, DOS, Nintendo Switch, and PS Vita
- Supports touch with virtual controls
- Implements a handful of DSP audio effects, various kinds of delay/reverb or filtering

## [Aleph One](https://github.com/Aleph-One-Marathon/alephone)
- Implementation of Marathon in C++ on SDL2 with Lua for scripting, Autoconf for build
- Involves a "vertical blank timing" system, originally designed to synchronize with CRT blanking interrupts 
- Custom UI widget system with several layout models and XML-driven theming
- Main loop uses an SDL event polling loop while interface states use use an SDL function that yields CPU until the next event
- Template-based binding system for Lua interfaces
- OpenGL and software rendering implementations, the OpenGL implementation appears to be heavily shader-based
- 2D / UI rendering appears to have both SDL and OpenGL implementations
- Supports TrueType and bitmap fonts, generating OpenGL texture atlases with display lists
- Uses OpenAL for 3D audio with a "soft loopback" for feeding into the SDL audio pipeline
- Audio players are processed in a dedicated audio thread
- Uses an LRU cache for loaded sounds
- Uses a star-topology for network play (client-server model innit?) where spokes send updates to the hub and then receive aggregated game state from the hub
- The "hub" receives actions from all spokes, orders them by tick for deterministic execution, and distributes them to spokes
- A "metaserver" provides game discovery, player matching, and chat functionality

## [fhDOOM](https://github.com/eXistence/fhDOOM)
- Modernized Doom 3 / id Tech 4 engine, replacing legacy OpenGL and ARB2 assembly shaders with GLSL-based OpenGL 3.3
- Uses a CMake build system
- Also includes Qt-based editors and tools as an alternative to the original MFC-based tools
- Designed with a clear split between rendering frontend and backend, separating scene description from GPU execution
- Contains a virtualized file system layer, helping to support patching and modding as well as case-sensitivity differences
- "Declaration system" is a unified system for managing and parsing text-based data types, including materials, "sound shaders", and entity definitions
- Includes a custom platform abstraction layer above Windows and Linux/POSIX/X11, and for getting CPU and FPU capability information
- Includes a custom memory manager used in place of the standard C heap that are "significantly faster than MSVC implementations", with "new/delete" operator redirection
- Custom string classes with one being an owned string and the other being a reference
- Foundational math classes, vectors, matrices, quaternions, angles
- Custom dynamic array (list) implementation with associated "view" type, custom fixed-capacity array template, custom dictionary type
- Custom lexer and parser implementations
- SIMD implementations of heavy operations like "vertex skinning" or physics
- Translation from ARB2 to GLSL is implemented as a "declaration" parser/loader
- Materials can have a variable number of shader stages
- The rendering "frontend" is responsible for visibility determination, surface generation, and lighting interactions, resulting in a list of render commands
- The rendering "backend" processes these render commands into OpenGL calls
- The primary unit of work on the backend is a bundle of triangle data, a material definition, values for shader variables, and a screen-space clipping rectangle, and these units are further aggregated and associated with a projection and view matrix
- Includes an "immediate mode" debug drawing implementation backed by GLSL that emulates legacy fixed-function behavior
- Includes a custom GLSL preprocessor supporting `#include` directives
- Opaque surfaces fill the depth buffer and are rendered first while transparent surfaces are blended later
- Contains an event system for scheduled event dispatch
- Contains some kind of custom type system for entities that allows for fast runtime type-checking and instancing, linking C++ functions to scripted events, and serialization for saving
- Entities can be removed immediately or queued for "safe removal" at the end of the frame
- Key entity subtypes are actors, players, lights, projectiles, triggers, and "movers" which deal with doors or other moving objects
- Contains physics handling for rigid bodies, articulated figures (ragdolls), and parametric "movers"
- Collision detection or "clip system" uses queries referred to as "traces" or "sweeps" to determine if paths or shapes intersect with other geometry
- AI and pathfinding leverages the Area Awareness System that partitions the map into convex areas
- AAS is used for spatial reasoning queries such as finding cover, which uses the PVS to find areas not visible from a given point
- AI movement state captures position and velocity, movement type (e.g. animation-linked), and high level goal (e.g. move to cover)
- Skeletal animation system built around the MD5 model format
- Animations have "channels" to facilitate blending, including channels for head, legs, and torso (and "all" which overrides others)
- Inverse kinematics are used to adjust animation results, e.g. for accurate foot placement or turning a head to track a target
- Includes a tool to convert Maya models to MD5
- Scripts use a custom, C-style language that is compiled to bytecode and run in a stack-based virtual machine
- Audio system built on OpenAL software implementation and the EFX environmental audio framework (for reverb and occlusion effects)
- "Sound shaders" are declarations that control how a sound is played (e.g. looping, lead-ins, volume)
- Small, frequently used sounds may be fully decompressed and kept in memory, but longer sounds are "streamed", decompressed on-the-fly
- On Linux, ALSA and legacy OSS audio backends are supported
- Radiant level editor, an MFC application, which integrates with components from the game engine code
- Level geometry is built from brushes and "patches" for curved surfaces, and supports Constructive Solid Geometry operations
- Texture mapping can be done via shift/scale/rotate operations or "texture matrix coordinates"
- Editor manages entities as essentially containers of key-value pairs
- The "dmap" compiler transforms the raw map data into a BSP format while optimizing the geometry and generating shadow occlusion information
- Contains Qt-based editors for lighting and sound, but the material editor remains MFC-based

## [Julius](https://github.com/bvschaik/julius)
- Re-implementation of Caesar III in C on SDL2
- Uses CMake as its primary build system with some platform-specific build tools like Gradle or Xcode
- Contains a flexible display scaling system for different DPI and resolutions
- Contains a platform-agnostic core loop with platform-specific adaptations, like touch controls
- Support Windows, macOS, Linux, PS Vita, Switch, Android, and Web via Emscripten
- Implementation of "ghost" buildings during placement
- Implementation of special handling for multi-part structures, special placement rules
- Implementation of draggable infrastructure (roads, walls, aqueducts, bridges)
- Construction placement follows a state driven workflow starting with building type selection
- Labor seeker "figures" spawn from buildings and travel to find houses with an available workforce
- Original game used language-specific encodings, but Julius converts these to UTF-8
- Contains a rich text rendering system
- Contains a map/terrain editing mode involving multiple brush sizes and various tools

## [OpenMW](https://github.com/OpenMW/openmw)
- Re-implementation of Morrowind

## [Blitz 3D](https://github.com/blitz-research/blitz3d)
- A game development ecosystem combining a custom language compiler and a 3D engine
- Built on FreeImage, FMOD, and DirectX 7, and MFC
- The BlitzCC compiler transforms BlitzBasic source into native x86 code
- The custom compiler pipeline handles lexing/parsing, analysis, intermediate representation, code generation, and assembly/linking
- The lexer produces tokens which are turned into a syntax tree by the parser using a recursive descent approach
- Semantic analysis traverses the syntax tree, resolves types, tracks environment and stack requirements, and resolves names
- The processed tree is converted to another tree of more assembly-like primitive operations, the intermediate representation
- x86 code generation uses a "tiling approach" whereby subtrees in the intermediate representation are matched to potential "tiles" of instruction sequences
- The code generator also manages the limited set of x86 registers to minimize "memory spills"
- The final game executable is generated by taking a template "runtime" DLL and merging it with the compiled user code
- 3D engine component maintains a stateful scene graph consisting of cameras, lights, meshes, and pivots
- A "mesh" is a one or more surfaces, collections of triangles sharing a single brush (material)
- Supports both vertex animation and skeletal animation
- Collision detection supports Ellipsoid-to-Polygon and Ellipsoid-to-Ellipsoid interactions, utilizing a Bounding Volume Hierarchy for spatial queries. It supports stopping and sliding in response
- Includes specialized support for environment geometry, a terrain system with LOD support and support for Quake 3 indoor BSP models
- Natively supports the proprietary B3D format, the Autodesk 3DS format, and the X format
- Scene supports mirrors which trigger a secondary render pass from the reflected camera position
- Mesh animations use keyed positions, scales, and rotations for MD2-style vertex animation, and skeletal "skinned models" are also supported
- Also supports MilkShape 3D models, MS3D
- Collisions are enabled or disabled based on entity type pairs, and configured with a particular fidelity of collision detection (e.g. sphere to mesh, sphere to box)
- Includes MFC-based editor and debugging applications

## [Super Mario 64](https://github.com/n64decomp/sm64)
- Object system uses unions to share memory for different object types
- Behaviors are represented as a kind of "script" of commands, and a kind of VM involving a stack and a delayed execution timer
- Object system supports parent-child relationships and forming linked lists for iteration
- Objects track up to 4 recently collided objects and remember which platform they're standing on
- Graphics system built around a scene graph and a display-list based rendering approach
- Objects are linked to a scene node which is updated to reflect the object state
- Music is generated by processing sequences of MIDI-like instructions

## [Ship of Harkinian](https://github.com/HarbourMasters/Shipwright)
- Custom library called libultraship reimplements Nintendo's libultra SDK
- The Ocarina of Time decompilation project is the basis for the core game logic
- CMake is used as the build system
- Actors use the same structure but have categories that dictate how they are treated, such as update order and possible interactions
- Many actors use a simple state machine implementation where they change their current "action function" pointer

## [klib](https://github.com/attractivechaos/klib)
- Contains implementations of a hash table, AVL tree, B-tree, dynamic array, and linked list
- Contains core string utilities, a JSON parser, and a parser for mathematical and logical expressions
- Contains "bioinformatics" utilities, such as Smith-Waterman for sequence alignment, Newick tree format parsing, and dealing with FASTQ/FASTA files
- Contains utilities for threading and parallelism, such as a parallel for-loop
- Contains utilities for memory allocation and management in memory pools
- Contains utilities for command-line parsing
- Contains utilities for file and network I/O

## [Tomboy-NG](https://github.com/tomboy-notes/tomboy-ng)
- Rewrite of Tomboy in Free Pascal that adds multiple synchronization backends, rich text editing, snapshots and backups
- Implements IPC support for single-instance enforcement
- Runs background threads to index the XML note files for search when the application starts or a refresh is triggered, with each thread responsible for certain filename start characters
- Leverages the KMemo component for rich text editing
- If Search-While-You-Type mode is enabled, the application maintains full note contents in memory, otherwise notes are scanned on submission
- Tasks like detecting and updating links occurs on an interval of 2 seconds
- When saving, the editor component is locked and saving occurs on a secondary thread
- Notes are typically written to a temporary file and then copied semi-atomically over the original note
- Has synchronization backends for the file system, GitHub, and Misty HTTP servers
- Misty HTTP server allows for self-hosted note server with HTTP Basic Auth and a web-based note editor via the Quill JS component
- Uses Hunspell for spell-checking

## [Second Reality](https://github.com/mtuomi/SecondReality)

## [LMMS](https://en.m.wikipedia.org/wiki/LMMS)

## [Mastodon](https://github.com/mastodon/mastodon)

## [snort](https://github.com/snort3/snort3)

## [Tesseract](https://github.com/tesseract-ocr)



## [GP-GOMEA](https://github.com/marcovirgolin/GP-GOMEA)


## [manim](https://github.com/3b1b/manim)

## [Webamp](https://github.com/captbaritone/webamp)

## [FakeVim](https://github.com/hluk/FakeVim)

## [libui](https://github.com/andlabs/libui)


## [c2nim](https://github.com/nim-lang/c2nim)

## [ScyllaDB](https://github.com/scylladb/scylladb)

## [SQLite Browser](https://github.com/sqlitebrowser/sqlitebrowser)


## [iv](https://github.com/Constellation/iv)

## [ctags](https://github.com/arduino/ctags)

# XScreenSaver "Hacks"

## Hex Trails

- Hexagons tick forward, advancing through a state machine between IN, OUT, WAIT, and DONE states
- Hexagons start with a random color from a random palette of 8, but have an 80% chance of adopting the source color when receiving a line

## Abstractile

- The screen-filling mosaic is generated by dividing the screen into a grid and filling it with lines.
- Starting points are shuffled and sequentially selected from, and a line is drawn in an open direction until an obstacle is hit.
- Lines can branch off of existing ones.
- Lines are generated in a separate order from how they're drawn; the former aims to fill the grid and the latter aims to animate in a pleasing way.

## Binary Horizon

- Particles trace a path with particles being recycled upon reaching a certain age.
- Alternates between "white" and "black" color epochs periodically, and a new horizon line height is also selected.
- Particles receive an initial color based on the current color epoch palette, and colors fade gradually by making small random adjustments to RGB values.

## Blaster

- "Robots" move either linearly or through random perturbation and have a small chance of switching styles.
- They fire lasers at their current target, which also changes randomly with a small probability.

## Boing

- Recreation of classic Amiga bouncing ball demo
- The ball is rendered by dividing a sphere by a given number of latitude/longitude lines, producing quad faces.
- Checker pattern is done using an XOR calculation of the ball grid/face indices, independent of optional tesselation for smoothing.
- The shadow is rendered as flat circle (triangle fan) with a fixed offset.

## Braid

- Braids are represented as "braid words" where a sequence of generators specify how strands interact (crossings).
- Braids are rendered in a circular layout using polar coordinates.
- Smooth crossings are drawn using sine interpolation.

## Cage

- Draws an "impossible" cage by disabling depth testing and drawing a box frame.

## Celtic

- Generates patterns from different graph topologies, including: rectangular lattice, triangular lattice, polar / concentric, and "kennicott" (grid of clusters).
- Walks the graph using a turn rule to form closed loops, emitting Bezier segments for each crossing.
- Animates by drawing short segments along every spline each frame.

## Coral

- Implements a "diffusion-limited aggregation" (DLA). Random walkers wander pixel-wise until they hit existing "coral".
- A packed "bitboard" is used to track which pixels are filled/sticky.
- A walker that has not stuck takes a single random step up/down/left/right.
- Uses an optimized random function that extracts only the needed 2 bits for direction decisions and reduces calls to random().

## Cubic Grid

- A finite lattice of points are drawn (as OpenGL points).
- The view is centered in the middle of the lattice and the lattice rotates around, producing various patterns and alignments.

## Deep Stars

- OpenGL points are generated on a unit sphere around the viewpoint.
- Blending is enabled and depth testing is disabled such that repeated draws are layered and accumulate visually.
- The view matrix is rotated and drawn repeatedly, creating the effect of smeared trails.

## Dymaxion Map

- Displays an icosahedral Earth that repeatedly folds and unfolds into a 2D layout.
- The folding animation is state-machine driven, including folding, unfolding, and "stellation" into a more rounded sphere.
- Triangles are recursively rotated around two edges to fold them into an icosahedron.
- A "daylight mask", a grayscale image, encodes how much each point in the map is in day versus night based on the point's latitude/longitude.

## Euler 2D

- Simulates an "incompressible, inviscid flow" inside a bounded region.
- Evenly distributed tracer points are influenced by vortex points according to the Biot-Savart kernel plus "image vortices" that account for the shape of the boundary.
- Tracer points are time-stepped with an ODE solver that uses midpoint for the first step followed by Adams-Bashforth 2, which allows for tracer tail segments to curve more accurately.

## Fireworkx

- Simulates particle explosions with air drag, gravity, and ground bounces.
- A glow/blur (bloom) effect reads each pixel and 8 neighbors, weights the center pixel 8x more heavily, and writes the blurred result to a secondary buffer.
- Color flash effect uses a precomputed light map based on distance from explosion, multiplies each shell's flash color by the light intensity, then additively blends it into the output buffer with clamping.
- Uses SSE2 instructions when available to process 4 shells' lighting in parallel.

## Flow

- Simulates trajectories of continuous-time dynamical systems (ordinary differential equations), primarily "strange attractors" like Lorenz, Rossler, Birkhoff bagel, and Duffing.
- Particles represent integrations of the ODE using a 2nd-order Range-Kutta step, and a time tail of recent positions is shown per particle.
- The particles are transformed by a 3D projection matrix for viewing, apparently in software.
- Background routine attempts to explore random parameters and "find new attractors".

## Halftone

- Creates a dynamic halftone display by drawing a grid of dots influenced by "gravity points" that bounce around.
- Dot size is a factor of "gravity influence", or cumulative "closeness" to the moving dots.

## Hilbert

- Draws a recursive Hilbert space-filling curve in 2D or 3D.
- A Hilbert path is a single continuous line that can fill a volume without crossing itself.
- The property that points close on the line are also close in proximity in space has implications for linearly storing spatial data. In other words, it is a mapping of a 1D interval to a 2D square (or higher dimensional space).

## IMS Map

- Implements an "iterated midpoint-subdivision" or midpoint displacement fractal (diamond/box style). It repeatedly subdivides a grid, sets midpoint heights to the average of surrounding heights plus a random perturbation.
- The heights are displayed as colors, resulting in a terrain-like image that gets progressively refined.

## Interaggregate

- Invisible circles of various sizes move slowly around the visible space.
- When two circles intersect, a sine-parameterized scribble is drawn between the two intersection points.

## Lavalite

- The lava is modeled as groups of moving metaballs.
- Each frame, the metaballs are moved, an implicit scalar field is built from their influences, and then polygonized via marching cubes.

## m6502

- Emulates a Motorola 6502 CPU. Video output is handled by a range of memory used as a video buffer in the VM.
- The video output is then fed through an NTSC-ish TV simulation filter.

## Maze 3D

- Re-creation of the Windows 95 maze screensaver.
- Uses a randomized maze-growing Prim's algorithm variant on a grid where real cells live at odd indices and walls at even indices.

## Pac-man

- Mazes are generated with a "recursive, tile-based backtracker", or chosen from built-in standard layouts.
- For generation, the "jail" is placed and then, grows the level out from there until a placed-dot percentage is met. Then, remaining empty cells are converted to walls and appropriate wall characters are chosen (rounded, vertical, etc.).
- Tiles are pulled from a weighted table of 5x5 patterns. The algorithm tries to place tiles and backtracks if placement is impossible.

## Penrose

- Implements a "well-known" incremental growth algorithm that builds a Penrose tiling.
- The "fringe" border of the existing pattern so far is tracked and the growth algorithm places a tile along the fringe according to Penrose rules.
- The pattern tiles are recorded in a "5D integer coordinate system" based on the 5 angles in which the pattern can grow.

## Polyominoes

- Attempts to fill a rectangle with irregularly shaped pieces using depth-first backtracking.
- Scores potential next locations and attempts to choose a small, "hard" location to fill first.

## Quasicrystals

- Generates a sine wave texture which is then applied to many scaled and rotated planes.
- Planes are drawn as quads with blending such that interference patterns appear.

## RD-Bomb

- Simulates the Pearson reaction-diffusion equations where two "chemical quantities" evolve over time on a 2D grid.
- The quantities diffuse through several diffusion patterns that involve averaging a neighborhood of pixels.
- The quantities react using the Pearson equations, creating feedback loops and producing wave-like patterns.

## Substrate

- Primary "cracks" grow in a given direction, either straight or at a determined radius and arc-length.
- Perpendicular to each crack's forward direction, "sand" is painted with sine-wave modulation and alpha blending.

## Swirl

- Color values are calculated based on the influence of "knots" at a given point (attractors/repellers)
- The same function is evaluated progressively at increasing resolutions

## Unknown Pleasures

- Waveforms are created by summing random cosine spikes with an envelope.
- The waveforms are represented by 3D geometry and move backward, but orthographic projection makes them appear 2D.

## Vermiculate

- Autonomous "worm" agents move around with various rules for turning, bouncing, following, etc.
- Can produce very different results depending on randomized parameters, including whether long trails persist.

## Whirlwind Warp

- A field of "star" particles are influenced by 2D force fields.
- Stars are respawned if they're pushed outside the view bounds or extremely close to the center.

## XRaySwarm

- Target particles wander randomly while swarms of "bug" particles accelerate toward the nearest target.
- Particle position histories are maintained in order to draw particle tails.

## XSpirograph

- Draws lines by sampling a hypotrochoid-like parametric equation with randomized radii, offset, and distance.
- Sampled points are connected with lines, and parameters are varied between layers.