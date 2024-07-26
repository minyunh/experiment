# RoadRunner

https://zhuanlan.zhihu.com/p/552983835

## New

1. Open RoadRunner
2. Choose NewProject->Select save path -> Base+Add on(all of Asset)
3. Scenes: Only for map / Scenarios: Also autopolit
4. New Scene(empty one)

## Save

A. In roadrunner

1. File→ export → CARLA(.fbx, xodr, .rrdata.xml)
2. Choose file path, and save→ export.

→ get .fbx and .xodr file

B. Open UE

1. Content/RoadRunne/Static (If not exisit, create)
2. right click static → Add/import content → import to / Game/RoadRunner/Static
3. Choose the file .fbx (step A-2)
4. New window (MathWorks RoadRunner Import Options) → choose Import
5. New window (FBX Scene Import Options) 
    1. Scene→ Hierarchy Type → choos Create one Blueprint
    2. Scene→ Texture→Invert Normal Maps
    3. Static Meshes →Normal Import Method → Import Normals
    
    And choos Import.
    
6. right click FbxScene_XXX→choose Edit 
    1. new window up-left coner → choose  Components: DefaultSceneRoot
    2. Right side → Details → Transform → Mobility → Static
    3. Compile and Save
7. File->Save Current As...→Save XXX.umap in Content/RoadRunner/Maps
8. Copy  **carla\Unreal**\CarlaUE4\Content\Carla\Maps\OpenDrive\XXX.xodr to \CarlaUE4\Content\RoadRunner\Maps\OpenDrive (if not exisit, create OpenDrive)

→ Press button “Play” and run demo code !
